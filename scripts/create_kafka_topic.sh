docker exec kafka kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic user_service_logs \
  --partitions 1 \
  --replication-factor 1
