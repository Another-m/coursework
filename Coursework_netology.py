import requests
from pprint import pprint

def get_photo(method_name, token_vk, id):
    url = 'https://api.vk.com/method/' + method_name
    params = {'owner_id': id, 'album_id': 'profile', 'access_token': token_vk, 'extended': 1, 'v': 5.131}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        photos = response.json()
        return photos
    else: print(response.status_code)

def download(photos_vk, token_yd):
    likes_list = []
    log = []
    files = []
    count = photos_vk['response']['count']
    for num, content in enumerate(photos_vk['response']['items']):
        url_photo = content['sizes'][-1]['url']
        type_size = content['sizes'][-1]['type']
        likes = content['likes']['count']
        date = content['date']
        if likes not in likes_list:
            likes_list.append(likes)
        else:
            likes = str(likes) + "_" + str(date)
        log.append({'file_name': str(likes) + '.jpg', 'size': type_size})
        file_path = f"images_vk/{likes}.jpg"
        download = requests.get(url_photo)
        file = upload(token_yd, file_path, download)
        files.append(file[1])
        print(f'{round((num+1)/count*100, 2)} %')
    log_file = {'count_photo': count, 'photos': log}
    return [log_file, files]

def upload(token_yd, file_path, data):
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(url=url, headers=headers, params=params).json()
    link = response['href']
    filename = file_path.split("/")
    upload_file = requests.put(link, data)
    if upload_file.status_code == 201:
        return filename

def create_folder(path, token_yd):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
    dir = requests.put(f'{url}?path={path}', headers=headers)
    if dir.status_code != 200:
        requests.put(f'{url}?path={path}', headers=headers)

def main_func(id, token_vk, token_yd):
    method_name_vk = "photos.get"
    create_folder('images_vk', token_yd)
    photos_vk = get_photo(method_name_vk, token_vk, id)
    print('Loading...')
    data_list = download(photos_vk, token_yd)
    file_path = "images_vk/log_file.json"
    file = upload(token_yd, file_path, data_list[0])
    print('Сompleted!')
    print(f"Файлы {', '.join(data_list[1])} успешно загружены в директорию /{file[0]}/ на яндекс диск")
    return data_list[0]

def input_data():
    token_vk = input('Введите токен ВК: ')
    token_yd = input('Введите токен Яндекск диска: ')
    id = input('Введите ID пользователя ВК: ')
    log_file = main_func(id, token_vk, token_yd)
    ppr_log = input('\nРаспечатать лог файл? Ответ: \"да/y)\": ')
    if ppr_log == 'да' or ppr_log == '1' or ppr_log == 'y':
        pprint(log_file)
        input_data()
    else:
        print()
        input_data()

if __name__ == "__main__":
    input_data()
