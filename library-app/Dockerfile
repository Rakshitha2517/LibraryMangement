FROM python:3.12-slim
WORKDIR /app
COPY app/ app/
# Database file lives in /data so we can keep it outside the container
ENV DB_PATH=/data/library.db
RUN mkdir -p /data
CMD ["python", "-m", "app.main"]
