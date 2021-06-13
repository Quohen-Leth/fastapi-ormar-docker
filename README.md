docker-compose up --build --remove-orphans
docker-compose down --remove-orphans
docker-compose run web_book alembic upgrade head
docker-compose run web_book alembic revision --autogenerate -m"init"

docker-compose exec web_book sh

sudo fuser-k 8000/TCP kill port