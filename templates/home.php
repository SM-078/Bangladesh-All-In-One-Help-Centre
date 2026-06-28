<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Home</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          {% for category, message in messages %}
            <div class="flash-messages {{ category }}">{{ message }}</div>
          {% endfor %}
        {% endif %}
      {% endwith %}

    <header class="logo-header">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" width="500" />
    </header>
    <header>
        <h1>Bangladesh All-In-One Help Center</h1>
        <p>Get immediate support in case of emergency, accident, shelter, for any need all in one site!</p>
        <p>Work of Swapnadip Mohajan, student of CGS under Cambridge Education, dedicated to research and public assistance.</p>
    </header>

    <h3>Welcome, {{ session['user'] }}</h3>
    <ul>
        <li><a href="{{ url_for('emergency_contact') }}">Emergency Contact</a></li>
        <li><a href="{{ url_for('accident_support') }}">Accident Support</a></li>
        <li><a href="{{ url_for('refugee_services') }}">Refugee Services</a></li>
        <li><a href="{{ url_for('govt_helpcenters') }}">Government Help Centers</a></li>
        <li><a href="{{ url_for('sim_help') }}">SIM Help</a></li>
        <li><a href="{{ url_for('international_help') }}">International Help</a></li>
        <li><a href="{{ url_for('quick_contact') }}">Quick Contact</a></li>
        <li><a href="{{ url_for('add_idea') }}">Add New Idea</a></li>
        <li><a href="{{ url_for('view_ideas') }}">View All New Ideas</a></li>
        <li><a href="{{ url_for('logout') }}">Logout</a></li>
    </ul>
    <p>Total Registered Users: <strong><?php echo file_get_contents("counter.txt"); ?></strong></p>

    <footer>
        <p>&copy; 2025 Bangladesh All-In-One Help Center. All rights reserved.</p>
    </footer>

</body>
</html>

