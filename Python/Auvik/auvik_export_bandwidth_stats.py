import requests, json, csv
import logging, datetime, traceback
import time, datetime
import sys
from requests.auth import HTTPBasicAuth
from datetime import datetime


api_url_base = "https://auvikapi.my.auvik.com/v1"

user = ''
apikey = ''

#?limit=10&offset=0

tenants_api_url = api_url_base + "/tenants/detail?tenantDomainPrefix=bluebird&filter[availableTenants]=true"

f = csv.writer(open("auvik_bw.csv", 'w', newline=''))
row = ["Client", "TimeStamp", "Mbps"]
f.writerow(row)

def write_client_data_firewall(clientName,ClientID):

    bwstats_api_url = api_url_base + "/stat/device/bandwidth?filter[fromTime]=2021-07-01T00:00:00.000Z&filter[thruTime]=2021-07-31T23:59:59.000Z&filter[interval]=hour&filter[deviceType]=firewall&tenants=" + ClientID

    req = requests.get(bwstats_api_url, auth=HTTPBasicAuth(user,apikey))
    data = req.json()

    for set in data["data"]:
        for line in set["attributes"]["stats"][0]["data"]:
            timestamp = line[0]*60
            timestamp_out = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            bw = line[3]
            client = clientName
            row = [client, timestamp_out, bw]
            f.writerow(row)

def write_client_data_router(clientName,ClientID):

    bwstats_api_url = api_url_base + "/stat/device/bandwidth?filter[fromTime]=2021-07-01T00:00:00.000Z&filter[thruTime]=2021-07-31T23:59:59.000Z&filter[interval]=hour&filter[deviceType]=router&tenants=" + ClientID

    req = requests.get(bwstats_api_url, auth=HTTPBasicAuth(user,apikey))
    data = req.json()

    for set in data["data"]:
        for line in set["attributes"]["stats"][0]["data"]:
            timestamp = line[0]*60
            timestamp_out = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            bw = line[3]
            client = clientName
            row = [client, timestamp_out, bw]
            f.writerow(row)


req = requests.get(tenants_api_url, auth=HTTPBasicAuth(user,apikey))

#print(req.json())

data = req.json()

tenant_data = {}

for tenant in data["data"]:
    print(tenant["attributes"]["displayName"])
    tenant_data[tenant["attributes"]["displayName"]] = tenant["id"]

#print(tenant_data)

for tenant in tenant_data:
    #time.sleep(0.5)
    print("Getting data for: ",tenant,"...")
    write_client_data_firewall(tenant, tenant_data[tenant])
    write_client_data_router(tenant, tenant_data[tenant])

