#!/usr/bin/env python3

from flask import Flask, render_template_string, redirect, url_for, jsonify, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Sicherer Secret Key für die Session
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Klasse für Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

def validate_awx_credentials(username, password, instance_url):
    try:
        response = requests.get(
            f"{instance_url}/api/v2/me/",
            auth=(username, password),
            verify=False,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        instance = request.form.get('instance', 'AWX1')
        
        if instance in AWX_INSTANCES:
            instance_url = AWX_INSTANCES[instance]['url']
            if validate_awx_credentials(username, password, instance_url):
                user = User(username)
                login_user(user)
                return redirect(url_for('index'))
            
        flash('Ungültige Anmeldedaten', 'error')
    
    return render_template_string(LOGIN_TEMPLATE, instances=AWX_INSTANCES)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Login Template
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AWX Tools Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: red;
            text-align: center;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>AWX Tools Login</h2>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="error">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="form-group">
                <label>AWX Instance:</label>
                <select name="instance">
                    {% for instance_name in instances %}
                    <option value="{{ instance_name }}">{{ instance_name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

# AWX Verbindungsdetails
AWX_INSTANCES = {
    'AWX1': {
        'url': 'https://awxlabor.apps.ocpdev.jungheinrich.com//',
        'username': 'awx_project_user',
        'password': 'E8BpZ-cDvwH-8hBsj-oUB8f'
    },
    'AWX2': {
        'url': 'https://awxtest.apps.ocpdev.jungheinrich.com//',
        'username': 'awx_project_user',
        'password': 'E8BpZ-cDvwH-8hBsj-oUB8f'
    },
    'AWX3': {
        'url': 'https://awx.apps.ocp.jungheinrich.com//',
        'username': 'awx_project_user',
        'password': 'E8BpZ-cDvwH-8hBsj-oUB8f'
    }
}

AWX_HOST = AWX_INSTANCES['AWX1']['url']  # Standard-Instanz
AWX_USERNAME = AWX_INSTANCES['AWX1']['username']
AWX_PASSWORD = AWX_INSTANCES['AWX1']['password']
API_VERSION = 'v2'

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sven's AWX Tools</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .button-container {
            text-align: center;
            margin: 20px 0;
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .button:hover {
            background-color: #45a049;
        }
        .script-section {
            background-color: white;
            padding: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            width: fit-content;  /* Breite an Inhalt anpassen */
            margin-left: auto;   /* Horizontale Zentrierung */
            margin-right: auto;
        }
        .script-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);  /* 2 Buttons pro Zeile */
            gap: 15px;
            margin-top: 20px;
            min-width: 450px;    /* Minimale Breite für 2 Buttons */
        }
        .script-button {
            padding: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            width: 200px;        /* Feste Breite für Buttons */
            margin: 0 auto;      /* Zentrieren in der Grid-Zelle */
        }
        .script-button:hover {
            background-color: #45a049;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background-color: white;
            margin: 15% auto;
            padding: 20px;
            width: 70%;
            max-width: 600px;
            border-radius: 4px;
            position: relative;
        }
        .close {
            position: absolute;
            right: 10px;
            top: 5px;
            font-size: 24px;
            cursor: pointer;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .error {
            color: red;
            margin-top: 5px;
        }
        .success {
            color: green;
            margin-top: 5px;
        }
        .host-list table {
            border-collapse: collapse;
            width: 100%;
        }
        
        .host-list th, .host-list td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .host-list th {
            background-color: #4CAF50;
            color: white;
        }
        
        .host-list tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        .host-list tr:hover {
            background-color: #ddd;
        }
        
        .variables-cell {
            font-family: monospace;
            white-space: pre-wrap;
            max-width: 300px;
            overflow-x: auto;
        }
        
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
            gap: 20px;
            flex-direction: column;
        }
        
        .logo {
            width: 50px;
            height: 50px;
        }
        
        .logo svg {
            width: 100%;
            height: 100%;
        }
        
        .logo path {
            fill: #4CAF50;
        }
        
        h1 {
            margin: 0;
        }

        .awx-url {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }

        .instance-selector {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 5px;
        }
        
        .instance-selector select {
            padding: 4px 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }

        .content-wrapper {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }

        .jobs-panel {
            flex: 0 0 800px;  /* Breite auf 800px erhöht */
            background: white;
            padding: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            max-height: 800px;
            overflow-y: auto;
        }

        .main-content {
            flex: 1;
            min-width: 0;
        }

        .job-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .job-item {
            padding: 15px;  /* Padding erhöht */
            border-bottom: 1px solid #eee;
            font-size: 16px;  /* Schriftgröße erhöht */
        }

        .job-item:last-child {
            border-bottom: none;
        }

        .job-name {
            font-weight: bold;
            margin-bottom: 8px;  /* Abstand erhöht */
            font-size: 18px;  /* Schriftgröße für den Namen erhöht */
        }

        .job-instance {
            font-size: 14px;  /* Schriftgröße erhöht */
            color: #666;
            margin-bottom: 5px;
        }

        .job-time {
            font-size: 14px;  /* Schriftgröße erhöht */
            color: #666;
        }

        .job-status {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
            margin-left: 5px;
        }

        .status-success {
            background-color: #dff0d8;
            color: #3c763d;
        }

        .status-error {
            background-color: #f2dede;
            color: #a94442;
        }

        .status-running {
            background-color: #d9edf7;
            color: #31708f;
        }

        .status-pending {
            background-color: #fcf8e3;
            color: #8a6d3b;
        }

        .status-unknown {
            background-color: #f5f5f5;
            color: #777;
        }

        .refresh-info {
            font-size: 12px;
            color: #666;
            text-align: right;
            margin-top: 5px;
        }

        .user-info {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .logout-button {
            padding: 8px 15px;
            background-color: #666;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
        }
        
        .logout-button:hover {
            background-color: #555;
        }
        
        .username {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="user-info">
        <span class="username">{{ current_user.id }}</span>
        <a href="{{ url_for('logout') }}" class="logout-button">Logout</a>
    </div>
    
    <div class="container">
        <div class="header">
            <div class="logo">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                    <path fill="#4CAF50" d="M50 6.9c23.7 0 43.1 19.3 43.1 43.1 0 23.7-19.3 43.1-43.1 43.1-23.7 0-43.1-19.3-43.1-43.1 0-23.7 19.3-43.1 43.1-43.1zm0 7.2c-19.8 0-35.8 16-35.8 35.8s16 35.8 35.8 35.8 35.8-16 35.8-35.8-16-35.8-35.8-35.8zm-.2 13.4l24.1 41.8h-48.3l24.2-41.8zm0 12l-12.1 21h24.2l-12.1-21z"/>
                </svg>
            </div>
            <div>
                <h1>Sven's AWX Tools</h1>
                <div class="instance-selector">
                    <select id="awxInstance" onchange="changeInstance(this.value)">
                        {% for instance_name, instance_data in instances.items() %}
                        <option value="{{ instance_name }}" {% if instance_data.url == current_instance %}selected{% endif %}>
                            {{ instance_name }}
                        </option>
                        {% endfor %}
                    </select>
                    <div class="awx-url">{{ current_instance }}</div>
                </div>
            </div>
        </div>

        <div class="content-wrapper">
            <div class="jobs-panel">
                <h3 style="margin-top: 0;">Aktuelle Jobs</h3>
                <div id="jobsList">
                    <ul class="job-list">
                        {% for job in jobs %}
                        <li class="job-item">
                            <div class="job-name">
                                {{ job.name }} ({{ job.type }})
                                <span class="job-status status-{{ job.status_class }}">{{ job.status }}</span>
                            </div>
                            <div class="job-instance">{{ job.instance }}</div>
                            <div class="job-time">
                                Start: {{ job.started }}<br>
                                {% if job.finished != 'Läuft noch' %}
                                Ende: {{ job.finished }}
                                {% endif %}
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>

                <div class="refresh-info">Aktualisierung alle 10 Sekunden</div>
            </div>

            <div class="main-content">
                <div class="script-section">
                    <h2>Create Scripts</h2>
                    <div class="script-grid">
                        <button onclick="openModal('template')" class="script-button">Create Template</button>
                        <button onclick="openModal('project')" class="script-button">Create Project</button>
                        <button onclick="openModal('inventory')" class="script-button">Create Inventory</button>
                        <button onclick="openModal('host')" class="script-button">Add Host to Inventory</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Template Modal -->
    <div id="templateModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('template')">&times;</span>
            <h2>Create Template</h2>
            <form id="templateForm" onsubmit="submitForm('template', event)">
                <div class="form-group">
                    <label>Template Type:</label>
                    <select name="template_type" required onchange="toggleJobTemplateFields(this.value)">
                        <option value="job">Job Template</option>
                        <option value="workflow">Workflow Template</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <input type="text" name="description">
                </div>
                <div id="jobTemplateFields">
                    <div class="form-group">
                        <label>Project:</label>
                        <select name="project" required onchange="loadPlaybooks(this.value)">
                            <option value="">Projekt auswählen...</option>
                            {% for project in projects %}
                            <option value="{{ project.id }}">{{ project.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Playbook:</label>
                        <select name="playbook" required>
                            <option value="">Erst Projekt auswählen...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Inventory:</label>
                        <select name="inventory" required>
                            <option value="">Inventory auswählen...</option>
                            {% for inv in inventories %}
                            <option value="{{ inv.id }}">{{ inv.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Credential:</label>
                        <select name="credential" required>
                            <option value="">Credential auswählen...</option>
                            {% for cred in credentials %}
                            <option value="{{ cred.id }}">{{ cred.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                <button type="submit" class="button">Create</button>
                <div id="templateResult"></div>
            </form>
        </div>
    </div>

    <!-- Project Modal -->
    <div id="projectModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('project')">&times;</span>
            <h2>Create Project</h2>
            <form id="projectForm" onsubmit="submitForm('project', event)">
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" name="name" required placeholder="Projektname">
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <input type="text" name="description" placeholder="Optionale Beschreibung">
                </div>
                <div class="form-group">
                    <label>SCM Type:</label>
                    <select name="scm_type" required onchange="toggleScmFields(this.value)">
                        <option value="manual">Manual</option>
                        <option value="git">Git</option>
                    </select>
                </div>
                <div id="scmFields" style="display: none;">
                    <div class="form-group">
                        <label>SCM URL:</label>
                        <input type="text" name="scm_url" placeholder="https://github.com/user/repo.git">
                    </div>
                    <div class="form-group">
                        <label>SCM Branch:</label>
                        <input type="text" name="scm_branch" placeholder="main">
                    </div>
                    <div class="form-group">
                        <label>Credential:</label>
                        <select name="credential">
                            <option value="">Keine Credentials</option>
                            {% for cred in credentials %}
                            <option value="{{ cred.id }}">{{ cred.name }}</option>
                            {% endfor %}
                        </select>
                        <small style="display: block; color: #666;">Credentials für den Git-Zugriff (optional)</small>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" name="scm_clean">
                            Clean
                        </label>
                        <small style="display: block; color: #666;">Löscht nicht versionierte Dateien aus dem Projektverzeichnis</small>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" name="scm_delete_on_update">
                            Delete on Update
                        </label>
                        <small style="display: block; color: #666;">Löscht das Projektverzeichnis vor jedem Update</small>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" name="scm_update_on_launch">
                            Update on Launch
                        </label>
                        <small style="display: block; color: #666;">Aktualisiert das Projekt vor jedem Job-Start</small>
                    </div>
                </div>
                <button type="submit" class="button">Create Project</button>
                <div id="projectResult"></div>
            </form>
        </div>
    </div>

    <!-- Inventory Modal -->
    <div id="inventoryModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('inventory')">&times;</span>
            <h2>Create Inventory</h2>
            <form id="inventoryForm" onsubmit="submitForm('inventory', event)">
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <input type="text" name="description">
                </div>
                <button type="submit" class="button">Create</button>
                <div id="inventoryResult"></div>
            </form>
        </div>
    </div>

    <!-- Host Modal -->
    <div id="hostModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('host')">&times;</span>
            <h2>Add Host to Inventory</h2>
            
            <div class="form-group">
                <label>Inventory:</label>
                <select name="inventory_id" id="inventorySelect" required onchange="loadInventoryHosts(this.value)">
                    <option value="">Inventory auswählen...</option>
                    {% for inv in inventories %}
                    <option value="{{ inv.id }}">{{ inv.name }}</option>
                    {% endfor %}
                </select>
            </div>

            <!-- Vorhandene Hosts -->
            <div id="existingHosts" style="display: none;">
                <h3>Vorhandene Hosts</h3>
                <div class="host-list" style="max-height: 200px; overflow-y: auto;">
                    <table style="width: 100%;">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Beschreibung</th>
                                <th>Variablen</th>
                            </tr>
                        </thead>
                        <tbody id="hostList">
                        </tbody>
                    </table>
                </div>
                <div style="margin-top: 20px; text-align: center;">
                    <button type="button" onclick="showHostForm()" class="button">Add Host</button>
                </div>
            </div>

            <!-- Host Formular -->
            <form id="hostForm" onsubmit="submitForm('host', event)" style="display: none;">
                <hr style="margin: 20px 0;">
                <h3>Neuen Host hinzufügen</h3>
                <div class="form-group">
                    <label>Hostname:</label>
                    <input type="text" name="name" required placeholder="z.B. webserver01">
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <input type="text" name="description" placeholder="Optionale Beschreibung">
                </div>
                <div class="form-group">
                    <label>IP Address / FQDN:</label>
                    <input type="text" name="host" required placeholder="z.B. 192.168.1.100 oder server.domain.com">
                </div>
                <div class="form-group">
                    <label>Variables (YAML Format):</label>
                    <textarea name="variables" rows="4" placeholder="ansible_host: 192.168.1.100&#10;ansible_user: admin&#10;ansible_connection: ssh"></textarea>
                </div>
                <div style="margin-top: 20px;">
                    <button type="submit" class="button">Add Host</button>
                    <button type="button" onclick="cancelHostForm()" class="button" style="background-color: #999;">Abbrechen</button>
                </div>
                <div id="hostResult"></div>
            </form>
        </div>
    </div>

    <script>
        // Neue Funktion für die Aktualisierung der Jobs
        function updateJobs() {
            console.log("🔄 Starte Job-Update...");

            fetch('/get_jobs')
                .then(response => response.json())
                .then(jobs => {
                    const jobsList = document.getElementById('jobsList');
                    let html = '<ul class="job-list">';
                    jobs.forEach(job => {
                        const jobType = job.type ? job.type : "Job";
                        html += `
                            <li class="job-item">
                                <div class="job-name">
                                    ${job.name} (${jobType})
                                    <span class="job-status status-${job.status_class}">${job.status}</span>
                                </div>
                                <div class="job-instance">${job.instance}</div>
                                <div class="job-time">
                                    Start: ${job.started}<br>
                                    ${job.finished !== 'Läuft noch' ? 'Ende: ' + job.finished : ''}
                                </div>
                            </li>
                        `;
                    });
                    html += '</ul>';
                    jobsList.innerHTML = html;
                    console.log("✅ Jobs erfolgreich in die UI geschrieben.");
                })
                .catch(error => console.error("❌ Fehler beim Abrufen der Jobs:", error));
        }


        // Aktualisiere die Jobs alle 10 Sekunden
        setInterval(updateJobs, 10000);

        function openModal(type) {
            document.getElementById(type + 'Modal').style.display = 'block';
            if (type === 'host') {
                const inventorySelect = document.querySelector('select[name="inventory_id"]');
                if (inventorySelect.value) {
                    loadInventoryHosts(inventorySelect.value);
                }
            }
        }

        function closeModal(type) {
            const modal = document.getElementById(type + 'Modal');
            modal.style.display = 'none';
            
            if (type === 'project') {
                const form = document.getElementById('projectForm');
                form.reset();
                document.getElementById('scmFields').style.display = 'none';
            }
            document.getElementById(type + 'Result').innerHTML = '';
        }

        function submitForm(type, event) {
            event.preventDefault();
            const form = document.getElementById(type + 'Form');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/create/' + type, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById(type + 'Result');
                if (data.success) {
                    resultDiv.innerHTML = '<div class="success">' + data.message + '</div>';
                    setTimeout(() => {
                        closeModal(type);
                        window.location.reload();
                    }, 2000);
                } else {
                    resultDiv.innerHTML = '<div class="error">' + data.message + '</div>';
                }
            })
            .catch(error => {
                document.getElementById(type + 'Result').innerHTML = 
                    '<div class="error">Ein Fehler ist aufgetreten: ' + error + '</div>';
            });
        }

        function toggleJobTemplateFields(type) {
            const jobFields = document.getElementById('jobTemplateFields');
            if (type === 'job') {
                jobFields.style.display = 'block';
                jobFields.querySelectorAll('select').forEach(select => select.required = true);
            } else {
                jobFields.style.display = 'none';
                jobFields.querySelectorAll('select').forEach(select => select.required = false);
            }
        }

        function loadPlaybooks(projectId) {
            if (!projectId) return;
            
            fetch('/get_playbooks/' + projectId)
                .then(response => response.json())
                .then(playbooks => {
                    const playbookSelect = document.querySelector('select[name="playbook"]');
                    playbookSelect.innerHTML = '<option value="">Playbook auswählen...</option>';
                    playbooks.forEach(playbook => {
                        const option = document.createElement('option');
                        option.value = playbook;
                        option.textContent = playbook;
                        playbookSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error loading playbooks:', error));
        }

        function loadInventoryHosts(inventoryId) {
            const existingHosts = document.getElementById('existingHosts');
            const hostForm = document.getElementById('hostForm');

            if (!inventoryId) {
                existingHosts.style.display = 'none';
                hostForm.style.display = 'none';
                return;
            }

            fetch('/get_inventory_hosts/' + inventoryId)
                .then(response => response.json())
                .then(hosts => {
                    const hostList = document.getElementById('hostList');
                    hostList.innerHTML = '';
                    
                    hosts.forEach(host => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${host.name}</td>
                            <td>${host.description || ''}</td>
                            <td class="variables-cell">${host.variables || ''}</td>
                        `;
                        hostList.appendChild(row);
                    });
                    
                    existingHosts.style.display = 'block';
                    hostForm.style.display = 'none';
                })
                .catch(error => console.error('Error loading hosts:', error));
        }

        function showHostForm() {
            document.getElementById('existingHosts').style.display = 'none';
            document.getElementById('hostForm').style.display = 'block';
        }

        function cancelHostForm() {
            document.getElementById('hostForm').style.display = 'none';
            document.getElementById('existingHosts').style.display = 'block';
            document.getElementById('hostForm').reset();
        }

        function toggleScmFields(scmType) {
            const scmFields = document.getElementById('scmFields');
            const scmInputs = scmFields.querySelectorAll('input[type="text"]');
            const credentialSelect = scmFields.querySelector('select[name="credential"]');
            
            if (scmType === 'git') {
                scmFields.style.display = 'block';
                scmInputs[0].required = true; // SCM URL wird pflichtfeld
            } else {
                scmFields.style.display = 'none';
                scmInputs[0].required = false;
                // Reset SCM fields
                scmInputs.forEach(input => input.value = '');
                credentialSelect.value = '';
                scmFields.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
            }
        }

        function changeInstance(instanceName) {
            // Speichere die ausgewählte Instanz in einem Cookie
            document.cookie = "selected_instance=" + instanceName + ";path=/";
            // Lade die Seite neu
            window.location.reload();
        }

        // Initialize template type fields on page load
        document.addEventListener('DOMContentLoaded', function() {
            toggleJobTemplateFields('job');
        });
    </script>
</body>
</html>
'''

def get_all_templates():
    templates = []
    
    # Hole Job Templates
    job_templates_url = f"{AWX_HOST}/api/{API_VERSION}/job_templates/"
    workflow_templates_url = f"{AWX_HOST}/api/{API_VERSION}/workflow_job_templates/"
    
    try:
        # Job Templates abrufen
        response = requests.get(
            job_templates_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        job_templates = response.json()
        
        # Workflow Templates abrufen
        response = requests.get(
            workflow_templates_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        workflow_templates = response.json()
        
        # Templates zur Liste hinzufügen
        for template in job_templates['results']:
            templates.append({
                'name': template['name'],
                'type': 'Job Template',
                'created': template['created']
            })
            
        for template in workflow_templates['results']:
            templates.append({
                'name': template['name'],
                'type': 'Workflow Template',
                'created': template['created']
            })
            
        # Nach Erstellungsdatum sortieren (neueste zuerst)
        return sorted(templates, key=lambda x: x['created'], reverse=True)
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Templates: {str(e)}")
        return []

def format_datetime(dt_string):
    # Entferne das 'Z' (UTC-Indikator), falls vorhanden
    dt_string = dt_string.replace('Z', '')
    
    # Wandle den String ins passende Datumsformat um
    dt = datetime.strptime(dt_string.split(".")[0], "%Y-%m-%dT%H:%M:%S")
    
    # Gib das Datum in einem besseren Format aus
    return dt.strftime('%d.%m.%Y %H:%M:%S')

def get_projects():
    try:
        response = requests.get(
            f"{AWX_HOST}/api/{API_VERSION}/projects/",
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        return response.json()['results']
    except:
        return []

def get_inventories():
    try:
        response = requests.get(
            f"{AWX_HOST}/api/{API_VERSION}/inventories/",
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        return response.json()['results']
    except:
        return []

def get_credentials():
    try:
        response = requests.get(
            f"{AWX_HOST}/api/{API_VERSION}/credentials/",
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        return response.json()['results']
    except:
        return []

def get_project_playbooks(project_id):
    try:
        response = requests.get(
            f"{AWX_HOST}/api/{API_VERSION}/projects/{project_id}/playbooks/",
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except:
        return []

@app.route('/get_playbooks/<int:project_id>')
def get_playbooks(project_id):
    playbooks = get_project_playbooks(project_id)
    return jsonify(playbooks)



def get_jobs_from_instance(instance_url, username, password):
    try:
        ########################################################################
        ### pruefen ob die jobs aus der instanz kommen - Done ##################
    #     print(f"Abfrage von {instance_url}/api/{API_VERSION}/jobs/")
        
    #     response = requests.get(
    #         f"{instance_url}/api/{API_VERSION}/jobs/",
    #         params={'order_by': '-started', 'page_size': 100},
    #         auth=(username, password),
    #         verify=False
    #     )
    #     print(f"Response Code: {response.status_code}")
        
    #     if response.status_code != 200:
    #         print(f"Fehler: {response.status_code}, Antwort: {response.text}")
    #         return []
        
    #     jobs = response.json().get('results', [])
    #     print(f"Gefundene Jobs in Funktion: {len(jobs)}")
        
    #     for job in jobs:
    #         print(f"Job Name: {job.get('name')}, Type: {job.get('job_type')}, Status: {job.get('status')}")

    #     return jobs  # Gib alle Jobs zurück
    # except Exception as e:
    #     print(f"Fehler in get_jobs_from_instance: {str(e)}")
    #     return []
        ########################################################################
        all_jobs = []
        
        # Liste der Job-Endpunkte
        job_endpoints = [
            'jobs',                    # Standard Jobs
            'project_updates',         # Projekt Updates
            'inventory_updates',       # Inventory Updates
            'workflow_jobs',           # Workflow Jobs
            'system_jobs'          # System Jobs
            

        ]


        # Hole Jobs von allen Endpunkten
        for endpoint in job_endpoints:
            try:
                # Erweitere die API-Abfrage um alle Status-Typen einzuschließen
                response = requests.get(
                    f"{instance_url}/api/{API_VERSION}/{endpoint}/",
                    params={
                        'order_by': '-started',  # Nach Startzeit sortieren
                        'page_size': 100,        # Mehr Ergebnisse pro Seite
                    },
                    auth=(username, password),
                    verify=False,
                    timeout=5  # Timeout erhöht
                )
                response.raise_for_status()
                jobs = response.json()['results']

                ##################################################################################################################
                # print(f"API-Call: {instance_url}/api/{API_VERSION}/{endpoint}/ -> Status: {response.status_code}")  # Debug-Print

                # for job in jobs[:10]:  # Zeigt die ersten 10 Jobs an
                #     print(f"Job gefunden: {job.get('name')} | Type: {job.get('job_type')} | Status: {job.get('status')}")

                # all_jobs = get_jobs_from_instance(AWX_HOST, AWX_USERNAME, AWX_PASSWORD)
                # print(f"Alle Jobs nach dem Abrufen: {len(all_jobs)} gefunden")
                # for job in all_jobs:
                #     print(f"Job UI: {job['name']} | Type: {job['type']} | Status: {job['status']}")
                ####################################################################################################################

                for job in jobs:
                    status = job.get('status', 'unknown')
                    status_class = {
                        'successful': 'success',
                        'failed': 'error',
                        'running': 'running',
                        'pending': 'pending',
                        'canceled': 'error',
                        'error': 'error',
                        'waiting': 'pending'
                    }.get(status, 'unknown')
                    
                    # Bestimme den Job-Typ
                    job_type = {
                        'jobs': 'job',
                        'project_updates': 'Project Update',
                        'inventory_updates': 'Inventory Update',
                        'workflow_jobs': 'Workflow Job',
                        'system_jobs': 'System Job'
                    }.get(endpoint, 'Unknown')
                    
                    started_date = job.get('started', '')
                    
                    # Nur Jobs mit Startdatum hinzufügen
                    if started_date:
                        # Füge zusätzliche Job-Details hinzu
                        job_name = job.get('name', '')
                        if not job_name and endpoint == 'project_updates':
                            job_name = f"Project Update: {job.get('project_display', 'Unknown Project')}"
                        elif not job_name and endpoint == 'inventory_updates':
                            job_name = f"Inventory Update: {job.get('inventory_source_display', 'Unknown Source')}"
                        elif not job_name and endpoint == 'system_jobs':
                            job_name = f"System Job: {job.get('job_type', 'Unknown Type')}"
                        
                        all_jobs.append({
                            'name': job_name or 'Unbekannt',
                            'type': job_type,
                            'instance': instance_url,
                            'status': status,
                            'status_class': status_class,
                            'started': format_datetime(started_date),
                            'finished': format_datetime(job.get('finished', '')) if job.get('finished') else 'Läuft noch',
                            'sort_date': started_date
                        })
                    
            except requests.exceptions.RequestException as e:
                print(f"Fehler beim Abrufen von {endpoint}: {str(e)}")
                continue
                
        return all_jobs
    except Exception as e:
        print(f"Allgemeiner Fehler: {str(e)}")
        return []

@app.route('/get_jobs')
@login_required
def get_jobs():
    # Hole Jobs von allen Instanzen
    all_jobs = []
    #######################################################################################################
    #### test 1 #####
    # for instance_name, instance_data in AWX_INSTANCES.items():
    #     print(f"Jobs von {instance_name} ({instance_data['url']}) abrufen...")
    #     jobs = get_jobs_from_instance(
    #         instance_data['url'],
    #         instance_data['username'],
    #         instance_data['password']
    #     )
    #     print(f"{len(jobs)} Jobs von {instance_name} erhalten.")
        
    #     if not jobs:
    #         print(f"⚠️ WARNUNG: Keine Jobs von {instance_name} erhalten!")

    #     all_jobs.extend(jobs)

    # print(f"🔍 Alle Jobs vor Sortierung: {len(all_jobs)}")
    
    # # Falls all_jobs leer ist, sind die Jobs hier verloren gegangen.
    # if not all_jobs:
    #     print("❌ FEHLER: Nach dem Sammeln gibt es KEINE JOBS!")

    # all_jobs.sort(key=lambda x: x.get('sort_date', ''), reverse=True)
    # print(f"📊 Alle Jobs nach Sortierung: {len(all_jobs)}")

    # all_jobs = all_jobs[:50]  # Begrenzung auf 50 Jobs
    # print(f"📢 Jobs, die ans UI gesendet werden: {len(all_jobs)}")
    
    # return jsonify(all_jobs)
    #######################################################################################################
    ### test 2 ######
    # for instance_name, instance_data in AWX_INSTANCES.items():
    #     print(f"Jobs von {instance_name} ({instance_data['url']}) abrufen...")
    #     jobs = get_jobs_from_instance(
    #         instance_data['url'],
    #         instance_data['username'],
    #         instance_data['password']
    #     )
    #     print(f"{len(jobs)} Jobs von {instance_name} erhalten.")

    #     for job in jobs:
    #         print(f"🔎 Job: {job['name']}, Type: {job.get('type', 'UNKNOWN')}, Status: {job['status']}")

    #     all_jobs.extend(jobs)

    # print(f"🔍 Alle Jobs vor Sortierung: {len(all_jobs)}")

    # # Falls die Liste leer ist, wird sie hier entfernt.
    # if not all_jobs:
    #     print("❌ FEHLER: Nach dem Sammeln gibt es KEINE JOBS!")
    #     return jsonify([])

    # all_jobs.sort(key=lambda x: x.get('sort_date', ''), reverse=True)
    # print(f"📊 Alle Jobs nach Sortierung: {len(all_jobs)}")

    # # LIMIT ERHÖHEN ODER DEAKTIVIEREN
    # # all_jobs = all_jobs[:50]  # Falls Playbook Runs fehlen, vielleicht höher setzen?
    # print(f"📢 Jobs, die ans UI gesendet werden: {len(all_jobs)}")

    # return jsonify(all_jobs)
    #######################################################################################################
    #### test 3 ####
    for instance_name, instance_data in AWX_INSTANCES.items():
        print(f"Jobs von {instance_name} ({instance_data['url']}) abrufen...")
        jobs = get_jobs_from_instance(
            instance_data['url'],
            instance_data['username'],
            instance_data['password']
        )
        print(f"{len(jobs)} Jobs von {instance_name} erhalten.")

        all_jobs.extend(jobs)

    print(f"🔍 Alle Jobs vor Sortierung: {len(all_jobs)}")
    all_jobs.sort(key=lambda x: x.get('sort_date', ''), reverse=True)
    print(f"📊 Alle Jobs nach Sortierung: {len(all_jobs)}")

    # Prüfen, ob Playbook Runs wirklich dabei sind
    playbook_run_count = 0
    for job in all_jobs:
        job_type = job.get("type", "UNKNOWN")
        if job_type == "job":
            print(f"✅ Playbook Run: {job['name']} - Status: {job['status']}")
            playbook_run_count += 1

    print(f"🎭 Anzahl der Playbook Runs: {playbook_run_count}")

    return jsonify(all_jobs)
    #######################################################################################################
    for instance_name, instance_data in AWX_INSTANCES.items():
        jobs = get_jobs_from_instance(
            instance_data['url'],
            instance_data['username'],
            instance_data['password']
        )
        all_jobs.extend(jobs)
    
    # Sortiere alle Jobs nach dem Startdatum (neueste zuerst)
    all_jobs.sort(key=lambda x: x.get('sort_date', ''), reverse=True)
    
    # Zeige mehr Jobs an
    all_jobs = all_jobs[:50]  # Zeige die 50 neuesten Jobs
    
    ########################################################################################
    print("Jobs, die ans UI geschickt werden:")
    for job in all_jobs:
        print(f"UI: {job['name']} | Type: {job['type']} | Status: {job['status']}")


    ########################################################################################

    return jsonify(all_jobs)

@app.route('/')
@login_required
def index():
    # Deaktiviere Warnungen für unsichere HTTPS-Requests
    requests.packages.urllib3.disable_warnings()
    
    # Hole die ausgewählte Instanz aus dem Cookie
    selected_instance = request.cookies.get('selected_instance', 'AWX1')
    
    # Setze die globalen Variablen für die ausgewählte Instanz
    global AWX_HOST, AWX_USERNAME, AWX_PASSWORD
    AWX_HOST = AWX_INSTANCES[selected_instance]['url']
    AWX_USERNAME = AWX_INSTANCES[selected_instance]['username']
    AWX_PASSWORD = AWX_INSTANCES[selected_instance]['password']
    
    # Hole Jobs von allen Instanzen
    all_jobs = []
    for instance_name, instance_data in AWX_INSTANCES.items():
        jobs = get_jobs_from_instance(
            instance_data['url'],
            instance_data['username'],
            instance_data['password']
        )
        
        all_jobs.extend(jobs)
    
    # Sortiere alle Jobs nach dem Startdatum (neueste zuerst)
    all_jobs.sort(key=lambda x: x.get('sort_date', ''), reverse=True)
    
    # Beschränke auf die neuesten Jobs
    #all_jobs = all_jobs[:200]  # Zeige die 50 neuesten Jobs
    
    # Hole zusätzliche Daten für das Template-Formular
    projects = get_projects()
    inventories = get_inventories()
    credentials = get_credentials()
    
    return render_template_string(HTML_TEMPLATE, 
        projects=projects,
        inventories=inventories,
        credentials=credentials,
        instances=AWX_INSTANCES,
        current_instance=AWX_HOST,
        jobs=all_jobs
    )

@app.route('/create/template', methods=['POST'])
@login_required
def create_template():
    data = request.get_json()
    
    try:
        if data['template_type'] == 'job':
            url = f"{AWX_HOST}/api/{API_VERSION}/job_templates/"
            # Job Template mit allen erforderlichen Feldern
            template_data = {
                'name': data['name'],
                'description': data.get('description', ''),
                'job_type': 'run',
                'inventory': int(data['inventory']),
                'project': int(data['project']),
                'playbook': data['playbook'],
                'credential': int(data['credential']),
                'ask_variables_on_launch': True
            }
        else:
            url = f"{AWX_HOST}/api/{API_VERSION}/workflow_job_templates/"
            template_data = {
                'name': data['name'],
                'description': data.get('description', ''),
            }
            
        response = requests.post(
            url,
            json=template_data,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        return jsonify({
            'success': True,
            'message': f"Template '{data['name']}' wurde erfolgreich erstellt!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Fehler beim Erstellen des Templates: {str(e)}"
        })

@app.route('/create/project', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    
    try:
        project_data = {
            'name': data['name'],
            'description': data.get('description', ''),
            'scm_type': data['scm_type'],
            'scm_url': data.get('scm_url', ''),
            'scm_branch': data.get('scm_branch', ''),
            'scm_clean': data.get('scm_clean', False),
            'scm_delete_on_update': data.get('scm_delete_on_update', False),
            'scm_update_on_launch': data.get('scm_update_on_launch', False),
            'organization': 1,  # Standard-Organisation
        }

        # Credential hinzufügen, wenn ausgewählt
        if data.get('credential'):
            project_data['credential'] = int(data['credential'])

        # Wenn kein SCM verwendet wird, einige Felder entfernen
        if data['scm_type'] == 'manual':
            project_data.pop('scm_url', None)
            project_data.pop('scm_branch', None)
            project_data.pop('scm_clean', None)
            project_data.pop('scm_delete_on_update', None)
            project_data.pop('scm_update_on_launch', None)
            project_data.pop('credential', None)

        response = requests.post(
            f"{AWX_HOST}/api/{API_VERSION}/projects/",
            json=project_data,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        return jsonify({
            'success': True,
            'message': f"Projekt '{data['name']}' wurde erfolgreich erstellt!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Fehler beim Erstellen des Projekts: {str(e)}"
        })

@app.route('/create/inventory', methods=['POST'])
@login_required
def create_inventory():
    data = request.get_json()
    
    try:
        response = requests.post(
            f"{AWX_HOST}/api/{API_VERSION}/inventories/",
            json={
                'name': data['name'],
                'description': data.get('description', ''),
                'organization': 1,  # Standard-Organisation
            },
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        return jsonify({
            'success': True,
            'message': f"Inventory '{data['name']}' wurde erfolgreich erstellt!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Fehler beim Erstellen des Inventories: {str(e)}"
        })

@app.route('/create/host', methods=['POST'])
@login_required
def create_host():
    data = request.get_json()
    
    try:
        # Überprüfe ob das Inventory existiert
        inventory_id = int(data['inventory_id'])
        
        # Bereite die Host-Variablen vor
        variables = data.get('variables', '')
        if not variables:
            # Standard-Variablen, wenn keine angegeben wurden
            variables = {
                'ansible_host': data['host']
            }
        else:
            # Versuche YAML zu parsen
            try:
                import yaml
                variables = yaml.safe_load(variables)
                if not isinstance(variables, dict):
                    variables = {'ansible_host': data['host']}
            except:
                variables = {'ansible_host': data['host']}

        # Host erstellen
        response = requests.post(
            f"{AWX_HOST}/api/{API_VERSION}/hosts/",
            json={
                'name': data['name'],
                'description': data.get('description', ''),
                'inventory': inventory_id,
                'variables': variables
            },
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        return jsonify({
            'success': True,
            'message': f"Host '{data['name']}' wurde erfolgreich zum Inventory hinzugefügt!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Fehler beim Hinzufügen des Hosts: {str(e)}"
        })

def get_inventory_hosts(inventory_id):
    try:
        response = requests.get(
            f"{AWX_HOST}/api/{API_VERSION}/inventories/{inventory_id}/hosts/",
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        return response.json()['results']
    except:
        return []

@app.route('/get_inventory_hosts/<int:inventory_id>')
@login_required
def get_hosts(inventory_id):
    hosts = get_inventory_hosts(inventory_id)
    # Formatiere die Host-Variablen für bessere Lesbarkeit
    for host in hosts:
        if 'variables' in host and host['variables']:
            try:
                import yaml
                if isinstance(host['variables'], str):
                    host['variables'] = yaml.safe_load(host['variables'])
                host['variables'] = yaml.dump(host['variables'], default_flow_style=False)
            except:
                pass
    return jsonify(hosts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 

print(f"API-Call: {instance_url}/api/{API_VERSION}/{endpoint}/ -> Status: {response.status_code}")  
for job in jobs:
    print(f"Job gefunden: {job.get('name')} | Type: {job.get('job_type')} | Status: {job.get('status')}")


# https://awx.apps.ocp.jungheinrich.com//api/v2/jobs/

