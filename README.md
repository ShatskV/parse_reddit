# Топ авторов постов и топ авторов комментариев в subreddit'ах с [reddit.com](https://www.reddit.com/)

Скрипт умеет: 
- Спрашивать сабреддит, парситm с него все посты за последние 3 дня и выводит топ пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов

### Как установить

- Python3 должен быть установлен
- Затем используйте `pip` (или `pip3`, еслить есть конфликт с Python2) для установки зависимостей: 
    ```
    pip install -r requirements.txt
    ```

- Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.


### Как пользоваться
## Cкрипт парсинга запускается через терминал:

```
   python3 get_top_authors.py
```
- Топ авторов будет записан в файл **reddit_results.json**:
    ```
    {
    "top_authors": [
        {
            "AutoModerator": 1
        },
        {
            "SugarAddict98": 1
        }
    ],
    "top_commentators": [
        {
            "Ywaina": 11
        },
        {
            "gonegoat": 7
        },
        {
            "Elysium_Chronicle": 7
        },
        {
            "MyFilmmakingJourney": 6
        },
        {
            "JoeCartersLeap": 5
        }
    ]
    }
    ```

- Можно указать следующие аргументы в терминале:
    - Имя сабреддита
    - Количество авторов в топе
    - Лимит постов запроса у Реддита
    - Дни за которые брать посты с текущей даты

    ```
    $ python3 get_top_authors.py -h
    usage: get_top_authors.py [-h] [-n SUBREDDIT_NAME] [-a AUTHORS_AMOUNT] [-l LIMIT] [-d DAYS]

    Set parameters for subreddit parser:

    options:
    -h, --help            show this help message and exit
    -n SUBREDDIT_NAME, --subreddit_name SUBREDDIT_NAME
                            Name of subreddit (default: gaming)
    -a AUTHORS_AMOUNT, --authors_amount AUTHORS_AMOUNT
                            Amount of top authors (default: 5)
    -l LIMIT, --limit LIMIT
                            Posts limit, 0 for None (default: 10)
    -d DAYS, --days DAYS  Posts for n days (default: 3)
    ```
        
    ``` 
    python3 get_top_authors.py -n gaming -l 50
    ```

- Скрипт записывает в лог ошибки при выполнении, файл **reddit_parse.log**
 

### Цель проекта

Код написан в образовательный целях на онлайн-курсе для python-разработчиков [learn.python.ru/advanced/](https://learn.python.ru/advanced/).
