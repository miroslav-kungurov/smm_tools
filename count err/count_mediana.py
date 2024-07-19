# -*- coding: utf-8 -*-
import json
import statistics

def process_json_file(file_path):
    # Чтение JSON из файла
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Добавление медианного значения просмотров
    for channel in data.values():
        if 'posts' in channel:
            views = [post['views'] for post in channel['posts'].values()]
            channel['median_views'] = statistics.median(views)

    # Запись обновленных данных обратно в тот же файл
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Данные обработаны и сохранены в {file_path}")

# Пример использования:

