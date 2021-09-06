from GetPhotoVK import GetPhotoVK
from YaUploader import YaUploader


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    user_id = input('Введите ID или screen_name аккаунта VK: ')
    number_photo = input('Введите количество получаемых из одного альбома фотографий (Enter = 5): ')

    # Блок VK
    with open('VK_token.txt', encoding='utf-8') as f:
        VK_TOKEN = f.readline().strip()
    get_photo_vk = GetPhotoVK(VK_TOKEN, user_id)
    photo_vk = get_photo_vk.get_photo(number_photo)
    print(photo_vk)

    # Блок Yandex
    # Получить путь к загружаемому файлу и токен от пользователя
    with open('YaD_token.txt', encoding='utf-8') as f:
        YaD_TOKEN = f.readline().strip()
    uploader = YaUploader(YaD_TOKEN)
    uploader.upload(photo_vk)
