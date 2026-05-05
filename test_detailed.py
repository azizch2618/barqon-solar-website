import urllib.request
from urllib.error import HTTPError
import json

data = {
    'name': 'Test Detailed',
    'phone': '123456',
    'city_area': 'Lahore',
    'property_type': 'home',
    'monthly_bill': '50000',
    'connection_phase': '3',
    'ac': '2',
    'appliance_data': '{"acs":[]}'
}

import urllib.parse
encoded_data = urllib.parse.urlencode(data).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:8000/automation/submit-lead/', 
    data=encoded_data, 
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except HTTPError as e:
    print("HTTPError:", e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print("Exception:", str(e))
