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
Prism Element Plugin for PRTG

Benedikt Heuser
'''

INFO = '''

'''

if __name__=='__main__':


  parser = argparse.ArgumentParser(																	# Build the Option Parser and add some helpful Texts
    epilog=EPILOG, description=INFO, formatter_class=RawTextHelpFormatter
  )
  parser.add_argument("-H", dest="ip", default='empty', help="IP Address of Prism Element")					# Add some Arguments
  parser.add_argument("-U", dest="user", default='empty', help="Prism Element User")
  parser.add_argument("-P", dest="password", default='empty', help="Prism Elemet Password")
  (args) = parser.parse_args()
  if len(sys.argv)!=7:
    parser.print_help(sys.stderr)
    sys.exit(1)

  url = "https://" + args.ip + ":9440/PrismGateway/services/rest/v2.0/clusters/"
  try:
    res = requests.get(url, auth=HTTPBasicAuth(args.user, args.password), verify=False, headers = headers, data=json.dumps(data))
  except:
    print('0:Prism Central with IP:%s not reachable.' % args.ip)
    sys.exit(2)
  if res.status_code != 200:
      print('0:Prism Central with IP:%s not reachable.' % args.ip)
      sys.exit(2)
  response_data = res.json()

  #print(json.dumps(response_data, indent=2))

  storage_usage_bytes = response_data['entities'][0]['usage_stats']['storage.usage_bytes']
  storage_free_bytes = response_data['entities'][0]['usage_stats']['storage.free_bytes']
  storage_sum_byte = int(storage_usage_bytes) + int(storage_free_bytes)
  storage_usage_proz = int(storage_usage_bytes) / storage_sum_byte * 100

  storage_free_gb = int(storage_free_bytes) / 1024 / 1024 / 1024
  storage_usage_gb = int(storage_usage_bytes) / 1024 / 1024 / 1024
  storage_sum_gb = storage_usage_gb + storage_free_gb

  print("%s Procent Storage free on Cluster. %s of %s GB used"
         % (str(round(storage_usage_proz, 2)), str(round(storage_usage_gb,2)), str(round(storage_sum_gb,2))))

  exit_code = 0

 # print('%s:%s kritische Alarme in PrismCentral aktiv.' % (str(not_resolved), str(not_resolved)))
  sys.exit(exit_code)
