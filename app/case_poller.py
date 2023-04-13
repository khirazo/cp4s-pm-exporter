#!/usr/bin/env python3
'''
Created on 2023/04/09

@author: khrz
'''
import sys
from threading import Timer
# from pprint import pprint
import netlib, dblib
from loglib import applog

applog

result_keys = ['healthcheck_results_1', 'healthcheck_results_2', 'healthcheck_results_3', 'healthcheck_results_4']
item_names = ['qradar_offense', 'de', 'tii', 'ldap']
in_progress = False
poll_interval = 1

def populate_db():
    global in_progress

    if in_progress:
        applog.warning("The previous thread is still in progress. Skipping...")
    else:
        in_progress = True
        applog.info("Executing the thread...")

        data = [] 
        item = {}
        case_data = netlib.get_soar_latest_healthcheck_case()
    
        for i, result_key in enumerate(result_keys):
            item = case_data.get(result_key)        
            if item:
                item['index'] = item.get('index')
                item['name'] = item_names[i]
                item['summary'] = item.get('summary')
                item['content'] = item.get('content')
                item['execution_time_ms'] = item.get('execution_time_ms')
                item['last_update_epoc_ms'] = item.get('last_update_epoc_ms')
                data.append(item)
    
        dblib.update_info(data)
        applog.info("The metrics have been updated.")
        in_progress = False

    time = Timer(poll_interval, populate_db)
    time.start()    

def main():
    global poll_interval

    dblib.check_table()
    netlib.load_config_values()
    # pprint(netlib.config)
    soar_config = netlib.config.get('soar-config')
    poll_interval = soar_config.get('healthcheck_poll_interval_mins')    

    if int(poll_interval) < 1:
        applog.error("Poll interval {} mins is too small.".format(poll_interval))
        sys.exit(1)
    else:
        poll_interval = int(poll_interval) * 60
        applog.info("Poll interval is set to {} secs.".format(poll_interval))

    populate_db()

    # populate_db()
    # pprint(dblib.dump_db())
    # pprint(dblib.get_metrics())

if __name__ == '__main__':
    main()
