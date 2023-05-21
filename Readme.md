## Локальный запуск

### Установка зависимостей

```
   pip install -r ./ArticlesReccomender/requirements.txt
   pip install -r ./interface/requirements.txt
```

Экспорт переменных окружения

Убедитесь что в файле ./ArticlesReccomender/.env и ./interface/.env прописаны все переменные окружения,
для локального запуска должен стоять флаг DEVELOPMENT=True

```
   export eval `cat ./ArticlesReccomender/.env`
   export eval `cat ./interface/.env`
```

### Запуск

```
   cd ./ArticlesReccomender && python manage.py runserver
   cd ./interface && python articleBot.py
```

## Запуск в Docker

```
   docker-compose up --build
```