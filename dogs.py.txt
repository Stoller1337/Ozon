import requests

class Dogs:
    BASE_URL = "https://dog.ceo/api/breed/"
    def __init__(self, yandex_client):
	self.yandex_client = yandex_client

    # Получение дочерних пород
    def get_sub_breeds(self, breed):
        try:
            res = requests.get(self.BASE_URL  + f"{breed}/list")
            res.raise_for_status()
            return res.json().get('message', [])
       except requests.RequestException as e:
            raise Exception(f"Failed to get sub-breeds for breed {breed}. Error: {e}")


    # Получение всех url'ов пород и подпород
    def get_breed_urls(self, breed, sub_breeds):
        url_images = []
        try:
            if sub_breeds:
                for sub_breed in sub_breeds:
                    res = requests.get(self.BASE_URL + f"{breed}/{sub_breed}/images/random")
                    res.raise_for_status()
                    sub_breed_urls = res.json().get('message')
                    url_images.append(sub_breed_urls)
            else:
                res = requests.get(self.BASE_URL + f"{breed}/images/random")
                res.raise_for_status()
                url_images.append(res.json().get('message'))
        except requests.RequestException as e:
            raise Exception(f"Failed to get images for breed {breed}. Error: {e}")
        return url_images

    # Скачиваение и загрузка фото пород на ЯД 
    def upload_dog_images(self, breed, folder_name):
        sub_breeds = self.get_sub_breeds(breed)
        urls = self.get_breed_urls(breed, sub_breeds)
        self.yandex_client.create_folder(folder_name)
        for url in urls:
            part_name = url.split('/')
            name = '_'.join([part_name[-2], part_name[-1]])
            self.yandex_client.upload_photos_to_yd(folder_name, url, name)
