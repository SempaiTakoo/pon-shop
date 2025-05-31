FROM golang:1.24.2-alpine AS builder
WORKDIR /app
COPY . .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o review-service .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/review-service .
COPY --from=builder /app/docs ./docs
EXPOSE 8080
CMD ["./review-service"]