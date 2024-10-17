import pytest
import os

@pytest.mark.parametrize('breed', ['doberman', 'bulldog', 'collie'])
def test_check_upload_dog(breed, dogs):
    folder_name = 'test_folder'
    token = os.getenv('TOKEN', 'AgAAAAAJtest_tokenxkUEdew')
    
    dogs.upload_dog_images(breed, folder_name)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {token}'
    }
    response = requests.get(f'{url_create}?path=/{folder_name}', headers=headers)
    response.raise_for_status()
    assert response.json()['type'] == "dir"
    assert response.json()['name'] == folder_name

    sub_breeds = dogs.get_sub_breeds(breed)
    items = response.json().get('_embedded', {}).get('items', [])
    if not sub_breeds:
        assert len(items) == 1
    else:
        assert len(items) == len(sub_breeds)

    for item in items:
        assert item['type'] == 'file'
        assert item['name'].startswith(breed)

    # Удаление данных после теста
    requests.delete(f'{url_create}?path=/{folder_name}', headers=headers)
