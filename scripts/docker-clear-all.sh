docker system prune -f
docker-compose down --rmi all --volumes
rm -rf postgres-data/