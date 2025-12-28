from flask import Flask, redirect, url_for, session, render_template_string, request
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mock user database (username: password, role)
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Admin User'},
    'teacher': {'password': 'teacher123', 'role': 'teacher', 'name': 'Teacher User'},
    'student': {'password': 'student123', 'role': 'student', 'name': 'Student User'}
}

# Role-based decorator
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                return "Access Denied: Insufficient permissions", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif role == 'student':
        return redirect(url_for('student_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template_string(ADMIN_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'])

@app.route('/teacher')
@role_required('teacher', 'admin')
def teacher_dashboard():
    return render_template_string(TEACHER_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'])

@app.route('/student')
@role_required('student', 'teacher', 'admin')
def student_dashboard():
    return render_template_string(STUDENT_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'])

@app.route('/state')
@role_required('student', 'teacher', 'admin')
def state_page():
    return render_template_string(STATE_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'])

@app.route('/materials')
@role_required('teacher', 'admin')
def materials_page():
    return render_template_string(MATERIALS_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'])

@app.route('/standards/<board>')
@role_required('teacher', 'admin')
def standards_page(board):
    return render_template_string(STANDARDS_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board)

@app.route('/subjects/<board>/<standard>')
@role_required('teacher', 'admin')
def subjects_page(board, standard):
    return render_template_string(SUBJECTS_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board,
                                   standard=standard)

@app.route('/language-options/<board>/<standard>/<subject>')
@role_required('teacher', 'admin')
def language_options_page(board, standard, subject):
    return render_template_string(LANGUAGE_OPTIONS_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board,
                                   standard=standard,
                                   subject=subject)

@app.route('/lessons/<board>/<standard>/<subject>/<language_level>')
@role_required('teacher', 'admin')
def lessons_page(board, standard, subject, language_level):
    return render_template_string(LESSONS_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board,
                                   standard=standard,
                                   subject=subject,
                                   language_level=language_level)

@app.route('/lesson-content/<board>/<standard>/<subject>/<language_level>/<int:lesson_number>')
@role_required('teacher', 'admin')
def lesson_content_page(board, standard, subject, language_level, lesson_number):
    return render_template_string(LESSON_CONTENT_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board,
                                   standard=standard,
                                   subject=subject,
                                   language_level=language_level,
                                   lesson_number=lesson_number)

@app.route('/subject-content/<board>/<standard>/<subject>')
@role_required('teacher', 'admin')
def subject_content_page(board, standard, subject):
    return render_template_string(SUBJECT_CONTENT_TEMPLATE, 
                                   name=session['name'], 
                                   username=session['user'],
                                   board=board,
                                   standard=standard,
                                   subject=subject)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Education Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        h1 { 
            color: #333; 
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-group { 
            margin-bottom: 20px; 
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            color: #333;
            font-weight: 500;
        }
        input[type="text"], input[type="password"] { 
            width: 100%; 
            padding: 12px; 
            border: 2px solid #e0e0e0; 
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, input[type="password"]:focus { 
            outline: none; 
            border-color: #667eea;
        }
        .btn { 
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 14px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .error { 
            background: #fee; 
            color: #c33; 
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            border-left: 4px solid #c33;
        }
        .demo-info {
            margin-top: 25px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 13px;
        }
        .demo-info h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .demo-info p {
            margin: 5px 0;
            color: #666;
        }
        .demo-info strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Education Portal</h1>
        <p class="subtitle">Sign in to continue</p>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        
        <div class="demo-info">
            <h3>Demo Accounts:</h3>
            <p><strong>Admin:</strong> admin / admin123</p>
            <p><strong>Teacher:</strong> teacher / teacher123</p>
            <p><strong>Student:</strong> student / student123</p>
        </div>
    </div>
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #dc3545;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:hover { 
            background: white;
            color: #dc3545;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .welcome {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .welcome h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .welcome p {
            color: #666;
            font-size: 16px;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .card { 
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
            border-left: 4px solid #dc3545;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .card.clickable {
            cursor: pointer;
            border-left-width: 6px;
        }
        .card.clickable:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(40,167,69,0.3);
        }
        .card h4 {
            color: #333;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .card p {
            color: #666;
            line-height: 1.6;
        }
        .card-icon {
            font-size: 36px;
            margin-bottom: 15px;
        }
        .nav-links {
            margin-top: 30px;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .nav-links a {
            color: #667eea;
            text-decoration: none;
            margin-right: 20px;
            font-weight: 600;
        }
        .nav-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>🛠️ Admin Dashboard</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">ADMINISTRATOR</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <div class="welcome">
            <h3>Welcome back, {{ name }}! 👋</h3>
            <p>You have full administrative access to all system features.</p>
        </div>
        
        <div class="cards">
            <div class="card">
                <div class="card-icon">👥</div>
                <h4>User Management</h4>
                <p>Manage all users, assign roles, and monitor user activity across the platform.</p>
            </div>
            <div class="card">
                <div class="card-icon">⚙️</div>
                <h4>System Settings</h4>
                <p>Configure system-wide settings, preferences, and security options.</p>
            </div>
            <div class="card">
                <div class="card-icon">📊</div>
                <h4>Reports & Analytics</h4>
                <p>View comprehensive reports, analytics, and performance metrics.</p>
            </div>
            <div class="card">
                <div class="card-icon">🔒</div>
                <h4>Security & Permissions</h4>
                <p>Manage security settings, permissions, and access control policies.</p>
            </div>
            <div class="card">
                <div class="card-icon">📚</div>
                <h4>Course Management</h4>
                <p>Oversee all courses, curricula, and educational content.</p>
            </div>
            <div class="card">
                <div class="card-icon">💬</div>
                <h4>Communication Hub</h4>
                <p>Send announcements, manage notifications, and moderate discussions.</p>
            </div>
        </div>
        
        <div class="nav-links">
            <strong>Quick Access:</strong>
            <a href="/teacher">→ Teacher Dashboard</a>
            <a href="/student">→ Student Dashboard</a>
        </div>
    </div>
</body>
</html>
'''

TEACHER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .welcome {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .welcome h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .welcome p {
            color: #666;
            font-size: 16px;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .card { 
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
            border-left: 4px solid #28a745;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .card h4 {
            color: #333;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .card p {
            color: #666;
            line-height: 1.6;
        }
        .card-icon {
            font-size: 36px;
            margin-bottom: 15px;
        }
        .nav-links {
            margin-top: 30px;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .nav-links a {
            color: #667eea;
            text-decoration: none;
            margin-right: 20px;
            font-weight: 600;
        }
        .nav-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📚 Teacher Dashboard</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <div class="welcome">
            <h3>Welcome back, {{ name }}! 👋</h3>
            <p>Manage your classes, assignments, and student progress.</p>
        </div>
        
        <div class="cards">
            <div class="card">
                <div class="card-icon">🏫</div>
                <h4>My Classes</h4>
                <p>View and manage all your classes, schedules, and student rosters.</p>
            </div>
            <div class="card">
                <div class="card-icon">📝</div>
                <h4>Assignments</h4>
                <p>Create, distribute, and grade assignments for your students.</p>
            </div>
            <div class="card">
                <div class="card-icon">📊</div>
                <h4>Grade Book</h4>
                <p>Track student performance, grades, and generate progress reports.</p>
            </div>
            <div class="card">
                <div class="card-icon">📅</div>
                <h4>Schedule</h4>
                <p>View your teaching schedule, upcoming classes, and important dates.</p>
            </div>
            <div class="card clickable" onclick="window.location.href='/materials'">
                <div class="card-icon">📖</div>
                <h4>Course Materials</h4>
                <p>Upload and organize course materials, lectures, and resources.</p>
            </div>
            <div class="card">
                <div class="card-icon">💬</div>
                <h4>Communication</h4>
                <p>Message students, send announcements, and manage discussions.</p>
            </div>
        </div>
        
        <div class="nav-links">
            <strong>Quick Access:</strong>
            <a href="/student">→ Student Dashboard</a>
        </div>
    </div>
</body>
</html>
'''

STUDENT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #007bff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:hover { 
            background: white;
            color: #007bff;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .welcome {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .welcome h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .welcome p {
            color: #666;
            font-size: 16px;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .card { 
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
            border-left: 4px solid #007bff;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .card.clickable {
            cursor: pointer;
            border-left-width: 6px;
        }
        .card.clickable:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(0,123,255,0.3);
        }
        .card h4 {
            color: #333;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .card p {
            color: #666;
            line-height: 1.6;
        }
        .card-icon {
            font-size: 36px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📖 Student Dashboard</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">STUDENT</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <div class="welcome">
            <h3>Welcome back, {{ name }}! 👋</h3>
            <p>Continue your learning journey and track your progress.</p>
        </div>
        
        <div class="cards">
            <div class="card clickable" onclick="window.location.href='/state'">
                <div class="card-icon">📚</div>
                <h4>My Courses</h4>
                <p>Access all your enrolled courses and learning materials.</p>
            </div>
            <div class="card">
                <div class="card-icon">✍️</div>
                <h4>Assignments</h4>
                <p>View pending assignments, submit work, and track deadlines.</p>
            </div>
            <div class="card">
                <div class="card-icon">📊</div>
                <h4>Grades</h4>
                <p>Check your grades, view feedback, and monitor your academic progress.</p>
            </div>
            <div class="card">
                <div class="card-icon">📅</div>
                <h4>Schedule</h4>
                <p>View your class schedule, upcoming exams, and important dates.</p>
            </div>
            <div class="card">
                <div class="card-icon">📖</div>
                <h4>Resources</h4>
                <p>Access course materials, textbooks, and supplementary resources.</p>
            </div>
            <div class="card">
                <div class="card-icon">💬</div>
                <h4>Messages</h4>
                <p>Communicate with teachers and classmates, view announcements.</p>
            </div>
        </div>
    </div>
</body>
</html>
'''

STATE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My Courses - State</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #007bff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #007bff;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #007bff;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .page-header h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .page-header p {
            color: #666;
            font-size: 16px;
        }
        .courses-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }
        .course-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .course-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
        }
        .course-header h4 {
            font-size: 22px;
            margin-bottom: 8px;
        }
        .course-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .course-body {
            padding: 25px;
        }
        .course-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 14px;
            color: #666;
        }
        .course-progress {
            margin-bottom: 15px;
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
            color: #333;
            font-weight: 600;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            transition: width 0.3s;
        }
        .course-actions {
            display: flex;
            gap: 10px;
        }
        .action-btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .primary-btn {
            background: #007bff;
            color: white;
        }
        .primary-btn:hover {
            background: #0056b3;
        }
        .secondary-btn {
            background: #f8f9fa;
            color: #333;
            border: 2px solid #e0e0e0;
        }
        .secondary-btn:hover {
            background: #e9ecef;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📚 My Courses</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">STUDENT</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/student" class="back-link">← Back to Dashboard</a>
        
        <div class="page-header">
            <h3>My Enrolled Courses</h3>
            <p>Continue learning and track your progress across all courses.</p>
        </div>
        
        <div class="courses-grid">
            <div class="course-card">
                <div class="course-header">
                    <h4>Introduction to Python Programming</h4>
                    <p>Instructor: Dr. Sarah Johnson</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Sep 2024</span>
                        <span>⏱️ 12 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>75%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 75%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <div class="course-card">
                <div class="course-header">
                    <h4>Data Structures & Algorithms</h4>
                    <p>Instructor: Prof. Michael Chen</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Oct 2024</span>
                        <span>⏱️ 14 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>45%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 45%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <div class="course-card">
                <div class="course-header">
                    <h4>Web Development Fundamentals</h4>
                    <p>Instructor: Emily Rodriguez</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Nov 2024</span>
                        <span>⏱️ 10 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>90%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 90%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <div class="course-card">
                <div class="course-header">
                    <h4>Database Management Systems</h4>
                    <p>Instructor: Dr. James Wilson</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Dec 2024</span>
                        <span>⏱️ 12 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>20%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 20%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <div class="course-card">
                <div class="course-header">
                    <h4>English Language & Literature</h4>
                    <p>Instructor: Prof. Amanda Clarke</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Sep 2024</span>
                        <span>⏱️ 16 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>60%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 60%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <div class="course-card">
                <div class="course-header">
                    <h4>Kannada Language & Culture</h4>
                    <p>Instructor: Dr. Ramesh Kumar</p>
                </div>
                <div class="course-body">
                    <div class="course-meta">
                        <span>📅 Started: Oct 2024</span>
                        <span>⏱️ 14 weeks</span>
                    </div>
                    <div class="course-progress">
                        <div class="progress-label">
                            <span>Progress</span>
                            <span>55%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 55%"></div>
                        </div>
                    </div>
                    <div class="course-actions">
                        <button class="action-btn primary-btn">Continue Learning</button>
                        <button class="action-btn secondary-btn">View Details</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

MATERIALS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Course Materials</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .page-header h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .page-header p {
            color: #666;
            font-size: 16px;
        }
        .boards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }
        .board-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .board-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .board-header {
            padding: 40px 30px;
            color: white;
            text-align: center;
        }
        .board-header.cbse {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .board-header.state {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .board-header.icse {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .board-icon {
            font-size: 64px;
            margin-bottom: 15px;
        }
        .board-header h4 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .board-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .board-body {
            padding: 30px;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .features {
            margin-bottom: 20px;
        }
        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            color: #666;
        }
        .feature-item::before {
            content: "✓";
            color: #28a745;
            font-weight: bold;
            margin-right: 10px;
            font-size: 18px;
        }
        .action-button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 16px;
        }
        .action-button.cbse {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .action-button.state {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .action-button.icse {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📖 Course Materials</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/teacher" class="back-link">← Back to Dashboard</a>
        
        <div class="page-header">
            <h3>Select Education Board</h3>
            <p>Choose the board curriculum to access and manage course materials.</p>
        </div>
        
        <div class="boards-grid">
            <!-- CBSE Board -->
            <div class="board-card" onclick="window.location.href='/standards/cbse'">
                <div class="board-header cbse">
                    <div class="board-icon">🎓</div>
                    <h4>CBSE</h4>
                    <p>Central Board of Secondary Education</p>
                </div>
                <div class="board-body">
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">156</div>
                            <div class="stat-label">Materials</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">24</div>
                            <div class="stat-label">Subjects</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">8</div>
                            <div class="stat-label">Classes</div>
                        </div>
                    </div>
                    <div class="features">
                        <div class="feature-item">NCERT Textbooks & Solutions</div>
                        <div class="feature-item">Sample Papers & Question Banks</div>
                        <div class="feature-item">Video Lectures & Tutorials</div>
                        <div class="feature-item">Assignment Templates</div>
                    </div>
                    <button class="action-button cbse" onclick="event.stopPropagation();">Access CBSE Materials</button>
                </div>
            </div>

            <!-- State Board -->
            <div class="board-card" onclick="window.location.href='/standards/state'">
                <div class="board-header state">
                    <div class="board-icon">🏛️</div>
                    <h4>State Board</h4>
                    <p>Karnataka State Board</p>
                </div>
                <div class="board-body">
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">142</div>
                            <div class="stat-label">Materials</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">22</div>
                            <div class="stat-label">Subjects</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">7</div>
                            <div class="stat-label">Classes</div>
                        </div>
                    </div>
                    <div class="features">
                        <div class="feature-item">State Syllabus Materials</div>
                        <div class="feature-item">Previous Year Question Papers</div>
                        <div class="feature-item">Kannada Medium Resources</div>
                        <div class="feature-item">Local Context Examples</div>
                    </div>
                    <button class="action-button state" onclick="event.stopPropagation();">Access State Board Materials</button>
                </div>
            </div>

            <!-- ICSE Board -->
            <div class="board-card" onclick="window.location.href='/standards/icse'">
                <div class="board-header icse">
                    <div class="board-icon">📚</div>
                    <h4>ICSE</h4>
                    <p>Indian Certificate of Secondary Education</p>
                </div>
                <div class="board-body">
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">168</div>
                            <div class="stat-label">Materials</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">26</div>
                            <div class="stat-label">Subjects</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">9</div>
                            <div class="stat-label">Classes</div>
                        </div>
                    </div>
                    <div class="features">
                        <div class="feature-item">Comprehensive Study Materials</div>
                        <div class="feature-item">Board Exam Preparation</div>
                        <div class="feature-item">Project & Practical Guides</div>
                        <div class="feature-item">English Literature Resources</div>
                    </div>
                    <button class="action-button icse" onclick="event.stopPropagation();">Access ICSE Materials</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

STANDARDS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Select Standard - {{ board.upper() }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .page-header h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .page-header p {
            color: #666;
            font-size: 16px;
        }
        .board-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .board-badge.cbse {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .board-badge.state {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .board-badge.icse {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        .standards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        .standard-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
            cursor: pointer;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .standard-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        .standard-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .standard-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        .standard-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        .standard-subtitle {
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        .subjects-count {
            display: inline-block;
            background: #f0f0f0;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: #666;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📚 Select Standard</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/materials" class="back-link">← Back to Boards</a>
        
        <div class="page-header">
            <span class="board-badge {{ board }}">{{ board.upper() }}</span>
            <h3>Select Standard/Class</h3>
            <p>Choose a standard to access course materials, textbooks, and resources.</p>
        </div>
        
        <div class="standards-grid">
            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/10'">
                <div class="standard-icon">🎯</div>
                <div class="standard-title">10th Standard</div>
                <div class="standard-subtitle">Board Exam Year</div>
                <span class="subjects-count">15 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/9'">
                <div class="standard-icon">📘</div>
                <div class="standard-title">9th Standard</div>
                <div class="standard-subtitle">Secondary Education</div>
                <span class="subjects-count">14 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/8'">
                <div class="standard-icon">📗</div>
                <div class="standard-title">8th Standard</div>
                <div class="standard-subtitle">Middle School</div>
                <span class="subjects-count">13 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/7'">
                <div class="standard-icon">📙</div>
                <div class="standard-title">7th Standard</div>
                <div class="standard-subtitle">Middle School</div>
                <span class="subjects-count">12 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/6'">
                <div class="standard-icon">📕</div>
                <div class="standard-title">6th Standard</div>
                <div class="standard-subtitle">Middle School</div>
                <span class="subjects-count">11 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/5'">
                <div class="standard-icon">📔</div>
                <div class="standard-title">5th Standard</div>
                <div class="standard-subtitle">Primary Education</div>
                <span class="subjects-count">10 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/4'">
                <div class="standard-icon">📓</div>
                <div class="standard-title">4th Standard</div>
                <div class="standard-subtitle">Primary Education</div>
                <span class="subjects-count">9 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/3'">
                <div class="standard-icon">📒</div>
                <div class="standard-title">3rd Standard</div>
                <div class="standard-subtitle">Primary Education</div>
                <span class="subjects-count">8 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/2'">
                <div class="standard-icon">📖</div>
                <div class="standard-title">2nd Standard</div>
                <div class="standard-subtitle">Primary Education</div>
                <span class="subjects-count">7 Subjects</span>
            </div>

            <div class="standard-card" onclick="window.location.href='/subjects/{{ board }}/1'">
                <div class="standard-icon">📚</div>
                <div class="standard-title">1st Standard</div>
                <div class="standard-subtitle">Primary Education</div>
                <span class="subjects-count">6 Subjects</span>
            </div>
        </div>
    </div>
</body>
</html>
'''

SUBJECTS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Subjects - {{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .page-header h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .page-header p {
            color: #666;
            font-size: 16px;
        }
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            font-size: 14px;
        }
        .board-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
        }
        .board-badge.cbse {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .board-badge.state {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .board-badge.icse {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        .standard-badge {
            background: #f0f0f0;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
            color: #666;
        }
        .subjects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }
        .subject-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
            cursor: pointer;
        }
        .subject-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .subject-header {
            padding: 30px;
            color: white;
            text-align: center;
            position: relative;
        }
        .subject-header.english {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .subject-header.kannada {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .subject-header.hindi {
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
        }
        .subject-header.maths {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }
        .subject-header.science {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        }
        .subject-header.social {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }
        .subject-icon {
            font-size: 56px;
            margin-bottom: 15px;
        }
        .subject-header h4 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        .subject-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .subject-body {
            padding: 25px;
        }
        .resources-list {
            list-style: none;
        }
        .resource-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
            color: #666;
            font-size: 14px;
        }
        .resource-item:last-child {
            border-bottom: none;
        }
        .resource-item::before {
            content: "📄";
            margin-right: 10px;
            font-size: 16px;
        }
        .materials-count {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-top: 15px;
        }
        .materials-count strong {
            color: #28a745;
            font-size: 24px;
        }
        .materials-count span {
            display: block;
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📚 Select Subject</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/standards/{{ board }}" class="back-link">← Back to Standards</a>
        
        <div class="page-header">
            <div class="breadcrumb">
                <span class="board-badge {{ board }}">{{ board.upper() }}</span>
                <span>›</span>
                <span class="standard-badge">{{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</span>
            </div>
            <h3>Select Subject</h3>
            <p>Choose a subject to access textbooks, study materials, and teaching resources.</p>
        </div>
        
        <div class="subjects-grid">
            <!-- English -->
            <div class="subject-card" onclick="window.location.href='/language-options/{{ board }}/{{ standard }}/english'">
                <div class="subject-header english">
                    <div class="subject-icon">📖</div>
                    <h4>English</h4>
                    <p>Language & Literature</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Workbooks</li>
                        <li class="resource-item">Grammar Guides</li>
                        <li class="resource-item">Reading Comprehension</li>
                        <li class="resource-item">Writing Exercises</li>
                        <li class="resource-item">Sample Papers</li>
                    </ul>
                    <div class="materials-count">
                        <strong>42</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>

            <!-- Kannada -->
            <div class="subject-card">
                <div class="subject-header kannada">
                    <div class="subject-icon">🇮🇳</div>
                    <h4>Kannada</h4>
                    <p>ಭಾಷೆ ಮತ್ತು ಸಾಹಿತ್ಯ</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Guides</li>
                        <li class="resource-item">Grammar & Composition</li>
                        <li class="resource-item">Literature Study</li>
                        <li class="resource-item">Poetry & Prose</li>
                        <li class="resource-item">Practice Worksheets</li>
                    </ul>
                    <div class="materials-count">
                        <strong>38</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>

            <!-- Hindi -->
            <div class="subject-card">
                <div class="subject-header hindi">
                    <div class="subject-icon">📚</div>
                    <h4>Hindi</h4>
                    <p>भाषा और साहित्य</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Study Material</li>
                        <li class="resource-item">Grammar Lessons</li>
                        <li class="resource-item">Literature Analysis</li>
                        <li class="resource-item">Comprehension Practice</li>
                        <li class="resource-item">Model Question Papers</li>
                    </ul>
                    <div class="materials-count">
                        <strong>35</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>

            <!-- Mathematics -->
            <div class="subject-card">
                <div class="subject-header maths">
                    <div class="subject-icon">🔢</div>
                    <h4>Mathematics</h4>
                    <p>Numbers & Problem Solving</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Solutions</li>
                        <li class="resource-item">Formula Sheets</li>
                        <li class="resource-item">Practice Problems</li>
                        <li class="resource-item">Worksheets & Exercises</li>
                        <li class="resource-item">Previous Year Papers</li>
                    </ul>
                    <div class="materials-count">
                        <strong>56</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>

            <!-- Science -->
            <div class="subject-card">
                <div class="subject-header science">
                    <div class="subject-icon">🔬</div>
                    <h4>Science</h4>
                    <p>Physics, Chemistry & Biology</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Lab Manuals</li>
                        <li class="resource-item">Experiments & Practicals</li>
                        <li class="resource-item">Diagrams & Charts</li>
                        <li class="resource-item">Video Demonstrations</li>
                        <li class="resource-item">Test Papers & MCQs</li>
                    </ul>
                    <div class="materials-count">
                        <strong>64</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>

            <!-- Social Studies -->
            <div class="subject-card">
                <div class="subject-header social">
                    <div class="subject-icon">🌍</div>
                    <h4>Social Studies</h4>
                    <p>History, Geography & Civics</p>
                </div>
                <div class="subject-body">
                    <ul class="resources-list">
                        <li class="resource-item">Textbooks & Notes</li>
                        <li class="resource-item">Maps & Atlases</li>
                        <li class="resource-item">Timeline Charts</li>
                        <li class="resource-item">Case Studies</li>
                        <li class="resource-item">Question Banks</li>
                    </ul>
                    <div class="materials-count">
                        <strong>48</strong>
                        <span>Materials Available</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

LANGUAGE_OPTIONS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>English Language Options - {{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .page-header h3 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .page-header p {
            color: #666;
            font-size: 16px;
        }
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            font-size: 14px;
        }
        .board-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
        }
        .board-badge.state {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .standard-badge {
            background: #f0f0f0;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
            color: #666;
        }
        .language-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }
        .language-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
            cursor: pointer;
        }
        .language-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .language-header {
            padding: 40px 30px;
            color: white;
            text-align: center;
        }
        .language-header.first {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .language-header.second {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .language-header.third {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .language-icon {
            font-size: 64px;
            margin-bottom: 15px;
        }
        .language-header h4 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .language-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .language-body {
            padding: 30px;
        }
        .description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
            font-size: 15px;
        }
        .features-list {
            margin-bottom: 20px;
        }
        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            color: #666;
            font-size: 14px;
        }
        .feature-item::before {
            content: "✓";
            color: #28a745;
            font-weight: bold;
            margin-right: 10px;
            font-size: 18px;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 20px 0;
            border-top: 2px solid #f0f0f0;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📖 English Language Options</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/subjects/{{ board }}/{{ standard }}" class="back-link">← Back to Subjects</a>
        
        <div class="page-header">
            <div class="breadcrumb">
                <span class="board-badge {{ board }}">{{ board.upper() }}</span>
                <span>›</span>
                <span class="standard-badge">{{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</span>
                <span>›</span>
                <span class="standard-badge">English</span>
            </div>
            <h3>Select English Language Level</h3>
            <p>Choose the appropriate English language course based on proficiency level.</p>
        </div>
        
        <div class="language-grid">
            <!-- First Language -->
            <div class="language-card" onclick="window.location.href='/lessons/{{ board }}/{{ standard }}/{{ subject }}/first-language'">
                <div class="language-header first">
                    <div class="language-icon">🥇</div>
                    <h4>English First Language</h4>
                    <p>Advanced Level - Primary Language of Instruction</p>
                </div>
                <div class="language-body">
                    <p class="description">
                        English as First Language is designed for students with high proficiency in English. 
                        This course covers advanced literature, complex grammar, and sophisticated writing skills.
                    </p>
                    <div class="features-list">
                        <div class="feature-item">Advanced Literary Analysis</div>
                        <div class="feature-item">Complex Grammar Structures</div>
                        <div class="feature-item">Creative & Academic Writing</div>
                        <div class="feature-item">Debate & Public Speaking</div>
                        <div class="feature-item">Critical Thinking & Essays</div>
                    </div>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">28</div>
                            <div class="stat-label">Lessons</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">12</div>
                            <div class="stat-label">Chapters</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">156</div>
                            <div class="stat-label">Materials</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Second Language -->
            <div class="language-card">
                <div class="language-header second">
                    <div class="language-icon">🥈</div>
                    <h4>English Second Language</h4>
                    <p>Intermediate Level - Additional Language Study</p>
                </div>
                <div class="language-body">
                    <p class="description">
                        English as Second Language focuses on developing strong communication skills for students 
                        who use another language as their primary medium of instruction.
                    </p>
                    <div class="features-list">
                        <div class="feature-item">Practical Communication Skills</div>
                        <div class="feature-item">Essential Grammar & Vocabulary</div>
                        <div class="feature-item">Reading Comprehension</div>
                        <div class="feature-item">Conversational English</div>
                        <div class="feature-item">Basic Writing Skills</div>
                    </div>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">24</div>
                            <div class="stat-label">Lessons</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">10</div>
                            <div class="stat-label">Chapters</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">128</div>
                            <div class="stat-label">Materials</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Third Language -->
            <div class="language-card">
                <div class="language-header third">
                    <div class="language-icon">🥉</div>
                    <h4>English Third Language</h4>
                    <p>Foundation Level - Basic Language Learning</p>
                </div>
                <div class="language-body">
                    <p class="description">
                        English as Third Language provides foundational English skills for students learning English 
                        as an additional language alongside two other languages.
                    </p>
                    <div class="features-list">
                        <div class="feature-item">Basic Grammar Fundamentals</div>
                        <div class="feature-item">Simple Vocabulary Building</div>
                        <div class="feature-item">Elementary Reading Skills</div>
                        <div class="feature-item">Basic Sentence Formation</div>
                        <div class="feature-item">Simple Conversations</div>
                    </div>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">20</div>
                            <div class="stat-label">Lessons</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">8</div>
                            <div class="stat-label">Chapters</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">96</div>
                            <div class="stat-label">Materials</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

LESSONS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Lessons - {{ language_level.replace('-', ' ').title() }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .page-header h3 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        .page-header p {
            opacity: 0.9;
            font-size: 18px;
        }
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
            font-size: 14px;
        }
        .breadcrumb-item {
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 20px;
        }
        .lessons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .lesson-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
            cursor: pointer;
            border-left: 4px solid #667eea;
        }
        .lesson-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            border-left-width: 6px;
        }
        .lesson-number {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .lesson-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        .lesson-description {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .lesson-meta {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #999;
        }
        .lesson-icon {
            font-size: 32px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📚 Lessons</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/language-options/{{ board }}/{{ standard }}/{{ subject }}" class="back-link">← Back to Language Options</a>
        
        <div class="page-header">
            <div class="breadcrumb">
                <span class="breadcrumb-item">{{ board.upper() }}</span>
                <span>›</span>
                <span class="breadcrumb-item">{{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</span>
                <span>›</span>
                <span class="breadcrumb-item">{{ subject.title() }}</span>
                <span>›</span>
                <span class="breadcrumb-item">{{ language_level.replace('-', ' ').title() }}</span>
            </div>
            <h3>English First Language - Lessons</h3>
            <p>Karnataka State Board Textbook - Part 1 (2025-26)</p>
        </div>
        
        <div class="lessons-grid">
            <div class="lesson-card" onclick="window.location.href='/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/1'">
                <div class="lesson-icon">📖</div>
                <div class="lesson-number">Lessons</div>
                <div class="lesson-title">Lessons</div>
                <div class="lesson-description">By Dr. ABC</div>
                <div class="lesson-meta">
                    <span>📄 Prose</span>
                    <span>⏱️ 45 min</span>
                </div>
            </div>

            <div class="lesson-card" onclick="window.location.href='/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/2'">
                <div class="lesson-icon">💧</div>
                <div class="lesson-number">Previous year Exam Papers</div>
                <div class="lesson-title">Previous year Exam Papers</div>
                <div class="lesson-description">By Pro. ABC.</div>
                <div class="lesson-meta">
                    <span>📄 Prose</span>
                    <span>⏱️ 50 min</span>
                </div>
            </div>

        </div>
    </div>
</body>
</html>
'''

LESSON_CONTENT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Lesson {{ lesson_number }} - LMS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        /* Top Navigation Bar */
        .top-nav {
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .top-nav-left {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .back-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 8px 16px;
            border: 2px solid white;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .back-btn:hover {
            background: white;
            color: #28a745;
        }
        .lesson-title-nav {
            font-size: 18px;
            font-weight: 600;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        /* Main Layout */
        .main-container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        /* Sidebar */
        .sidebar {
            width: 280px;
            background: white;
            border-right: 1px solid #e0e0e0;
            overflow-y: auto;
        }
        .sidebar-header {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        .sidebar-header h3 {
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        }
        .sidebar-header p {
            font-size: 12px;
            color: #666;
        }
        .lesson-list {
            padding: 10px;
        }
        .lesson-item {
            padding: 15px;
            margin: 5px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .lesson-item:hover {
            background: #f0f0f0;
        }
        .lesson-item.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .lesson-item-number {
            font-size: 14px;
            font-weight: bold;
            background: rgba(0,0,0,0.1);
            padding: 5px 10px;
            border-radius: 5px;
        }
        .lesson-item.active .lesson-item-number {
            background: rgba(255,255,255,0.3);
        }
        .lesson-item-title {
            font-size: 13px;
            flex: 1;
        }
        
        /* Content Area */
        .content-area {
            flex: 1;
            overflow-y: auto;
            padding: 30px;
            background: white;
        }
        .lesson-header {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }
        .lesson-number-display {
            font-size: 16px;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .lesson-title-display {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .lesson-author {
            font-size: 18px;
            color: #666;
            font-style: italic;
        }
        .lesson-content {
            max-width: 900px;
            line-height: 1.8;
            color: #333;
        }
        .section-title {
            font-size: 24px;
            color: #667eea;
            margin: 30px 0 15px 0;
            font-weight: 600;
        }
        .pre-reading {
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
            border-radius: 5px;
        }
        .pre-reading h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .story-paragraph {
            margin: 20px 0;
            text-align: justify;
            font-size: 16px;
        }
        .glossary {
            background: #fff9e6;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
        }
        .glossary h3 {
            color: #f39c12;
            margin-bottom: 15px;
        }
        .glossary-item {
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #f0e5c8;
        }
        .glossary-term {
            font-weight: bold;
            color: #333;
        }
        .glossary-definition {
            color: #666;
            margin-left: 20px;
        }
        .comprehension-section {
            background: #f0f8ff;
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
        }
        .comprehension-section h3 {
            color: #007bff;
            margin-bottom: 20px;
        }
        .question {
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .question-number {
            font-weight: bold;
            color: #007bff;
            margin-bottom: 8px;
        }
        .navigation-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        .nav-button {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .nav-button.prev {
            background: #6c757d;
            color: white;
        }
        .nav-button.next {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .nav-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .nav-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <!-- Top Navigation -->
    <div class="top-nav">
        <div class="top-nav-left">
            <a href="/lessons/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}" class="back-btn">← Back to Lessons</a>
            <span class="lesson-title-nav">Lesson {{ lesson_number }}</span>
        </div>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <span style="font-weight: 600;">{{ name }}</span>
        </div>
    </div>

    <!-- Main Container -->
    <div class="main-container">
        <!-- Sidebar with Lesson List -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h3>All Lessons</h3>
                <p>English First Language</p>
            </div>
            <div class="lesson-list">
                {% for i in range(1, 16) %}
                <div class="lesson-item {% if i == lesson_number %}active{% endif %}" 
                     onclick="window.location.href='/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/{{ i }}'">
                    <span class="lesson-item-number">{{ '%02d' % i }}</span>
                    <span class="lesson-item-title">
                        {% if i == 1 %}A Wrong Man in Workers' Paradise
                        {% elif i == 2 %}The Elixir of Life
                        {% elif i == 3 %}The Gift of the Magi
                        {% elif i == 4 %}Louis Pasteur
                        {% elif i == 5 %}What is Moral Action?
                        {% elif i == 6 %}To a Pair of Sarus Cranes
                        {% elif i == 7 %}Abraham Lincoln's Letter
                        {% elif i == 8 %}Vachana
                        {% elif i == 9 %}Lochinvar
                        {% elif i == 10 %}A Poison Tree
                        {% elif i == 11 %}Treasure Island
                        {% elif i == 12 %}Karna
                        {% elif i == 13 %}Grammar Revisited
                        {% elif i == 14 %}Speaking Activities
                        {% else %}Language Activities{% endif %}
                    </span>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Content Area -->
        <div class="content-area">
            {% if lesson_number == 1 %}
            <div class="lesson-header">
                <div class="lesson-number-display">LESSON 01</div>
                <h1 class="lesson-title-display">A Wrong Man in Workers' Paradise</h1>
                <p class="lesson-author">- Rabindranath Tagore</p>
            </div>

            <div class="pre-reading">
                <h4>📚 Pre-Reading Activity</h4>
                <p><em>If you have a garden, you grow not only coconuts, vegetables and fruits, but also roses. Why? Discuss in pairs and answer.</em></p>
            </div>

            <div class="lesson-content">
                <div class="story-paragraph">
                    <strong>1.</strong> The man had never believed in mere utility.
                </div>

                <div class="story-paragraph">
                    <strong>2.</strong> Having had no useful work, he indulged in mad whims. He made little pieces of sculpture - men, women and castles, quaint earthen things dotted over with sea-shells. He painted. Thus, he wasted his time on all that was useless, needless. People laughed at him. At times, he vowed to shake off his whims, but they lingered in his mind.
                </div>

                <div class="story-paragraph">
                    <strong>3.</strong> Some boys seldom ply their books and yet pass their tests. A similar thing happened to this man. He spent his Earth-life in useless work and yet after his death, the gates of Heaven opened wide for him.
                </div>

                <div class="story-paragraph">
                    <strong>4.</strong> But, the Moving Finger writes even in Heaven. So, it came to pass that the aerial messenger who took charge of the man made a mistake and found him a place in Workers' Paradise.
                </div>

                <div class="story-paragraph">
                    <strong>5.</strong> In this Paradise you find everything except leisure.
                </div>

                <div class="story-paragraph">
                    <strong>6.</strong> Here men say: "God! We haven't a moment to spare." Women whisper: "Let's move on, time's a flying." All exclaim: "Time is precious." "We have our hands full, we make use of every single minute," they sigh complainingly, and yet those words make them happy and exalted.
                </div>

                <div class="story-paragraph">
                    <strong>7.</strong> But this newcomer, who had passed all his life on Earth without doing a scrap of useful work, did not fit in with the scheme of things in Workers' Paradise. He lounged in the streets absently and jostled the hurrying men. He lay down in the green meadows, or close to the fast-flowing streams, and was taken to task by busy farmers. He was always in the way of others.
                </div>

                <div class="story-paragraph">
                    <strong>8.</strong> A bustling girl went every day to a silent torrent (silent, since in the Workers' Paradise even a torrent wouldn't waste its energy singing) to fill her pitchers.
                </div>

                <div class="story-paragraph">
                    <strong>9.</strong> The girl's movement on the road was like the rapid movement of a skilled hand on the strings of a guitar. Her hair was carelessly done, inquisitive wisps peeped often over her forehead to peer at the dark wonder of her eye.
                </div>

                <div class="story-paragraph">
                    <strong>10.</strong> The idler was standing by the stream. As a princess sees a lonely beggar and is filled with pity, so the busy girl of Heaven saw this one and was filled with pity.
                </div>

                <div class="story-paragraph">
                    <strong>11.</strong> "A - ha!" she cried with concern. "You have no work in hand, have you?"<br>
                    The man sighed. "Work! I've not a moment to spare for work."
                </div>

                <div class="story-paragraph">
                    <strong>12.</strong> The girl did not understand his words, and said, "I shall spare some work for you to do, if you like."
                </div>

                <div class="story-paragraph">
                    <strong>13.</strong> The man replied: "Girl of the silent torrent, all this time I have been waiting to take some work from your hands."
                </div>

                <div class="story-paragraph">
                    <strong>14.</strong> "What kind of work would you like?"
                </div>

                <div class="story-paragraph">
                    <strong>15.</strong> "Will you give me one of your pitchers, one that you can spare?"
                </div>

                <div class="story-paragraph">
                    <strong>16.</strong> She asked: "A pitcher? You want to draw water from the torrent?"
                </div>

                <div class="story-paragraph">
                    <strong>17.</strong> "No, I shall draw pictures on your pitcher."
                </div>

                <div class="story-paragraph">
                    <strong>18.</strong> The girl was annoyed.
                </div>

                <div class="story-paragraph">
                    <strong>19.</strong> "Pictures, indeed! I have no time to waste on such as you. I'm going." And she walked away.
                </div>

                <div class="story-paragraph">
                    <strong>20.</strong> But how could a busy person get the better of one who had nothing to do? Every day they met and every day he said to her, "Girl of the silent torrent, give me one of your clay pitchers. I shall draw pictures on it!"
                </div>

                <div class="story-paragraph">
                    <strong>21.</strong> She yielded at last. She gave him one of her pitchers.
                </div>

                <div class="story-paragraph">
                    <strong>22.</strong> The man started painting. He drew line after line, he put colour after colour.
                </div>

                <div class="story-paragraph">
                    <strong>23.</strong> When he had completed his work, the girl held up the pitcher and stared at its sides, her eyes puzzled.
                </div>

                <div class="story-paragraph">
                    <strong>24.</strong> Brows drawn, she asked: "What do they mean, all those lines and colours? What is their purpose?"
                </div>

                <div class="story-paragraph">
                    <strong>25.</strong> The man laughed.
                </div>

                <div class="story-paragraph">
                    <strong>26.</strong> "Nothing. A picture may have no meaning and serve no purpose."
                </div>

                <div class="story-paragraph">
                    <strong>27.</strong> The girl went away with her pitcher. At home, away from prying eyes, she held it in the light, turned it round and round and scanned the painting from all angles. At night she moved out of bed, lighted a lamp and scanned it again in silence. For the first time in her life she had seen something that had no meaning and no purpose at all.
                </div>

                <div class="story-paragraph">
                    <strong>28.</strong> When she set out for the torrent the next day, her hurrying feet were a little less hurried than before. For a new sense seemed to have awakened in her, a sense that seemed to have no meaning and no purpose at all.
                </div>

                <div class="story-paragraph">
                    <strong>29.</strong> She saw the painter standing by the torrent and asked in confusion:
                </div>

                <div class="story-paragraph">
                    <strong>30.</strong> "What do you want of me?"
                </div>

                <div class="story-paragraph">
                    <strong>31.</strong> "Only some more work from your hands."
                </div>

                <div class="story-paragraph">
                    <strong>32.</strong> "What kind of work would you like?"
                </div>

                <div class="story-paragraph">
                    <strong>33.</strong> "Let me make a coloured ribbon for your hair," he answered.
                </div>

                <div class="story-paragraph">
                    <strong>34.</strong> "And what for?"
                </div>

                <div class="story-paragraph">
                    <strong>35.</strong> "Nothing."
                </div>

                <div class="story-paragraph">
                    <strong>36.</strong> Ribbons were made, bright with colours. The busy girl of Workers' Paradise had now to spend a lot of time every day tying the coloured ribbon around her hair. The minutes slipped by, unutilized. Much work was left unfinished.
                </div>

                <div class="story-paragraph">
                    <strong>37.</strong> In Workers' Paradise, work had, of late, begun to suffer. Many persons who had been active before were now idle, wasting their precious time on useless things such as painting and sculpture.
                </div>

                <div class="story-paragraph">
                    <strong>38.</strong> The elders became anxious. A meeting was called. All agreed that such a state of affairs had so far been unknown in the history of the Workers' Paradise.
                </div>

                <div class="story-paragraph">
                    <strong>39.</strong> The aerial messenger hurried in, bowed before the elders and made a confession.
                </div>

                <div class="story-paragraph">
                    <strong>40.</strong> "I brought a wrong man into this paradise," he said. "It is all because of him."
                </div>

                <div class="story-paragraph">
                    <strong>41.</strong> The man was summoned. As he came the elders saw his fantastic dress, his quaint brushes, his paints, and they knew at once that he was not the right sort for Workers' Paradise.
                </div>

                <div class="story-paragraph">
                    <strong>42.</strong> Stiffly the president said: "This is no place for the like of you. You must leave."
                </div>

                <div class="story-paragraph">
                    <strong>43.</strong> The man sighed in relief and gathered up his brush and paints. But as he was about to go, the girl of the silent torrent came up tripping and cried,"Wait a moment! I shall come with you."
                </div>

                <div class="story-paragraph">
                    <strong>44.</strong> The elders gasped in surprise. Never before had a thing like this happened in Workers' Paradise - a thing that had no meaning and no purpose at all.
                </div>

                <div class="glossary">
                    <h3>📖 I. GLOSSARY</h3>
                    <div class="glossary-item">
                        <span class="glossary-term">whim:</span>
                        <span class="glossary-definition">sudden desire</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">quaint:</span>
                        <span class="glossary-definition">fanciful/attractive in an unusual way</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">linger:</span>
                        <span class="glossary-definition">continue to exist longer than expected</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">ply:</span>
                        <span class="glossary-definition">(here) read, study</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">Moving Finger:</span>
                        <span class="glossary-definition">fate, destiny</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">aerial messenger:</span>
                        <span class="glossary-definition">God's messenger</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">exalted:</span>
                        <span class="glossary-definition">feel delighted or elated</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">jostle:</span>
                        <span class="glossary-definition">to push roughly against</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">bustling:</span>
                        <span class="glossary-definition">moving in a hurried way</span>
                    </div>
                    <div class="glossary-item">
                        <span class="glossary-term">absently:</span>
                        <span class="glossary-definition">without concentrating on what is happening</span>
                    </div>
                </div>

                <div class="comprehension-section">
                    <h3>💡 II. COMPREHENSION QUESTIONS</h3>
                    <h4 style="margin: 20px 0 15px 0; color: #007bff;">A. Answer briefly the following questions</h4>
                    
                    <div class="question">
                        <div class="question-number">1.</div>
                        <div>"The man indulged in mad whims." Who considers the man's work as "mad whims?"<br>
                        a) The man himself<br>
                        b) the writer<br>
                        c) the people in workers' paradise</div>
                    </div>

                    <div class="question">
                        <div class="question-number">2.</div>
                        <div>Explain the comparison in para 3.<br>
                        a) "Some boys" compared to ...........<br>
                        b) "They are not studying" compared to .........<br>
                        c) "Yet passing in the test" compared to .........</div>
                    </div>

                    <div class="question">
                        <div class="question-number">3.</div>
                        <div>When the men say "We haven't a moment to spare" (para 6) it means that<br>
                        a) they are over-burdened with their work<br>
                        b) they are happy and proud to be so busy<br>
                        c) they are indifferent</div>
                    </div>

                    <div class="question">
                        <div class="question-number">4.</div>
                        <div>Why is the torrent in the workers paradise silent?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">5.</div>
                        <div>"The girl's hair was carelessly done." (para 9) This indicates that<br>
                        a) she was interested only in her work<br>
                        b) she did not like to dress her hair properly<br>
                        c) she was unaware of any sense of dressing</div>
                    </div>

                    <div class="question">
                        <div class="question-number">6.</div>
                        <div>Why did the "girl of the silent torrent" feel sorry for the man?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">7.</div>
                        <div>"The girl scanned the painted pot at home secretly." (Para 27) This line indicates that<br>
                        a) the girl was impressed by art and beauty<br>
                        b) the girl did not want the artist to know that she was impressed by his work<br>
                        c) the girl was afraid of the elders' rebuke for wasting her time</div>
                    </div>

                    <div class="question">
                        <div class="question-number">8.</div>
                        <div>"The hurrying feet" of the girl became "less hurried" because<br>
                        a. she became lazy like the man<br>
                        b. she was attracted by art<br>
                        c. she was trying to re-arrange priorities<br>
                        d. the meaningless was slowly becoming meaningful</div>
                    </div>

                    <div class="question">
                        <div class="question-number">9.</div>
                        <div>Why did the elders of the Workers' Paradise become anxious?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">10.</div>
                        <div>The girl follows the man out of the Workers' Paradise. This suggests that the girl<br>
                        a. was bored with workers' paradise<br>
                        b. was fascinated with the man's skill in painting<br>
                        c. saw new possibilities open-up before her</div>
                    </div>

                    <div class="question">
                        <div class="question-number">11.</div>
                        <div>What does the line "the man never believed in mere utility" mean?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">12.</div>
                        <div>What changes occur in the girl's behaviour/attitude at the following stages in the story:<br>
                        a. Before she agreed to give her pitcher to the wrong man<br>
                        b. After she gave her pitcher to the wrong man<br>
                        c. When the wrong man offered to make ribbons for her<br>
                        d. When she followed the wrong man out of the workers paradise</div>
                    </div>

                    <div class="question">
                        <div class="question-number">13.</div>
                        <div>At the end of the story, there is a complete change in the girl's attitude to life. Who should the credit go to?<br>
                        (is it to the idler-artist's ability to impact others? or is it the girl's readiness and the open-mindedness to change?)</div>
                    </div>

                    <h4 style="margin: 30px 0 15px 0; color: #007bff;">B. Close Study</h4>
                    <p style="margin-bottom: 15px; color: #666;">Read the following extracts carefully. Discuss in pairs and then write the answers to the questions given below them.</p>

                    <div class="question">
                        <div class="question-number">1.</div>
                        <div><strong>"But the Moving Finger writes even in heaven."</strong><br>
                        a) What does "Moving Finger" mean here?<br>
                        b) What figure of speech is used in "Moving Finger"?<br>
                        c) What does the sentence mean in the context?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">2.</div>
                        <div><strong>"As a princess sees a lonely beggar and is filled with pity, so the busy girl of heaven was filled with pity."</strong><br>
                        a) Who is compared to a lonely beggar?<br>
                        b) Why was the girl filled with pity?<br>
                        c) How did the girl offer to help him?</div>
                    </div>

                    <div class="question">
                        <div class="question-number">3.</div>
                        <div><strong>"When she set out for the torrent the next day, her hurrying feet were a little less hurried than before."</strong><br>
                        a) What had happened the previous night?<br>
                        b) What does "hurrying feet" suggest?<br>
                        c) Why did they become less hurried?</div>
                    </div>
                </div>

                <div class="section-title">📝 III. PARAGRAPH WRITING</div>
                <p style="margin: 15px 0; color: #666;">Discuss the answers to the following questions in pairs or groups of four. Individually note down the important points for each question, and then develop the points into one paragraph answers.</p>

                <div class="question">
                    <div class="question-number">1.</div>
                    <div>Men in Workers' Paradise say "God! We haven't a moment to spare" (para 6)<br>
                    The man says, "I haven't a moment to spare for work" (para 11)<br>
                    Keeping in mind the above statements, contrast the attitude of the men in the paradise with that of the man (artist).</div>
                </div>

                <div class="question">
                    <div class="question-number">2.</div>
                    <div>There are two worlds in the story: the world of the idler-artist and the world of the inhabitants of the Workers' Paradise. Which world is better? Why?</div>
                </div>

                <div class="question">
                    <div class="question-number">3.</div>
                    <div>Have a debate in the classroom on the following topic:<br>
                    <strong>Aesthetics V/s Utility</strong><br>
                    You can make use of the following points:<br>
                    a. Art for the sake of art × Art for making money<br>
                    b. Knowledge for the sake of knowledge × Knowledge for the sake of a job<br>
                    c. Man is not satisfied with bread alone.</div>
                </div>

                <div class="section-title">📚 IV. VOCABULARY EXERCISES</div>
                <p style="margin: 15px 0;"><strong>Antonyms</strong></p>
                <p style="margin: 10px 0;">Fill in the blanks with the antonyms of the words underlined:</p>
                
                <div class="question">
                    <div>1. The people <u>utilize</u> every minute of their life. Whereas the man _____________ his time.</div>
                </div>
                <div class="question">
                    <div>2. The <u>busy</u> farmers laughed at the _____________ artist.</div>
                </div>
                <div class="question">
                    <div>3. Some students <u>always</u> work hard but many ___________ do so.</div>
                </div>
                <div class="question">
                    <div>4. Every individual must have <u>confidence</u> in his abilities. However, we notice _______________ in many individuals.</div>
                </div>
                <div class="question">
                    <div>5. The workers thought that the artist was <u>worthless</u> whereas the girl of the silent torrent considered him ______________.</div>
                </div>
            </div>

            <div class="navigation-buttons">
                <button class="nav-button prev" disabled>← Previous Lesson</button>
                <a href="/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/2" class="nav-button next">Next Lesson →</a>
            </div>

            {% else %}
            <div class="lesson-header">
                <div class="lesson-number-display">LESSON {{ '%02d' % lesson_number }}</div>
                <h1 class="lesson-title-display">
                    {% if lesson_number == 2 %}The Elixir of Life
                    {% elif lesson_number == 3 %}The Gift of the Magi
                    {% elif lesson_number == 4 %}Louis Pasteur, Conqueror of Disease
                    {% elif lesson_number == 5 %}What is Moral Action?
                    {% elif lesson_number == 6 %}To a Pair of Sarus Cranes
                    {% elif lesson_number == 7 %}Abraham Lincoln's Letter
                    {% elif lesson_number == 8 %}Vachana
                    {% elif lesson_number == 9 %}Lochinvar
                    {% elif lesson_number == 10 %}A Poison Tree
                    {% elif lesson_number == 11 %}Treasure Island
                    {% elif lesson_number == 12 %}Karna
                    {% elif lesson_number == 13 %}Grammar Revisited
                    {% elif lesson_number == 14 %}Speaking Activities
                    {% else %}Language Activities{% endif %}
                </h1>
                <p class="lesson-author">
                    {% if lesson_number == 2 %}- C.V. Raman
                    {% elif lesson_number == 3 %}- O. Henry
                    {% elif lesson_number == 4 %}- E.H. Carter
                    {% elif lesson_number == 5 %}- M.K. Gandhi
                    {% elif lesson_number == 6 %}- Manmohan Singh
                    {% elif lesson_number == 7 %}- Abraham Lincoln
                    {% elif lesson_number == 8 %}- Basavanna
                    {% elif lesson_number == 9 %}- Walter Scott
                    {% elif lesson_number == 10 %}- William Blake
                    {% elif lesson_number == 11 %}- R.L. Stevenson
                    {% elif lesson_number == 12 %}- C. Rajagopalachari
                    {% else %}{% endif %}
                </p>
            </div>

            <div class="lesson-content">
                <div style="background: #f8f9fa; padding: 40px; border-radius: 10px; text-align: center;">
                    <h2 style="color: #667eea; margin-bottom: 15px;">📚 Lesson Content</h2>
                    <p style="color: #666; font-size: 18px;">The full content for this lesson will be displayed here.</p>
                    <p style="color: #999; margin-top: 10px;">This is a placeholder for Lesson {{ lesson_number }}.</p>
                </div>
            </div>

            <div class="navigation-buttons">
                {% if lesson_number > 1 %}
                <a href="/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/{{ lesson_number - 1 }}" class="nav-button prev">← Previous Lesson</a>
                {% else %}
                <button class="nav-button prev" disabled>← Previous Lesson</button>
                {% endif %}
                
                {% if lesson_number < 15 %}
                <a href="/lesson-content/{{ board }}/{{ standard }}/{{ subject }}/{{ language_level }}/{{ lesson_number + 1 }}" class="nav-button next">Next Lesson →</a>
                {% else %}
                <button class="nav-button next" disabled>Next Lesson →</button>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

SUBJECT_CONTENT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject.title() }} - {{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
        }
        .navbar { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white; 
            padding: 20px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h2 { font-size: 24px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
        }
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            color: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
        }
        .role-badge { 
            background: rgba(255,255,255,0.3);
            padding: 6px 12px; 
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .btn { 
            background: rgba(255,255,255,0.2);
            color: white; 
            padding: 10px 20px; 
            border: 2px solid white;
            border-radius: 8px; 
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }
        .btn:hover { 
            background: white;
            color: #28a745;
        }
        .content { 
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 30px;
        }
        .back-link {
            display: inline-block;
            color: #28a745;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .page-header h3 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        .page-header p {
            opacity: 0.9;
            font-size: 18px;
        }
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
            font-size: 14px;
        }
        .breadcrumb-item {
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 20px;
        }
        .lesson-card {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .lesson-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #f0f0f0;
        }
        .lesson-icon {
            font-size: 64px;
        }
        .lesson-info h4 {
            font-size: 32px;
            color: #333;
            margin-bottom: 8px;
        }
        .lesson-info p {
            color: #666;
            font-size: 16px;
        }
        .lesson-content {
            font-size: 18px;
            line-height: 1.8;
            color: #333;
        }
        .lesson-content h5 {
            font-size: 24px;
            color: #667eea;
            margin: 30px 0 15px 0;
        }
        .lesson-content p {
            margin-bottom: 20px;
        }
        .highlight-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .highlight-box strong {
            color: #667eea;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h2>📖 {{ subject.title() }} Content</h2>
        <div class="user-info">
            <div class="user-avatar">{{ name[0].upper() }}</div>
            <div>
                <div style="font-weight: 600;">{{ name }}</div>
                <span class="role-badge">TEACHER</span>
            </div>
            <a href="/logout" class="btn">Logout</a>
        </div>
    </div>
    
    <div class="content">
        <a href="/subjects/{{ board }}/{{ standard }}" class="back-link">← Back to Subjects</a>
        
        <div class="page-header">
            <div class="breadcrumb">
                <span class="breadcrumb-item">{{ board.upper() }}</span>
                <span>›</span>
                <span class="breadcrumb-item">{{ standard }}{{ 'st' if standard == '1' else 'nd' if standard == '2' else 'rd' if standard == '3' else 'th' }} Standard</span>
                <span>›</span>
                <span class="breadcrumb-item">{{ subject.title() }}</span>
            </div>
            <h3>{{ subject.title() }}</h3>
            <p>Course Material & Lessons</p>
        </div>
        
        <div class="lesson-card">
            <div class="lesson-header">
                <div class="lesson-icon">📚</div>
                <div class="lesson-info">
                    <h4>English First Laal</h4>
                    <p>Introduction to English Language Learning</p>
                </div>
            </div>
            
            <div class="lesson-content">
                <div class="highlight-box">
                    <strong>English First Laal</strong>
                    <p style="margin-top: 10px;">Welcome to the foundational lesson of English language learning!</p>
                </div>
                
                <h5>📖 What is "First Laal"?</h5>
                <p>"Laal" means "lesson" or "chapter" in Kannada. This is your first comprehensive English lesson designed to build a strong foundation in the English language.</p>
                
                <h5>🎯 Learning Objectives</h5>
                <p>In this lesson, students will:</p>
                <ul style="margin-left: 30px; margin-bottom: 20px;">
                    <li style="margin-bottom: 10px;">Understand basic English alphabets and pronunciation</li>
                    <li style="margin-bottom: 10px;">Learn fundamental vocabulary and common words</li>
                    <li style="margin-bottom: 10px;">Practice simple sentence formation</li>
                    <li style="margin-bottom: 10px;">Develop reading and comprehension skills</li>
                </ul>
                
                <h5>📝 Topics Covered</h5>
                <p>This first lesson introduces students to:</p>
                <ul style="margin-left: 30px; margin-bottom: 20px;">
                    <li style="margin-bottom: 10px;"><strong>The English Alphabet:</strong> A to Z with proper pronunciation</li>
                    <li style="margin-bottom: 10px;"><strong>Basic Greetings:</strong> Hello, Good morning, Thank you</li>
                    <li style="margin-bottom: 10px;"><strong>Simple Words:</strong> Common nouns, verbs, and adjectives</li>
                    <li style="margin-bottom: 10px;"><strong>Introduction to Grammar:</strong> Subject and verb basics</li>
                </ul>
                
                <div class="highlight-box">
                    <strong>Teaching Tip:</strong>
                    <p style="margin-top: 10px;">Encourage students to practice pronunciation daily. Use visual aids and interactive activities to make learning engaging and fun!</p>
                </div>
                
                <h5>✍️ Practice Activities</h5>
                <p>Students should complete the following exercises:</p>
                <ul style="margin-left: 30px; margin-bottom: 20px;">
                    <li style="margin-bottom: 10px;">Write the English alphabet 5 times</li>
                    <li style="margin-bottom: 10px;">Learn and use 10 new English words daily</li>
                    <li style="margin-bottom: 10px;">Form 5 simple sentences using learned vocabulary</li>
                    <li style="margin-bottom: 10px;">Practice reading short paragraphs aloud</li>
                </ul>
                
                <h5>📚 Additional Resources</h5>
                <p>Teachers can use these supplementary materials:</p>
                <ul style="margin-left: 30px;">
                    <li style="margin-bottom: 10px;">Flashcards for vocabulary building</li>
                    <li style="margin-bottom: 10px;">Audio recordings for pronunciation practice</li>
                    <li style="margin-bottom: 10px;">Worksheets for writing exercises</li>
                    <li style="margin-bottom: 10px;">Story books with simple English text</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)