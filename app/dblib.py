'''
Created on 2023/04/02

@author: khrz
'''
import sqlite3
from loglib import applog

applog

DB_PATH = '../store/metrics.db'
TABLE_NAME = 'metrics'

def check_table():
    # Check if the table exists and create one when doesn't
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='{}'".format(TABLE_NAME))
    count = cur.fetchone()
    if count and int(count[0]) == 0:
        cur.execute('CREATE TABLE {}(id INTEGER PRIMARY KEY, name TEXT, summary TEXT, content TEXT, execution_time_ms REAL, last_update_epoc_ms REAL)'.format(TABLE_NAME))
        conn.commit()
    cur.close()
    conn.close()

def escape_sq(string):
    if string:
        return str(string).replace("'", "''")
    else:
        return string
    
def update_info(data_dict_list):
    # update table with metrics data dict list
    #   index, name, summary, content, execution_time_ms, last_update_epoc_ms
    # check_table()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if data_dict_list and len(data_dict_list) > 0:
        for item in data_dict_list:
            cur.execute("REPLACE INTO {} values({}, '{}', '{}', '{}', {}, {})"
                        .format(TABLE_NAME, item.get('index'), escape_sq(item.get('name')), 
                                escape_sq(item.get('summary')), escape_sq(item.get('content')), 
                                item.get('execution_time_ms'), item.get('last_update_epoc_ms')))
    else:
        cur.execute("REPLACE INTO {} values({}, '{}', '{}', '{}', {}, {})".format(TABLE_NAME, 1, "", "", "", 0, 0))
        cur.execute("REPLACE INTO {} values({}, '{}', '{}', '{}', {}, {})".format(TABLE_NAME, 2, "", "", "", 0, 0))
        cur.execute("REPLACE INTO {} values({}, '{}', '{}', '{}', {}, {})".format(TABLE_NAME, 3, "", "", "", 0, 0))
        cur.execute("REPLACE INTO {} values({}, '{}', '{}', '{}', {}, {})".format(TABLE_NAME, 4, "", "", "", 0, 0))
        
    conn.commit()
    cur.close()
    conn.close()

def get_metrics():
    # get table data and create metrics dict data for Jinja template
    metrics = {
        'cp4s_qradar_up': 0,
        'cp4s_qradar_last_udpate_time_msec': 0,
        'cp4s_qradar_execution_time_ms': 0,
        'cp4s_de_up': 0,
        'cp4s_de_last_udpate_time_msec': 0,
        'cp4s_de_execution_time_ms': 0,
        'cp4s_tii_up': 0,
        'cp4s_tii_last_udpate_time_msec': 0,
        'cp4s_tii_execution_time_ms': 0,
        'cp4s_ldap_up': 0,
        'cp4s_ldap_last_udpate_time_msec': 0,
        'cp4s_ldap_execution_time_ms': 0
        }

    # check_table()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, summary, execution_time_ms, last_update_epoc_ms FROM {}'.format(TABLE_NAME))
    data = cur.fetchall()
    cur.close()
    conn.close()

    if data and len(data) > 0:
        for metric in data:
            if metric[0] == 1:
                # qradar
                metrics['cp4s_qradar_up'] = 1 if metric[1] == 'successful' else 0
                metrics['cp4s_qradar_last_udpate_time_msec'] = metric[3]
                metrics['cp4s_qradar_execution_time_ms'] = metric[2]
            elif metric[0] == 2:
                # de
                metrics['cp4s_de_up'] = 1 if metric[1] == 'successful' else 0
                metrics['cp4s_de_last_udpate_time_msec'] = metric[3]
                metrics['cp4s_de_execution_time_ms'] = metric[2]
            elif metric[0] == 3:
                # tii
                metrics['cp4s_tii_up'] = 1 if metric[1] == 'successful' else 0
                metrics['cp4s_tii_last_udpate_time_msec'] = metric[3]
                metrics['cp4s_tii_execution_time_ms'] = metric[2]
            elif metric[0] == 4:
                # ldap
                metrics['cp4s_ldap_up'] = 1 if metric[1] == 'successful' else 0
                metrics['cp4s_ldap_last_udpate_time_msec'] = metric[3]
                metrics['cp4s_ldap_execution_time_ms'] = metric[2]

    return metrics

def dump_db():
    check_table()
       
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT * FROM {}'.format(TABLE_NAME))
    data = cur.fetchall()
    
    cur.close()
    conn.close()

    return data
