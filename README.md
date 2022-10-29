# Test Comments

Система вложенных комментариев блога на Django Rest Framework.

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
DATABASE_URL_DOCKER=postgres://postgres:postgres@db:5432/postgres
```

Установите зависимости проекта с помощью pip и активируйте виртуальную среду:

```bash
python -m venv .venv 
```
```bash
.venv\Scripts\Activate.ps1 
```
```bash
pip install -r requirements.txt
```

После этого примените миграции и запустите сервер:

```bash
python manage.py migrate
```
```bash
python manage.py runserver  
```

### Docker

Чтобы запустить приложение с помощью Docker, выполните команду:

```bash
docker-compose up -d --build
```

Запустите миграции:

```bash
docker-compose exec web python manage.py migrate
```

Приложение будет доступно по адресу: `http://localhost:8000/`. Чтобы остановить все контейнеры:

```bash
docker-compose down
```
