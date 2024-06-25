# Используем официальный образ Python
FROM python:3.12.3

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /bot

RUN pip install --upgrade pip

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы приложения в рабочую директорию
COPY . .

# Указываем команду, которая будет выполняться при запуске контейнера
CMD ["python", "-m", "app"]
