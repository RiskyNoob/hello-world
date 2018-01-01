function load_json(url, placeName, callback) {
    var xObj = new XMLHttpRequest();
    xObj.overrideMimeType("application/json");
    //console.log("search url " + url);
    xObj.open('GET', url, true);
    xObj.onreadystatechange = function () {
        if (xObj.readyState == 4 && xObj.status == "200") {
            //console.log(xObj.responseText);
            //console.log("articles retrieved from server");
            callback(xObj.responseText, placeName);
        }
    };
    xObj.send();
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

//  style="max-width: 20rem;"

function prepare_card() {
    console.log("Preparing card");
    var card = '<div class="card text-white bg-primary">';
    //card += '<div class="card-header">' + lookupKey + '</div>';
    card += '<div class="card-body">';
    card += '<h4 class="card-title">' + "Card Title" + ' </h4>';
    card += '<p class="card-text">';
    card += "This is test."
    card += '</p>';
    card += '</div>';
    card += '</div>';

    card = '<div class="card col-2">'
    //+ '<img class="card-img-top" src="..." alt="Card image cap">'
    + '<div class="card-block bg-secondary">'
    + '<h4 class="card-title">Card title</h4>'
    + '<p class="card-text">Some quick example text to build on the card title and make up the bulk of the cards content.</p>'
    + '</div>'
    + '<ul class="list-group list-group-flush">'
    +   '<li class="list-group-item">Cras justo odio</li>'
    +   '<li class="list-group-item">Dapibus ac facilisis in</li>'
    +   '<li class="list-group-item">Vestibulum at eros</li>'
    + '</ul>'
    + '<div class="card-block">'
    + '<a href="#" class="card-link">Card link</a>'
    + '<a href="#" class="card-link">Another link</a>'
    + '</div>'
    + '</div>';

    return card;
}



function tag_entities(response, placeName, ) {
    var data = JSON.parse(response);

    var out = "";
    var articles = data.articles;
    var persons = data.persons;
    var nodes = data.network.nodes;
    var links = data.network.links;

    for (j = 0; j < persons.length; ++j) {
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


function tag_articles(response, place_name) {
    var articles = JSON.parse(response);
    console.log("tag_articles: number of articles " + articles.length);

    var out = "";
    var row_start = '<div class="row" style="padding:1px;">' ;
    var row_end = "</div>" ;
    var col1 = '<div class="col-2" ></div>';
    var col2_start = "<div class='col-8'>"  ;
    var col2_body = "";
    var col2_end = "</div>";
    var col3_start = '<div class="col-2">';
    var col3_body = "";
    var col3_end = '</div>';
    if (articles.length == 0) {
        col2_body = "<div class='row text-left h5' style='padding-left:0px;'>"
            + "No matching articles found"
            + "</div>";

        out += row_start 
            + col1 
            + col2_start + col2_body + col2_end 
            + col3_start + col3_body + col3_end
            row_end; 

    } else {
        for (var i = 0; i < articles.length; ++i) {
            col2_body =  
                "<div class='row text-left h5' style='padding-left:0px;'>" // title row start
                    + "<a href='" + articles[i].url + "'>"
                    + articles[i].title
                    + "</a>"
                + "</div>"  // title row end
                + "<div class='row text-left' style='padding-left:0px;'>" // body row start
                    + "<p>"
                    + "<small>"
                        + moment(articles[i].date).format("MMM DD, YYYY Z")
                    + "</small> "
                    + articles[i].text.substring(0, 600)
                    + "<a href='" 
                        + articles[i].url + "'> More ..."
                    + " </a>"
                    + "</p> " 
                + "</div>"; // body row end 

            //col3_body = prepare_card();

            out += row_start 
            + col1 
            + col2_start + col2_body + col2_end 
            + col3_start + col3_body + col3_end
            + row_end; 

            //console.log(out);
        }
        
    }
    $(place_name).html(out);
}

function fetch_articles(search_term, place_name) {
    url = "http://localhost:5000/articles/" + search_term;
    // console.log("Calling load_json with "
    //     + "\nsearch_term " + search_term
    //     + "\nplace_name " + place_name
    //     + "\nurl " + url);

    load_json(url, place_name, tag_articles);
}


function search() {
    // TODO - Fix this to take a search term 
    console.log("searching for articles now ");
    search_term = document.getElementById("searchBox").value;
    fetch_articles(search_term, "#articles")

}