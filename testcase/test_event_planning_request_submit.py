# test_app.py

import csv
import os
from flask import Flask, request, redirect, url_for

from app import app, evnetPlanningRequestSubmit


# Function to simulate a test
def test_event_planning_request_submit():
    # Prepare test data
    test_data = {
        "record_number": "001",
        "client_name": "John Doe",
        "event_type": "Conference",
        "start_date": "2024-01-01",
        "duration": "2",
        "attendees_number": "100",
        "preferences": "Vegetarian",
        "budget": "1000",
    }

    # Mock request context
    with app.test_request_context(
        "/customerservice/form/submit", method="POST", data=test_data
    ):
        # Call the function directly
        evnetPlanningRequestSubmit()

    # Verify that the data was written to the CSV file
    with open("event_request.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

        # Check the number of rows in the CSV file
        assert len(rows) == 2  # 1 header + 1 data row

        # Check if the data row matches the input data
        assert rows[1] == [
            "001",
            "John Doe",
            "Conference",
            "2024-01-01",
            "2",
            "100",
            "Vegetarian",
            "1000",
        ]

    # Cleanup: remove the test CSV file
    os.remove("event_request.csv")


# Call the test function
if __name__ == "__main__":
    test_event_planning_request_submit()
    print("Test passed!")
