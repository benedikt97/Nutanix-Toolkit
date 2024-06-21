import requests
import json
import sys
import argparse
from argparse import RawTextHelpFormatter
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
data = {
  "kind": "alert",
  "sort_attribute": "",
  "length": 100,
  "sort_order": "ASCENDING",
  "offset": 0
}

EPILOG = '''
Prism Central Plugin for PRTG

Benedikt Heuser
'''

INFO = '''

'''

if __name__=='__main__':


  parser = argparse.ArgumentParser(																	# Build the Option Parser and add some helpful Texts
    epilog=EPILOG, description=INFO, formatter_class=RawTextHelpFormatter
  )
  parser.add_argument("-H", dest="ip", default='empty', help="IP Address of Prism Central")					# Add some Arguments
  parser.add_argument("-U", dest="user", default='empty', help="Prism Central User")
  parser.add_argument("-P", dest="password", default='empty', help="Prism Central Password")
  (args) = parser.parse_args()
  if len(sys.argv)!=7:
    parser.print_help(sys.stderr)
    sys.exit(1)

  url = "https://" + args.ip + ":9440/api/nutanix/v3/alerts/list"
  try:
    res = requests.post(url, auth=HTTPBasicAuth(args.user, args.password), verify=False, headers = headers, data=json.dumps(data))
  except Exception as error:
    print("An exception occurred:", error)
    sys.exit(2)
  if res.status_code != 200:
      print('0:Prism Central with IP:%s not reachable. HTTP Status: %s' % (args.ip, res.status_code))
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
