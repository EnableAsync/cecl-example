# FROM pcarstens8698/tensorflow-1.12.0-py3-none-linux_aarch64:latest
FROM sixsq/opencv-python:master-arm64
ENV DEBIAN_FRONTEND=noninteractive
COPY . /facenet
WORKDIR /facenet
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libgtk-3-0 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip && python3 -m pip --default-timeout=10000 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["python3","-u","/facenet/face_recognize.py"]
