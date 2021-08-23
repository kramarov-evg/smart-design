# Тестовое задание
## Как использовать
### Подготовка окружения

- Рекомендуется: создать виртуальное окружение во избежание конфликтов версий библиотек;
- Установить необходимые пакеты (`pip install -r requirements.txt`);
- Запустить Mongo локально или в контейнере, чтобы к нему можно было получить доступ через `localhost:27017`;
- Рекомендуется: Перед началом тестового использования выполнить `python populate.py`
Эта команда добавит в БД два простых документа, на которых можно демонстрировать тестовые сценарии. Документы имеют вид:
```
{
    'name': 'Item1',
    'description': 'First Item',
    'params': {
        'param1': 1,
        'param2': 'b'
    }
},
{
    'name': 'Item2',
    'description': 'Second Item',
    'params': {
        'param1': 10,
        'param2': 'beta'
    }
}
```

### Использование
1. Запуск сервера: `python main.py`
2. Запросы к серверу. Ниже приведены примеры запросов с помощью cURL и ответы на них.

**Боле полную документацию по запросам можно найти в WIKI этого репозитория**

### Примеры cURL-запросов
1. Создание товара. Запрос:
```
curl -X POST http://localhost:5000/products/add \
    -H 'Content-Type: application/json' \
    -d '{
            "name": "Item3",
            "description": "Not an item",
            "params": [
                ["param1", 100],
                ["param2", "epsilon"],
                ["param3", "param3"]
            ]
        }'
```
Ответ:
```
{
  "_id": {
    "$oid": "612386406d72879ddc521809"
  },
  "description": "Not an item",
  "name": "Item3",
  "params": {
    "param1": 100,
    "param2": "epsilon",
    "param3": "param3"
  }
}
```
2. Поиск товара по параметру. Запрос:
```
curl -X POST http://localhost:5000/products/search \
    -H 'Content-Type: application/json' \
    -d '{
            "param3": {
                "method": "endsWith",
                "pattern": "3"
            }
        }'
```
Ответ:
```
{
  "_id": {
    "$oid": "612386406d72879ddc521809"
  },
  "description": "Not an item",
  "name": "Item3",
  "params": {
    "param1": 100,
    "param2": "epsilon",
    "param3": "param3"
  }
}
```
3. Получить детали товара по ID. Запрос:
```
curl -X GET http://localhost:5000/products/612386406d72879ddc521809 \
    -H 'Content-Type: application/json'
```
Ответ:
```
{
  "_id": {
    "$oid": "612386406d72879ddc521809"
  },
  "description": "Not an item",
  "name": "Item3",
  "params": {
    "param1": 100,
    "param2": "epsilon",
    "param3": "param3"
  }
}
```