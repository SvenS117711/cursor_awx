# AWX Tools Web-Anwendung - Installationsanleitung

## Systemvoraussetzungen

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## Installation

1. **Projektverzeichnis erstellen**:
```bash
mkdir awx_tools
cd awx_tools
```

2. **Virtuelle Umgebung erstellen und aktivieren**:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Projektdateien kopieren**:
- Kopieren Sie `awx_api_scripts/templates_web.py` in das Verzeichnis
- Kopieren Sie `requirements.txt` in das Verzeichnis

4. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt
```

5. **Berechtigungen anpassen**:
```bash
chmod +x templates_web.py
```

6. **Anwendung starten**:
```bash
python3 templates_web.py
```

Die Anwendung läuft dann standardmäßig auf:
- URL: `http://localhost:5000`
- Port: 5000
- Host: 0.0.0.0 (zugänglich von allen Netzwerkschnittstellen)

## Zusätzliche Konfigurationen

### Firewall-Konfiguration
Falls eine Firewall aktiv ist, muss Port 5000 freigegeben werden:
```bash
sudo ufw allow 5000
```

### Produktionsserver mit Gunicorn
Für Produktionsumgebungen wird die Verwendung von Gunicorn empfohlen:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 templates_web:app
```

### Systemd-Service (optional)
1. Service-Datei erstellen:
```bash
sudo nano /etc/systemd/system/awx-tools.service
```

2. Folgende Konfiguration einfügen:
```ini
[Unit]
Description=AWX Tools Web Application
After=network.target

[Service]
User=<ihr_username>
WorkingDirectory=/pfad/zu/awx_tools
Environment="PATH=/pfad/zu/awx_tools/venv/bin"
ExecStart=/pfad/zu/awx_tools/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 templates_web:app

[Install]
WantedBy=multi-user.target
```

3. Service aktivieren und starten:
```bash
sudo systemctl enable awx-tools
sudo systemctl start awx-tools
```

### Logging
Logs können mit `journalctl` eingesehen werden:
```bash
journalctl -u awx-tools.service -f
```

## Abhängigkeiten
Die folgenden Python-Pakete werden automatisch installiert:
```
Flask==3.0.2
Flask-Login==0.6.3
requests==2.31.0
PyYAML==6.0.1
urllib3==2.2.1
Werkzeug==3.0.1
```

## Sicherheitshinweise
- Die Anwendung deaktiviert SSL-Warnungen für die AWX-API
- In einer Produktionsumgebung sollte ein gültiges SSL-Zertifikat verwendet werden
- Stellen Sie sicher, dass die Firewall-Regeln korrekt konfiguriert sind
- Verwenden Sie starke Passwörter für die AWX-Authentifizierung # cursor_awx
# cursor_awx
