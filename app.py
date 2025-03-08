from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for using sessions

# ✅ Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",       # Change if using a remote database
    user="root",            # Your MySQL username
    password="ashwin@123",  # Your MySQL password
    database="login_db"     # The database name you created
)
cursor = db.cursor()

# ✅ Home Route
@app.route("/")
def home():
    return render_template("login.html")  # Shows login page

# ✅ Login Route
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    # Debugging: Print values to check
    print("Trying to login with:", email, password)

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    print("Database result:", user)  # Check what MySQL returns

    if user:
        session["user"] = email
        return "Login Successful! 🎉"
    else:
        return "Invalid credentials, try again."

# ✅ Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        
        return "Registration Successful! 🎉"  # You can redirect to login page

    return render_template("register.html")

# ✅ Clear Session Route (Fix for Chrome Login Issue)
@app.route("/clear_session")
def clear_session():
    session.clear()  # Clears all stored session data
    return "Session cleared! Try logging in again."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
