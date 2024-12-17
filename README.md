# Устанавливаем библиотеки

pip install https://github.com/KurimuzonAkuma/pyrogram/archive/v2.1.33.zip --force-reinstall  
pip install pandas openpyxl  
pip install -U tgcrypto  

# Создаем приложение в ТГ

Создаем приложение по адресу [https://my.telegram.org/apps](https://my.telegram.org/apps) и вставляем в скрипт значения  

- api_id = ''"
    
- api_hash = ''"
    

  

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXfLklX5n4p93z6wuZ_5lxuxlmRRQWWpwVjwlKZwH-jbR7xp0N1XrjRAIVG62RwaeoY2Fgk0cCfOxbkk0rzRPwxuMacRfDYTzvH2NQx_4d0bmatSOa8eChGTQ_Fg5AUfUEjShx92ktG6nxPzNZb2uw-mVcSg?key=2GhdH-Aip7wH5rSx552uZQ)

# Запускаем скрипт tg_err_count.py из папки count err by id

Создаем таблицу table.xlsx, заполняем 2, 3, 4 колонки и сохраняем таблицу  
![](https://lh7-us.googleusercontent.com/docsz/AD_4nXe6k5YWzOySI4N2rxuwgqrinXAi5YIZS2GhFWqvc-k8Oc9XMz7KJVXQM1EEz4tLvp3IhrP2GJXO-931bZeGF38IfSBXwEtci7WUIlugZkfu-jEUAS5hgiMtocIorvYEJvo2gljjvDeFMz65Vl8u3GiP22-n?key=2GhdH-Aip7wH5rSx552uZQ)

Копируем таблицу table.xlsx в папку со скриптом.

  

Запускаем скрипт:

1. Вводим номер телефона
    
2. Вводим код
    
3. Вводим пароль (опционально)
      

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXeZ8HKE_NepvXOPSvCDCrJYc_ulxjjCHhPsLL60UOCaH38yY8DAJprsKdFpREST7takhoJoQV0osz1JlHl2v9sniXuv3lu0DomgDoNteQeCvg4n2MAtv5R_zLrIRMfbTi_0mJG2-CIK7NL2PaRYgbE7j1xh?key=2GhdH-Aip7wH5rSx552uZQ)

Дубликаты постов не считаются (когда больше 1-й картинки в посте, пост повторяется с разными ID  и одинаковой датой публикации), удаленные посты (их ID) пропускаются.


# Результат

Результат сохраняется в файл metrics.xlsx

![image](https://github.com/user-attachments/assets/205c4d16-3c00-4bf3-ae9e-92c75f46c9a8)


Второй скрипт count by date фильтрует по дате
![image](https://github.com/user-attachments/assets/4a98bcba-cf3f-47e4-b2d0-cb7e87d496be)


# Запускаем скрипт tg_reactions_count.py
Скрипт считает реакции на посты в одном тг-канале.

Вводим значения:
- first_post_id = 1
- last_post_id = 2884
- channel = "@itmemlib"

![image](https://github.com/miroslav-kungurov/smm_tools/assets/56649199/83601135-7889-41dc-85c3-8b38570246ca)

Запускаем скрипт, результат сохраняется в файл telegram_reactions.xlsx

![image](https://github.com/user-attachments/assets/a459cbc2-b6e8-4bd6-bac0-8f282f46ea2a)






