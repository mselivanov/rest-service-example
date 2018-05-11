docker-compose -f docker-compose.yml -f docker-compose-win.yml build
docker-compose -f docker-compose.yml -f docker-compose-win.yml up -d
docker-compose exec app flask db init 
docker-compose exec app flask db migrate 
docker-compose exec app flask db upgrade 
