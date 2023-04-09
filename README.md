# Руководство по запуску
1. В корневой директории переименовать файл '.env.example' на '.env', разархивировать бд:
```
sudo tar xvzf postgres_data.tar.gz
```
2. В терминале выполнить команду:
```
docker compose up --build
```
3. Для запуска тестов выполнить команду:
```
docker exec fastapi pytest
```
