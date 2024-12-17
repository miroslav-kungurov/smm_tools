# -*- coding: utf-8 -*-
import json

def add_metrics_to_json(input_json, output_json):
    # Чтение данных из входного JSON файла
    with open(input_json, 'r', encoding='utf-8') as f:
        channels_data = json.load(f)

    # Добавление новых метрик для каждого канала
    for channel_name, channel_data in channels_data.items():
        posts = channel_data.get('posts', {})
        post_count = len(posts)
        total_views = sum(post['views'] for post in posts.values())
        average_reach = total_views / post_count if post_count > 0 else 0
        subscribers_count = channel_data.get('subscribers', 0)
        engagement_rate = (average_reach / subscribers_count) if subscribers_count > 0 else 0

        channels_data[channel_name]['post_count'] = post_count
        channels_data[channel_name]['total_views'] = total_views
        channels_data[channel_name]['average_reach'] = average_reach
        channels_data[channel_name]['engagement_rate'] = engagement_rate

    # Сохранение обновленных данных в выходной JSON файл
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(channels_data, f, ensure_ascii=False, indent=4)

    print(f"Данные сохранены в файл {output_json}")



