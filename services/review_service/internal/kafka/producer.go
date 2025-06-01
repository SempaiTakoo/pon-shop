package kafka

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"time"

	"github.com/segmentio/kafka-go"
)

const (
	topic           = "review_service_logs"
	eventTypeCreate = "review_created"
	eventTypeUpdate = "review_updated"
	eventTypeDelete = "review_deleted"
)

type Producer struct {
	writer *kafka.Writer
}

type ReviewEvent struct {
	EventType string    `json:"event_type"`
	ReviewID  uint64    `json:"review_id"`
	ProductID uint64    `json:"product_id,omitempty"`
	UserID    uint64    `json:"user_id,omitempty"`
	Rating    int       `json:"rating,omitempty"`
	Comment   string    `json:"comment,omitempty"`
	CreatedAt time.Time `json:"created_at,omitempty"`
	EventTime time.Time `json:"event_time"`
}

func NewProducer() (*Producer, error) {
	// Получаем адрес Kafka из переменных окружения или используем значение по умолчанию
	kafkaBroker := getEnv("KAFKA_BROKER", "kafka:9092")

	log.Printf("Создаю Kafka продюсер с адресом брокера: %s", kafkaBroker)

	// Получаем хост и порт
	parts := strings.Split(kafkaBroker, ":")
	if len(parts) != 2 {
		log.Printf("Некорректный формат адреса Kafka: %s", kafkaBroker)
		return nil, fmt.Errorf("некорректный формат адреса Kafka")
	}

	host := parts[0]
	// Логируем информацию о хосте
	log.Printf("Проверяем хост Kafka: %s", host)
	ips, err := net.LookupIP(host)
	if err != nil {
		log.Printf("Не удалось разрешить хост %s: %v", host, err)
	} else {
		log.Printf("Хост %s разрешается в IP: %v", host, ips)
	}

	// Создаем директорию для информации о топиках
	err = createTopicIfNotExists(kafkaBroker, topic)
	if err != nil {
		log.Printf("Ошибка при создании топика: %v. Продолжаем работу...", err)
	}

	// Создаем writer для Kafka
	writer := &kafka.Writer{
		Addr:         kafka.TCP(kafkaBroker),
		Topic:        topic,
		Balancer:     &kafka.LeastBytes{},
		BatchTimeout: 10 * time.Millisecond,
		RequiredAcks: kafka.RequireOne,
	}

	log.Printf("Kafka продюсер успешно создан")
	return &Producer{
		writer: writer,
	}, nil
}

// createTopicIfNotExists создает топик если он не существует
func createTopicIfNotExists(broker, topicName string) error {
	conn, err := kafka.Dial("tcp", broker)
	if err != nil {
		return fmt.Errorf("невозможно подключиться к %s: %w", broker, err)
	}
	defer conn.Close()

	controller, err := conn.Controller()
	if err != nil {
		return fmt.Errorf("невозможно получить контроллер: %w", err)
	}

	controllerConn, err := kafka.Dial("tcp", net.JoinHostPort(controller.Host, fmt.Sprintf("%d", controller.Port)))
	if err != nil {
		return fmt.Errorf("невозможно подключиться к контроллеру %s:%d: %w", controller.Host, controller.Port, err)
	}
	defer controllerConn.Close()

	// Проверяем наличие топика
	partitions, err := conn.ReadPartitions(topicName)
	if err == nil && len(partitions) > 0 {
		log.Printf("Топик %s уже существует", topicName)
		return nil
	}

	// Создаем топик если не существует
	log.Printf("Создаем топик %s", topicName)
	return controllerConn.CreateTopics(kafka.TopicConfig{
		Topic:             topicName,
		NumPartitions:     1,
		ReplicationFactor: 1,
	})
}

// PublishReviewCreated публикует событие о создании отзыва
func (p *Producer) PublishReviewCreated(ctx context.Context, review interface{}) error {
	log.Printf("Публикуем событие о создании отзыва")
	return p.publishEvent(ctx, eventTypeCreate, review)
}

// PublishReviewUpdated публикует событие об обновлении отзыва
func (p *Producer) PublishReviewUpdated(ctx context.Context, review interface{}) error {
	log.Printf("Публикуем событие об обновлении отзыва")
	return p.publishEvent(ctx, eventTypeUpdate, review)
}

// PublishReviewDeleted публикует событие об удалении отзыва
func (p *Producer) PublishReviewDeleted(ctx context.Context, reviewID uint64) error {
	log.Printf("Публикуем событие об удалении отзыва с ID: %d", reviewID)
	event := ReviewEvent{
		EventType: eventTypeDelete,
		ReviewID:  reviewID,
		EventTime: time.Now(),
	}

	return p.publish(ctx, event)
}

// publishEvent формирует и публикует событие на основе данных отзыва
func (p *Producer) publishEvent(ctx context.Context, eventType string, review interface{}) error {
	reviewJSON, err := json.Marshal(review)
	if err != nil {
		return fmt.Errorf("ошибка маршалинга отзыва: %w", err)
	}

	var reviewData map[string]interface{}
	if err := json.Unmarshal(reviewJSON, &reviewData); err != nil {
		return fmt.Errorf("ошибка анмаршалинга отзыва: %w", err)
	}

	event := ReviewEvent{
		EventType: eventType,
		EventTime: time.Now(),
	}

	// Заполняем поля события из данных отзыва
	if id, ok := reviewData["review_id"].(float64); ok {
		event.ReviewID = uint64(id)
	}
	if id, ok := reviewData["product_id"].(float64); ok {
		event.ProductID = uint64(id)
	}
	if id, ok := reviewData["user_id"].(float64); ok {
		event.UserID = uint64(id)
	}
	if rating, ok := reviewData["rating"].(float64); ok {
		event.Rating = int(rating)
	}
	if comment, ok := reviewData["comment"].(string); ok {
		event.Comment = comment
	}
	if createdAtStr, ok := reviewData["created_at"].(string); ok {
		t, err := time.Parse(time.RFC3339, createdAtStr)
		if err == nil {
			event.CreatedAt = t
		}
	}

	return p.publish(ctx, event)
}

// publish отправляет событие в Kafka
func (p *Producer) publish(ctx context.Context, event interface{}) error {
	value, err := json.Marshal(event)
	if err != nil {
		return err
	}

	reviewEvent, ok := event.(ReviewEvent)
	if !ok {
		return fmt.Errorf("неверный тип события")
	}

	log.Printf("Отправляем сообщение в Kafka с ключом '%d'", reviewEvent.ReviewID)

	msg := kafka.Message{
		Key:   []byte(fmt.Sprintf("%v", reviewEvent.ReviewID)),
		Value: value,
		Time:  time.Now(),
	}

	// Устанавливаем короткий таймаут для операции записи
	ctxWithTimeout, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	err = p.writer.WriteMessages(ctxWithTimeout, msg)
	if err != nil {
		log.Printf("Ошибка при отправке сообщения в Kafka: %v", err)
		return fmt.Errorf("ошибка при отправке сообщения в Kafka: %w", err)
	}

	log.Printf("Сообщение успешно отправлено в топик Kafka: %s", topic)
	return nil
}

// Close закрывает соединение с Kafka
func (p *Producer) Close() error {
	log.Printf("Закрываем соединение с Kafka")
	return p.writer.Close()
}

// getEnv получает значение переменной окружения или возвращает значение по умолчанию
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
