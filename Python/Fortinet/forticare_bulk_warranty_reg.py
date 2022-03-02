import requests
import json
import csv


url = "https://support.fortinet.com/ES/api/registration/v3/products/register"

def reg_device(serial, contract, description):
    payload = json.dumps({
    "registrationUnits": [
        {
        "serialNumber": serial,
        "contractNumber": contract,
        "description": description,
        "isGovernment": False
        }
    ]
    })

    headers = {
    'Authorization': '',
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    print('next')

with open('reglist.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        serial = row['serial']
        contract = row['contract']
        description = row['description']

        print(f'Registering {description} - {serial} - {contract}')

        reg_device(serial, contract, description)


