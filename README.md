# BackLabs
Repository for Backend Labs

# Render
https://backlabs-lab2.onrender.com/healthcheck

# Postman Collection
https://api.postman.com/collections/31806616-6f3a3093-8e04-472b-9628-489850172943?access_key=PMAT-01HHN2CP2794P3P73Y1CXF07CM

# Postman Flow picture
link: https://web.postman.co/workspace/My-Workspace~1cef47a4-2011-4e56-8164-029b7387fa4d/flow/657b59fd5cfdcd0032d99edd

[postman_flow1.png](postman/postman_flow1.png)


# Lab2

## Setup
Для запуску у себе на пк 

Потрібно клонувати проект в свою робочу директорію:
```
> git clone https://github.com/Napchik/BackLabs/tree/Lab2
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
Перевірка get-ендпоинтів healthcheck:
```
Your domen/healthcheck
Your domen/users
Your domen/categories
Example: http://127.0.0.1:5000/users
```

## Docker
Далі потрібно збілдити image такою командою:
```
>  docker build . --tag <image-name>:latest
Example: docker build . --tag lab2:latest
```
Якщо image упішно збілдився, то його можна запустити і перевірити:
```
> docker run -d -p 5000:5000 <image-name>
Example: docker run -d -p 5000:5000 lab2
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
## Список енд-поинтів
Get:
```
<domen>/users
<domen>/categories
<domen>/records (acquires user_id or category_id)

<domen>/user/<user_id>
<domen>/category/<category_id>
<domen>/record/<record_id>
```
Post:
```
<domen>/user
<domen>/category
<domen>/record
```

Delete:
```
<domen>/user/<user_id>
<domen>/category/<category_id>
<domen>/record/<record_id>
```

