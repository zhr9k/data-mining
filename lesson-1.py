from pathlib import Path
import requests

from GefMar.les1 import Parse5Ka
# импортнул ваш класс, чтобы дергать парсер и сейвер
# урлы и сразу словарь с категориями товаров
url = "https://5ka.ru/api/v2/special_offers/"
cats_url = 'https://5ka.ru/api/v2/categories/'
cats_json = requests.get(cats_url).json()

# путь для сохранения
save_path = Path(__file__).parent.joinpath('prods_by_cats')
if not save_path.exists():
    save_path.mkdir()
# создаем объект класса и делаем словарь с параметрами, т.к. явно надо будет указывать категорию товаров
parser = Parse5Ka(url, save_path)
params = {
    "categories": "null",
    "records_per_page": 50,
}


for i in cats_json:
    cat_id = i['parent_group_code']
    params['categories'] = cat_id
    response = requests.get(url, params=params).json()
# значит берем первую страницу акций по конкретной категории, суем сразу все ее товары в список,
    prods = response['results']
# а потом ссылку на следующую страницу отдаем парсеру, который остальные страницы (если они есть) парсит
# и возвращаемые продукты докладываем в список
    for j in parser._parse(response['next']):
        prods.append(j)
    i['products'] = prods
# ну, и сохраняем все
    item_path = save_path.joinpath(f'cat_{cat_id}.json')
    parser._save(i, item_path)


