import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Initialize Firebase Admin
cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

docs = list(db.collection("survey_data").stream())

column_order = ["UID", "Email", "Location", "IsAndroid", "IsIOS", "Rating", "WhatWouldYouAdd", "Feedback", "BusinessContactInfo", "EventInfo" "Date"]

# Write to CSV
with open("survey_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=column_order)
    writer.writeheader()
    for doc in docs:
        # Extract document data
        data = doc.to_dict()

        # Ensure all fields exist and handle missing fields
        for key in column_order:
            if key not in data:
                data[key] = False if key in ["IsAndroid", "IsIOS"] else ""

        # Convert boolean values to strings
        for key, value in data.items():
            if isinstance(value, bool):
                data[key] = str(value).lower()
            # Convert GeoPoint objects to "latitude,longitude"
            elif isinstance(value, firestore.GeoPoint):
                data[key] = f"{value.latitude},{value.longitude}"
            # Convert other non-serializable objects to strings
            elif not isinstance(value, (str, int, float)):
                data[key] = str(value)

        # Reorder the data dictionary to match the column order
        reordered_data = {key: data.get(key, "") for key in column_order}
        writer.writerow(reordered_data)