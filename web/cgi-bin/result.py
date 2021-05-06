#!/usr/bin/env python3
import json2table
import json
import glob
import cgi
import sys
import codecs
from os import getcwd, path

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html\n")
print("""
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Моніторинг</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    var secondsToUpdate = 600;
    function tick() {
        document.getElementById("timer").innerHTML = secondsToUpdate;
        if (secondsToUpdate <= 0) {
	    secondsToUpdate = 600;
	    location.reload(true);
	} else {
	    setTimeout("tick()", 1000);
	    secondsToUpdate -= 1;
	}
    }
</script>
</head>
<body onLoad = "JavaScript:tick()">
<nav class="navbar navbar-expand-lg nav-pills" style="background-color: #ccd9d9;">
  <a class="nav-link" href="/">Моніторинг сервісів</a>
  <a class="nav-link active" href="/cgi-bin/result.py">Сервіси ХДУ - загальний статус</a>
  <a class="nav-link" href="/cgi-bin/charts.py">Графіки</a>
</nav>
<div class="container-fluid">
<h1>Сервіси ХДУ - загальний статус</h1>
<div class="row align-items-start">
<div class="col">
""")

form = cgi.FieldStorage()
host1 = form.getfirst("p_host", "kspu.edu")[:100]

dir_charts  = "charts_data"
dir_results = "results"

# Колонка з графіком
print(f"<h2>{host1}</h2>")
print('<p>Сторінка буде перезавантажена за <span id="timer">600</span> сек.</p>')

print("""
<script type="text/javascript">
google.charts.load('current', {packages: ['line', 'corechart']});
google.charts.setOnLoadCallback(drawLine);

function drawLine() {
      var data = new google.visualization.DataTable();
      var options = {
          title: 'Check HTTP',
          legend: {position: 'top'},
          width: 600,
          series: {
              0: {type: 'line', targetAxisIndex: 0, color: 'grey'},
              1: {type: 'steppedArea', targetAxisIndex: 1, color: '#c76f61'}
          },
          hAxis: {
              title: 'Time',
              format: 'HH:mm'
          },
          vAxes: [
               {title: 'Latency, ms', label: 'Latency, ms'},
               {label: 'Access', ticks: [0, 1], textPosition: 'none'}
          ]
      };
      data.addColumn('datetime', 'Date');
      data.addColumn('number', 'Latency');
      data.addColumn('number', 'Access');
      data.addRows([
""")

chart_file = f"{dir_charts}/{host1}.http.data"
is_error = False

try:
    with open(chart_file, "r") as f1:
        for x in f1:
            (d, a, lt) = x.split()
            print(f"[new {d}, {lt}, {a}],")
except FileNotFoundError:
    print("[new Date(2000,0,1,0,0), 0, 0]")
    is_error = True

print("""
      ]);

      var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
      chart.draw(data, options);
}
</script>
<div id="chart_div"></div>
""")

if is_error:
    print(f"<p>Failed to find data for domain {host1}</p>")


# Таблиця з файлу results/domain.json
print("<br/>")

result_file = f"{dir_results}/{host1}.json"
with open(result_file, "rb") as jsonfile:
    infoFromJson = json.load(jsonfile)
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"class": "table table-sm table-condensed table-bordered"}
    print(json2table.convert(infoFromJson, build_direction=build_direction, table_attributes=table_attributes))

print("</div>")

# Колонка з таблицею статусів

res_files = glob.glob(f"{dir_results}/*.json")
res_files.sort()

print ("""
<div class="col">
<table class="table table-sm table-condensed table-bordered table-hover w-auto text-xsmall">
<thead><tr><th scope="col">Name</th><th scope="col">Check date</th><th scope="col">Ping</th><th scope="col">http</th></tr></thead>
<tbody>
</div>
</div>
""")

for f in res_files:
    with open(f, "rb") as jsonfile:
        json_str = json.load(jsonfile)
        domain = json_str['domain']
        check_time = json_str['timestamp']
        if 'results' in json_str:
            if 'ping' in json_str['results']:
                check_ping = json_str['results']['ping']['status'] if 'status' in json_str['results']['ping'] else 'fail'
            if 'http' in json_str['results']:
                check_http = json_str['results']['http']['status'] if 'status' in json_str['results']['http'] else 'fail'
        else:
            check_ping = 'fail'
            check_http = 'fail'

        td_check_ping = f'<td class="table-success">{check_ping}</td>' if check_ping == 'ok' else f'<td class="table-danger">{check_ping}</td>'
        td_check_http = f'<td class="table-success">{check_http}</td>' if check_http == 'ok' else f'<td class="table-danger">{check_http}</td>'


        print (f"<tr><th scope=\"row\"><a href=\"/cgi-bin/result.py?p_host={domain}\">{domain}</a></td><td>{check_time}</td>{td_check_ping}{td_check_http}</tr>\n")
print ('</tbody></table>')


print("""</div>
        </body>
        </html>""")
