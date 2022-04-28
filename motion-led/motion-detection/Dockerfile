# need build on arm64 devices
FROM pachyderm/opencv:arm64
COPY . /motion-detection
WORKDIR /motion-detection
RUN pip install -r requirements.txt
ENTRYPOINT ["python3","-u", "/motion-detection/detec_fram.py"]