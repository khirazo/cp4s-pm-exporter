#!/opt/app-root/bin/python
'''
Created on 2023/04/11

@author: khrz
'''
# from pprint import pprint
import netlib
from loglib import applog

applog

def main():
    # Create a healthcheck case
    incident = netlib.create_healthcheck_case()

    if incident:
        applog.info("Incident id {} has been created.".format(incident['id']))

if __name__ == '__main__':
    main()
