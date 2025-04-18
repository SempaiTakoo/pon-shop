package main

import (
	"review-service/internal/database"
	"review-service/internal/handlers"
	
	"github.com/gin-gonic/gin"
)

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

	router.Run(":8080")
}