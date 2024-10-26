# test_script.py

from app import update_event_request_status
import csv


# Function to read CSV and check status for a given record
def get_event_request_status(record_number):
    with open("event_request.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Record Number"] == record_number:
                return row["Status"]
    return None


# Test accept functionality
def test_accept_event():
    record_number = (
        "23945729348"  # Replace with an actual test record number in your CSV
    )
    update_event_request_status(record_number, "Accepted")

    # Check if the status was updated correctly
    status = get_event_request_status(record_number)
    if status == "Accepted":
        print("Test passed: Record was accepted successfully.")
    else:
        print("Test failed: Record status is not 'Accepted'.")


# Test reject functionality
def test_reject_event():
    record_number = (
        "23945729348"  # Replace with an actual test record number in your CSV
    )
    update_event_request_status(record_number, "Rejected")

    # Check if the status was updated correctly
    status = get_event_request_status(record_number)
    if status == "Rejected":
        print("Test passed: Record was rejected successfully.")
    else:
        print("Test failed: Record status is not 'Rejected'.")


# Run the tests
print("Running tests...")
test_accept_event()
test_reject_event()
