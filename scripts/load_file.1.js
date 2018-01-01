function loadJSON(url, callback) {
    var xObj = new XMLHttpRequest();
    xObj.overrideMimeType("application/json");
    xObj.open('GET', url, true);
    xObj.onreadystatechange = function () {
        if (xObj.readyState == 4 && xObj.status == "200") {
            //console.log(xObj.responseText);
            callback(xObj.responseText);
        }
    };
    xObj.send(null);
}

function addEntityTags(input) {
    var out = "";
    loadJSON("data/person.json", function(response) {
        var persons = JSON.parse(response);
        if (persons.length > 0 ) {
            for (i =0; i < persons.length; ++i) {
                console.log("person " + i);
                for ( x in persons[i]) {
                    //console.log(x, persons[i][x]);
                    if ( x.valueOf() == "name") {
                        console.log("Length of input string BEFORE " + input.length + " replace name " + persons[i][x]);
                        out = input.replace(persons[i][x], "<p class='h1'>" + persons[i][x] + "</p>");
                        console.log("Length of input string AFTER " + input.length);
                    }
                }
            }
        }
    });
    return out.valueOf();
}

function addTags(dataType, arr, complete = false) {
    var out = "";
    //console.log("Inside add Tags " + dataType);
    if (dataType == "table") {
        console.log("Adding table tags now");
        for (i = 0; i < arr.length; ++i) {
            out += "<tr>";
            for (x in arr[i]) {
                out += "<td>" + arr[i][x] + "</td>";
            }
            out += "</tr>";
        }
        if (complete == true) {
            out = "<table>" + out + "</table>";
        }
        
    }
    if (dataType == "article") {
        console.log("Adding article tags now ");
        for (i = 0; i < arr.length; ++i) {
            
            //console.log("Printing article " + i + ". " + arr[i].article);
            out += "<div class='article row text-left'><h5>" + arr[i].title + "</h5></div>";
            out += "<div class='article row text-left'><p>" + arr[i].article.substring(0,600)  + "</p></div>";
        } 
        //console.log(" BEFORE adding entity tags " + out.length);
        //var out2 = addEntityTags(out);
        //console.log(" AFTER adding entity tags " + out2.length);
        return out;
        
    }
    
    return out;
}

function jsonToHTML(url, placeName, dataType, toggle = true) {
    //console.log("inside jsonToHTML \n" + url + " " + placeName + " " + dataType);
    loadJSON(url, function (response) {
        var text = JSON.parse(response);
        if (text.length > 0 && toggle === true) {
            //console.log("number of elements " + text.length);
            $(placeName).show();
            var out = addTags(dataType, text);
            var oldHTML = $(placeName).html();
            //console.log(out);
            $(placeName).html(oldHTML + out);
            return i;
        }
        else {
            //console.log("toggle" + toggle);
            //console.log("number of elements " + text.length);
            console.log("No records found");
        }
    });

    return 0;
}