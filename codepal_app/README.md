# Code.Pal

![Alt text](![Alt text](<../postman/Screenshot 2024-04-10 at 11.23.41 AM.png>))

### Overview

Code.pal is a freelance website aims to connect developers and clients, providing a platform where clients can find a developer according to his need. The website facilitates communication and collaboration between clients and developers, enabling them to manage projects. Code.pal have feature that a client can review the developer and a developer can review the client. We also add a Follow and Following feature, so both client and developer can follow eachother.

## Installation

Download the API by forking and cloneing this repository

```
bash
~ git clone https://github.com/zackcinal/codepal-backend
~ cd codepal-backend

In the directroy run
~ pipenv shell

Install django packages
~ pipenv install django psycopg2-binary djangorestframework

Create a database
~ psql -f create-db.sql

Setup the admin panel
~ python manage.py createsuperuser
```


## Routes

Open **Postman** to test the API and its full **CRUD** functionality. You will find some examples of the routes availble and how to access them.

To view the admin. 
```bash
GET http://127.0.0.1:8000/admin

```
To view the all developer
```bash
GET http://127.0.0.1:8000/developer/roles

```
To see the Follow
```bash
GET  http://127.0.0.1:8000/follow/<int:follower_id>/<int:following_id>
```

**Full CRUD routes**

These routes are requied to authorization by using the Authorization key and BEARER in your header on Postman when making a request. 

## Feature

- Full functionality through routes and controllers.
- Full authentication.
- Password protection.

## Run Local Server 
 
GO to the directrory that you cloned from github
Seed data to psql
```bash
psql -f create-db.sql
``` 

Make migrations
```bash
python manage.py makemigrations
```

Make migrate
```bash
python manage.py migrate
```

Run the server
```bash
python manage.py runserver
```

## ERD diagram 

![Alt text](<Screenshot 2024-04-10 at 12.25.48 PM.png>)

## Component Hierachy
![Alt text](<https://private-user-images.githubusercontent.com/90149052/320118003-3ee76456-65ed-425e-9493-6b8ad1eb7743.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTI3NjcyMjgsIm5iZiI6MTcxMjc2NjkyOCwicGF0aCI6Ii85MDE0OTA1Mi8zMjAxMTgwMDMtM2VlNzY0NTYtNjVlZC00MjVlLTk0OTMtNmI4YWQxZWI3NzQzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDEwVDE2MzUyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdjOGMzNzc4YTE2N2FjNWQ2NjU4ZDk4ZTc3OGYxNDk5ODQ3MDFmNzA0MmIwNDg5YTE5NjVhM2M4Yjk1M2YxNzEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.ptmgVoCumjM1BkYdXs5SkkXZeCe2lchAoxUo93StIS4>)



## License
This project is licensed under the MIT License.


## Creater
- [Abdul Rehman](https://github.com/arehmanlatif1)
- [Zack Cinal](https://github.com/zackcinal)
- [Cesar Iparrea](https://github.com/CIparrea)
- [Antonio Felix](https://github.com/afelixj89)

