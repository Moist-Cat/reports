import os
import hashlib

from flask import Flask, render_template, request, url_for, redirect

from report.api import DBClient
from report.conf import settings

app = Flask(__name__)

client = DBClient()

@app.route("/")
def index():
    return redirect(url_for("report"))

@app.route("/reports", methods=["POST", "GET"])
def report():
    if request.method=="POST":
        kwargs = request.form
        client.create_report(**kwargs)

    reports = client.list_report()
    return render_template("reports.html", reports=reports)

@app.route("/reports/<id>")
def report_detail(id):
    report =  client.get_report(id)
    return render_template("reports_detail.html", report=report)

@app.route("/reports/<id>/delete", methods=["DELETE"])
def report_delete(self, id):
    client.delete_report(id)
    return (204, "")

@app.route("/reports/<id>/update", methods=["PUT", "PATCH"])
def report_update(self, id):
    kwargs = request.form
    client.update_report(id, **kwargs)
    return (200, "")

@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    if request.method=="POST":
        kwargs = request.form
        client.create_task(**kwargs)
    tasks = client.list_task()
    return render_template("tasks.html", tasks=tasks)

@app.route("/tasks/<id>")
def task_detail(id):
    task = client.get_task(id)
    return render_template("task_detail.html", task=task)

@app.route("/tasks/<id>/delete", methods=["DELETE"])
def task_delete(self, id):
    client.delete_task(id)
    return (204, "")

@app.route("/tasks/<id>/update", methods=["PUT", "PATCH"])
def task_update(self, id):
    kwargs = request.form
    client.update_task(id, **kwargs)
    return (200, "")

def runserver():
    app.run(port=5050)
