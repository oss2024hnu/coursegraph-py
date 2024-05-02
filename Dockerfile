FROM python:3

WORKDIR /app

# 현재 디렉토리의 모든 파일을 해당 경로에 복사
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/coursegraph"]


