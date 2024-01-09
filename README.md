# Топ авторов постов и топ авторов комментариев в subreddit'ах с [reddit.com](https://www.reddit.com/)

Скрипт умеет: 
- Спрашивать сабреддит, парсит с него все посты за последние 3 дня и выводит топ пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов

### Как установить

- Python3 должен быть установлен
- Poetry должен быть установлен
- Затем используйте `poetry` для установки зависимостей: 
    ```
    poetry install
    ```

- Рекомендуется использовать виртуальное окружение для изоляции проекта:
    ```
    poetry shell
    ```

- Создать в корне проекта файл **.env**, указать креды из зарегистрированного приложения reddit:
    ```
    USER_AGENT=subredits_top
    CLIENT_ID=dfdfdfdfdjfjdKzJt0eHNw
    SECRET=ddjdjfdfkjsdffjFJforgiQ
    ```


### Как пользоваться
## Cкрипт парсинга запускается через терминал:

```
   make run
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
    $ make run params='-h'
    python3 redditparser -h

    Usage: redditparser [OPTIONS]

    options:
       -n      TEXT     Name of subreddit [default: gaming]
       -a      INTEGER  Amount of top authors [default: 5]
       -l      INTEGER  Posts limit, 0 for None [default: 10]
       -d      INTEGER  Posts for n days [default: 3]
       -h               Show this message and exit.
    ```
        
    ``` 
    make run params='-n gaming -l 50'
    ```

- Скрипт записывает в лог ошибки при выполнении, файл **reddit_parse.log**
 

### Цель проекта

Код написан в образовательный целях на онлайн-курсе для python-разработчиков [learn.python.ru/advanced/](https://learn.python.ru/advanced/)
