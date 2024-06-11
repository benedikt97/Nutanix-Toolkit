import requests
import json
import sys
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = "https://" + sys.argv[1] + ":9440/api/nutanix/v3/alerts/list"
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
data = {
  "kind": "alert",
  "sort_attribute": "",
  "length": 60,
  "sort_order": "ASCENDING",
  "offset": 0
}

try:
  res = requests.post(url, auth=HTTPBasicAuth('prtg', 'LoSiErEyeLBo!9440'), verify=False, headers = headers, data=json.dumps(data))
except:
  print('0:Prism Central with IP:%s not reachable.' % sys.argv[1])
  sys.exit(2)
if res.status_code != 200:
    print('0:Prism Central with IP:%s not reachable.' % sys.argv[1])
    sys.exit(2)
response_data = res.json()

not_resolved = 0
for r in response_data['entities']:
  affected_entity = r['status']['resources']['affected_entity_list'][0]['name']
  title = r['status']['resources']['title']
  parameters = r['status']['resources']['parameters']
  resolved = r['status']['resources']['resolution_status']['is_true']
  severity = r['status']['resources']['severity']
  if not resolved and "critical" in severity:
    not_resolved = not_resolved + 1

exit_code = 0
if not_resolved != 0:
  exit_code = 1

print('%s:%s kritische Alarme in PrismCentral aktiv.' % (str(not_resolved), str(not_resolved)))
sys.exit(exit_code)
