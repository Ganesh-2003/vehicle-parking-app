import csv
import sqlite3
import os
from datetime import datetime

def generate_csv_job(user_id, job_id):
    conn = sqlite3.connect("parking.db")
    cursor = conn.cursor()

    query = """
        SELECT 
            r.lot_id,
            pl.location_name,
            r.spot_id,
            r.vehicle_number,
            r.parking_timestamp,
            r.leaving_timestamp,
            r.parking_cost
        FROM Reserve_Parking_Spot r
        JOIN ParkingLot pl ON pl.lot_id = r.lot_id
        WHERE r.user_id = ?
        ORDER BY r.parking_timestamp DESC
    """
    rows = cursor.execute(query, (user_id,)).fetchall()

    # Path: /exports/user_5_20250121.csv
    os.makedirs("exports", exist_ok=True)
    file_path = f"exports/parking_history_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "lot_id", "location", "spot_id", "vehicle_number",
            "parking_timestamp", "leaving_timestamp",
            "parking_cost"
        ])
        writer.writerows(rows)

    conn.close()

    # Notify user via email, DB status update, or dashboard alert
    notify_export_complete(user_id, file_path)

def notify_export_complete(user_id, file_path):
    conn = sqlite3.connect("parking.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ExportHistory (user_id, file_path) VALUES (?, ?)",
        (user_id, file_path)
    )
    conn.commit()
    conn.close()
