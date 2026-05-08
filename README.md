# Эксплуатационная практика: Docker + Web-приложение

Этот репозиторий содержит пример выполнения задания ЭП:
- изучение основ Docker;
- развёртывание web-приложения из **frontend** и **backend**, которые общаются по HTTP.

## Структура проекта

- `frontend` — статический интерфейс (HTML/JS) в контейнере Nginx;
- `backend` — API на Flask;
- `docker-compose.yml` — запуск обоих сервисов.

## Быстрый запуск

1. Установить Docker и Docker Compose.
2. В корне проекта выполнить:

```bash
docker compose up --build
```

3. Открыть:
- Frontend: http://localhost:8080
- Backend healthcheck: http://localhost:5000/api/health

## Как это работает

- Frontend отправляет HTTP-запросы на backend:
  - `GET /api/tasks` — получить список задач;
  - `POST /api/tasks` — добавить задачу.
- Backend хранит задачи в памяти (для учебной демонстрации).

## Остановка

```bash
docker compose down
```

## Связь с заданием

Проект соответствует требованиям:
1. Используются базовые элементы Docker: Dockerfile, образы, контейнеры, сеть, docker-compose.
2. Есть минимум 2 части (frontend + backend), взаимодействующие по HTTP.
