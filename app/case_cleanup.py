#!/usr/bin/env python3
'''
Created on 2023/04/12

@author: khrz
'''
# from pprint import pprint
from loglib import applog
import netlib

applog

def main():
    case_remove_list = netlib.get_soar_closed_healthcheck_case_ids()
    len_removed_incidents = netlib.delete_cases(case_remove_list)

    if len_removed_incidents:
        applog.info("{} cases has been removed.".format(len_removed_incidents))

if __name__ == '__main__':
    main()
