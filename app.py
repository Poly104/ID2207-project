from flask import Flask, render_template, url_for, request, redirect
import csv


app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/customerservice/home")
def customerServiceHome():
    return render_template("customerServiceHome.html")


@app.route("/customerservice/form")
def customerServiceForm():
    return render_template("customerServiceForm.html")


@app.route("/customerservice/form/submit", methods=["POST"])
def evnetPlanningRequestSubmit():
    # Get data from form
    record_number = request.form.get("record_number")
    client_name = request.form.get("client_name")
    event_type = request.form.get("event_type")
    start_date = request.form.get("start_date")
    duration = request.form.get("duration")
    attendees_number = request.form.get("attendees_number")
    preferences = request.form.get("preferences")
    budget = request.form.get("budget")

    # Save data to a file
    with open("event_request.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Record Number",
                    "Client Name",
                    "Event Type",
                    "Start Date",
                    "Duration",
                    "Attendees Number",
                    "Preferences",
                    "Budget",
                ]
            )

        writer.writerow(
            [
                record_number,
                client_name,
                event_type,
                start_date,
                duration,
                attendees_number,
                preferences,
                budget,
            ]
        )
    return redirect(url_for("customerServiceHome"))


if __name__ == "__main__":
    app.run(debug=True)
