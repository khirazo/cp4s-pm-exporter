'''
Created on 2023/02/05

@author: khrz
'''
import urllib3, json, yaml
from resilient import SimpleClient
from time import sleep, time
from loglib import applog

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

applog

# Globals
CONFIG_FILE = '../store/config.yml'
config = None
res_client = None
incident_types = {}

# Reads configuration yaml file and returns configuration dict
def load_config_values():
    global config
    # ret_values = {}

    if config == None:  # Reconsider this check if config file may be updated while running this script
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
            return
        raise Exception("Error occurred while reading {}".format(CONFIG_FILE))

# Returns SOAR SimpleClient
def get_soar_simple_client():
    load_config_values()
    soar_config = config.get('soar-config')
    global res_client
    global incident_types

    if res_client == None:       
        # Instanciate SimpleClient
        res_client = SimpleClient(
            org_name = soar_config.get('soar_org_name'),
            base_url = soar_config.get('soar_server_uri'),
            verify = soar_config.get('validate_certs')
        )
    
        # Set the API Key
        res_client.set_api_key(
            api_key_id = soar_config.get('soar_api_key_id'),
            api_key_secret = soar_config.get('soar_api_key_secret')
        )

        # Fill up the incident_types dict
        response = res_client.get("/")
        if response:
            incident_types = response.get("incident_types")

    return res_client

# Returns SOAR incident type id by name
def get_incident_type_id_by_name(incident_type_name):
    '''
    returns incident_type_id
    '''
    for incident_type_id in incident_types:
        if incident_types[incident_type_id]["name"] == incident_type_name:
            return int(incident_type_id)

# Json to Python dict
def json_to_dict(text):
    if not text:
        return {}
    else:
        return json.loads(text)

# Returns the latest SOAR open case (debug purpose)
def get_soar_latest_open_case():
    '''
    returns incident_dict
    '''
    res_client = get_soar_simple_client()

    # Setup the request payload for search
    payload = {
        "filters": [
            {
                "conditions": [
                    {"field_name": "plan_status",
                      "method": "equals",
                      "value": "A"}
                    ],
                "logic_type": "ANY"
            }
        ],
        "sorts": [
            {"field_name": "create_date", "type": "desc"}
        ],
        "length": 1
    }

    # Invoke the request
    response = res_client.post("/incidents/query_paged?return_level=full",
                               payload=payload)

    # Return results
    if response["data"] != None:
        return response["data"][0]
    else:
        return None

# Returns the latest Healthcheck SOAR case
def get_soar_latest_healthcheck_case():
    '''
    returns custom_dict
    '''
    res_client = get_soar_simple_client()

    # Setup the request payload for search
    payload = {
        # "filters": [
        #     {
        #         "conditions": [
        #             {"field_name": "plan_status",
        #               "method": "equals",
        #               "value": "A"},
        #             {"field_name": "incident_type_ids",
        #               "method": "contains",
        #               "value": get_incident_type_id_by_name("Healthcheck")}
        #             ],
        #         "logic_type": "ALL"
        #     }
        # ],
        "filters": [
            {
                "conditions": [
                    {"field_name": "plan_status",
                      "method": "equals",
                      "value": "C"},
                    {"field_name": "properties.is_health_check",
                      "method": "equals",
                      "value": True}
                    ],
                "logic_type": "ALL"
            }
        ],
        "sorts": [
            {"field_name": "inc_last_modified_date", "type": "desc"}
        ],
        "length": 1       
    }

    # Invoke the request
    response = res_client.post("/incidents/query_paged?return_level=normal&field_handle=healthcheck_results_1&field_handle=healthcheck_results_2&field_handle=healthcheck_results_3&field_handle=healthcheck_results_4",
                               payload=payload)

    # Return results
    ret_dict = {}
   
    if response["data"] != None:
        incident = response["data"][0]

        ret_dict["id"] = incident.get("id")
        ret_dict["name"] = incident.get("name")
        ret_dict["create_date"] = incident.get("create_date")
        ret_dict["inc_last_modified_date"] = incident.get("inc_last_modified_date")

        inc_props = incident.get("properties") 
        ret_dict["healthcheck_results_1"] = json_to_dict(inc_props.get("healthcheck_results_1"))
        ret_dict["healthcheck_results_2"] = json_to_dict(inc_props.get("healthcheck_results_2"))
        ret_dict["healthcheck_results_3"] = json_to_dict(inc_props.get("healthcheck_results_3"))
        ret_dict["healthcheck_results_4"] = json_to_dict(inc_props.get("healthcheck_results_4"))

    return ret_dict

# Returns the closed Healthcheck cases older than
def get_soar_closed_healthcheck_case_ids():
    '''
    returns incident_id_list
    '''
    res_client = get_soar_simple_client()

    soar_config = config.get('soar-config')
    config_days = soar_config.get('healthcheck_clean_days_after')

    # if days and int(days) >= 0:
    #     days = days
    if config_days and int(config_days) > 0:
        days = config_days
    else:
        applog.info('"healthcheck_clean_days_after" is not configured. No old case will be removed')
        return []

    # print(days)
    elapsed_epoc_msec = days * 60*60*24*1000
    border_epoc_msec = time()*1000 - elapsed_epoc_msec

    # Setup the request payload for search
    payload = {
        "filters": [
            {
                "conditions": [
                    {"field_name": "plan_status",
                      "method": "equals",
                      "value": "C"},
                    {"field_name": "properties.is_health_check",
                      "method": "equals",
                      "value": True},                   
                    {"field_name": "inc_last_modified_date",
                      "method": "lt",
                      "value": border_epoc_msec}
                    ],
                "logic_type": "ALL"
            }
        ],
        "sorts": [
            {"field_name": "inc_last_modified_date", "type": "desc"}
        ]
    }

    # Invoke the request
    response = res_client.post("/incidents/query_paged?return_level=partial",
                               payload=payload)

    # Return results
    ret_list = []
    
    if response["data"] != None:
        for inc in response["data"]:
            ret_list.append(inc['id'])

    return ret_list

# Close Tasks of the case
def close_all_case_tasks(case_id):
    res_client = get_soar_simple_client()
    
    # Get the tasks in the case
    tasks = res_client.get("/incidents/{}/tasks".format(case_id))
    
    for task in tasks:
        task["status"] = "C"
        res_client.put("/tasks/{}".format(task.get("id")), payload=task)

# Create a case of Healthcheck
def create_healthcheck_case():
    '''
    returns incident_dict
    '''
    res_client = get_soar_simple_client()

    # Setup the request payload
    start_date_epoch = int(time() * 1000)
    json_dict = {
        "name" : "Health check",
        "description": "CP4S Health check for QRadar, DE, TII, and LDAP", 
        "severity_code": 'Low', 
        "discovered_date": start_date_epoch,
        "start_date" : start_date_epoch,
        "properties": {
            "is_health_check": True 
            }
        }

    # Invoke the request
    incident = res_client.post('/incidents', json_dict)
    return incident

# Close a case
def close_case(case_id):
    res_client = get_soar_simple_client()
    
    incident = res_client.get("/incidents/{}".format(case_id))
    incident["plan_status"] = "C"
    incident["resolution_id"] = "Resolved"
    incident["resolution_summary"] = "Healthcheck completed"
    incident = res_client.put('/incidents/{}'.format(case_id), payload=incident)

# Delete cases
def delete_cases(case_id_list):
    res_client = get_soar_simple_client()
    # Get the tasks in the case

    if len(case_id_list) > 0:    
        for case_id in case_id_list:
            status = res_client.delete("/incidents/{}".format(case_id))
            applog.info("Case id {} removal success: {}".format(case_id, status.get('success')))
            sleep(5)
    else:
        applog.info("No case to remove")

    return len(case_id_list)
