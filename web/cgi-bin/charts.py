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
        </head>
        <body>
        <div>             
""")

form = cgi.FieldStorage()
host1 = form.getfirst("p_host", "kspu.edu")[:100]
host1 = html.escape(host1)

print(f"<h1>Графік {host1}</h1>")

print("""

<script type="text/javascript">
google.charts.load('current', {packages: ['line', 'corechart']});

google.charts.setOnLoadCallback(drawLine);

function drawLine() {
      var data = new google.visualization.DataTable();
      var options = {
          title: 'Check HTTP',
          legend: {position: 'top'},
          hAxis: {
              title: 'Time',
              ticks: [0, 1]
          },
          vAxis: {
               title: 'Access'
          },
          colors: ['#a52714']
      };

      data.addColumn('date', 'Date');
      data.addColumn('number', 'Access');

      data.addRows([

""")

pwd = getcwd()
dir = path.join(pwd, 'charts_data')
res_file = f"{dir}/{host1}.http.data"

with open(res_file, "r") as f1:
    for x in f1:
        (d, a, rt) = x.split()
        print(f"[new {d}, {a}],")

print("""
      ]);

      var chart = new google.visualization.SteppedAreaChart(document.getElementById('chart_div'));
      chart.draw(data, options);
}
</script>
<div id="chart_div"></div>
</div>
</body>
</html>""")
