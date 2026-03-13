import time
import threading
from google.cloud import firestore
from geopy.distance import geodesic
import os

<<<<<<< HEAD
# --- CONFIGURATION ---
SERVICE_ACCOUNT_KEY_FILE = "truck-tracker-demo-firebase-adminsdk-fbsvc-ae28fd03a8.json"

# The distance in meters to be considered "nearby"
NEARBY_DISTANCE_METERS = 500
=======

# NEW: Put the name of your key file here. **
# Make sure this JSON file is in the SAME FOLDER as this Python script.
SERVICE_ACCOUNT_KEY_FILE = "truck-tracker-demo-firebase-adminsdk-fbsvc-035a1fbb0a.json"

# --- CONFIGURATION ---
# Coordinates of your laptop (or the location you want to track from)
LAPTOP_COORDS = (17.152335 , 79.618608)

# The distance in meters to be considered "nearby"
NEARBY_DISTANCE_METERS = 10  
>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45

# --- SCRIPT ---

# Check if the key file exists before trying to connect
if not os.path.exists(SERVICE_ACCOUNT_KEY_FILE):
    print(f"Authentication Error: The key file was not found.")
    print(f"Please make sure the file '{SERVICE_ACCOUNT_KEY_FILE}' is in the same folder as the script.")
    exit()

<<<<<<< HEAD
# Create a client to connect to Firestore
=======
# Create a client to connect to Firestore using the key file directly
>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45
try:
    db = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_KEY_FILE)
    print("Successfully connected to Firestore.")
except Exception as e:
<<<<<<< HEAD
    print(f"Authentication Error: Could not create Firestore client.")
    print(f"Error details: {e}")
    exit()

# --- Fetch user location dynamically from Firebase ---
def get_user_location():
    """Reads the resident's saved location from Firestore."""
    try:
        doc = db.collection('user').document('location').get()
        if doc.exists:
            data = doc.to_dict()
            lat = data.get('latitude')
            lon = data.get('longitude')
            if lat and lon:
                return (lat, lon)
        print("\nWARNING: No user location found in database.")
        print("Please open user.html on your device and share your location first.")
        return None
    except Exception as e:
        print(f"Error fetching user location: {e}")
        return None

# A threading Event to signal when the script should stop.
callback_done = threading.Event()

# Fetch user location once at startup
print("\nFetching your location from database...")
USER_COORDS = get_user_location()

if USER_COORDS:
    print(f"Your location loaded: {USER_COORDS}")
else:
    print("Could not load user location. Tracker will wait for truck updates but cannot calculate distance.")

=======
    print(f"Authentication Error: Could not create Firestore client from key file.")
    print(f"Error details: {e}")
    exit()

# A threading Event to signal when the script should stop.
callback_done = threading.Event()

>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45
# This function will be called every time the truck's location changes in the database.
def on_snapshot(doc_snapshot, changes, read_time):
    """Callback function for Firestore listener."""
    for doc in doc_snapshot:
        print(f"\n--- Received Update ---")
<<<<<<< HEAD

        # Always re-fetch user location so it stays dynamic
        current_user_coords = get_user_location()

        if current_user_coords is None:
            print("Cannot calculate distance: user location not set.")
            print("Open user.html and share your location first.")
            continue

=======
        
>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45
        # Get truck's location data from the database
        truck_data = doc.to_dict()
        truck_lat = truck_data.get('latitude')
        truck_lon = truck_data.get('longitude')

        if truck_lat is None or truck_lon is None:
            print("Waiting for valid truck coordinates...")
            continue
<<<<<<< HEAD

        truck_coords = (truck_lat, truck_lon)
        print(f"Truck Location:  {truck_coords}")
        print(f"Your Location:   {current_user_coords}")

        # Calculate the distance
        try:
            distance_m = geodesic(current_user_coords, truck_coords).meters
            distance_km = distance_m / 1000

            if distance_m < 1000:
                print(f"Distance: {distance_m:.0f} meters")
            else:
                print(f"Distance: {distance_km:.2f} km")

            # Check if the truck is nearby
            if distance_m <= NEARBY_DISTANCE_METERS:
                print("\n" + "="*40)
                print("  *** ALERT: TRUCK IS NEARBY! ***")
                print("="*40 + "\n")
            else:
                print(f"Truck is not nearby. (Alert radius: {NEARBY_DISTANCE_METERS}m)")
=======
            
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
>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45

        except Exception as e:
            print(f"Could not calculate distance. Error: {e}")

# Create a reference to the specific document we want to watch
doc_ref = db.collection('truck').document('location')

print("\nStarting tracker...")
<<<<<<< HEAD
print(f"Alert radius set to: {NEARBY_DISTANCE_METERS} meters")
=======
print(f"Watching for updates from the truck. You are at {LAPTOP_COORDS}.")
print(f"Will notify when truck is within {NEARBY_DISTANCE_METERS} meters.")
>>>>>>> e13466b0397aef8cc585ad8bee4d7bcc7c8f6c45
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
