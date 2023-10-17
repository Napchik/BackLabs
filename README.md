# BackLabs
Repository for Backend Labs

# Render
https://backlabs-test.onrender.com

# Lab1

## Setup
Для запуску у себе на пк 

Потрібно клонувати проект в свою робочу директорію:
```
> git clone https://github.com/Napchik/BackLabs.git
```
Активувати віртуальне середовище:
```
> source ./env/bin/activate
```
Встановити flask допомогою команди:
```
> pip install flask
```
Тут є .flaskenv файл, тому потрібно поставити python-dotenv:
```
> pip install python-dotenv
```

## Flask
Запуск лабораторної роботи через flask:
```
> flask --app src/views run -h 0.0.0.0 -p 5000
```
Перевірка ендпоинту healthcheck:
```
Your ip/healthcheck
Example: http://127.0.0.1:5000/healthcheck
```

## Docker
Далі потрібно збілдити image такою командою:
```
>  docker build . --tag <image-name>:latest
Example: docker build . --tag lab1:latest
```
Якщо image упішно збілдився, то його можна запустити і перевірити:
```
> docker run -d -p 5000:5000 <image-name>
Example: docker run -d -p 5000:5000 lab1
```

## Docker-compose
Збілдити контейнер: 
```
> docker-compose build
```
Запустити контейнер:
```
> docker-compose up
```