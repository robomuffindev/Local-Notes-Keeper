import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Add custom filters
from datetime import datetime

def format_datetime(value):
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return value

def format_size(bytes):
    if not bytes:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    bytes = float(bytes)
    while bytes >= 1024 and i < len(size_names)-1:
        bytes /= 1024
        i += 1
    return f"{bytes:.1f}{size_names[i]}"

def nl2br(value):
    if not value:
        return ""
    return value.replace('\n', '<br>')

app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['format_size'] = format_size
app.jinja_env.filters['nl2br'] = nl2br

# Base directory for app data
BASE_DIR = Path(__file__).resolve().parent / "app_data"
USERS_FILE = BASE_DIR / "users.json"

# Ensure base directories exist
BASE_DIR.mkdir(exist_ok=True)

# Initialize users file if it doesn't exist
if not USERS_FILE.exists():
    with open(USERS_FILE, "w") as f:
        json.dump({
            "admin": {
                "password": generate_password_hash("admin"),
                "is_admin": True,
                "created_at": datetime.now().isoformat()
            }
        }, f, indent=4)
    print("Created initial admin user with password: admin")

def get_users():
    """Load users from JSON file"""
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_user_dir(username):
    """Get the directory for user data"""
    user_dir = BASE_DIR / username
    user_dir.mkdir(exist_ok=True)
    
    # Create notes and files directories if they don't exist
    (user_dir / "notes").mkdir(exist_ok=True)
    (user_dir / "files").mkdir(exist_ok=True)
    
    return user_dir

def get_notes(username):
    """Get all notes for a user"""
    notes_dir = get_user_dir(username) / "notes"
    notes = []
    
    for note_file in notes_dir.glob("*.json"):
        with open(note_file, "r") as f:
            note = json.load(f)
            notes.append(note)
    
    # Sort notes by last modified time (newest first)
    notes.sort(key=lambda x: x.get("modified_at", ""), reverse=True)
    return notes

def get_note(username, note_id):
    """Get a specific note for a user"""
    note_file = get_user_dir(username) / "notes" / f"{note_id}.json"
    if note_file.exists():
        with open(note_file, "r") as f:
            return json.load(f)
    return None

def save_note(username, note):
    """Save a note for a user"""
    notes_dir = get_user_dir(username) / "notes"
    with open(notes_dir / f"{note['id']}.json", "w") as f:
        json.dump(note, f, indent=4)

def delete_note(username, note_id):
    """Delete a note for a user"""
    note_file = get_user_dir(username) / "notes" / f"{note_id}.json"
    if note_file.exists():
        note_file.unlink()
        return True
    return False

def get_files(username):
    """Get all files for a user"""
    files_dir = get_user_dir(username) / "files"
    files = []
    
    for file_path in files_dir.glob("*"):
        if file_path.is_file():
            files.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            })
    
    # Sort files by creation time (newest first)
    files.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return files

@app.route("/")
def index():
    """Main landing page"""
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        users = get_users()
        if username in users and check_password_hash(users[username]["password"], password):
            session["username"] = username
            session["is_admin"] = users[username].get("is_admin", False)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Handle user logout"""
    session.pop("username", None)
    session.pop("is_admin", None)
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    """User dashboard"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    return render_template(
        "dashboard.html",
        notes=get_notes(username),
        files=get_files(username),
        is_admin=session.get("is_admin", False)
    )

@app.route("/notes/new", methods=["GET", "POST"])
def new_note():
    """Create a new note"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if not title:
            flash("Note title is required")
            return render_template("note_form.html", content=content)
        
        username = session["username"]
        timestamp = datetime.now().isoformat()
        note_id = f"{int(datetime.now().timestamp())}"
        
        note = {
            "id": note_id,
            "title": title,
            "content": content,
            "created_at": timestamp,
            "modified_at": timestamp
        }
        
        save_note(username, note)
        flash("Note created successfully")
        return redirect(url_for("dashboard"))
    
    return render_template("note_form.html")

@app.route("/notes/<note_id>")
def view_note(note_id):
    """View a note"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    note = get_note(username, note_id)
    
    if note:
        return render_template("note_view.html", note=note)
    
    flash("Note not found")
    return redirect(url_for("dashboard"))

@app.route("/notes/<note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    """Edit a note"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    note = get_note(username, note_id)
    
    if not note:
        flash("Note not found")
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if not title:
            flash("Note title is required")
            return render_template("note_form.html", note=note)
        
        note["title"] = title
        note["content"] = content
        note["modified_at"] = datetime.now().isoformat()
        
        save_note(username, note)
        flash("Note updated successfully")
        return redirect(url_for("dashboard"))
    
    return render_template("note_form.html", note=note)

@app.route("/notes/<note_id>/delete", methods=["POST"])
def delete_note_route(note_id):
    """Delete a note"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    
    if delete_note(username, note_id):
        flash("Note deleted successfully")
    else:
        flash("Note not found")
    
    return redirect(url_for("dashboard"))

@app.route("/files/upload", methods=["POST"])
def upload_file():
    """Upload a file"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("dashboard"))
    
    file = request.files["file"]
    
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("dashboard"))
    
    if file:
        username = session["username"]
        filename = secure_filename(file.filename)
        file_path = get_user_dir(username) / "files" / filename
        
        # If file already exists, append a timestamp to make it unique
        if file_path.exists():
            name, ext = os.path.splitext(filename)
            timestamp = int(datetime.now().timestamp())
            filename = f"{name}_{timestamp}{ext}"
            file_path = get_user_dir(username) / "files" / filename
        
        file.save(file_path)
        flash("File uploaded successfully")
    
    return redirect(url_for("dashboard"))

@app.route("/files/<filename>")
def download_file(filename):
    """Download a file"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    files_dir = get_user_dir(username) / "files"
    
    return send_from_directory(files_dir, filename, as_attachment=True)

@app.route("/files/<filename>/delete", methods=["POST"])
def delete_file(filename):
    """Delete a file"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    file_path = get_user_dir(username) / "files" / filename
    
    if file_path.exists():
        os.remove(file_path)
        flash("File deleted successfully")
    else:
        flash("File not found")
    
    return redirect(url_for("dashboard"))

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """User settings"""
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    users = get_users()
    
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        
        if not check_password_hash(users[username]["password"], current_password):
            flash("Current password is incorrect")
            return render_template("settings.html")
        
        if new_password != confirm_password:
            flash("New passwords do not match")
            return render_template("settings.html")
        
        users[username]["password"] = generate_password_hash(new_password)
        save_users(users)
        flash("Password updated successfully")
    
    return render_template("settings.html")

@app.route("/admin")
def admin():
    """Admin panel"""
    if not session.get("is_admin", False):
        flash("Access denied")
        return redirect(url_for("dashboard"))
    
    users = get_users()
    return render_template("admin.html", users=users)

@app.route("/admin/users/add", methods=["POST"])
def add_user():
    """Add a new user"""
    if not session.get("is_admin", False):
        flash("Access denied")
        return redirect(url_for("dashboard"))
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    is_admin = request.form.get("is_admin") == "on"
    
    if not username or not password:
        flash("Username and password are required")
        return redirect(url_for("admin"))
    
    users = get_users()
    if username in users:
        flash("Username already exists")
        return redirect(url_for("admin"))
    
    users[username] = {
        "password": generate_password_hash(password),
        "is_admin": is_admin,
        "created_at": datetime.now().isoformat()
    }
    
    save_users(users)
    get_user_dir(username)  # Create user directories
    flash(f"User '{username}' created successfully")
    
    return redirect(url_for("admin"))

@app.route("/admin/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete a user"""
    if not session.get("is_admin", False):
        flash("Access denied")
        return redirect(url_for("dashboard"))
    
    if username == "admin":
        flash("Cannot delete the main admin user")
        return redirect(url_for("admin"))
    
    if username == session["username"]:
        flash("Cannot delete your own account")
        return redirect(url_for("admin"))
    
    users = get_users()
    if username in users:
        del users[username]
        save_users(users)
        
        # Remove user's directory
        user_dir = BASE_DIR / username
        if user_dir.exists():
            shutil.rmtree(user_dir)
        
        flash(f"User '{username}' deleted successfully")
    else:
        flash(f"User '{username}' not found")
    
    return redirect(url_for("admin"))

@app.route("/admin/users/<username>/reset-password", methods=["POST"])
def reset_user_password(username):
    """Reset a user's password"""
    if not session.get("is_admin", False):
        flash("Access denied")
        return redirect(url_for("dashboard"))
    
    new_password = request.form.get("new_password", "").strip()
    
    if not new_password:
        flash("New password is required")
        return redirect(url_for("admin"))
    
    users = get_users()
    if username in users:
        users[username]["password"] = generate_password_hash(new_password)
        save_users(users)
        flash(f"Password for user '{username}' reset successfully")
    else:
        flash(f"User '{username}' not found")
    
    return redirect(url_for("admin"))

@app.route("/admin/users/<username>/toggle-admin", methods=["POST"])
def toggle_admin(username):
    """Toggle admin status for a user"""
    if not session.get("is_admin", False):
        flash("Access denied")
        return redirect(url_for("dashboard"))
    
    if username == "admin":
        flash("Cannot change admin status for the main admin user")
        return redirect(url_for("admin"))
    
    users = get_users()
    if username in users:
        users[username]["is_admin"] = not users[username].get("is_admin", False)
        save_users(users)
        
        status = "granted" if users[username]["is_admin"] else "revoked"
        flash(f"Admin status for user '{username}' {status}")
    else:
        flash(f"User '{username}' not found")
    
    return redirect(url_for("admin"))

if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all network interfaces
    port = 5000
    print(f"LocalNotes running at http://{host}:{port}")
    
    # Print local IP addresses for convenience
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Access from other devices at: http://{local_ip}:{port}")
    
    app.run(host=host, port=port, debug=True)