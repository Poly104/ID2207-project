from flask import Flask, render_template, url_for, request, redirect
import csv
import random


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


def update_budget_request_status_service(record_number, new_status):
    updated_rows = []
    with open("budget_request_service.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Project Reference"] == record_number:
                row["Status"] = new_status  # Update the status
            updated_rows.append(row)

    # Write the updated rows back to the CSV
    with open("budget_request_service.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)


def update_budget_request_status_production(record_number, new_status):
    updated_rows = []
    with open("budget_request_production.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Project Reference"] == record_number:
                row["Status"] = new_status  # Update the status
            updated_rows.append(row)

    # Write the updated rows back to the CSV
    with open("budget_request_production.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)


def update_new_hire_status(record_number, new_status):
    updated_rows = []
    with open("new_hire.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Reference Number"] == record_number:
                row["Status"] = new_status  # Update the status
            updated_rows.append(row)

    # Write the updated rows back to the CSV
    with open("new_hire.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)


def create_csv_with_headers(filename, headers):
    # Open the file in write mode, which will create a new file or overwrite an existing one
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row to the CSV file
        writer.writerow(headers)


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


# Service Manager
@app.route("/servicemanager/home")
def serviceManagerHome():
    data_task = read_csv("task_service.csv")
    data_extrabudget = read_csv("budget_request_service.csv")
    return render_template(
        "serviceManagerHome.html",
        data_task=data_task,
        data_extrabudget=data_extrabudget,
    )


@app.route("/servicemanager/newtask")
def serviceManagerNewTask():
    return render_template("serviceManagerNewTask.html")


@app.route("/servicemanager/newtask/submit", methods=["POST"])
def newTaskSubmit_service():
    # Get data from form
    project_reference = request.form.get("project_reference")
    assignee = request.form.get("assignee")
    priority = request.form.get("priority")
    description = request.form.get("description")
    status = "assigned"
    assignee_edit = ""

    # Save data to a file
    with open("task_service.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Project Reference",
                    "Assignee",
                    "Priority",
                    "Description",
                    "Status",
                    "Assignee Edit",
                ]
            )

        writer.writerow(
            [project_reference, assignee, priority, description, status, assignee_edit]
        )
    return redirect(url_for("serviceManagerHome"))


@app.route("/servicemanager/home/accept/<record_number>", methods=["POST"])
def accept_budget_request_by_servicemanager(record_number):
    update_budget_request_status_service(record_number, "approved by service manager")
    return "", 204


@app.route("/servicemanager/home/reject/<record_number>", methods=["POST"])
def reject_budget_request_by_servicemanager(record_number):
    update_budget_request_status_service(record_number, "rejected by service manager")
    return "", 204


@app.route("/servicemanager/newhire")
def serviceManagerNewHire():
    return render_template("serviceManagerNewHire.html")


@app.route("/servicemanager/newhire/submit", methods=["POST"])
def serviceManagerNewHireSubmit():
    # Get data from form
    reference = random.randint(1, 1000000)
    contract_type = request.form.get("contract_type")
    department = request.form.get("department")
    experience = request.form.get("experience")
    job_title = request.form.get("job_title")
    description = request.form.get("description")
    status = "pending"

    # Save data to a file
    with open("new_hire.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Reference Number",
                    "Contract Type",
                    "Requesting Department",
                    "Year of Experience",
                    "Job Title",
                    "Job Description",
                    "Status",
                ]
            )

        writer.writerow(
            [
                reference,
                contract_type,
                department,
                experience,
                job_title,
                description,
                status,
            ]
        )
    return redirect(url_for("serviceManagerHome"))


# service subteam
@app.route("/serviceteam/home")
def serviceTeamHome():
    data = read_csv("task_service.csv")
    return render_template(
        "serviceTeamHome.html",
        data=data,
    )


@app.route("/serviceteam/home/update/<int:row_id>", methods=["POST"])
def serviceTeamEditTaskSubmit(row_id):
    new_value = request.json["new_value"]
    data = read_csv("task_service.csv")

    # Update the specific column in the selected row
    data[row_id]["Assignee Edit"] = new_value
    data[row_id]["Status"] = "Edited by Assignee"

    # Write updated data back to CSV
    with open("task_service.csv", "w", newline="") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return redirect(url_for("serviceTeamHome"))


@app.route("/serviceteam/budgetrequest")
def serviceTeamBudgetRequest():
    return render_template("serviceTeamBudgetRequest.html")


@app.route("/serviceteam/budgetrequest/submit", methods=["POST"])
def serviceTeamBudgetRequestSubmit():
    # Get data from form
    project_reference = request.form.get("project_reference")
    department = request.form.get("department")
    amount = request.form.get("amount")
    sender = request.form.get("sender")
    reason = request.form.get("reason")
    status = "new"

    # Save data to a file
    with open("budget_request_service.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Project Reference",
                    "Department",
                    "Required Amount",
                    "Sender",
                    "Reason",
                    "Status",
                ]
            )

        writer.writerow([project_reference, department, amount, sender, reason, status])
    return redirect(url_for("serviceTeamHome"))


# Production Manager
@app.route("/productionmanager/home")
def productionManagerHome():
    data_task = read_csv("task_production.csv")
    data_extrabudget = read_csv("budget_request_production.csv")
    return render_template(
        "productionManagerHome.html",
        data_task=data_task,
        data_extrabudget=data_extrabudget,
    )


@app.route("/producitonmanager/newtask")
def productionManagerNewTask():
    return render_template("productionManagerNewTask.html")


@app.route("/productionmanager/newtask/submit", methods=["POST"])
def newTaskSubmit_production():
    # Get data from form
    project_reference = request.form.get("project_reference")
    assignee = request.form.get("assignee")
    priority = request.form.get("priority")
    description = request.form.get("description")
    status = "assigned"
    assignee_edit = ""

    # Save data to a file
    with open("task_production.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Project Reference",
                    "Assignee",
                    "Priority",
                    "Description",
                    "Status",
                    "Assignee Edit",
                ]
            )

        writer.writerow(
            [project_reference, assignee, priority, description, status, assignee_edit]
        )
    return redirect(url_for("productionManagerHome"))


@app.route("/productionmanager/home/accept/<record_number>", methods=["POST"])
def accept_budget_request_by_productionmanager(record_number):
    update_budget_request_status_production(
        record_number, "approved by production manager"
    )
    return "", 204


@app.route("/productionmanager/home/reject/<record_number>", methods=["POST"])
def reject_budget_request_by_productionmanager(record_number):
    update_budget_request_status_production(
        record_number, "rejected by production manager"
    )
    return "", 204


@app.route("/productionmanager/newhire")
def productionManagerNewHire():
    return render_template("productionManagerNewHire.html")


@app.route("/productionmanager/newhire/submit", methods=["POST"])
def productionManagerNewHireSubmit():
    # Get data from form
    reference = random.randint(1, 1000000)
    contract_type = request.form.get("contract_type")
    department = request.form.get("department")
    experience = request.form.get("experience")
    job_title = request.form.get("job_title")
    description = request.form.get("description")
    status = "pending"

    # Save data to a file
    with open("new_hire.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Reference Number",
                    "Contract Type",
                    "Requesting Department",
                    "Year of Experience",
                    "Job Title",
                    "Job Description",
                    "Status",
                ]
            )

        writer.writerow(
            [
                reference,
                contract_type,
                department,
                experience,
                job_title,
                description,
                status,
            ]
        )
    return redirect(url_for("productionManagerHome"))


# production subteam
@app.route("/productionteam/home")
def productionTeamHome():
    data = read_csv("task_production.csv")
    return render_template(
        "productionTeamHome.html",
        data=data,
    )


@app.route("/productionteam/home/update/<int:row_id>", methods=["POST"])
def productionTeamEditTaskSubmit(row_id):
    new_value = request.json["new_value"]
    data = read_csv("task_production.csv")

    # Update the specific column in the selected row
    data[row_id]["Assignee Edit"] = new_value
    data[row_id]["Status"] = "Edited by Assignee"

    # Write updated data back to CSV
    with open("task_production.csv", "w", newline="") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return redirect(url_for("productionTeamHome"))


@app.route("/productionteam/budgetrequest")
def productionTeamBudgetRequest():
    return render_template("productionTeamBudgetRequest.html")


@app.route("/productionteam/budgetrequest/submit", methods=["POST"])
def productionTeamBudgetRequestSubmit():
    # Get data from form
    project_reference = request.form.get("project_reference")
    department = request.form.get("department")
    amount = request.form.get("amount")
    sender = request.form.get("sender")
    reason = request.form.get("reason")
    status = "new"

    # Save data to a file
    with open("budget_request_production.csv", "a", newline="") as f:  # Append mode
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(
                [
                    "Project Reference",
                    "Department",
                    "Required Amount",
                    "Sender",
                    "Reason",
                    "Status",
                ]
            )

        writer.writerow([project_reference, department, amount, sender, reason, status])
    return redirect(url_for("productionTeamHome"))


# HR
@app.route("/hrteam/home")
def hrTeamHome():
    data = read_csv("new_hire.csv")
    return render_template(
        "hrTeamHome.html",
        data=data,
    )


@app.route("/hrteam/home/accept/<record_number>", methods=["POST"])
def resolve_request_by_hr(record_number):
    update_new_hire_status(record_number, "resolved")
    return "", 204


@app.route("/hrteam/home/reject/<record_number>", methods=["POST"])
def reject_request_by_hr(record_number):
    update_new_hire_status(record_number, "rejected")
    return "", 204


# Financial Manager
@app.route("/financialmanager/home")
def financialManagerHome():
    data_event = read_csv("event_request.csv")
    data_service = read_csv("budget_request_service.csv")
    data_production = read_csv("budget_request_production.csv")
    return render_template(
        "financialManagerHome.html",
        data_event=data_event,
        data_service=data_service,
        data_production=data_production,
    )


@app.route("/financialmanager/home/update/<int:row_id>", methods=["POST"])
def financialManagerCommentSubmit(row_id):
    new_value = request.json["new_value"]
    data = read_csv("event_request.csv")

    # Update the specific column in the selected row
    data[row_id]["Comment"] = new_value
    data[row_id]["Status"] = "reviewed by financial manager"

    # Write updated data back to CSV
    with open("event_request.csv", "w", newline="") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return redirect(url_for("financialManagerHome"))


@app.route("/financialmanager/home/service/accept/<record_number>", methods=["POST"])
def accept_request_by_financail_manager_service(record_number):
    update_budget_request_status_service(record_number, "approved by financial manager")
    return "", 204


@app.route("/financialmanager/home/service/reject/<record_number>", methods=["POST"])
def reject_request_by_financail_manager_service(record_number):
    update_budget_request_status_service(record_number, "rejected")
    return "", 204


@app.route("/financialmanager/home/production/accept/<record_number>", methods=["POST"])
def accept_request_by_financail_manager_production(record_number):
    update_budget_request_status_production(
        record_number, "approved by financial manager"
    )
    return "", 204


@app.route("/financialmanager/home/production/reject/<record_number>", methods=["POST"])
def reject_request_by_financail_manager_production(record_number):
    update_budget_request_status_production(record_number, "rejected")
    return "", 204


if __name__ == "__main__":
    create_csv_with_headers(
        "budget_request_production.csv",
        [
            "Project Reference",
            "Department",
            "Required Amount",
            "Sender",
            "Reason",
            "Status",
        ],
    )
    create_csv_with_headers(
        "budget_request_service.csv",
        [
            "Project Reference",
            "Department",
            "Required Amount",
            "Sender",
            "Reason",
            "Status",
        ],
    )
    create_csv_with_headers(
        "event_request.csv",
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
        ],
    )
    create_csv_with_headers(
        "new_hire.csv",
        [
            "Reference Number",
            "Contract Type",
            "Requesting Department",
            "Year of Experience",
            "Job Title",
            "Job Description",
            "Status",
        ],
    )
    create_csv_with_headers(
        "task_production.csv",
        [
            "Project Reference",
            "Assignee",
            "Priority",
            "Description",
            "Status",
            "Assignee Edit",
        ],
    )
    create_csv_with_headers(
        "task_service.csv",
        [
            "Project Reference",
            "Assignee",
            "Priority",
            "Description",
            "Status",
            "Assignee Edit",
        ],
    )
    app.run(debug=True)
