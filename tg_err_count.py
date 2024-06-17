import pandas as pd
from pyrogram import Client

# Замените эти значения своими
api_id = ''
api_hash = ''

app = Client("my_account", api_id=api_id, api_hash=api_hash)

def get_views_and_date(app, channel, message_id):
    views = None
    post_date = None
    try:
        message = app.get_messages(channel, message_id)
        views = message.views
        post_date = message.date
    except Exception as e:
        print(f"Ошибка при получении данных для {channel}/{message_id}: {e}")
    return views, post_date

def get_subscribers(app, channel):
    subscribers = None
    try:
        chat = app.get_chat(channel)
        subscribers = chat.members_count
    except Exception as e:
        subscribers = f"Ошибка: {str(e)}"
    return subscribers

# Открываем файл table.xlsx и читаем его содержимое
df = pd.read_excel('table.xlsx')

# Начинаем со второй строки (индекс 1), берем ссылки и значения из второго, третьего и четвертого столбцов
links = df.iloc[0:, 1]  # Второй столбец
start_values = df.iloc[0:, 2]  # Третий столбец
end_values = df.iloc[0:, 3]  # Четвертый столбец

# Создаем список для хранения результатов
results = []

# Словарь для хранения уникальных постов по каналам
channel_data = {}

# Запускаем клиент Pyrogram
with app:
    for link, start, end in zip(links, start_values, end_values):
        if pd.notna(start) and pd.notna(end):  # Проверяем, что значения не пустые
            if 't.me' not in link:
                continue  # Пропускаем URL, которые не содержат t.me

            channel_name = link.split('/')[-1]
            if channel_name not in channel_data:
                channel_data[channel_name] = {}

            for value in range(int(start), int(end) + 1):
                views, post_date = get_views_and_date(app, channel_name, value)
                if views is None or post_date is None:
                    continue  # Пропускаем сообщение, если просмотры или дата равны None

                # Проверка на дублирующиеся даты публикации
                if post_date in channel_data[channel_name]:
                    continue  # Пропускаем дублирующую дату

                channel_data[channel_name][post_date] = {'views': views, 'id': value}
    print(channel_data)

    # Обработка данных для записи в DataFrame
    for channel_name, posts in channel_data.items():
        total_views = sum(post['views'] for post in posts.values() if post['views'] is not None)
        post_count = len(posts)

        # Обновление DataFrame
        row_index = df[df.iloc[:, 1].str.contains(channel_name)].index
        for idx in row_index:
            df.at[idx, 'Кол-во просмотров всего'] = total_views
            df.at[idx, 'Кол-во постов'] = post_count

    # Извлекаем количество подписчиков для каждого канала
    for channel_name in channel_data.keys():
        subscribers = get_subscribers(app, channel_name)
        row_index = df[df.iloc[:, 1].str.contains(channel_name)].index
        for idx in row_index:
            df.at[idx, 'Подписчики'] = subscribers

    # Рассчитываем вовлеченность и обновляем DataFrame
    for idx in df.index:
        if pd.notna(df.at[idx, 'Кол-во просмотров всего']) and pd.notna(df.at[idx, 'Кол-во постов']) and pd.notna(df.at[idx, 'Подписчики']):
            total_views = df.at[idx, 'Кол-во просмотров всего']
            post_count = df.at[idx, 'Кол-во постов']
            subscribers = df.at[idx, 'Подписчики']
            average_reach = total_views / post_count
            engagement_rate = average_reach / subscribers
            df.at[idx, 'Вовлеченность'] = engagement_rate

# Сохраняем обновленный DataFrame в новый файл
df.to_excel('updated_table.xlsx', index=False)
