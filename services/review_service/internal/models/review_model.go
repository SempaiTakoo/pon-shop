package models

import (
	"time"
)

type Review struct {
	ReviewID  uint64    `gorm:"primaryKey;column:review_id;autoIncrement:true" json:"review_id"`
	ProductID uint64    `gorm:"column:product_id;not null" json:"product_id"`
	UserID    uint64    `gorm:"column:user_id;not null" json:"user_id"`
	Rating    int       `gorm:"column:rating;not null;check:rating >= 1 AND rating <= 5" json:"rating"`
	Comment   string    `gorm:"column:comment;type:text" json:"comment"`
	CreatedAt time.Time `gorm:"column:created_at;default:CURRENT_TIMESTAMP" json:"created_at"`
}

// CreateReviewRequest представляет данные для создания нового отзыва
// Не содержит поле created_at, которое будет установлено автоматически
type CreateReviewRequest struct {
	ProductID uint64 `json:"product_id"`
	UserID    uint64 `json:"user_id"`
	Rating    int    `json:"rating" binding:"required,min=1,max=5"`
	Comment   string `json:"comment"`
}

func (Review) TableName() string {
	return "reviews"
}
