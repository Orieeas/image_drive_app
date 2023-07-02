# Используйте официальный образ Python в качестве базового образа
FROM python:3.10
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# Установите зависимости приложения
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install --upgrade pip


# Установите рабочую директорию
WORKDIR /mpz

# Копируйте содержимое директории проекта в рабочую директорию контейнера
COPY . /mpz

# Запустите приложение при помощи uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]