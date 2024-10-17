import random
import pytest
import requests
import os


class YaUploader:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # Создание папки на ЯД
    def create_folder(self, path):
        url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.put(f'{url_create}?path={path}', headers=self.headers)
        response.raise_for_status()
        if response.status_code != 201:
            raise Exception(f"Failed to create folder {path}. Response: {response.json()}")

    # Загрузка фото в папку на ЯД
    def upload_photos_to_yd(self, path, url_file, name):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        response = requests.post(url, headers=self.headers, params=params)
        response.raise_for_status()
        if response.status_code != 202:
            raise Exception(f"Failed to upload file {name}. Response: {response.json()}")


# Получение дочерних пород
def get_sub_breeds(breed):
    try:
        res = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
        res.raise_for_status()
        return res.json().get('message', [])
    except requests.RequestException as e:
        raise Exception(f"Failed to get sub-breeds for breed {breed}. Error: {e}")


# Получение всех url'ов пород и подпород
def get_breed_urls(breed, sub_breeds):
    url_images = []
    try:
        if sub_breeds:
            for sub_breed in sub_breeds:
                res = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random")
                res.raise_for_status()
                sub_breed_urls = res.json().get('message')
                url_images.append(sub_breed_urls)
        else:
            res = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
            res.raise_for_status()
            url_images.append(res.json().get('message'))
    except requests.RequestException as e:
        raise Exception(f"Failed to get images for breed {breed}. Error: {e}")
    return url_images

# Скачиваение и загрузка фото пород на ЯД 
def upload_dog_images(breed, folder_name, token):
    sub_breeds = get_sub_breeds(breed)
    urls = get_urls(breed, sub_breeds)
    yandex_client = YaUploader(token)
    yandex_client.create_folder(folder_name)
    for url in urls:
        part_name = url.split('/')
        name = '_'.join([part_name[-2], part_name[-1]])
        yandex_client.upload_photos_to_yd(folder_name, url, name)
