import requests

url = "http://127.0.0.1:8001/"
session = requests.Session()
# Get CSRF token
r1 = session.get(url)
csrftoken = session.cookies['csrftoken']

data = {
    'csrfmiddlewaretoken': csrftoken,
    'name': 'Test Lead',
    'phone': '03001234567',
    'city_area': 'Lahore',
    'bill_amount_1': '25000',
    'subject': 'Smart Solar Assessment Request',
    'message': 'Customer requested a smart solar assessment.',
    'property_type': 'home',
}

r2 = session.post(url, data=data)
print(f"Status Code: {r2.status_code}")
if "success=true" in r2.url:
    print("Success! Redirected to success page.")
else:
    print("Failed. No success redirect.")
    # Look for errors in HTML
    if "sol-error-summary" in r2.text:
        print("Found error summary in response.")
        # Extract errors
        import re
        errors = re.findall(r'<li>(.*?)</li>', r2.text)
        for err in errors:
            print(f"Error: {err}")
    else:
        print("No error summary found in response.")
