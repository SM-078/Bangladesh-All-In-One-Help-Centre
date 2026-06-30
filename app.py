from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with something secure

# --- Database Setup ---
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        # 1. Users Table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
        # 2. Ideas Table
        c.execute('''CREATE TABLE IF NOT EXISTS ideas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        topic TEXT,
                        idea TEXT,
                        contact TEXT
                    )''')
        # 3. Permanent Counter Table
        c.execute('''CREATE TABLE IF NOT EXISTS site_stats (
                        metric TEXT UNIQUE,
                        value INTEGER
                    )''')
        # Initialize counter row at 0 if it doesn't exist yet
        c.execute("INSERT OR IGNORE INTO site_stats (metric, value) VALUES ('login_count', 0)")
        conn.commit()

# Run database creation automatically when script starts up
init_db()

# --- Permanent Database Counter Helpers ---
def get_live_count():
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT value FROM site_stats WHERE metric='login_count'")
            row = c.fetchone()
            return row[0] if row else 0
    except Exception:
        return 0

def increment_live_count():
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE site_stats SET value = value + 1 WHERE metric='login_count'")
            conn.commit()
    except Exception:
        pass


# --- Routes ---
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?",
                      (username, password))
            user = c.fetchone()
            
        if user:
            session['user'] = username
            flash("Logged in successfully!", "success")
            
            # --- DATABASE DRIVEN PERMANENT COUNTER ---
            increment_live_count()
            
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password", "error")
            
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()

            if existing_user:
                flash(" User already exists, please re-enter", "error")
            else:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash(" Registered successfully! Please log in.", "success")
                return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    # Read directly from the persistent database
    current_users = get_live_count()
    return render_template('home.html', total_users=current_users)


@app.route('/accident_support')
def accident_support(): 
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('accident_support.html') 


@app.route('/emergency_contact')
def emergency_contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('emergency_contact.html')


@app.route('/refugee_services')
def refugee_services():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('refugee_services.html')


@app.route('/govt_helpcenters')
def govt_helpcenters():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('govt_helpcenters.html')


@app.route('/SIM_help')
def sim_help():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('SIM_help.html')


@app.route('/international_help')
def international_help():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('international_help.html')


@app.route('/quick_contact')
def quick_contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quick_contact.html')


@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        topic = request.form['topic']
        idea = request.form['idea']
        contact = request.form['contact']
        user = session['user']

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO ideas (user, topic, idea, contact) VALUES (?, ?, ?, ?)",
                (user, topic, idea, contact)
            )
            conn.commit()

        return render_template('add_idea.html', submitted=True)

    return render_template('add_idea.html', submitted=False)


@app.route('/view_ideas')
def view_ideas():
    if 'user' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT user, topic, idea, contact FROM ideas")
        ideas = c.fetchall()

    return render_template('view_ideas.html', ideas=ideas)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 81))
    app.run(host='0.0.0.0', port=port, debug=True)
