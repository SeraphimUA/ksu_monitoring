#!/usr/bin/env python3
import glob
import cgi
import html
import sys
import codecs
from os import getcwd, path

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("Content-type: text/html\n\n")

print("""<!DOCTYPE HTML>
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
        <body onLoad="JavaScript:tick()">
        <div>             
	<nav class="navbar navbar-expand-lg nav-pills" style="background-color: #ccd9d9;">
	  <a class="nav-link" href="/">Моніторинг сервісів</a>
	  <a class="nav-link" href="/cgi-bin/result.py">Сервіси ХДУ - загальний статус</a>
	  <a class="nav-link active" href="/cgi-bin/charts.py">Графіки</a>
	</nav>
""")

form = cgi.FieldStorage()
host1 = form.getfirst("p_host", "kspu.edu")[:100]
host1 = html.escape(host1)
# insert check if data file exists

print(f"<h1>Графік {host1}</h1>")
print('<p>Сторінка буде перезавантажена за <span id="timer">600</span> сек.</p>')

print("""

<script type="text/javascript">
google.charts.load('current', {packages: ['line', 'corechart']});

google.charts.setOnLoadCallback(drawLine);

function drawLine() {
      var data = new google.visualization.DataTable();

      var date_formatter = new google.visualization.DateFormat({ 
         pattern: "MMM dd, yyyy HH:mm"
      }); 

      var options = {
          title: 'Check HTTP',
          legend: {position: 'top'},
          series: {
              0: {type: 'line', targetAxisIndex: 0, color: 'grey'},
              1: {type: 'steppedArea', targetAxisIndex: 1, color: '#c76f61'}
          },
          hAxis: {
              title: 'Time',
              format: 'HH:mm'
          },
          vAxes: [
               {label: 'Latency, ms'},
               {label: 'Access', ticks: [0, 1], textPosition: 'none'}
          ]
      };

      data.addColumn('datetime', 'Date');
      data.addColumn('number', 'Latency');
      data.addColumn('number', 'Access');

      data.addRows([

""")

pwd = getcwd()
dir = path.join(pwd, 'charts_data')
res_file = f"{dir}/{host1}.http.data"
is_error = False

try:
    with open(res_file, "r") as f1:
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
</div>""")

if is_error:
    print("<p>Failed to find data for such domain</p>")

print("""</body>
</html>""")
