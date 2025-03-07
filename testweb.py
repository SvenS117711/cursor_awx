import requests

instance_url = "https://awx.apps.ocp.jungheinrich.com"
username = "awx_project_user"
password = "E8BpZ-cDvwH-8hBsj-oUB8f"
api_version = "v2"

url = f"{instance_url}/api/{api_version}/jobs/"
response = requests.get(url, auth=(username, password), verify=False)

if response.status_code == 200:
    jobs = response.json().get('results', [])
    print(f"Gefundene Jobs: {len(jobs)}")
    for job in jobs:
        print(f"Job Name: {job.get('name')}, Type: {job.get('job_type')}, Status: {job.get('status')}")
else:
    print(f"Fehler: {response.status_code}")
