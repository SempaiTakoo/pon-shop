package models

// User представляет модель пользователя в базе данных
type User struct {
	UserID   uint64 `gorm:"primaryKey;column:user_id" json:"user_id"`
	Username string `gorm:"column:username;not null" json:"username"`
}

// TableName возвращает имя таблицы в базе данных
func (User) TableName() string {
	return "users"
}
