docker exec kafka kafka-topics.sh --create --bootstrap-server kafka:9092 --topic user_service_logs --partitions 1 --replication-factor 1
docker exec kafka kafka-topics.sh --create --bootstrap-server kafka:9092 --topic product_service_logs --partitions 1 --replication-factor 1
docker exec kafka kafka-topics.sh --create --bootstrap-server kafka:9092 --topic review_service_logs --partitions 1 --replication-factor 1
docker exec kafka kafka-topics.sh --create --bootstrap-server kafka:9092 --topic order_service_logs --partitions 1 --replication-factor 1
