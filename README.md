# Test Comments

Тестовое задание: система комментариев блога на Django.

### Документация

Swagger: `http://<your_domain>/swagger/`

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

Приложение будет доступно по адресу: `http://localhost:8888/`. Чтобы остановить все контейнеры и удалить артефакты:

```bash
docker-compose down --remove-orphans
```
