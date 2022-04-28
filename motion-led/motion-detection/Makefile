# make led_light_mapper
.DEFAULT_GOAL := led_light_mapper

.PHONY: led_light_mapper
led_light_mapper:
	docker buildx build --platform linux/arm64 -t motion-detection:v1.0 .
	docker tag motion-detection:v1.0 192.168.43.145:5000/motion-detection:v1.0
	docker push 192.168.43.145:5000/motion-detection:v1.0