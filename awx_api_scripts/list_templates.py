#!/usr/bin/env python3

import requests
from datetime import datetime
from operator import itemgetter

# AWX Verbindungsdetails
AWX_HOST = 'http://awx-test.fritz.box'
AWX_USERNAME = 'cursor'
AWX_PASSWORD = 'Test001'
API_VERSION = 'v2'

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
        
        # Job Templates zur Liste hinzufügen
        for template in job_templates['results']:
            templates.append({
                'name': template['name'],
                'type': 'Job Template',
                'created': template['created']
            })
            
        # Workflow Templates zur Liste hinzufügen
        for template in workflow_templates['results']:
            templates.append({
                'name': template['name'],
                'type': 'Workflow Template',
                'created': template['created']
            })
            
        return templates
            
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Templates: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
        return None

def format_datetime(dt_string):
    dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    return dt.strftime('%d.%m.%Y %H:%M:%S')

def list_templates():
    # Hole alle Templates
    templates = get_all_templates()
    
    if not templates:
        print("Keine Templates gefunden oder Fehler beim Abrufen.")
        return
    
    # Sortiere nach Erstellungsdatum (neueste zuerst)
    templates.sort(key=itemgetter('created'), reverse=True)
    
    # Ausgabe
    print("\nAlle Templates (sortiert nach Erstellungsdatum, neueste zuerst):")
    print("=" * 80)
    
    for template in templates:
        print(f"Name: {template['name']}")
        print(f"Erstellt am: {format_datetime(template['created'])}")
        print("-" * 80)

if __name__ == '__main__':
    # Deaktiviere Warnungen für unsichere HTTPS-Requests
    requests.packages.urllib3.disable_warnings()
    
    print("AWX Template Übersicht")
    print("=====================")
    list_templates() 