# Vehicle Parking App

Deployment URL: https://parkmate-vehicle-parking-app-production.up.railway.app/login

A Flask-based vehicle parking management system that allows users to book parking spots and admins to manage parking lots. Features include user registration, vehicle management, spot booking/release, and administrative controls.

## Technologies Used
- **Backend**: Python 3.9+, Flask
- **Database**: SQLite
- **Authentication**: bcrypt for password hashing
- **Frontend**: HTML, CSS, JavaScript
- **API**: Flask-RESTX

## How to Run

### Prerequisites
- Python 3.9+

### Setup & Run
```bash
# Navigate to project directory
cd /home/ganesh/Coding/vehicle-parking-app

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install Flask flask-restx bcrypt python-dotenv

# Set secret key (required)
export SECRET_KEY="dev-secret-key"

# Run the application
python app.py
```

### Access the App
- Open: http://127.0.0.1:5000/
- **Admin Login**:
  - Email: `admin@parking.com`
  - Password: `admin@123`

### Troubleshooting
- **Port 5000 in use?** Run: `FLASK_RUN_PORT=5001 python app.py`
- **Database issues?** Delete `database/parking.db` to reset (loses data)
