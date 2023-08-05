#!/usr/bin/env python

from opsgenielib import OpsGenie
import json
from opsgenielib.opsgenielibexceptions import InvalidApiKey


try:
    opsgenie = OpsGenie('3244807b-413f-4228-99f7-5dc2252d69d6')
except InvalidApiKey:
    raise SystemExit('I am sorry to say that the provided api key is invalid.')

## list maintenance policy

response = opsgenie.get_team_logs_by_name("team5")
print(response)
response = opsgenie.get_team_logs_by_id("027af724-a97d-4c1a-989b-f20e52ff2a9e")
print(response)
# response = opsgenie.

# response = opsgenie.list_alerts("team5", 50)
# print(json.dumps(response, indent=4, sort_keys=True))

# Del_Maintenace_Result = opsgenie.del_maintenance_policy('b8faa6e8-ee8b-4914-be66-8a23f3673e4f')
# print(json.dumps(Del_Maintenace_Result, indent=4, sort_keys=True))
# set_maintenance_policy_schedule(self, team_id, start_date, end_date, rules_type,  # pylint: disable=too-many-arguments
#                                         rules_id, description, state="enabled"):

# set_maintenance_policy_hours(self, team_id, hours, rules_id, rules_type, description, state="enabled"):

# cancel_maintenance_policy(self, maintenance_id):

# get_alerts(self, id_):

# ack_alerts(self, id_):

# list_alerts(self, team_name, limit):

# query_alerts(self, query):


@policy_alerts.command(name='create')
@click.option('--state', type=click.Choice(['match-any-condition', 'match-all-conditions']), help='Choose if all condition should be met or atleast one.')
# @click.argument('--condition_one', nargs=4, help='field/operation/expectedValue or field/key/not(optional)/operation/expectedValue. \
#     Example: Message, contains, dynamodb. or Example2: extra-properties, host, not, regex, ^sbpojira.*$')
@click.option('--name', help='Specify the name of the alert policies.')
@click.pass_context
def policy_alerts_create(context, state, name):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/policies?teamId={context.obj.get('teamid')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        }
    body = {
        "type":"alert",
        "description":f"{name}",
        "enabled":"true",
        "filter":{
            "type":f"{state}",
            "conditions": [
                {
                    "field": "extra-properties",
                    "key": "host",
                    "not": "true",
                    "operation": "starts-with",
                    "expectedValue": "expected3"
                }
            ]
        },
        "name":f"{name}",
        "message":"{{message}}",
        "tags":["filtered"],
        "alertDescription":"{{description}}"
    }
    response = requests.post(url, headers=headers, json=body)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))