docker compose -f services/kafka_service/docker-compose.yml up up -d
docker compose -f services/order_service/docker-compose.yml up -d

docker compose -f services/user_service/docker-compose.yml \
               --env-file .user_service.env up -d
