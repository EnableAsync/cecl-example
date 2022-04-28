# make led_light_mapper
.DEFAULT_GOAL := led_light_mapper

.PHONY: led_light_mapper
led_light_mapper:
	GOARCH=arm64 go build light_mapper.go
	docker buildx build --platform linux/arm64 -t led-light-mapper:v1.2 .
	docker tag led-light-mapper:v1.2 192.168.43.145:5000/led-light-mapper:v1.2
	docker push 192.168.43.145:5000/led-light-mapper:v1.2