## Celery

Expects a RabbitMQ broker listening on port 5672.
Start the celery worker with
```
celery -A scan_app worker -l info
```

## Django

Start django server with
```
python manage.py runserver
```
Listens on port 8000 by default.