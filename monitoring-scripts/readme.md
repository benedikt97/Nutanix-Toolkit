# Nutanix Monitoring-Scripts

These simple Scrips can be used to monitor Nutanix-Environments. The outputs of the scripts is formated according to PRTG at the moment and needs to be changed for other environments like Nagios.
PRTG expects a return code and a message on stdout '0:Message'. The value at the beginning can be used as metric for performance charts.
The scripts querys against the Nutanix RestAPI.

## prtg-prismelement-check.py

This checks reads the physical used and free bytes from the cluster a calculates whe utiliztation of the storage. You can give different threshold for yellow and red alerts in prtg. Usually the red alert should be the 'resilient' threshold of the nutanix cluster. Usage of the script can be obtained with the -h parameter.

## prtg-ntnx-criticalalerts-check.py

This script counts the number of unresolved critical alerts on the nutanix cluster. When critical alerts occour, you receive an warning in prtg.