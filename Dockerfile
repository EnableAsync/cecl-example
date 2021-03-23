FROM python:3.7
COPY . /CECL
WORKDIR /CECL
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r /CECL/requirements.txt
ENV PATH=$PATH:/CECL
ENV PYTHONPATH /CECL
EXPOSE 5000
CMD ["python", "/CECL/main.py"]