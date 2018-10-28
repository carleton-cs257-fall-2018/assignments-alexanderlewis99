/*
 * books.js
 * Jeff Ondich, 27 April 2016
 * Updated, 4 May 2018
 *
 * A little bit of Javascript showing one small example of AJAX
 * within the "books and authors" sample for Carleton CS257,
 * Spring Term 2017.
 *
 * This example uses a very simple-minded approach to Javascript
 * program structure, which suffers from the problem of
 * "global namespace pollution". We'll talk more about this after
 * you get a feel for some Javascript basics.
 */

// IMPORTANT CONFIGURATION INFORMATION
// The contents of getBaseURL below reflects our assumption that
// the web application (books_website.py) and the API (books_api.py)
// will be running on the same host but on different ports.
//
// But if you take a look at the contents of getBaseURL, you may
// ask: where does the value of api_port come from? The answer is
// a little bit convoluted. (1) The command-line syntax of
// books_website.py includes an argument for the API port;
// and (2) the index.html Flask/Jinja2 template includes a tiny
// bit of Javascript that declares api_port and assigns that
// command-line API port argument to api_port. This happens
// before books.js is loaded, so the functions in books.js (like
// getBaseURL) can access api_port as needed.

initialize();

function initialize() {
    var element = document.getElementById('majors_button');
    if (element) {
        element.onclick = onMajorsButtonClicked;
    }
}

function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + api_port;
    return baseURL;
}

function onMajorsButtonClicked() {

    var myParam = '?';
    var formData = document.getElementById("majors_form");
    if(formData){
      var args = {
      "lim": formData.elements[0].value,
      "cat": formData.elements[1].value,
      "maj": formData.elements[2].value,
      "min_sal": formData.elements[3].value,
      "sort": formData.elements[4].value
        };
      if (args["lim"]){
        myParam = myParam + 'lim=' + args['lim'] + '&';
      }
      if (args["cat"]){
        myParam = myParam + 'cat=' + args['cat'].replace("&", "and") + '&';
      }
      if (args["maj"]){
        myParam = myParam + 'maj=' + args['maj'] + '&';
      }
      if (args["min_sal"]){
        myParam = myParam + 'min_sal=' + args['min_sal'] + '&';
      }
      if (args["sort"]){
        myParam = myParam + 'sort=' + args['sort'] + '&';
      }
      myParam = myParam.substring(0, myParam.length-1);

    } else {
      myParam = ""
    }

    var url = getBaseURL() + '/majors/' + myParam;
    // Send the request to the Books API /majors/ endpoint
    //wish able to see the url
    var columns = ['major'];
    var requested_data_types = document.getElementById("column_requirements_form");
    if(requested_data_types){
        /*for (var k = 0; k < requested_data_types.length; k++){
          data_type = requested_data_types.elements[k].value;
          if (data_type != ""){
              columns.push(data_type)
          }
        }*/
        for (var element in requested_data_types.elements){
            data_type = element.value;
            if (data_type != ""){
                columns.push(data_type)
            }
        }
    }
    var top ='<tr>';
    for (data_type in columns){
      data_type = data_type.replace("_", " ");
      top += '<th>' + data_type +'</th>';
    }
    top += '</tr>';
    fetch(url, {method: 'get'})
    // When the results come back, transform them from JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(majorsList) {
        // Build the table body.
        var tableBody = '';
        tableBody += url;
        tableBody += top;
        for (data_type in columns){
          tableBody += data_type;
        }
        for (var k = 0; k < majorsList.length; k++) {
            tableBody += '<tr>';
            for (data_type in columns){
              tableBody += '<td>' + majorsList[k][data_type] +'</td>';
            }
            tableBody += '</tr>';
        }
        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function getAuthor(authorID, authorName) {
    // Very similar pattern to onAuthorsButtonClicked, so I'm not
    // repeating those comments here. Read through this code
    // and see if it makes sense to you.
    var url = getBaseURL() + '/books/author/' + authorID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(booksList) {
        var tableBody = '<tr><th>' + authorName + '</th></tr>';
        for (var k = 0; k < booksList.length; k++) {
            tableBody += '<tr>';
            tableBody += '<td>' + booksList[k]['title'] + '</td>';
            tableBody += '<td>' + booksList[k]['publication_year'] + '</td>';
            tableBody += '</tr>';
        }
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}
