#!/usr/bin/env python3

import sys
import json
import requests

# AWX Verbindungsdetails
AWX_HOST = 'http://awx-test.fritz.box'
AWX_USERNAME = 'cursor'
AWX_PASSWORD = 'Test001'
API_VERSION = 'v2'

def get_scm_types():
    return {
        '1': '',           # Manual
        '2': 'git',        # Git
        '3': 'svn',        # Subversion
        '4': 'insights',   # Red Hat Insights
        '5': 'archive'     # Remote Archive
    }

def get_organization_id():
    # API Endpunkt
    api_url = f"{AWX_HOST}/api/{API_VERSION}/organizations/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        organizations = response.json()
        
        print("\nVerfügbare Organisationen:")
        for org in organizations['results']:
            print(f"ID: {org['id']}, Name: {org['name']}")
            
        org_id = input("\nBitte geben Sie die gewünschte Organizations-ID ein (Enter für keine): ")
        return int(org_id) if org_id else None
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Organisationen: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def get_scm_credentials():
    # API Endpunkt
    api_url = f"{AWX_HOST}/api/{API_VERSION}/credentials/"
    
    try:
        response = requests.get(
            api_url,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        response.raise_for_status()
        credentials = response.json()
        
        # Zeige alle verfügbaren Credentials
        print("\nVerfügbare Credentials:")
        for cred in credentials['results']:
            print(f"ID: {cred['id']}, Name: {cred['name']}, Typ: {cred['credential_type']}")
            
        cred_id = input("\nBitte geben Sie die gewünschte Credential-ID ein (Enter für keine): ")
        return int(cred_id) if cred_id else None
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Credentials: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def create_project():
    # Hole verfügbare SCM Typen
    scm_types = get_scm_types()
    
    print("\nVerfügbare SCM Typen:")
    for key, value in scm_types.items():
        scm_type_name = value if value else "Manual"
        print(f"{key}: {scm_type_name}")
    
    # Projekt Informationen sammeln
    name = input("\nProjektname: ")
    description = input("Projektbeschreibung (optional): ")
    scm_type_key = input("SCM Typ (Nummer aus der Liste oben): ")
    scm_type = scm_types.get(scm_type_key, '')
    
    # Zusätzliche Informationen für Git/SVN Projekte
    scm_url = ""
    scm_branch = ""
    scm_credential = None
    if scm_type in ['git', 'svn']:
        scm_url = input("SCM URL: ")
        scm_branch = input("SCM Branch (optional, Enter für Standard): ")
        scm_credential = get_scm_credentials()
    
    # Organization ID
    organization = get_organization_id()
    
    # API Endpunkt
    api_url = f"{AWX_HOST}/api/{API_VERSION}/projects/"
    
    # Projekt Daten
    project_data = {
        'name': name,
        'description': description,
        'scm_type': scm_type,
        'scm_url': scm_url,
        'scm_branch': scm_branch,
        'allow_override': True
    }
    
    # Füge Organization hinzu, wenn ausgewählt
    if organization:
        project_data['organization'] = organization
        
    # Füge SCM Credential hinzu, wenn ausgewählt
    if scm_credential:
        project_data['credential'] = scm_credential
    
    try:
        # Sende POST Request
        response = requests.post(
            api_url,
            json=project_data,
            auth=(AWX_USERNAME, AWX_PASSWORD),
            verify=False
        )
        
        # Prüfe Response
        response.raise_for_status()
        
        # Parse Response
        project = response.json()
        print(f"\nProjekt wurde erfolgreich erstellt:")
        print(f"Name: {project['name']}")
        print(f"ID: {project['id']}")
        print(f"Typ: {project['scm_type'] if project['scm_type'] else 'Manual'}")
        if project['scm_url']:
            print(f"URL: {project['scm_url']}")
        if project.get('credential'):
            print(f"SCM Credential ID: {project['credential']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\nFehler beim Erstellen des Projekts: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return False

if __name__ == '__main__':
    # Deaktiviere Warnungen für unsichere HTTPS-Requests
    requests.packages.urllib3.disable_warnings()
    
    print("AWX Projekt erstellen")
    print("====================")
    create_project() 