# make face-recognize
.DEFAULT_GOAL := face-recognize

.PHONY: face-recognize
face-recognize:
	docker builder build --platform linux/arm64 -t face-recognize:v1.0 .
	docker tag face-recognize:v1.0 192.168.43.145:5000/face-recognize:v1.0
	docker push 192.168.43.145:5000/face-recognize:v1.0
