import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    q1 = request.form.get("q1")
    q2 = request.form.get("q2")
    q3 = request.form.get("q3")
    q4 = request.form.get("q4")
    # error check to make sure each of the values have been entered
    if not name or not q1 or not q2 or not q3 or not q4:
        return render_template("error.html")
    # write the submission into the csv
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "q1", "q2", "q3", "q4"])
        writer.writerow({"name": name, "q1": q1, "q2": q2, "q3": q3, "q4": q4})
    file.close()
    #redirect to sheet
    return redirect("/sheet")




@app.route("/sheet", methods=["GET"])
def get_sheet():
    # read through the file line by line
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    responses = list(reader)
    file.close()
    return render_template("sheet.html", responses=responses)


