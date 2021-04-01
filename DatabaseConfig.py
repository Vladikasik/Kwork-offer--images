import json


class Database:

    def __init__(self):
        self.db_name = 'users.json'

    def get_all_ids(self):
        data = self._get_data()

        exit_data = [i['id'] for i in data]

        return exit_data

    def create_user(self, user_id, name, start_balance):
        user = {"id": user_id,
                "name": name,
                "balance": start_balance}

        data = self._get_data()
        data.append(user)

        self._post_data(data)

    def get_balance(self, user_id):
        data = self._get_data()
        exit_data = [i['balance'] for i in data if i['id'] == user_id]
        return exit_data[0]

    def write_settings_exact(self, user_id, coordinates, metres):
        data = self._get_data()
        user = data.index([i for i in data if i['id'] == user_id][0])
        data[user]["settings"]['gps'] = {
                                            "coordinates": coordinates,
                                            "raszbros": metres
                                        }
        self._post_data(data)

    def _get_data(self):
        with open(self.db_name, 'r') as file:
            data = json.load(file)

        return data

    def _post_data(self, data):
        with open(self.db_name, 'w') as file:
            json.dump(data, file, indent=4)
