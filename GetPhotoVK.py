import json
import requests
from pprint import pprint
from datetime import datetime


class GetPhotoVK:
    def __init__(self, token, vk_id):
        self.token = token
        self.user_id = vk_id
        self.url = 'https://api.vk.com/method/'

        # Получение user_ids в случае передачи screen_name
        method = 'users.get?'
        params = {
            'user_ids': self.user_id,
            'access_token': self.token,
            'v': '5.131'
        }
        user_info = requests.get(self.url + method, params=params)
        self.user_id = user_info.json()['response'][0]['id']
        user_first_name = user_info.json()['response'][0]['first_name']
        user_last_name = user_info.json()['response'][0]['last_name']
        self.user_name = f'{user_first_name} {user_last_name}'

        # Общие параметры запросов
        self.common_parameters = {
            'owner_id': self.user_id,
            'access_token': self.token,
            'v': 5.131
        }

    def get_albums(self):
        '''Метод получает названия и id альбомов'''
        method = '/photos.getAlbums?'
        params_get_albums = {
            'need_system': '1',
            'album_id': ['saved', 'profile', 'wall']
        }
        albums = requests.get(self.url + method, params={**params_get_albums, **self.common_parameters})

        # Формирование библиотеки альбомов
        albums_list = {}
        if 'response' in albums.json():
            # Перебор альбомов
            for album in albums.json()['response']['items']:
                # Проверка наличия фотографий в альбоме
                if album['size'] > 0:
                    album_title = album['title']
                    album_id = album['id']
                    albums_list[album_title] = album_id
        # Если библиотека не пустая
        if bool(albums_list) is True:
            pprint(f'У {self.user_name} есть следующие альбомы:')
            print(list(albums_list.keys()))
            return albums_list
        # Если библиотека пустая
        else:
            return

    def get_photo(self, count_photo=5):
        '''Метод получает id и количество лайков каждой фотографии'''

        # Получение библиотеки альбомов
        albums_list = self.get_albums()
        method = 'photos.get?'
        params_photos_get = {
            'extended': 1,
            'photo_sizes': 1,
            'count': count_photo
        }
        # Информация по фотографиям в json-файле в формате {'название': 'индекс размера'}
        photo_list_file = 'photo_list.json'
        r = []
        count_iter = 1

        # Если библиотека альбомов не пустая
        if bool(albums_list) is False:
            return

        else:
            # Получение списка желаемых альбомов, пустой список == все альбомы
            input_albums_list = input('Введите, через запятую, нужные альбомы (Enter = все): ')

            # Проверка списка желаемых альбомов:
            ## берутся все альбомы;
            if bool(input_albums_list) is False:
                albums_title = list(albums_list.keys())
            ## берутся введенные альбомы;
            else:
                albums_title = [vol.strip() for vol in input_albums_list.split(',')]

            # Формирование библиотеки альбомов и фотографий:
            photo_and_album_list = {}
            ## перебор по названию альбомов
            for album_title in albums_title:
                photos = requests.get(self.url + method,
                                      params={'album_id': albums_list[album_title], **params_photos_get,
                                              **self.common_parameters})
                ## формирование библиотеки фотографий
                photos_lib = {}
                ## проверка на доступность фотографий
                if 'response' in photos.json():
                    ### перебор фотографий в альбоме
                    for photo in photos.json()['response']['items']:
                        photo_likes = photo['likes']['count']
                        photo_data = str(datetime.fromtimestamp(photo['date'])).replace(':', '_')

                        # URL самой большой копии
                        photo_size = photo['sizes']
                        s = [size['height'] + size['width'] for size in photo_size]
                        max_s = s.index(max(s))
                        max_photo_size = photo['sizes'][max_s]
                        max_photo_size_url = max_photo_size['url']

                        # Индекс самой большой копии
                        size_index = photo_size[max_s]['type']

                        # добавление фотографии в библиотеку фотографий
                        photos_lib.update({max_photo_size_url: [photo_likes, photo_data]})

                        # Список с названиями файлов
                        r.append({"file_name": f'{photo_likes} likes, {photo_data}.jpg',
                                  "size": size_index})
                        count_iter += 1

                # обновление библиотеки альбомов и фотографий
                photo_and_album_list[album_title] = photos_lib

            # Создание файла с результатами
            r.insert(0, f'Всего фотографий: {count_iter - 1}')
            with open(photo_list_file, 'w') as file:
                json.dump(r, file, ensure_ascii=False, indent=2)

            return photo_and_album_list


if __name__ == '__main__':
    with open('VK_token.txt', encoding='utf-8') as f:
        VK_TOKEN = f.readline().strip()
    user_id = '31977902'
    get_photo_vk = GetPhotoVK(VK_TOKEN, user_id)
    pprint(get_photo_vk.get_photo())
