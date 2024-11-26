# -*- coding: utf-8 -*-
import openpyxl
from pyrogram import Client
from datetime import datetime, timedelta

api_id = ''
api_hash = ''

# Задаем параметры непосредственно в коде
months_period = 1  # Количество месяцев для сохранения постов
channels = ["@proglibrary", "@frontendproglib", "@csharpproglib", "@goproglib", "@mobileproglib",
            "@hackproglib", "@dsproglib", "@javaproglib", "@cppproglib", "@devopsslib",
            "@testerlib", "@phpproglib", "@progbook"]  # Список каналов для проверки





def process_channel(client, channel):
    print(f"\nОбработка канала: {channel}")

    # Создаем новую книгу Excel для каждого канала
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Заполняем заголовки столбцов
    sheet['A1'] = 'Канал'
    sheet['B1'] = 'Ссылка на пост'
    sheet['C1'] = 'Количество просмотров'
    sheet['D1'] = 'Количество репостов'
    sheet['E1'] = 'Сумма реакций'
    sheet['F1'] = 'Дата публикации'

    # Счетчик строк и столбцов
    row = 2
    column = 7  # Столбцы с эмодзи начинаются с седьмого столбца

    # Словарь для хранения всех возможных реакций
    all_reactions = {}

    # Вычисляем дату, начиная с которой нужно сохранять посты
    start_date = datetime.now() - timedelta(days=30 * months_period)

    try:
        for message in client.get_chat_history(channel):
            print('ID поста: ', message.id)
            try:
                # Проверяем дату поста
                if message.date < start_date:
                    print(f"Найден пост старше {months_period} месяца, переходим к следующему каналу")
                    break

                # Проверяем количество просмотров
                views = message.views if message.views is not None else 0
                if views == 0:
                    print(f"Пропускаем пост {message.id} (нет просмотров)")
                    continue

                # Заполняем первый столбец названием канала
                sheet.cell(row=row, column=1, value=channel)

                # Заполняем второй столбец ссылкой на пост
                post_link = f"https://t.me/{channel[1:]}/{message.id}"
                sheet.cell(row=row, column=2).hyperlink = post_link
                sheet.cell(row=row, column=2).value = post_link
                sheet.cell(row=row, column=2).style = "Hyperlink"

                # Заполняем третий столбец количеством просмотров
                sheet.cell(row=row, column=3, value=views)

                # Заполняем четвертый столбец количеством репостов
                forwards = message.forwards if message.forwards is not None else 0
                sheet.cell(row=row, column=4, value=forwards)

                # Проверяем, есть ли реакции на сообщение
                total_reactions = 0
                if message.reactions:
                    for reaction in message.reactions.reactions:
                        emoji = reaction.emoji
                        count = reaction.count
                        total_reactions += count
                        if emoji not in all_reactions:
                            all_reactions[emoji] = column
                            sheet.cell(row=1, column=column, value=emoji)
                            column += 1
                        sheet.cell(row=row, column=all_reactions[emoji], value=count)

                # Записываем сумму реакций в пятый столбец
                sheet.cell(row=row, column=5, value=total_reactions)

                # Записываем дату публикации в шестой столбец
                date = message.date.strftime("%Y-%m-%d %H:%M:%S")
                sheet.cell(row=row, column=6, value=date)

                row += 1
            except Exception as e:
                print(f"Error getting message {message.id}: ", e)

        # Заполняем нулями отсутствующие реакции
        for r in range(2, row):
            for c in range(7, column):
                if sheet.cell(row=r, column=c).value is None:
                    sheet.cell(row=r, column=c, value=0)

        # Сохраняем книгу Excel
        xlsx_name = f"{channel[1:]}_telegram_stats_{months_period}months.xlsx"
        workbook.save(xlsx_name)
        print(f"Данные канала {channel} сохранены в файл: {xlsx_name}")

    except Exception as e:
        print(f"Error processing channel {channel}: ", e)


# Основной код
with Client("my_account", api_id, api_hash) as client:
    for channel in channels:
        process_channel(client, channel)

print("\nОбработка всех каналов завершена")
