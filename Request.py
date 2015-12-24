import json

import requests


def get_json(token, route=""):
    """
    Return a JSON dump of Semaphore projects
    :param token: API token to access
    :param route: API path
    :return: Serialized JSON
    :rtype: str
    """
    r = requests.get('https://semaphoreapp.com/api/v1/projects' +
                     route + '?auth_token=' + token)
    if r.status_code is 200:
        return json.dumps(r.json())


def json_to_dict(data):
    """
    Convert serialized JSON to the custom structure I devised to handle everything. It's essentially a dictionary of
    lists of all the servers and their statuses. As functionality grows, this will become more functional.

    :param data: Data to parse
    :return: Parsed dictionary
    :rtype: dict
    """
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
