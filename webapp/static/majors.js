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

var advanced_options_visible = false;

function initialize() {
    var element = document.getElementById('majors_button');
    if (element) {
        element.onclick = onMajorsButtonClicked;
    }
}

function onMajorsButtonClicked() {
    var url = getUrl();
    var columns = getDataTypesForTableColumns();
    // Send the request to the Books API /majors/ endpoint
    //wish able to see the url
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
        tableBody += buildTableHeader(columns);
        tableBody += buildTableBody(majorsList, columns);
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

function getUrl() {
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
    myParam = "";
  }
  var url = getBaseURL() + '/majors/' + myParam;
  return url;
}

function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + api_port;
    return baseURL;
}

function getDataTypesForTableColumns() {
  if(advanced_options_visible){
    var columns = ['major'];
  }
  else {
    var columns = ['major', 'category', 'median', 'percent_employed'];
    var checkboxes = document.getElementById("advanced_options_form");
    if(checkboxes){
      for (var j = 0; j < checkboxes.length; j++){
        var checkbox = checkboxes.elements[j];
        if (checkbox.checked){
          var data_type = checkbox.getAttribute("value")
          columns.push(data_type);
        }
      }
    }
  }
  return columns;
}

function buildTableHeader(columns) {
  var header ='<tr>';
  for (var c = 0; c < columns.length; c++){
    var data_type = columns[c].replace("_", " ");
    header += '<th>' + data_type +'</th>';
  }
  header += '</tr>';
  return header;
}

function buildTableBody(majorsList, columns){
  var body = "";
  for (var k = 0; k < majorsList.length; k++) {
      var row = '<tr>';
      var major = majorsList[k]
      for (var c = 0; c < columns.length; c++){
        var data_type = columns[c];
        row += '<td>' + major[data_type] +'</td>';
      }
      row += '</tr>';
      body += row;
  }
  return body;
}

// later make "toggleAdvancedOptions"
function toggleAdvancedOptions() {
    var advanced_options_button = document.getElementById("advanced_options_button");
    var advanced_options_form_html = "";
    if(!advanced_options_visible){
      advanced_options_visible = true;
      advanced_options_button.textContent = "Hide Advanced Options";
      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='category' checked><label for='category'>Category</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='total'><label for='total'>Total Students</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='men'><label for='men'>Men</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='women'><label for='men'>Women</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_men'><label for='percent_men'>Percent Men</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_women'><label for='percent_women'>Percent Women</label><br>";
      advanced_options_form_html += "</div>";

      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='employed'><label for='employed'>Employed</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='full_time'><label for='full_time'>Employed Full Time</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='part_time'><label for='part_time'>Employed Part Time</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='unemployed'><label for='unemployed'>Unemployed</label><br>";
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
      advanced_options_form_html += "</div>";

      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='percent_employed' checked><label for='percent_employed'>Percent Employed</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_full_time'><label for='percent_full_time'>Percent Employed Full-time</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_part_time'><label for='percent_part_time'>Percent Employed Part-time</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='unemployment_rate'><label for='unemployment_rate'>Unemployed Rate</label><br>";
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
      advanced_options_form_html += "</div>";

      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='median' checked><label for='median'>Median Salary</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='p75th'><label for='p75th'>75th Percentile Salary</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='p25th'><label for='p25th'>25th Percentile Salary</label><br>";
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
      advanced_options_form_html += "</div>";

      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='college_jobs'><label for='college_jobs'>College Jobs</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='non_college_jobs'><label for='non_college_jobs'>Non College Jobs</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='low_wage_jobs'><label for='low_wage_jobs'>Low Wage Jobs</label><br>";
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
      advanced_options_form_html += "</div>";

      advanced_options_form_html += "<div class = 'column'>";
        advanced_options_form_html += "<input type='checkbox' value='percent_college_jobs'><label for='percent_college_jobs'>Percent College Jobs</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_non_college_jobs'><label for='percent_non_college_jobs'>Percent Non-College Jobs</label><br>";
        advanced_options_form_html += "<input type='checkbox' value='percent_low_wage_jobs'><label for='percent_low_wage_jobs'>Percent Low-Wage Jobs</label><br>";
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
        advanced_options_form_html += "<br>"
      advanced_options_form_html += "</div>";
    } else {
      advanced_options_visible = false;
      advanced_options_button.textContent = "Show Advanced Options";
    }
    document.getElementById("advanced_options_form").innerHTML = advanced_options_form_html;
}
