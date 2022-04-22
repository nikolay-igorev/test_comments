# Test Comments

Тестовое задание: система комментариев блога на Django.

Heroku: https://test-comments1.herokuapp.com/

### Установка

Сначала установите Postgres и запустите его.

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```. Измените username, password и dbname для
DATABASE_URl на те, которые используются в вашем локальном Postgres.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://username:password@localhost:5432/dbname
```

Установите зависимости проекта с помощью pipenv:

```bash
pipenv install
```

После этого активируйте виртуальную среду, примените миграции и запустите сервер:

```bash
pipenv shell
python manage.py migrate
python manage.py runserver
```

### Docker

Чтобы запустить приложение с помощью Docker, выполните команду:

```bash
docker-compose up
```

Если возникла проблема с доступом к файлу docker-entrypoint.sh:

```bash
chmod +x docker-entrypoint.sh
docker-compose build --no-cache
docker-compose up
```

Приложение будет доступно по адресу: `http:/localhost:8888`. Чтобы остановить все контейнеры и удалить артефакты:

```bash
docker-compose down --remove-orphans
```

### Endpoints


| URL                                      | Description                                          |
| ---------------------------------------- | -----------------------------------------------------|
| `/comments`                              | Все комментарии в виде дерева.                       |
| `/post/<int:pk>/comments`                | Список комментариев к посту до 3 уровня вложенности. |
| `/post/<int:pk>/comments/all`            | Полный список комментариев к посту.                  |
| `/comments/<int:pk>`                     | Список ответов к комментарию до 3 уровня вложенности.|
| `/comments/<int:pk>/all`                 | Список ответов к комментарию.                        |
| `/post/<int:pk>/comments/create`         | Создание комментария к посту.                        |
| `/comments/<int:pk>/create`              | Создание ответа на комментарий.                      |
