# -*- coding: utf-8 -*-
import pandas as pd
import json
from get_data_from_tg import process_channels
from clean_json import clean
from count_metrics import add_metrics_to_json

def add_metrics_to_excel(input_excel, input_json, output_excel):
    # Чтение данных из JSON файла
    with open(input_json, 'r', encoding='utf-8') as f:
        channels_data = json.load(f)

    # Чтение данных из Excel файла
    df = pd.read_excel(input_excel, header=0)

    # Добавление новых столбцов
    df['post_count'] = 0
    df['subscribers'] = 0
    df['total_views'] = 0
    df['average_reach'] = 0.0
    df['engagement_rate'] = 0.0

    # Обновление данных в DataFrame
    for index, row in df.iterrows():
        channel_link = row.iloc[1]
        channel_name = channel_link.split('/')[-1]

        if channel_name in channels_data:
            channel_data = channels_data[channel_name]
            df.at[index, 'post_count'] = channel_data.get('post_count', 0)
            df.at[index, 'subscribers'] = channel_data.get('subscribers', 0)
            df.at[index, 'total_views'] = channel_data.get('total_views', 0)
            df.at[index, 'average_reach'] = channel_data.get('average_reach', 0.0)
            df.at[index, 'engagement_rate'] = channel_data.get('engagement_rate', 0.0)

    # Переименование столбцов
    df.columns = ['Column1', 'Channel Link', 'Start ID', 'End ID', 'Post Count', 'Subscribers', 'Total Views', 'Average Reach', 'Engagement Rate']

    # Сохранение обновленных данных в новый Excel файл
    df.to_excel(output_excel, index=False)

    print(f"Данные сохранены в файл {output_excel}")

if __name__ == "__main__":
    process_channels('table.xlsx', 'channels_data.json')
    clean(json_file='channels_data.json')
    add_metrics_to_json('filtered_channels_data.json', 'channels_data_with_metrics.json')
    add_metrics_to_excel('table.xlsx', 'channels_data_with_metrics.json', 'metrics.xlsx')
