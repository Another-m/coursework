import requests

def get_photo(METHOD_NAME, token_vk, id):
    url = 'https://api.vk.com/method/' + METHOD_NAME
    if id == "self profile": owner = 'owner'
    else: owner = 'owner_id'
    params = {owner: id, 'album_id': 'profile', 'access_token': token_vk, 'extended': 1, 'v': 5.131}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        photos = response.json()
        return photos
    else: print(response.status_code)

def download(token_yd, id):
    token_vk = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
    METHOD_NAME = "photos.get"
    photos_vk = get_photo(METHOD_NAME, token_vk, id)

    count = photos_vk['response']['count']
    likes_list = []
    log = []
    files = []
    print('Loading...')
    for num, content in enumerate(photos_vk['response']['items']):
        url_photo = content['sizes'][-1]['url']
        type = content['sizes'][-1]['type']
        likes = content['likes']['count']
        date = content['date']
        if likes not in likes_list: likes_list.append(likes)
        else: likes = str(likes) + "_" + str(date)
        log.append({'file_name': str(likes) + '.jpg', 'size': type})
        print(f'{round((num+1)/count*100, 2)} %')
        file_path = f"images_vk/{likes}.jpg"
        download = requests.get(url_photo)
        file = upload(token_yd, file_path, download)
        files.append(file[1])

    log_file = {'count_photo': count, 'photos': log}
    file_path = "images_vk/log_file.json"
    file = upload(token_yd, file_path, log_file)
    print('Сompleted!')
    print(f"Файлы {', '.join(files)} успешно загружены в директорию /{file[0]}/ на яндекс диск")
    return log_file

def upload(token_yd, file_path, data):
    # Файлы загружаются в папку images_vk/ на я.диск
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(url=url, headers=headers, params=params).json()
    link = response['href']
    filename = file_path.split("/")
    upload_file = requests.put(link, data)
    if upload_file.status_code == 201:
        return filename

if __name__ == "__main__":
    token_yd = 'AQAAAAABNrQ-...'
    # id = "self profile"
    id = "1"

    download(token_yd, id)
