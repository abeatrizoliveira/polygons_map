FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENV FLASK_APP=src.back.app
EXPOSE 5000
# 0.0.0.0 é necessário para o navegador (fora do container) conseguir acessar
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
