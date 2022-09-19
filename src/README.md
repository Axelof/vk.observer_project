<div align="center">  
  <h3>version - 1.07</h3>  
</div>
<br/>



# TODO
- [x] слежка за упоминаниями, инвайтами, сокращёнными ссылками
- [x] слежка за добавлением / удалением пользователей 
- [ ] слежка за удалёнными && отредактированными сообщениями с сохранением истории
- [ ] слежка за определёнными типами аттачментов (photo, video, poll, etc)

# Config

#### `none` следует заменить на токены группы && пользователя.
```yaml
general:
    group:
        token:
            - none
    user:
        token:
            - none
```

<br/>

### Данная секция в [этой версии](https://github.com/Axelof/vk.observer_project/tree/master/src#version---107) не используется. 
#### Список ID`ов администраторов, перечислять через запятую.
```yaml
    admins:
        - 1
```

<br/>

#### Регулярные выражения. Изменение секции может прервать работоспособность.
```yaml
regexps:
    links_pattern: (https?:\/\/)?(www\.)?vk\.com\/(([a-zA-Z0-9._])*)\/?
    hyperlinks_pattern: (\[((club|id)[\d+]{1,9})\|([^]]*)])
    invite_links_pattern: ((http://|https://)?(vk\.me)\/join/([a-zA-Z0-9_./=]+))
    shortened_links_patterns: ((http://|https://)?(vk\.cc)\/([a-zA-Z0-9_./=]+))
```

<br/>

### Данная секция в [этой версии](https://github.com/Axelof/vk.observer_project/tree/master/src#version---107) не используется. 
#### Если установлен url, игнорируются параметры host, port, user, password.
```yaml
database:
    host: 127.0.0.1
    port: 3306
    user: admin
    password: admin

    database: none
    collection: none

    url: none
```

<br/>

#### Параметры принимают булево значение и отвечают за вкл/выкл триггеров.
#### т.е. `false - не работает` && `true - работает`
|    название    |             значение             |
|:--------------:|:--------------------------------:|
|   `mentions`   | упоминания пользователей / групп |
| `invite_links` |          инвайт ссылки           |
| `short_links`  |        сокращённые ссылки        |
|   `invites`    |           приглашения            |
```yaml
triggers:
    mentions:
        user: true
        group: false
    invite_links: true
    short_links: true
    invites: true
```

<br/>

#### Параметры принимают булево значение и отвечают за работу [мидлварей](https://github.com/Axelof/vk.observer_project/tree/master/src/middlewares) ([см. что такое мидлварь](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)).
```yaml
middlewares:
    ignore_group_messages: false
```

<br/>

#### Параметры принимают булево значение и отвечают за логирование.
| название          | значение                                                       |
|:------------------|:---------------------------------------------------------------|
| `log`             | логирование в файл                                             |
| `log_debug`       | включает логирование отладочной информации если `log` - `true` |
| `log_errors`      | логирование ошибок в файл                                      |
| `log_console`     | логирование в консоль                                          |
| `log_path`        | путь записи файлов с логами                                    |
| `log_errors_path` | путь записи файлов с логами ошибок                             |
```yaml
logging:
    log: true
    log_debug: false
    log_errors: false
    log_console: false
    log_path: logs/%Y-%m-%d_%H.log
    log_errors_path: logs/%Y-%m-%d_%H-error.log
```