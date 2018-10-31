// Alec Wang and Bat-Orgil Batjargal

initialize();

var advanced_options_visible = false;
var help_button_visible = false;

function initialize() {
    var element = document.getElementById('majors_button');
    if (element) {
        element.onclick = onMajorsButtonClicked;
    }
}

function onMajorsButtonClicked() {
    var url = getUrl();
    var columns = getDataTypesForTableColumns();
    fetch(url, {method: 'get'})
    // When the results come back, transform them from JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())
    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(majorsList) {
        // Build the table body.
        var tableBody = '';
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
  if(!(advanced_options_visible)){
    var columns = ['major', 'category', 'percent_employed', 'median'];
  }
  else {
    var columns = ['major'];
    var checkboxes = document.getElementById("advanced_options_form");
    if(checkboxes){
      for (var j = 0; j < checkboxes.length; j++){
        var checkbox = checkboxes.elements[j];
        if (checkbox.checked){
          var data_type = checkbox.getAttribute("value");
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
      var major = majorsList[k];
      for (var c = 0; c < columns.length; c++){
        var data_type = columns[c];
        row += '<td>' + major[data_type] +'</td>';
      }
      row += '</tr>';
      body += row;
  }
  return body;
}

function toggle_help(){
  var help_button = document.getElementById("help_button");
  var help_button_html = "";
  if (help_button.textContent == "Show help text"){
    help_button.textContent = "Hide help text";
    help_button_html += "<div class = 'help_text_box'>";
    help_button_html += "Max # of results: The max number of results to be displayed in the table. <br><br>";
    help_button_html += "Category: Filter results by the following categories:<br>";
    help_button_html += "<ol>";
    help_button_html += "<li>Agriculture & Natural Resources</li>";
    help_button_html += "<li>Arts</li>";
    help_button_html += "<li>Biology & Life Science</li>";
    help_button_html += "<li>Business</li>";
    help_button_html += "<li>Communications & Journalism</li>";
    help_button_html += "<li>Computers & Mathematics</li>";
    help_button_html += "<li>Education</li>";
    help_button_html += "<li>Engineering</li>";
    help_button_html += "<li>Health</li>";
    help_button_html += "<li>Humanities & Liberal Arts</li>";
    help_button_html += "<li>Industrial Arts & Consumer Services</li>";
    help_button_html += "<li>Interdisciplinary</li>";
    help_button_html += "<li>Law & Public Policy</li>";
    help_button_html += "<li>Physical Sciences</li>";
    help_button_html += "<li>Psychology & Social Work</li>";
    help_button_html += "<li>Social Science</li>";
    help_button_html += "</ol>";
    help_button_html += "Major: Search text used to find majors (i.e. physics) <br><br>";
    help_button_html += "Minimum Salary: Filters results so that they include only majors whose median salaries match or exceed the miniumum salary.<br><br>";
    help_button_html += "Sort By: Sorts the results by the given element in alphabetical or descending order.<br>";
    help_button_html += "</div>";
  }
  else{
    help_button.textContent = "Show help text";
  }
  document.getElementById("help_text").innerHTML = help_button_html;
}

function toggleAdvancedOptions() {
    var advanced_options_button = document.getElementById("advanced_options_button");
    var advanced_options_form_html = "";
    if(!advanced_options_visible){
      advanced_options_visible = true;
      advanced_options_button.textContent = "Hide Advanced Options";
      advanced_options_form_html += "<div class = 'advanced_options_form_box'>";
        advanced_options_form_html += "<div class = 'small_column'>";
          advanced_options_form_html += "<input type='checkbox' value='category' checked><label for='category'>Category</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='total'><label for='total'>Total Students</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='men'><label for='men'>Men</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='women'><label for='men'>Women</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_men'><label for='percent_men'>Percent Men</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_women'><label for='percent_women'>Percent Women</label><br>";
        advanced_options_form_html += "</div>";

        advanced_options_form_html += "<div class = 'small_column'>";
          advanced_options_form_html += "<input type='checkbox' value='employed'><label for='employed'>Employed</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='full_time'><label for='full_time'>Employed Full Time</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='part_time'><label for='part_time'>Employed Part Time</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='unemployed'><label for='unemployed'>Unemployed</label><br>";
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
        advanced_options_form_html += "</div>";

        advanced_options_form_html += "<div class = 'large_column'>";
          advanced_options_form_html += "<input type='checkbox' value='percent_employed' checked><label for='percent_employed'>Percent Employed</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_full_time'><label for='percent_full_time'>Percent Employed Full-time</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_part_time'><label for='percent_part_time'>Percent Employed Part-time</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='unemployment_rate'><label for='unemployment_rate'>Unemployed Rate</label><br>";
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
        advanced_options_form_html += "</div>";

        advanced_options_form_html += "<div class = 'large_column'>";
          advanced_options_form_html += "<input type='checkbox' value='median' checked><label for='median'>Median Salary</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='p75th'><label for='p75th'>75th Percentile Salary</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='p25th'><label for='p25th'>25th Percentile Salary</label><br>";
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
        advanced_options_form_html += "</div>";

        advanced_options_form_html += "<div class = 'small_column'>";
          advanced_options_form_html += "<input type='checkbox' value='college_jobs'><label for='college_jobs'>College Jobs</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='non_college_jobs'><label for='non_college_jobs'>Non College Jobs</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='low_wage_jobs'><label for='low_wage_jobs'>Low Wage Jobs</label><br>";
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
        advanced_options_form_html += "</div>";

        advanced_options_form_html += "<div class = 'large_column'>";
          advanced_options_form_html += "<input type='checkbox' value='percent_college_jobs'><label for='percent_college_jobs'>Percent College Jobs</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_non_college_jobs'><label for='percent_non_college_jobs'>Percent Non-College Jobs</label><br>";
          advanced_options_form_html += "<input type='checkbox' value='percent_low_wage_jobs'><label for='percent_low_wage_jobs'>Percent Low-Wage Jobs</label><br>";
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
          advanced_options_form_html += "<br>"
        advanced_options_form_html += "</div>";

      advanced_options_form_html += "</div>";
    } else {
      advanced_options_visible = false;
      advanced_options_button.textContent = "Show Advanced Options";
    }
    document.getElementById("advanced_options_form").innerHTML = advanced_options_form_html;
}
