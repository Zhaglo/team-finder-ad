# TeamFinder

TeamFinder — веб-приложение для поиска участников в pet-проекты. Пользователи могут регистрироваться, создавать проекты, присоединяться к чужим проектам, добавлять проекты в избранное и просматривать профили участников.

Проект выполнен в рамках дипломной работы Яндекс Практикума по backend-разработке на Python.

## Реализованный вариант

**Вариант 1: «Избранное» и фильтрация пользователей.**

Реализовано:

- добавление и удаление проектов из избранного;
- страница избранных проектов;
- фильтрация пользователей по критериям:
  - авторы избранных проектов;
  - авторы проектов, в которых я участвую;
  - пользователи, которым нравятся мои проекты;
  - участники моих проектов.

## Технологии

- Python
- Django 5.2
- PostgreSQL
- Docker Compose
- Pillow
- HTML/CSS/JavaScript

## Функциональность

- регистрация, вход и выход;
- редактирование профиля;
- смена пароля;
- автоматическая генерация аватарки пользователя;
- создание, редактирование и завершение проектов;
- участие в чужих проектах;
- избранные проекты;
- список пользователей и публичные профили;
- админ-панель;
- команда для наполнения тестовыми данными.

## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone <ссылка-на-репозиторий>
cd team-finder-ad
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

Для Windows:

```bash
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать `.env`

Скопируйте пример файла окружения:

```bash
cp .env_example .env
```

Пример значений:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
POSTGRES_DB=teamfinder
POSTGRES_USER=teamfinder_user
POSTGRES_PASSWORD=teamfinder_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Запустить PostgreSQL

```bash
docker compose up -d
```

Остановить контейнеры:

```bash
docker compose down
```

### 6. Применить миграции

```bash
python3 manage.py migrate
```

### 7. Создать суперпользователя

```bash
python3 manage.py createsuperuser
```

В проекте используется кастомная модель пользователя, вход выполняется по email.

### 8. Заполнить тестовыми данными

```bash
python3 manage.py seed
```

Тестовый аккаунт после выполнения команды:

```text
email: maria@yandex.ru
password: password
```

### 9. Запустить сервер

```bash
python3 manage.py runserver
```

Проект будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

Админ-панель:

```text
http://127.0.0.1:8000/admin/
```

## Основные страницы

```text
/projects/list/                     список проектов
/projects/favorites/                избранные проекты
/projects/create-project/           создание проекта
/projects/<id>/                     страница проекта
/projects/<id>/edit/                редактирование проекта

/users/register/                    регистрация
/users/login/                       вход
/users/logout/                      выход
/users/list/                        список пользователей
/users/<id>/                        профиль пользователя
/users/edit-profile/                редактирование профиля
/users/change-password/             смена пароля
```

---
Работу выполнил **Жагло И. Д.**\
Почта: **jagloig@yandex.ru**