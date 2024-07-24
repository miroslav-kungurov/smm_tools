# -*- coding: utf-8 -*-
import pandas as pd
from pyrogram import Client
import json
import time
from pyrogram.errors import FloodWait

# Настройки API
api_id = ''
api_hash = ''

# Инициализация клиента
app = Client("my_account", api_id=api_id, api_hash=api_hash)


def get_channel_data(app, channel_link, start_id, end_id):
    channel_name = channel_link.split('/')[-1]
    posts_data = {}

    # Получение информации о канале
    try:
        chat = app.get_chat(channel_name)
        subscribers_count = chat.members_count
    except Exception as e:
        print(f"Ошибка при получении информации о канале {channel_name}: {e}")
        subscribers_count = None

    for message_id in range(start_id, end_id + 1):
        try:
            message = app.get_messages(channel_name, message_id)
            if message and not message.empty and message.views is not None:
                posts_data[message_id] = {
                    "views": message.views,
                    "date": message.date.isoformat(),
                    "content": message.text or message.caption or ""
                }
            time.sleep(0.5)  # Задержка для избежания ограничений API
        except FloodWait as e:
            print(f"FloodWait: Ожидание {e.x} секунд")
            time.sleep(e.x)
        except Exception as e:
            print(f"Ошибка при получении сообщения {message_id} из {channel_name}: {e}")

    return {
        "link": channel_link,
        "subscribers": subscribers_count,
        "posts": posts_data
    }



def process_channels(excel_file, output_json):
    # Чтение Excel файла
    df = pd.read_excel(excel_file, header=0)

    # Создание словаря для хранения данных каналов
    channels_data = {}

    # Обработка данных из Excel
    with app:
        for index, row in df.iterrows():
            if pd.isna(row.iloc[1]) or pd.isna(row.iloc[2]) or pd.isna(row.iloc[3]):
                break  # Останавливаемся, если строка пустая

            channel_link = row.iloc[1]  # Второй столбец

            # Пропускаем строки, если ссылка не начинается с https://t.me/
            if not str(channel_link).startswith("https://t.me/"):
                continue

            start_id = int(row.iloc[2])  # Третий столбец
            end_id = int(row.iloc[3])  # Четвертый столбец

            channel_name = channel_link.split('/')[-1]
            print(f"Обработка канала: {channel_name}")

            channel_data = get_channel_data(app, channel_link, start_id, end_id)
            channels_data[channel_name] = channel_data

    # Сохранение данных в JSON файл
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(channels_data, f, ensure_ascii=False, indent=4)

    print(f"Данные сохранены в файл {output_json}")
