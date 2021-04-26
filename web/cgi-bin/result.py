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
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Моніторинг</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        <body>
        <div style="width: 600px">             
""")

print("<h1>Результати</h1>")

pwd = getcwd()
dir = path.join(pwd, 'results')
res_files = glob.glob(f"{dir}/*.json")

for f in res_files:
    with open(f, "rb") as jsonfile:
        infoFromJson = json.load(jsonfile)
        build_direction = "LEFT_TO_RIGHT"
        table_attributes = {"class": "table table-sm table-condensed table-bordered table-hover"}

        print(json2table.convert(infoFromJson, build_direction=build_direction, table_attributes=table_attributes))

print("""</div>
        </body>
        </html>""")
