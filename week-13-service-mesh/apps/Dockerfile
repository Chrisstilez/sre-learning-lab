FROM python:3.11-slim
WORKDIR /app
COPY . .
ARG APP_FILE=app.py
ENV APP_FILE=${APP_FILE}
CMD python ${APP_FILE}
