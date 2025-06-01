package database

import (
	"fmt"
	"os"
	"review-service/internal/models"

	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func InitDB() *gorm.DB {
	// Загружаем .env файл, если существует
	godotenv.Load()

	// Получаем настройки подключения к БД из переменных окружения
	host := getEnv("DB_HOST", "postgres")
	port := getEnv("DB_PORT", "5432")
	user := getEnv("DB_USER", "postgres")
	password := getEnv("DB_PASSWORD", "postgres")
	dbname := getEnv("DB_NAME", "reviews")
	sslMode := getEnv("DB_SSL_MODE", "disable")

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=%s",
		host, user, password, dbname, port, sslMode)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(fmt.Sprintf("Failed to connect to database: %v", err))
	}

	// Миграция таблицы отзывов и пользователей
	db.AutoMigrate(&models.Review{}, &models.User{})

	db.Exec(`
		DO $$ BEGIN
			IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_rating_range') THEN
				ALTER TABLE reviews ADD CONSTRAINT check_rating_range CHECK (rating >= 1 AND rating <= 5);
			END IF;
		END $$;
	`)

	return db
}

// getEnv возвращает значение переменной окружения или значение по умолчанию
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
