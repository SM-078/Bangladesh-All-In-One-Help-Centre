from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with something secure

# --- Safe Counter Helper Function ---
def get_live_count():
    try:
        if os.path.exists("counter.txt"):
            with open("counter.txt", "r") as f:
                return int(f.read().strip())
    except Exception:
        pass
    return 0

# --- Database Setup ---
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ideas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        topic TEXT,
                        idea TEXT,
                        contact TEXT
                    )''')
        conn.commit()

# Run database creation automatically when script starts up
init_db()


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
            
            # --- SAFE LOGIN INCREMENT ---
            current_count = get_live_count()
            with open("counter.txt", "w") as f: 
                f.write(str(current_count + 1))
                
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
            # Check if the username already exists
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
        
    # Get the live text counter and pass it directly to home.html
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


# --- Add New Ideas Page ---
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
    app.run(host='0.0.0.0', port=81, debug=True)
