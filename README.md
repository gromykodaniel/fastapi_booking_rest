# Проект API Cервиса бронирования отелей
## О приложении:
Проект  представляет собой cервис,
в которой пользователи имеют возможность создать учетную запись, 
возможность просмотра свободных отелей и номер ,бронь. 
Он предоставляет клиентам доступ к базе данных. Данные передаются в формате JSON.
Примененные технологии:
### Backend
+ API — FastAPI
+ База Данных — PostgreSQL
+ Кэширование — Redis
+ Фоновые задачи — Celery
+ Контейнеризация — Docker и Docker Compose
+ Мониторинг - Grafana , Prometheus
+ Логирование - Centry
### Python
+ Автоматическое тестирование — pytest
+ Валидация данных — Pydantic
+ ORM — SQLAlchemy



Клонирование репозитория и переход в него в командной строке:
```
git clone git@github.com:gromykodaniel/fastapi_booking_rest.git
cd api_final_yatube
```
### Cоздать и активировать виртуальное окружение:
Виртуальное окружение должно использовать Python 3.9

```
pyhton -m venv venv
```
+ Если у вас Linux/MacOS

```
source venv/bin/activate
```
+ Если у вас windows
```
source venv/scripts/activate
```
### Установка зависимостей из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```


### Примеры запросов к API:
POST-запрос на эндпоинт api/v1/posts/:
```
{
    "room_id": 5,
    "date_from": "2023-06-06",
    "date_to": "2023-07-07"
}
```
Ответ:
```
{
  "id": 39,
  "room_id": 5,
  "user_id": 4,
  "date_from": "2023-06-06",
  "date_to": "2023-07-07",
  "price": 7080,
  "total_cost": 219480,
  "total_days": 31
}
```

GET-запрос на эндпоинт api/v1/hotels/{location}/ вернет список свободных отелей в выбранном городе:
```
[
  {
    "id": 3,
    "name": "Ару-Кёль",
    "location": "Республика Алтай, Турочакский район, село Артыбаш, Телецкая улица, 44А",
    "services": [
      "Парковка"
    ],
    "rooms_quantity": 30,
    "image_id": 3,
    "rooms_left": 30
  },
  {
    "id": 1,
    "name": "Cosmos Collection Altay Resort",
    "location": "Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20",
    "services": [
      "Wi-Fi",
      "Бассейн",
      "Парковка",
      "Кондиционер в номере"
    ],
    "rooms_quantity": 15,
    "image_id": 1,
    "rooms_left": 15
  },
  
]
```
Документация к API доступна по ссылке http://localhost:7776/v1/docs после запуска docker-контейнера
