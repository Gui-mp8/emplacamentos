build:
	docker build -t emplacamentos .

run: build
	docker compose up -d
	sleep 180
	docker compose down
