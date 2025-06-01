package handlers

import (
	"net/http"
	"review-service/internal/models"
	"strconv"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

// UserHandler обрабатывает запросы к API пользователей
type UserHandler struct {
	db *gorm.DB
}

// NewUserHandler создает новый экземпляр UserHandler
func NewUserHandler(db *gorm.DB) *UserHandler {
	return &UserHandler{
		db: db,
	}
}

// GetUserByID обрабатывает запрос на получение информации о пользователе по ID
// @Summary Получение информации о пользователе
// @Description Получает информацию о пользователе по его ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "ID пользователя"
// @Success 200 {object} models.User
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users/{id} [get]
func (h *UserHandler) GetUserByID(c *gin.Context) {
	userID, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Неверный формат ID пользователя"})
		return
	}

	var user models.User
	result := h.db.Where("user_id = ?", userID).First(&user)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Пользователь не найден"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Ошибка при получении данных пользователя"})
		}
		return
	}

	c.JSON(http.StatusOK, user)
}

// GetUserUsername обрабатывает запрос на получение имени пользователя по ID
// @Summary Получение имени пользователя
// @Description Получает имя пользователя по его ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "ID пользователя"
// @Success 200 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users/{id}/username [get]
func (h *UserHandler) GetUserUsername(c *gin.Context) {
	userID, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Неверный формат ID пользователя"})
		return
	}

	var user models.User
	result := h.db.Select("username").Where("user_id = ?", userID).First(&user)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Пользователь не найден"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Ошибка при получении данных пользователя"})
		}
		return
	}

	c.JSON(http.StatusOK, gin.H{"username": user.Username})
}
