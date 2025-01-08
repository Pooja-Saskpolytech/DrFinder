from flask import Flask, render_template, request, redirect, url_for
from models import db, Doctor

app = Flask(__name__)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///family_doctors.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Initialize the database within the app context
with app.app_context():
    db.create_all()  # This ensures the database tables are created.

# Seed data function
def seed_data():
    # Ensure this runs inside the application context
    with app.app_context():
        if not Doctor.query.first():  # Check if the database is empty
            doctors = [
                Doctor(name="Dr. John Smith", specialty="Pediatrics", location="Saskatoon, SK", years_of_experience=10),
                Doctor(name="Dr. Jane Doe", specialty="Internal Medicine", location="Regina, SK", years_of_experience=15),
                Doctor(name="Dr. Emily Davis", specialty="Family Medicine", location="Toronto, ON", years_of_experience=8),
            ]
            db.session.add_all(doctors)  # Add the doctors to the session
            db.session.commit()  # Commit the changes to the database

seed_data()

@app.route("/")
def index():
    doctors = Doctor.query.all()
    return render_template("index.html", doctors=doctors)

@app.route("/doctor/<int:doctor_id>")
def doctor_details(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template("details.html", doctor=doctor)

if __name__ == "__main__":
    app.run(debug=True)
