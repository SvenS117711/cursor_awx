#!/usr/bin/env python3

import sys
import json
import requests
import time

# AWX Verbindungsdetails
AWX_HOST = 'http://awx-test.fritz.box'
AWX_USERNAME = 'cursor'
AWX_PASSWORD = 'Test001'
API_VERSION = 'v2'

def get_template_type():
    template_types = {
        '1': 'job_template',
        '2': 'workflow_template'
    }
    
    print("\nTemplate Typ:")
    print("1: Job Template")
    print("2: Workflow Template")
    
    choice = input("\nBitte wählen Sie den Template-Typ (1/2): ")
    return template_types.get(choice)

def get_projects():
    api_url = f"{AWX_HOST}/api/{API_VERSION}/projects/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        projects = response.json()
        
        print("\nVerfügbare Projekte:")
        for project in projects['results']:
            print(f"ID: {project['id']}, Name: {project['name']}")
            
        project_id = input("\nBitte geben Sie die Projekt-ID ein: ")
        return int(project_id) if project_id else None
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Projekte: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def sync_project(project_id):
    api_url = f"{AWX_HOST}/api/{API_VERSION}/projects/{project_id}/update/"
    
    try:
        print("\nStarte Projekt-Synchronisation...")
        
        # Starte Sync
        response = requests.post(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        job_data = response.json()
        job_id = job_data['id']
        
        # Warte auf Abschluss der Synchronisation
        while True:
            status_url = f"{AWX_HOST}/api/{API_VERSION}/project_updates/{job_id}/"
            status_response = requests.get(
                status_url,
                auth=(AWX_USERNAME, AWX_PASSWORD),
                verify=False
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            if status_data['status'] in ['successful', 'failed', 'error', 'canceled']:
                print(f"Synchronisation {status_data['status']}")
                return status_data['status'] == 'successful'
                
            print("Synchronisation läuft...")
            time.sleep(2)
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Projekt-Synchronisation: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return False

def get_project_playbooks(project_id):
    api_url = f"{AWX_HOST}/api/{API_VERSION}/projects/{project_id}/playbooks/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        playbooks = response.json()
        
        if not playbooks:
            print("\nKeine Playbooks im Projekt gefunden!")
            return None
        
        print("\nVerfügbare Playbooks:")
        for idx, playbook in enumerate(playbooks, 1):
            print(f"{idx}: {playbook}")
            
        choice = input("\nBitte wählen Sie ein Playbook (Nummer): ")
        try:
            return playbooks[int(choice)-1]
        except (ValueError, IndexError):
            print("Ungültige Auswahl!")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Playbooks: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def get_inventories():
    api_url = f"{AWX_HOST}/api/{API_VERSION}/inventories/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        inventories = response.json()
        
        print("\nVerfügbare Inventories:")
        for inv in inventories['results']:
            print(f"ID: {inv['id']}, Name: {inv['name']}")
            
        inv_id = input("\nBitte geben Sie die Inventory-ID ein: ")
        return int(inv_id) if inv_id else None
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Inventories: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def get_credentials():
    api_url = f"{AWX_HOST}/api/{API_VERSION}/credentials/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        credentials = response.json()
        
        print("\nVerfügbare Credentials:")
        for cred in credentials['results']:
            print(f"ID: {cred['id']}, Name: {cred['name']}, Typ: {cred['credential_type']}")
            
        cred_ids = input("\nBitte geben Sie die Credential-IDs ein (kommagetrennt, Enter für keine): ")
        if not cred_ids:
            return []
        return [int(cred_id.strip()) for cred_id in cred_ids.split(',')]
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Credentials: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return []

def create_job_template(project_id, playbook):
    name = input("\nTemplate Name: ")
    description = input("Template Beschreibung (optional): ")
    inventory_id = get_inventories()
    credential_ids = get_credentials()
    
    # API Endpunkt
    api_url = f"{AWX_HOST}/api/{API_VERSION}/job_templates/"
    
    # Template Daten
    template_data = {
        'name': name,
        'description': description,
        'job_type': 'run',
        'inventory': inventory_id,
        'project': project_id,
        'playbook': playbook,
        'credentials': credential_ids,
        'ask_variables_on_launch': True,
        'ask_limit_on_launch': True,
        'ask_tags_on_launch': True,
        'ask_skip_tags_on_launch': True
    }
    
    try:
        # Erstelle Template
        response = requests.post(
            api_url,
            json=template_data,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        # Parse Response
        template = response.json()
        
        # Füge Credentials hinzu
        if credential_ids:
            for cred_id in credential_ids:
                cred_url = f"{AWX_HOST}/api/{API_VERSION}/job_templates/{template['id']}/credentials/"
                cred_response = requests.post(
                    cred_url,
                    json={'id': cred_id},
                    auth=(AWX_USERNAME, AWX_PASSWORD),
                    verify=False
                )
                cred_response.raise_for_status()
        
        print(f"\nJob Template wurde erfolgreich erstellt:")
        print(f"Name: {template['name']}")
        print(f"ID: {template['id']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\nFehler beim Erstellen des Templates: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return False

def create_workflow_template():
    name = input("\nWorkflow Template Name: ")
    description = input("Workflow Template Beschreibung (optional): ")
    
    # API Endpunkt
    api_url = f"{AWX_HOST}/api/{API_VERSION}/workflow_job_templates/"
    
    # Template Daten
    template_data = {
        'name': name,
        'description': description,
        'ask_variables_on_launch': True
    }
    
    try:
        response = requests.post(
            api_url,
            json=template_data,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        
        template = response.json()
        print(f"\nWorkflow Template wurde erfolgreich erstellt:")
        print(f"Name: {template['name']}")
        print(f"ID: {template['id']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\nFehler beim Erstellen des Workflow Templates: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return False

def create_template():
    template_type = get_template_type()
    if not template_type:
        print("Ungültiger Template-Typ!")
        return False
        
    if template_type == 'job_template':
        # Hole und synchronisiere Projekt
        project_id = get_projects()
        if not project_id:
            print("Kein Projekt ausgewählt!")
            return False
            
        # Synchronisiere Projekt
        if not sync_project(project_id):
            print("Projekt-Synchronisation fehlgeschlagen!")
            return False
            
        # Hole Playbooks
        playbook = get_project_playbooks(project_id)
        if not playbook:
            print("Kein Playbook ausgewählt!")
            return False
            
        # Erstelle Job Template
        return create_job_template(project_id, playbook)
    else:
        # Erstelle Workflow Template
        return create_workflow_template()

if __name__ == '__main__':
    # Deaktiviere Warnungen für unsichere HTTPS-Requests
    requests.packages.urllib3.disable_warnings()
    
    print("AWX Template erstellen")
    print("=====================")
    create_template() 