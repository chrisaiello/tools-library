import requests, json, csv
import sys

bearer = ""
api_url = "https://www.forticloud.com/forticloudapi/v1/devices"

headers = {'Authorization': 'Bearer ' + bearer}

req = requests.get(api_url,headers=headers)

print(req.json())

data = req.json()

for fortigate in data:
    print(fortigate.keys())


f = csv.writer(open("forticloud.csv", 'w', newline=''))

row = ["sn", "name", "tunnelAlive", "model", "firmwareVersion", "management", "initialized", "total"]

f.writerow(row)

for fgt in data:
    f.writerow([fgt["sn"],
                fgt["name"],fgt["tunnelAlive"],fgt["model"],fgt["firmwareVersion"],fgt["management"],fgt["initialized"],fgt["total"]])