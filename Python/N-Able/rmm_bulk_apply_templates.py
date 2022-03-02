import json, sys, requests, csv


cookies = {
    'tc_attended_check_sso_e7dfaa55-c8c3-5648-e2d9-b868819fea23': '0',
    'PHPSESSID': '',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'TE': 'trailers',
}

postdata = {
  'function': 'create_apply_monitoring_template_device_action_for_client_or_site',
  'action': 'createAction',
  'dashaction': '24',
  'data': '1',
  'password': '',
  'confirmed': 'false',
  'applyMonitoringTemplateFromEntityTree': 'true',
  'siteid': '0',
  'clientid': '',
  'isWorkstation': 'true',
  'csrf_token': ''
}

with open('client_list.json') as f:
    data = json.load(f)

print(data["result"][1]["children"][0])

for client in data["result"][1]["children"]:
    name = client['name']
    id = client['dbid']

    user = input(f"Apply offboarding template for {name}? (y/N) : ")

    if user == "Y" or user == "y" :
        postdata['clientid'] = str(id)
        response = requests.post('https://myrmmserver/data_processor.php', headers=headers, cookies=cookies, data=postdata)
        print(f"Applied offboarding template for {name}, ID= {id}")
        try:
            print (response.json())
        except Exception as ex:
            print("Error parsing response")

        print("next")




