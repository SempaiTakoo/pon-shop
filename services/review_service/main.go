package main

import (
	"log"
	_ "review-service/docs" // Импорт сгенерированных Swagger-документов
	"review-service/internal/database"
	"review-service/internal/handlers"
	"review-service/internal/kafka"

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
	// Загружаем .env файл, если он существует
	godotenv.Load()

	// Инициализируем подключение к базе данных
	db := database.InitDB()

	// Инициализируем Kafka продюсер
	producer, err := kafka.NewProducer()
	if err != nil {
		log.Fatalf("Failed to create Kafka producer: %v", err)
	}
	defer producer.Close()

	// Инициализируем обработчики с доступом к БД и Kafka
	reviewHandler := handlers.NewReviewHandler(db, producer)

	router := gin.Default()

	// Review routes
	router.POST("/reviews", reviewHandler.CreateReview)
	router.GET("/reviews/:id", reviewHandler.GetReview)
	router.GET("/reviews", reviewHandler.GetAllReviews)
	router.PUT("/reviews/:id", reviewHandler.UpdateReview)
	router.DELETE("/reviews/:id", reviewHandler.DeleteReview)

	// Swagger документация
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	router.Run(":8080")
}
