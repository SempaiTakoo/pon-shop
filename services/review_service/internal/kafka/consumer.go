package kafka

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"review-service/internal/models"
	"strings"
	"time"

	"github.com/segmentio/kafka-go"
	"gorm.io/gorm"
)

// Consumer представляет Kafka consumer для обработки сообщений
type Consumer struct {
	reader *kafka.Reader
	db     *gorm.DB
}

// UserEvent представляет структуру события пользователя из Kafka
type UserEvent struct {
	Event string `json:"event"`
	Data  struct {
		User struct {
			ID       int    `json:"created_user.id"`
			Username string `json:"created_user.username"`
			Role     string `json:"created_user.role"`
			Email    string `json:"created_user.email"`
		} `json:"user"`
		UserID int `json:"user_id"`
		Count  int `json:"count"`
	} `json:"data"`
}

// NewConsumer создает новый экземпляр Consumer
func NewConsumer(db *gorm.DB) (*Consumer, error) {
	kafkaBroker := getEnv("KAFKA_BROKER", "kafka:9092")
	userServiceTopic := getEnv("USER_SERVICE_TOPIC", "user_service_logs")

	log.Printf("Создание Kafka consumer для топика %s с брокером %s", userServiceTopic, kafkaBroker)

	// Конфигурация reader
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        []string{kafkaBroker},
		Topic:          userServiceTopic,
		GroupID:        "review-service-consumer-group",
		MinBytes:       10e3, // 10KB
		MaxBytes:       10e6, // 10MB
		CommitInterval: time.Second,
		// Начинаем с самого начала, чтобы не пропустить существующие сообщения
		StartOffset: kafka.FirstOffset,
	})

	return &Consumer{
		reader: reader,
		db:     db,
	}, nil
}

// StartConsuming запускает обработку сообщений из Kafka
func (c *Consumer) StartConsuming(ctx context.Context) {
	log.Println("Запуск потребления сообщений из Kafka")

	// Сначала проверим соединение с Kafka и статус топика
	err := c.checkTopicStatus()
	if err != nil {
		log.Printf("Предупреждение: проблема с проверкой топика Kafka: %v", err)
	}

	// Запустим обработку в отдельной горутине
	go func() {
		log.Println("Горутина обработки сообщений Kafka запущена")

		for {
			select {
			case <-ctx.Done():
				log.Println("Остановка потребления сообщений из Kafka")
				if err := c.reader.Close(); err != nil {
					log.Printf("Ошибка при закрытии Kafka reader: %v", err)
				}
				return
			default:
				// Читаем сообщение с таймаутом
				readCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
				msg, err := c.reader.ReadMessage(readCtx)
				cancel()

				if err != nil {
					if strings.Contains(err.Error(), "context canceled") ||
						strings.Contains(err.Error(), "context deadline exceeded") {
						time.Sleep(1 * time.Second) // Небольшая пауза перед новой попыткой
						continue
					}
					log.Printf("Ошибка при чтении сообщения из Kafka: %v", err)
					continue
				}

				// Логируем полученное сообщение
				log.Printf("Получено сообщение из топика %s, partition: %d, offset: %d, значение: %s",
					msg.Topic, msg.Partition, msg.Offset, string(msg.Value))

				// Обрабатываем сообщение
				if err := c.processMessage(msg); err != nil {
					log.Printf("Ошибка при обработке сообщения: %v", err)
				}
			}
		}
	}()

	log.Println("Kafka consumer успешно запущен и ждет сообщений")
}

// checkTopicStatus проверяет доступность топика
func (c *Consumer) checkTopicStatus() error {
	conn, err := kafka.DialLeader(context.Background(), "tcp", c.reader.Config().Brokers[0], c.reader.Config().Topic, 0)
	if err != nil {
		return fmt.Errorf("невозможно подключиться к Kafka: %w", err)
	}
	defer conn.Close()

	log.Printf("Успешное подключение к топику %s", c.reader.Config().Topic)
	return nil
}

// processMessage обрабатывает полученное сообщение
func (c *Consumer) processMessage(msg kafka.Message) error {
	var event UserEvent
	if err := json.Unmarshal(msg.Value, &event); err != nil {
		return fmt.Errorf("ошибка при разборе JSON: %w, сообщение: %s", err, string(msg.Value))
	}

	// Выводим структуру сообщения для отладки
	eventJSON, _ := json.MarshalIndent(event, "", "  ")
	log.Printf("Разобранное сообщение: %s", string(eventJSON))

	// Обработка события в зависимости от типа
	switch event.Event {
	case "CREATE":
		// Обрабатываем только события CREATE с валидным ID пользователя
		if event.Data.User.ID > 0 {
			return c.handleCreateEvent(event)
		}

	case "UPDATE":
		// Обрабатываем событие обновления пользователя
		if event.Data.UserID > 0 {
			return c.handleUpdateEvent(event)
		}

	case "DELETE":
		// Обрабатываем событие удаления пользователя
		if event.Data.UserID > 0 {
			return c.handleDeleteEvent(event)
		}
	}

	log.Printf("Пропуск сообщения с типом '%s' или неверными данными", event.Event)
	return nil
}

// handleCreateEvent обрабатывает событие CREATE
func (c *Consumer) handleCreateEvent(event UserEvent) error {
	log.Printf("Обработка события CREATE для пользователя ID: %d, Username: %s",
		event.Data.User.ID, event.Data.User.Username)

	// Создаем или обновляем запись пользователя
	user := models.User{
		UserID:   uint64(event.Data.User.ID),
		Username: event.Data.User.Username,
	}

	// Сначала проверим, существует ли уже этот пользователь
	var existingUser models.User
	result := c.db.Where("user_id = ?", user.UserID).First(&existingUser)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			// Пользователь не найден, создаем новую запись
			log.Printf("Создание новой записи пользователя с ID %d", user.UserID)
			result = c.db.Create(&user)
			if result.Error != nil {
				return fmt.Errorf("ошибка при создании пользователя: %w", result.Error)
			}
		} else {
			// Другая ошибка при поиске
			return fmt.Errorf("ошибка при поиске пользователя: %w", result.Error)
		}
	} else {
		// Пользователь существует, обновляем его имя если необходимо
		if existingUser.Username != user.Username {
			log.Printf("Обновление имени пользователя с ID %d с '%s' на '%s'",
				user.UserID, existingUser.Username, user.Username)
			existingUser.Username = user.Username
			result = c.db.Save(&existingUser)
			if result.Error != nil {
				return fmt.Errorf("ошибка при обновлении пользователя: %w", result.Error)
			}
		} else {
			log.Printf("Пользователь с ID %d и именем '%s' уже существует, пропускаем",
				user.UserID, user.Username)
		}
	}

	log.Printf("Пользователь с ID %d успешно обработан", user.UserID)
	return nil
}

// handleUpdateEvent обрабатывает событие UPDATE
func (c *Consumer) handleUpdateEvent(event UserEvent) error {
	userID := uint64(event.Data.UserID)
	log.Printf("Обработка события UPDATE для пользователя ID: %d", userID)

	// Проверяем, существует ли пользователь
	var user models.User
	result := c.db.Where("user_id = ?", userID).First(&user)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			log.Printf("Пользователь с ID %d не найден при обработке события UPDATE", userID)
			return nil // Не считаем это ошибкой, просто логируем
		}
		return fmt.Errorf("ошибка при поиске пользователя для обновления: %w", result.Error)
	}

	// В текущей версии события UPDATE не содержат новых данных пользователя
	// Здесь можно добавить обработку других данных, если они будут в будущем

	log.Printf("Пользователь с ID %d существует, событие UPDATE обработано", userID)
	return nil
}

// handleDeleteEvent обрабатывает событие DELETE
func (c *Consumer) handleDeleteEvent(event UserEvent) error {
	userID := uint64(event.Data.UserID)
	log.Printf("Обработка события DELETE для пользователя ID: %d", userID)

	// Удаляем пользователя из базы данных
	result := c.db.Where("user_id = ?", userID).Delete(&models.User{})
	if result.Error != nil {
		return fmt.Errorf("ошибка при удалении пользователя: %w", result.Error)
	}

	if result.RowsAffected == 0 {
		log.Printf("Пользователь с ID %d не найден при обработке события DELETE", userID)
		return nil
	}

	log.Printf("Пользователь с ID %d успешно удален", userID)
	return nil
}

// Close закрывает соединение с Kafka
func (c *Consumer) Close() error {
	return c.reader.Close()
}
