# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def filter_posts(posts):
    sorted_posts = sorted(posts.items(), key=lambda x: x[1]['date'])
    filtered_posts = {}
    i = 0

    while i < len(sorted_posts):
        current_post = sorted_posts[i]
        current_date = datetime.fromisoformat(current_post[1]['date'])
        min_views_post = current_post

        j = i + 1
        while j < len(sorted_posts):
            next_post = sorted_posts[j]
            next_date = datetime.fromisoformat(next_post[1]['date'])
            if next_date - current_date <= timedelta(seconds=10):
                if next_post[1]['views'] < min_views_post[1]['views']:
                    min_views_post = next_post
                j += 1
            else:
                break

        filtered_posts[min_views_post[0]] = min_views_post[1]
        i = j

    return filtered_posts


def clean(json_file):
    data = load_json(json_file)

    for channel, channel_data in data.items():
        if 'posts' in channel_data:
            posts = channel_data['posts']
            filtered_posts = filter_posts(posts)
            data[channel]['posts'] = filtered_posts

    save_json(data, 'filtered_channels_data.json')
    print("Фильтрация завершена. Данные сохранены в файл filtered_channels_data.json")


