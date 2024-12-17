import pandas as pd
from pyrogram import Client
import json
import time
from pyrogram.errors import FloodWait
from datetime import datetime

# Настройки API
api_id = ''
api_hash = ''

# Инициализация клиента
app = Client("my_account", api_id=api_id, api_hash=api_hash)

def get_channel_data(app, channel_link, start_date, end_date):
    channel_name = channel_link.split('/')[-1]
    posts_data = {}
    subscribers_count = None

    # Получение информации о канале
    try:
        chat = app.get_chat(channel_name)
        subscribers_count = chat.members_count
    except Exception as e:
        print(f"Ошибка при получении информации о канале {channel_name}: {e}")

    # Преобразование Timestamp в объект datetime
    if isinstance(start_date, pd.Timestamp):
        start_date = start_date.to_pydatetime()
    if isinstance(end_date, pd.Timestamp):
        end_date = end_date.to_pydatetime()

    # Убедитесь, что end_date включает конец дня
    end_date = end_date.replace(hour=23, minute=59, second=59)

    # Получение сообщений в заданном диапазоне дат
    try:
        offset_id = 0
        while True:
            messages = list(app.get_chat_history(channel_name, offset_id=offset_id, limit=100))
            if not messages:
                break
            for message in messages:
                message_date = message.date.replace(tzinfo=None)  # Убираем информацию о временной зоне
                # Проверка, что дата сообщения находится в пределах заданного диапазона
                if message_date < start_date:
                    return posts_data, subscribers_count  # Завершаем обработку, если достигли сообщений до начальной даты
                if start_date <= message_date <= end_date and message.views is not None:
                    content = message.text or message.caption or ""
                    if content.strip():  # Проверяем, что контент не пустой
                        posts_data[message.id] = {
                            "views": message.views,
                            "date": message.date.isoformat(),
                            "content": content
                        }
            offset_id = messages[-1].id
            time.sleep(0.5)  # Задержка для избежания ограничений API
    except FloodWait as e:
        print(f"FloodWait: Ожидание {e.x} секунд")
        time.sleep(e.x)
    except Exception as e:
        print(f"Ошибка при получении сообщений из {channel_name}: {e}")

    return posts_data, subscribers_count



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

            start_date = row.iloc[2]  # Третий столбец
            end_date = row.iloc[3]  # Четвертый столбец

            channel_name = channel_link.split('/')[-1]
            print(f"Обработка канала: {channel_name}")

            posts_data, subscribers_count = get_channel_data(app, channel_link, start_date, end_date)
            channels_data[channel_name] = {
                "link": channel_link,
                "subscribers": subscribers_count,
                "posts": posts_data
            }

    # Сохранение данных в JSON файл
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(channels_data, f, ensure_ascii=False, indent=4)

    print(f"Данные сохранены в файл {output_json}")

# Пример вызова функции
#process_channels('table.xlsx', 'channels_data.json')
