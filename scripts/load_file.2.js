function loadJSON(url, placeName, callback) {
    var xObj = new XMLHttpRequest();
    xObj.overrideMimeType("application/json");
    xObj.open('GET', url, true);
    xObj.onreadystatechange = function () {
        if (xObj.readyState == 4 && xObj.status == "200") {
            //console.log(xObj.responseText);
            callback(xObj.responseText, placeName);
        }
    };
    xObj.send();
}

function sayhi() {
    alert("hi");
}

function prepareCollapsibleTags(lookupKey, i) {
    var quote = "'";
    return "<div class='collapse' id=" + quote + "person" + i + quote + ">" +
        '<div class="card" style="overflow:hidden;">' +
        //'<div class="card-header">Card Header' +
        // '</div>' +  // Card Header
        //'<div class="card-block"' +
        '<div class="card-body">' +
        //'<h4 class="card-title">Special title treatment</h4>' +
        '<small class="card-text text-muted" style="word-break:break-all;">With supporting text below as a natural lead-in to additional content.' +
        'This is a collapsible bar for ' + lookupKey + "." +
        '</small>' +
        '</div>' + // card-body
        //'</div>' + // card-block
        '<a href="#" class="btn btn-primary">Go somewhere</a>' +
        '</div>' + // card

        // 
        "</div>";  // person

}

function prepareCard(data, lookupKey, i) {
    var card = '<div class="card text-white bg-primary mb-3" style="max-width: 20rem;">';
    //card += '<div class="card-header">' + lookupKey + '</div>';
    card += '<div class="card-body">';
    card += '<h4 class="card-title">' + lookupKey + ' </h4>';
    card += '<p class="card-text">';
    card += lookupKey + " is a " + data[lookupKey].job + " and works at " + data[lookupKey].company;
    card += "The address is " + data[lookupKey].address;
    card += '</p>';
    card += '</div>';

    return card;
}



function tagify(response, placeName, ) {
    var data = JSON.parse(response);
    //console.log("Printing inside tagify ");
    //console.log(data);

    //console.log("number of elements " + text.length);
    //$(placeName).show();

    var out = "";
    var articles = data.articles;
    var persons = data.persons;
    var nodes = data.network.nodes;
    var links = data.network.links;

    console.log("No. of nodes " + nodes.length);
    console.log("No of links " + links.length);

    for (i = 0; i < articles.length; ++i) {
        //console.log(articles[i].title);
        out += "<div class='article col text-left h5' style='padding-left:0px;'>" + articles[i].title + "</div>";
        out += "<div class='article col text-left' style='padding-left:0px;'><p>" + articles[i].article.substring(0, 600) + "</p></div>";

  
        var pop_start = '<button href = "#person' + i + '" type="button" class="btn btn-link" ' +
            'data-toggle="collapse"> ';
        var pop_end = "</button>";


    }

    for ( j = 0; j < persons.length; ++j) {
        if (out.includes(persons[j].name) == true) {
            var amend = pop_start + persons[j].name +
                //prepareCollapsibleTags(persons[i].name, i) +
                pop_end;
            //console.log("Adding popover tags " + amend);
            out = out.replace(persons[j].name, amend);
            console.log("output contains " + persons[j].name);

        }
    }

    var oldHTML = $(placeName).html();
    //console.log(out);
    $(placeName).html(oldHTML + out);
    //$(placeName).append("#personTable").html(tableHeader + tableRows);

}




function jsonToHTML(url, placeName) {
    //console.log("inside jsonToHTML \n" + url + " " + placeName + " " + dataType);
    loadJSON(url, placeName, tagify);
    return 0;
}


function search() {
    console.log("searching for articles now ");
    //$("#articles").attr("data-toggle", "collapse in");
    jsonToHTML("data/data.json", "#articles");
    
}