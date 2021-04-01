import json


class Database:

    def __init__(self):
        self.db_name = 'users.json'

    def get_all_ids(self):

        data = self._get_data()

        exit_data = [i['id'] for i in data]

        return exit_data

    def create_user(self, id, name, start_balance):

        user = {"id": id,
                "name": name,
                "balance": start_balance}

        data = self._get_data()
        data.append(user)

        self._post_data(data)

    def get_balance(self, id):

        data = self._get_data()
        exit_data = [i['balance'] for i in data if i['id'] == id]
        return exit_data[0]

    def write_settings_exact(self, id, coordinates):

        data = self._get_data()
        user = data.index([i for i in data if i['id'] == id][0])
        data[user]["settings"] = {"type": "exact",
                                  "data": "coordinates"}

    def _get_data(self):

        with open(self.db_name, 'r') as file:
            data = json.load(file)

        return data

    def _post_data(self, data):
        with open(self.db_name, 'w') as file:
            json.dump(data, file, indent=4)
