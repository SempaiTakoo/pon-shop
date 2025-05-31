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

func (Review) TableName() string {
	return "reviews"
}