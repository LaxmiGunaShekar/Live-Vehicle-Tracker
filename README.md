# 🗑️ GarbageTrack — Live Garbage Truck Alerter

> *Know exactly when the truck is coming. No more waiting. No more missing it.*

A real-time GPS tracking system that tells residents when the garbage truck is approaching their street — built as a proof-of-concept for a genuine everyday problem across urban and semi-urban India.

**Live Demo →** [truck.html](https://laxmigunashekar.github.io/GarbageTrack/truck.html) · [user.html](https://laxmigunashekar.github.io/GarbageTrack/user.html)

---

## The Problem

In most neighborhoods across India, the garbage truck arrives without any warning. Residents either miss it entirely, or spend their morning listening for the horn. There is no system, no schedule, no notification — just luck.

This project is a working prototype that proves a simple idea: **a phone, a free database, and a browser are all you need to fix this.**

---

## Version History

---

### ⚙️ Version 1 — Python Terminal Alerter *(Initial Prototype)*

The first version was a minimal proof-of-concept. A webpage on the driver's phone sent GPS coordinates to Firebase, and a Python script on the resident's laptop watched the database and printed a terminal alert when the truck came within range.

**How it worked:**
- `truck.html` — opened on phone, sent live GPS to Firestore
- `tracker.py` — ran on laptop, watched Firestore, printed `*** ALERT: TRUCK IS NEARBY ***` in terminal
- Location was hardcoded in the Python script — no user input

**Limitation:** The resident had to keep a terminal open and manually enter their own coordinates. Not practical for real users.

---

### 🚀 Version 2 — Full Web Dashboard *(Current Version)*

Version 2 completely rethinks the resident experience. Everything now happens inside the browser — no Python, no terminal, no installation required. Any resident can open the page on their phone and have the full system running in seconds.

---

## What's New in Version 2

| Feature | V1 | V2 |
|---|---|---|
| Resident interface | Python terminal | Web dashboard |
| User location | Hardcoded in script | GPS from browser, saved to Firebase |
| Distance display | Terminal print | Live updating card, every 3 seconds |
| Alert | Terminal text | Animated banner + browser notification |
| Map | None | Live OpenStreetMap with both markers |
| Setup required | Python + pip install | Just open the URL |

---

## How It Works

```
📱 Driver's Phone          ☁️ Firebase              💻 Resident's Browser
  truck.html          →    Firestore DB    ←        user.html
 (sends GPS live)       (stores coords)         (reads + shows dashboard)
```

No backend server. No app install. Everything runs directly in the browser using Firebase's REST API.

---

## The Two Pages

### 🚛 `truck.html` — Driver / Transmitter
Designed to run on the garbage truck driver's phone.

- Captures live GPS using the browser's Geolocation API
- Sends coordinates to Firebase Firestore every few seconds
- Shows a radar pulse animation while transmitting
- Displays live latitude/longitude on screen
- Simple Stop/Start toggle button

### 🏠 `user.html` — Resident Dashboard
Everything the resident needs, in one page.

**Location Setup** (top section)
- One tap to share GPS and save home location to Firebase
- Location stored in database — persists across sessions
- Update button to re-share if moved

**Live Tracker** (bottom section, unlocks after location is set)
- 🔔 **Alert Banner** — pulses amber when truck is within 500m, green when safe
- 📏 **Distance Card** — live distance in meters or km, updates every 3 seconds
- 🚛 **Truck GPS Card** — live coordinates from the truck with a LIVE indicator
- 🗺️ **Interactive Map** — dark-themed OpenStreetMap showing both locations, connected by a dashed line, auto-zooms to fit

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Database | Google Firebase Firestore (REST API) |
| Maps | Leaflet.js + OpenStreetMap |
| GPS | Browser Geolocation API |
| Hosting | GitHub Pages |
| Legacy backend | Python 3, google-cloud-firestore, geopy |

---

## Running It Yourself

### Prerequisites
- A Google account (for Firebase)
- A phone with GPS and a browser

### Step 1 — Set up Firebase
1. Create a project at [firebase.google.com](https://firebase.google.com)
2. Enable **Firestore Database** in test mode
3. Update Firestore rules to allow read/write:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /truck/location { allow read, write: if true; }
    match /user/location  { allow read, write: if true; }
  }
}
```

### Step 2 — Add your Firebase config
In both `truck.html` and `user.html`, replace the `firebaseConfig` block with your own project's config (found in Firebase Console → Project Settings → Web App).

### Step 3 — Deploy
Push to GitHub and enable GitHub Pages from Settings → Pages → main branch. Both pages will be live at your GitHub Pages URL.

### Step 4 — Use it
1. Open `truck.html` on the driver's phone → tap **Start Transmitting**
2. Open `user.html` on the resident's device → tap **Share My Location**
3. The dashboard activates automatically and begins tracking

---

## Running the Legacy Python Alerter (V1)

If you want to run the original terminal-based version:

```bash
pip install google-cloud-firestore geopy
python tracker.py
```

Make sure your Firebase service account JSON key file is in the same folder and the filename matches `SERVICE_ACCOUNT_KEY_FILE` in the script.

> **Note:** The Python script requires `ngrok` to serve `truck.html` over HTTPS so the phone's browser grants GPS access. Run `python -m http.server 8000` and `ngrok http 8000` in separate terminals, then open the ngrok URL on your phone.

---

## Design Notes

- **GPS variance:** Consumer GPS chips have a natural accuracy range of 50–150 meters. The 500m alert radius is intentionally designed to compensate for device-level variance, ensuring residents receive timely alerts regardless of minor GPS drift.
- **Single resident:** The current prototype stores one user location at a time. Multi-resident support with individual user IDs is a planned future enhancement.
- **No backend:** All real-time communication is handled client-side via Firestore's REST API, keeping the system serverless and free to host.

---

## Future Enhancements

- 👥 Multi-resident support with unique user registration
- 📱 SMS/push notifications when browser is closed
- 🗺️ Truck route history and path visualization
- ⏰ Estimated arrival time based on truck speed and direction
- 🔐 Driver authentication to prevent spoofing

---

## Built With

Firebase · Leaflet.js · OpenStreetMap · GitHub Pages · Python

---

*GarbageTrack — Built as a BTech Mini Project, CSE, 3rd Year*
