docker network create kafka-net


docker compose -f services/order_service/docker-compose.yml up -d
# docker compose -f services/product_service/docker-compose.yml up -d
docker compose -f services/user_service/docker-compose.yml up -d
