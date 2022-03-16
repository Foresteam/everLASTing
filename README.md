# everLASTing games for EnergyHack2022
## Описание
Бот для дискорда, для прохождения тестов. Сами тесты составляются на языке XML, с довольно гибкими возможностями.
Сами же тесты проходить можно в ЛС и на сервере. Есть отображение результатов, их экспорт в .xlsx.
## Установка
*Инструкция работает для: OS Linux x86_64, 5.16.11-2-MANJARO*

### Пакеты:
* Python 3.10
* Git
* mongodb
* mongodb-compass (для инициализации БД, да и вообще работы с ней. Полезная вещь)

Нужно запустить сервер mongo и создать базу данных "everLASTing".

### Установка
```sh
git clone https://github.com/Foresteam/everLASTing.git

cd everLASTing

pip install -r install.txt

echo DISCORD_BOT_TOKEN > token
```
## Запуск
(Тоже из корня репозитория)
```sh
python src/XD.py
```
![](pylogo.png)
## Plan-kapkan
1.
    * Перевести [парсер команд](https://github.com/Foresteam/cmd-argparse) на Phyton.
      ### Status: ✓
    * Написать каркас бота. Он должен уметь отличать групповые диалоги(сервера) от ЛС, отправлять вложения. Для группы будет 1 тест на канал, а в ЛС - персональный. [нужен объект Message]
      ### Status: ✓
2.
    * Реализовать интерфейс диалога, API самого теста.
      ### Status: ✓ (но без кнопок)
    * Импорт теста, XML описание.
      ### Status: ✓
    * Придумать и сделать систему баллов, уровней.
      ### Status: ✓
    * Продумать админ панель. (админские команды, кому они доступны)
      ### Status: × (в виду отсутствия секретной информации, все открыто для всех)
3.
    * Заполнить бота вопросами и ответами.
      ### Status: ✓×
    * Научить робота показывать рейтинг (всех игроков in total, игроков на конкретных уровнях). Быть может сделать еще какие-то фильтры (**работа с БД**). Вероятно, будет экспорт таблиц в CSV. Можно сделать экспорт в виде скриншота части таблицы, если останется время.
      ### Status: ✓
