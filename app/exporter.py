#!/usr/bin/env python3
'''
Created on 2023/04/02

@author: khrz
'''
from flask import Flask, Response, render_template
import dblib, loglib

app = Flask(__name__)
app.logger.addHandler(loglib.handler)

@app.route("/")
def index():
    return '''
<html>
<head><title>CP4S Prometheus Exporter</title></head>
<body>
<h1>CP4S Prometheus Exporter</h1>
<p><a href="/metrics">Metrics</a></p>
</body>
</html>
'''

@app.route("/metrics")
def metrics():
    metrics = dblib.get_metrics()
    # print(metrics)
    return Response(render_template('metrics.txt', metrics=metrics), mimetype='text/plain')

if __name__ == '__main__':
    dblib.check_table()
    app.run(host="0.0.0.0", port=5000)