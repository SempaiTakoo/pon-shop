package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"review-service/internal/models"
)

type ReviewHandler struct {
	DB *gorm.DB
}

func NewReviewHandler(db *gorm.DB) *ReviewHandler {
	return &ReviewHandler{DB: db}
}

// CreateReview godoc
// @Summary Create a new review
// @Description Create a new product review
// @Tags reviews
// @Accept json
// @Produce json
// @Param review body models.Review true "Review data"
// @Success 201 {object} models.Review
// @Router /reviews [post]
func (h *ReviewHandler) CreateReview(c *gin.Context) {
	var review models.Review
	if err := c.ShouldBindJSON(&review); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if review.Rating < 1 || review.Rating > 5 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Rating must be between 1 and 5"})
		return
	}

	if result := h.DB.Create(&review); result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	c.JSON(http.StatusCreated, review)
}

// GetReview godoc
// @Summary Get a review by ID
// @Description Get review details by review ID
// @Tags reviews
// @Produce json
// @Param id path int true "Review ID"
// @Success 200 {object} models.Review
// @Router /reviews/{id} [get]
func (h *ReviewHandler) GetReview(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid review ID"})
		return
	}

	var review models.Review
	result := h.DB.First(&review, id)
	if result.Error != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Review not found"})
		return
	}

	c.JSON(http.StatusOK, review)
}

// GetAllReviews godoc
// @Summary Get all reviews
// @Description Get list of reviews with pagination
// @Tags reviews
// @Produce json
// @Param page query int false "Page number" default(1)
// @Param limit query int false "Items per page" default(10)
// @Success 200 {object} map[string]interface{}
// @Router /reviews [get]
func (h *ReviewHandler) GetAllReviews(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
	offset := (page - 1) * limit

	var reviews []models.Review
	var total int64

	h.DB.Model(&models.Review{}).Count(&total)
	result := h.DB.Offset(offset).Limit(limit).Find(&reviews)
	
	if result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"data":  reviews,
		"page":  page,
		"limit": limit,
		"total": total,
	})
}

// UpdateReview godoc
// @Summary Update a review
// @Description Update existing review by ID
// @Tags reviews
// @Accept json
// @Produce json
// @Param id path int true "Review ID"
// @Param review body models.Review true "Updated review data"
// @Success 200 {object} models.Review
// @Router /reviews/{id} [put]
func (h *ReviewHandler) UpdateReview(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid review ID"})
		return
	}

	var existingReview models.Review
	if result := h.DB.First(&existingReview, id); result.Error != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Review not found"})
		return
	}

	var updateData models.Review
	if err := c.ShouldBindJSON(&updateData); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if updateData.Rating != 0 && (updateData.Rating < 1 || updateData.Rating > 5) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Rating must be between 1 and 5"})
		return
	}

	// Обновляем только разрешенные поля
	h.DB.Model(&existingReview).Updates(models.Review{
		Rating:  updateData.Rating,
		Comment: updateData.Comment,
	})

	c.JSON(http.StatusOK, existingReview)
}

// DeleteReview godoc
// @Summary Delete a review
// @Description Delete review by ID
// @Tags reviews
// @Produce json
// @Param id path int true "Review ID"
// @Success 200 {object} map[string]string
// @Router /reviews/{id} [delete]
func (h *ReviewHandler) DeleteReview(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid review ID"})
		return
	}

	result := h.DB.Delete(&models.Review{}, id)
	if result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	if result.RowsAffected == 0 {
		c.JSON(http.StatusNotFound, gin.H{"error": "Review not found"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Review deleted successfully"})
}