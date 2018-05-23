docker-compose -f docker-compose.yml -f docker-compose-win.yml build
docker-compose -f docker-compose.yml -f docker-compose-win.yml up -d
docker-compose exec app /bin/bash /code/db_migrate.sh
