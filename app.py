<!DOCTYPE html>
<html>
<head>
    <title>Education Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; padding: 40px; }
        .card { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; }
        button { padding: 10px 20px; margin-top: 10px; }
        a { display: inline-block; margin-top: 15px; }
    </style>
</head>
<body>

<div class="card">

{% if page == 'login' %}
    <h2>Login</h2>

    {% if error %}
        <p style="color:red">{{ error }}</p>
    {% endif %}

    <form method="POST">
        <input name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>

    <p>
        Admin: admin / admin123<br>
        Teacher: teacher / teacher123<br>
        Student: student / student123
    </p>

{% elif page == 'dashboard' %}
    <h2>Welcome {{ name }}</h2>
    <p>Role: <strong>{{ role }}</strong></p>

    {% if role == 'admin' %}
        <p>🛠 Admin Dashboard</p>
    {% elif role == 'teacher' %}
        <p>📚 Teacher Dashboard</p>
        <a href="/materials">Go to Materials</a>
    {% elif role == 'student' %}
        <p>📖 Student Dashboard</p>
        <a href="/state">My Courses</a>
    {% endif %}

    <br><a href="/logout">Logout</a>

{% elif page == 'materials' %}
    <h2>Course Materials</h2>
    <p>Teacher/Admin access</p>
    <a href="/dashboard">Back</a>

{% elif page == 'state' %}
    <h2>My Courses</h2>
    <p>Student view</p>
    <a href="/dashboard">Back</a>

{% endif %}

</div>

</body>
</html>
