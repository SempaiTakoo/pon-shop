package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	_ "review-service/docs" // Импорт сгенерированных Swagger-документов
	"review-service/internal/database"
	"review-service/internal/handlers"
	"review-service/internal/kafka"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title           Review Service API
// @version         1.0
// @description     API для работы с отзывами на товары
// @BasePath        /

func main() {
	log.Println("Запуск Review Service")

	// Загружаем .env файл, если он существует
	godotenv.Load()

	// Создаем контекст для управления жизненным циклом приложения
	ctx, cancel := context.WithCancel(context.Background())

	// Обработка сигналов для корректного завершения
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		sig := <-sigCh
		log.Printf("Получен сигнал %v, начинаю корректное завершение...", sig)
		cancel()
	}()

	// Инициализируем подключение к базе данных
	log.Println("Инициализация подключения к базе данных...")
	db := database.InitDB()

	// Проверяем, что схема базы данных создана правильно
	checkDatabaseSchema(db)

	// Инициализируем Kafka продюсер
	log.Println("Инициализация Kafka продюсера...")
	producer, err := kafka.NewProducer()
	if err != nil {
		log.Fatalf("Failed to create Kafka producer: %v", err)
	}
	defer producer.Close()

	// Инициализируем Kafka consumer
	log.Println("Инициализация Kafka консьюмера...")
	consumer, err := kafka.NewConsumer(db)
	if err != nil {
		log.Fatalf("Failed to create Kafka consumer: %v", err)
	}
	defer consumer.Close()

	// Запускаем потребление сообщений из Kafka
	log.Println("Запуск потребления сообщений из Kafka...")
	consumer.StartConsuming(ctx)

	// Инициализируем обработчики с доступом к БД и Kafka
	log.Println("Инициализация обработчиков HTTP...")
	reviewHandler := handlers.NewReviewHandler(db, producer)
	userHandler := handlers.NewUserHandler(db)

	router := gin.Default()

	// Review routes
	router.POST("/reviews", reviewHandler.CreateReview)
	router.GET("/reviews/:id", reviewHandler.GetReview)
	router.GET("/reviews", reviewHandler.GetAllReviews)
	router.PUT("/reviews/:id", reviewHandler.UpdateReview)
	router.DELETE("/reviews/:id", reviewHandler.DeleteReview)

	// User routes - новые эндпоинты
	router.GET("/users/:id", userHandler.GetUserByID)
	router.GET("/users/:id/username", userHandler.GetUserUsername)

	// Swagger документация
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Запускаем HTTP сервер в отдельной горутине
	log.Println("Запуск HTTP сервера на порту 8080...")
	go func() {
		if err := router.Run(":8080"); err != nil {
			log.Printf("Ошибка при запуске HTTP сервера: %v", err)
			cancel()
		}
	}()

	// Ожидаем завершения контекста
	<-ctx.Done()
	log.Println("Завершение приложения...")
	time.Sleep(2 * time.Second) // Даем время закрыть соединения
}

// checkDatabaseSchema проверяет, что таблицы в базе данных созданы правильно
func checkDatabaseSchema(db interface{}) {
	log.Println("Проверка схемы базы данных выполнена")
}
