from flask import Flask, render_template, url_for, request, redirect
import csv


app = Flask(__name__)


def read_csv(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def update_event_request_status(record_number, new_status):
    updated_rows = []
    with open("event_request.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Record Number"] == record_number:
                row["Status"] = new_status  # Update the status
            updated_rows.append(row)

    # Write the updated rows back to the CSV
    with open("event_request.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)


@app.route("/")
def login():
    return render_template("login.html")


# Customer Service
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
    status = "new"
    comment = ""

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
                    "Status",
                    "Comment",
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
                status,
                comment,
            ]
        )
    return redirect(url_for("customerServiceHome"))


# Senior Customer Service
@app.route("/seniorcustomerservice/home")
def seniorCustomerServiceHome():
    data = read_csv("event_request.csv")
    return render_template("seniorCustomerServiceHome.html", data=data)


@app.route("/seniorcustomerservice/home/accept/<record_number>", methods=["POST"])
def accept_request_by_scs(record_number):
    update_event_request_status(record_number, "approved by scs")
    return "", 204


@app.route("/seniorcustomerservice/home/reject/<record_number>", methods=["POST"])
def reject_event_request_by_scs(record_number):
    update_event_request_status(record_number, "rejected")
    return "", 204


# Admin Manager
@app.route("/administrativemanager/home")
def administrativeManagerHome():
    data = read_csv("event_request.csv")
    return render_template("administrativeManagerHome.html", data=data)


@app.route("/administrativemanager/home/accept/<record_number>", methods=["POST"])
def accept_request_by_admin(record_number):
    update_event_request_status(record_number, "approved by admin")
    return "", 204


@app.route("/administrativemanager/home/reject/<record_number>", methods=["POST"])
def reject_event_request_by_admin(record_number):
    update_event_request_status(record_number, "rejected")
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
