import urllib.request
from urllib.error import HTTPError
import json
import uuid

boundary = uuid.uuid4().hex

fields = {
    'name': 'Test Multipart',
    'phone': '9999999',
    'city_area': 'Karachi',
    'property_type': 'home',
    'monthly_bill': '60000',
    'connection_phase': '3',
    'ac': '2',
    'appliance_data': '{"acs":[]}'
}

body = bytearray()
for key, value in fields.items():
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8'))
    body.extend(f'{value}\r\n'.encode('utf-8'))
body.extend(f'--{boundary}--\r\n'.encode('utf-8'))

req = urllib.request.Request(
    'http://127.0.0.1:8000/automation/submit-lead/', 
    data=bytes(body), 
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except HTTPError as e:
    print("HTTPError:", e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print("Exception:", str(e))
