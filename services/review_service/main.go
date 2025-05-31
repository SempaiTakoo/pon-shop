package main

import (
	_ "review-service/docs" // Импорт сгенерированных Swagger-документов
	"review-service/internal/database"
	"review-service/internal/handlers"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title           Review Service API
// @version         1.0
// @description     API для работы с отзывами на товары
// @BasePath        /

func main() {
	db := database.InitDB()
	reviewHandler := handlers.NewReviewHandler(db)

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
