import os
import hashlib

from flask import Flask, render_template, request, url_for, redirect
from markdown import markdown

from report.api import DBClient
from report.conf import settings

app = Flask(__name__)

client = DBClient()


@app.route("/")
def index():
    return redirect(url_for("report"))


@app.route("/reports", methods=["POST", "GET"])
def report():
    if request.method == "POST":
        kwargs = request.form
        report_id = kwargs["report_id"]
        params = {key: value for key, value in kwargs.items() if key != "report_id"}

        if report_id:
            client.update_report(report_id, **params)
        else:
            client.create_report(**params)

    reports = client.list_report()
    return render_template("reports.html", reports=reports)


@app.route("/reports/<int:id>", methods=["GET", "POST"])
def report_detail(id):
    report = client.get_report(id)
    tasks = report.tasks
    if request.method == "POST":
        kwargs = request.form
        task_id = kwargs["task_id"]
        params = {key: value for key, value in kwargs.items() if key != "task_id" and value}

        if task_id:
            client.update_task(task_id, **params)
        else:
            tasks = client.create_task(id, **params)

    app.logger.info("Serving report %d with %d tasks", id, len(tasks))
    return render_template("reports_detail.html", report=report, tasks=tasks)


@app.route("/reports/<int:id>/delete", methods=["GET"])
def report_delete(id):
    client.delete_report(id)
    return redirect(url_for("index"))

@app.route("/tasks/<int:id>/delete", methods=["GET"])
def task_delete(id):
    client.delete_task(id)
    return redirect(url_for("index"))

@app.route("/reports/<int:id>/markdown")
def report_markdown(id):
    report = client.get_report(id)
    text = report.as_markdown()
    app.logger.debug(text)
    return (markdown(text), 200)

@app.route("/tasks/<int:id>", methods=["GET", "POST"])
def task(id):
    task = client.get_task(id)
    if request.method == "POST":
        params = request.form

        client.update_task(id, **params)

    app.logger.info("Serving task %d", id)
    return render_template("task.html", task=task)

def runserver():
    app.run(port=5050)
