import requests


class YaUploader:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/"
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # Создание папки на ЯД
    def create_folder(self, path):
        url_create = self.BASE_URL  + "resources"
        response = requests.post(f'{url_create}?path={path}', headers=self.headers)
        response.raise_for_status()
        if response.status_code != 201:
            raise Exception(f"Failed to create folder {path}. Response: {response.json()}")

    # Загрузка фото в папку на ЯД
    def upload_photos_to_yd(self, path, url_file, name):
        url = self.BASE_URL + "upload"
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        response = requests.post(url, headers=self.headers, params=params)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception(f"Failed to upload file {name}. Response: {response.json()}")
