# Smart Attendance & Academic Assessment System

**A Facial Recognition Solution for Automated Grading and Attendance Tracking.**

## 📝 Project Summary

The **Smart Attendance System** is a high-performance Django application that replaces manual roll-calling with AI-powered facial recognition. Using **OpenCV's LBPH (Local Binary Patterns Histograms)** algorithm, the system identifies students in real-time, logs their entry/exit times, and automatically calculates academic assessment points based on their attendance consistency.

### Key Features:

* **Live AI Detection:** Real-time face recognition with confidence scoring.
* **Session Management:** Admin-controlled time windows to prevent "ghost" attendance.
* **One-Click Registration:** Admin-supervised student enrollment with live photo capture.
* **Automated Grading:** Instant calculation of "Grade Points" (out of 10) based on attendance percentages.
* **Responsive Dashboard:** A modern, mobile-friendly interface with real-time log updates.
* **Data Export:** One-click CSV generation for official records.

---

## 🚀 Installation Guide (Step-by-Step)

### 1. Prerequisites

Ensure you have the following installed:

* **Python 3.10+**
* **C++ Compiler** (Required for OpenCV/Dlib if not using pre-built wheels)
* **Git**

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-attendance-system.git
cd smart-attendance-system

# Create a virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install django opencv-python opencv-contrib-python numpy

```

### 4. Database Initialization

```bash
python manage.py makemigrations
python manage.py migrate

# Create the Admin account
python manage.py createsuperuser

```

### 5. Run the Server

```bash
python manage.py runserver

```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📖 User Manual

### Phase 1: Registration (The "Enrollment" Stage)

1. Log in as an **Admin**.
2. Navigate to the **Register Student** page.
3. Enter the Student ID and Full Name.
4. Position the student in front of the camera and click **Take Snapshot**.
5. If the image is clear, click **Confirm & Save**. The system will automatically retrain its AI model.

### Phase 2: Starting a Session

Attendance is only recorded during "Active Sessions."

1. Go to the **Django Admin Panel** (`/admin`).
2. Under **Sessions**, create a new session (e.g., "CSC101 Lecture").
3. Set the start and end times and ensure **Is Active** is checked.

### Phase 3: Live Attendance

1. Open the **Dashboard**.
2. As students walk past the camera, the system will identify them.
3. A green **START** badge appears in the log.
4. The system enforces a **7-minute rule**: Students cannot log a "Finish" time until 7 minutes after their "Start" time.

### Phase 4: Assessment & Grading

1. Navigate to the **Assessment Report** page.
2. View the real-time **Grade Points** (0.0 to 10.0) for every student.
3. Use the **Search Bar** to find specific students.
4. Click **Print PDF** to generate an official grade sheet.

---

## 🛠 Tech Stack

* **Backend:** Django (Python 3)
* **Computer Vision:** OpenCV (LBPH Face Recognizer)
* **Frontend:** HTML5, CSS3 (Modern Flexbox/CSS Variables), JavaScript (ES6)
* **Database:** SQLite (Default) / PostgreSQL
