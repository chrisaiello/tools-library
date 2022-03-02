import json, csv
import logging, json
import sys
import requests
from time import sleep
from random import randint

logging.basicConfig(filename="tc_add_clients.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

pcid_dict = {}
pcname_dict = {}

def create_user(name, email): #Creates a client user in Take Control

    cookies = {
        'filterDate_filters': '%5B%5D',
        'devicesMenu_osize': '250',
        'devicesList_osize': '1116',
        'devicesListTable_sort': '{"sortBy":"servername","sortDir":true}',
        'filterWildDevices_filters': '%5B%5D',
        'widget-sso-login-status': '0',
        'liveagent_chatted': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://admin.us3.swi-tc.com/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://admin.us3.swi-tc.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    data = {
    'create_user': '1',
    'name': name,
    'email': email,
    'valid_until': '2099-12-31',
    'user_is_client': '1',
    'permissions_profile': 'default',
    'TOKEN': ''
    }

    #Create user account and check for errors

    response = requests.post('https://admin.us3.swi-tc.com/admin_area_/ajax/save_tech_details.php', headers=headers, cookies=cookies, data=data)

    try:
        response_code = response.json()['code']
    except Exception as ex:
        logging.info("Error parsing response, check authorization")
        logging.info(ex)
        quit()

    response_userID = 0

    if response_code == -2:
        logging.info(f"Error: {response_code}. Failed to add {email}, user already exists.")
    elif response_code != 0:
        logging.info(f"Error: {response_code}. Failed to add {email}")
    elif response_code == 0:
        response_userID = response.json()['info']
        logging.info(f"Added user {email} userID: {response_userID}")
    return response_userID, response_code

def assign_pc(email, userID, computerList): # Assigns Take Control devices to a user


    # Assign Computer IDs to user

    cookies = {
        'filterDate_filters': '%5B%5D',
        'devicesMenu_osize': '250',
        'devicesList_osize': '1116',
        'devicesListTable_sort': '{"sortBy":"servername","sortDir":true}',
        'widget-sso-login-status': '0',
        'liveagent_chatted': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://admin.us3.swi-tc.com/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://admin.us3.swi-tc.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    data = { #Contains data on what computers are assigned to this userID. pcs_client[] entries need to be added for each computerID.
    'id': userID,
    #f'pcs_client[{ComputerID}]': '',
    'TOKEN': ''
    }

    for id in computerList: # Updates data with ID of each computer to be assigned.
        data[f"pcs_client[{id}]"]=''

    response = requests.post('https://admin.us3.swi-tc.com/admin_area_/ajax/save_tech_details.php', headers=headers, cookies=cookies, data=data)

    response_code = response.json()['code']

    if response_code != 0:
        logging.info(f"Error: {response_code}. Failed to assign computer to {email}")
    elif response_code == 0:
        logging.info(f"Assigned {computerList} to {email}")
    
    return response_code

def pcname_to_id(pcname): # Takes computer name and gets the associated Take Control computer ID.

    if pcname in pcid_dict:
        return pcid_dict[pcname]
    else:
        logging.info(f"ID not found for {pcname}")
        return -1

def load_ids(): # Reads in list of Take Control IDs from json files.
    with open('pcid_list01.json') as f:
        data = json.load(f)

        for entry in data['Rows']:
            if entry['servername'] in pcid_dict:
                logging.critical(f"Duplicate found, {entry['servername']}")
                logging.critical("Resolve all duplicates and run again.")
                quit()
            pcid_dict[entry['servername']] = entry['idpc']

    

def load_names():# Reads in list of client emails and computers.
    with open('client_pc_list.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        cur_email = ""
        for row in reader:
            email = row["ClientEmail"]
            pcname = row["ComputerName"]
            if email not in pcname_dict:
                pcname_dict[email] = list()
                pcname_dict[email].append(pcname)
            else:
                pcname_dict[email].append(pcname)  

load_ids()
logging.info("Loaded TakeControl Device IDs")
logging.info(f"Loaded {len(pcid_dict)} devices")

load_names()
logging.info("Loaded client list and PC names")
logging.info(f"Loaded {len(pcname_dict)} clients")

for client in pcname_dict:
    logging.info(f"{client} is assigned {pcname_dict[client]}")
    email = client

    sleep(randint(6,9)) #Faster requests generate errors

    id,result = create_user(email, email)

    if (result==0) and (id > 0):
        computers = pcname_dict[email]
        print(f"{email} is associated with {computers}")

        computerList = []

        for computer in computers:
            computerid = pcname_to_id(computer)
            if computerid > 0:
                computerList.append(computerid)

        sleep(randint(3,5))
        result = assign_pc(email, id, computerList)
        print(result)






            
