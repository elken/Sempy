import json

import requests


def get_json(token):
    r = requests.get('https://semaphoreapp.com/api/v1/projects?auth_token=' + token)
    if r.status_code is 200:
        return json.dumps(r.json())


def json_to_dict(data):
    info = {}
    for server in data:
        values = {}
        for s in ("hash_id", "html_url", "owner", "name"):
            values[s] = (server[s])

        for branch in server['branches']:
            values['branch_name'] = branch['branch_name']

            try:
                if branch['result'] is "stopped":
                    values['result'] = "failed"
                else:
                    values['result'] = branch['result']
            except KeyError:
                values['result'] = "not built"

        key = str(server['owner'] + "/" + server['name'])
        info[key] = values

    return info
