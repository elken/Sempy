TOKEN = "RPncz4FMpxviSzesVeDo"
API_URL = 'https://semaphoreapp.com/api/v1/projects?auth_token=' + TOKEN

import json

import requests


class TeaTrayRequest:
    def __init__(self):
        self._info = {}

        self.json_data = self.get_json()
        self.data = json.loads(self.json_data)
        for server in self.data:
            values = {}
            for s in ("hash_id", "html_url", "owner", "name"):
                values[s] = (server[s])

            for branch in server['branches']:
                values['branch_name'] = branch['branch_name']

                if branch['result'] is "stopped":
                    values['result'] = "failed"
                else:
                    values['result'] = branch['result']

            key = str(server['owner'] + "/" + server['name'])
            self._info[key] = values

        # print(json.dumps(self.data, sort_keys=True, indent=4))

    @staticmethod
    def get_json():
        r = requests.get(API_URL)
        if r.status_code is 200:
            return json.dumps(r.json())
        else:
            print("Error getting JSON from " + API_URL + ". Check network settings. (" + str(r.status_code) + ")")

    @property
    def info(self):
        return self._info

