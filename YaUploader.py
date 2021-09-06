import requests
from tqdm import tqdm
from GetPhotoVK import GetPhotoVK


class YaUploader:
    def __init__(self, token):
        self.token = token

    def upload(self, photo_list):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        if bool(photo_list) is False:
            print('У пользователя нет доступных альбомов.')
            return
        else:
            # print(photo_list)
            url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
            headers = {
                'Authorization': self.token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            # Создание папки пользователя
            for album_name, photo in photo_list.items():
                # Настройки прогрессбара
                tqdm_params = {
                    'desc': f'Загружается альбом \'{album_name}\'',
                    'colour': 'green'
                }

                # Создание папки альбома
                requests.put(url, headers=headers, params={'path': f'{album_name}'})

                # Создание имени файлв
                for url_photo, val in tqdm(photo.items(), **tqdm_params):
                    like = str(val[0])
                    date = str(val[1])
                    photo_name = f'{like} likes, {date}.jpg'

                    # Загрузка файла на диск
                    params_post_photo = {
                        'path': f'{album_name}/{photo_name}',
                        'url': url_photo,
                        'overwrite': 'true'
                    }
                    requests.post(url + '/upload', headers=headers, params=params_post_photo)
            return


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    # Блок VK
    with open('VK_token.txt', encoding='utf-8') as f:
        VK_TOKEN = f.readline().strip()
    user_id = input('Введите ID или screen_name аккаунта VK: ')
    get_photo_vk = GetPhotoVK(VK_TOKEN, user_id)
    photo_vk = get_photo_vk.get_photo()

    # Блок Yandex
    # Получить путь к загружаемому файлу и токен от пользователя
    with open('YaD_token.txt', encoding='utf-8') as f:
        YaD_TOKEN = f.readline().strip()
    uploader = YaUploader(YaD_TOKEN)
    uploader.upload(photo_vk)
