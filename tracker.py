import time
import threading
from google.cloud import firestore
from geopy.distance import geodesic
import os


# NEW: Put the name of your key file here. **
# Make sure this JSON file is in the SAME FOLDER as this Python script.
SERVICE_ACCOUNT_KEY_FILE = "truck-tracker-demo-firebase-adminsdk-fbsvc-035a1fbb0a.json"

# --- CONFIGURATION ---
# Coordinates of your laptop (or the location you want to track from)
LAPTOP_COORDS = (17.152335 , 79.618608)

# The distance in meters to be considered "nearby"
NEARBY_DISTANCE_METERS = 10  

# --- SCRIPT ---

# Check if the key file exists before trying to connect
if not os.path.exists(SERVICE_ACCOUNT_KEY_FILE):
    print(f"Authentication Error: The key file was not found.")
    print(f"Please make sure the file '{SERVICE_ACCOUNT_KEY_FILE}' is in the same folder as the script.")
    exit()

# Create a client to connect to Firestore using the key file directly
try:
    db = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_KEY_FILE)
    print("Successfully connected to Firestore.")
except Exception as e:
    print(f"Authentication Error: Could not create Firestore client from key file.")
    print(f"Error details: {e}")
    exit()

# A threading Event to signal when the script should stop.
callback_done = threading.Event()

# This function will be called every time the truck's location changes in the database.
def on_snapshot(doc_snapshot, changes, read_time):
    """Callback function for Firestore listener."""
    for doc in doc_snapshot:
        print(f"\n--- Received Update ---")
        
        # Get truck's location data from the database
        truck_data = doc.to_dict()
        truck_lat = truck_data.get('latitude')
        truck_lon = truck_data.get('longitude')

        if truck_lat is None or truck_lon is None:
            print("Waiting for valid truck coordinates...")
            continue
            
        truck_coords = (truck_lat, truck_lon)
        print(f"Truck Location: {truck_coords}")
        print(f"Your Location:  {LAPTOP_COORDS}")

        # Calculate the distance
        try:
            distance_m = geodesic(LAPTOP_COORDS, truck_coords).meters
            print(f"Distance: {distance_m:.2f} meters")

            # Check if the truck is nearby
            if distance_m <= NEARBY_DISTANCE_METERS:
                print("\n*** ALERT: TRUCK IS NEARBY! ***\n")
            else:
                print("Truck is not nearby.")

        except Exception as e:
            print(f"Could not calculate distance. Error: {e}")

# Create a reference to the specific document we want to watch
doc_ref = db.collection('truck').document('location')

print("\nStarting tracker...")
print(f"Watching for updates from the truck. You are at {LAPTOP_COORDS}.")
print(f"Will notify when truck is within {NEARBY_DISTANCE_METERS} meters.")
print("--------------------------------------------------")

# Watch the document for changes.
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Keep the script running to listen for updates.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping tracker...")
    doc_watch.unsubscribe()
