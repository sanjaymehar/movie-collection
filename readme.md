`http://127.0.0.1:8000/register/`
To register user
send a POST request with the required input data in JSON format:
```sh
{
    "username":"admin",
    "password":"admin"
}
```
In return you will get access token

```sh
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5NTQ5ODA3LCJpYXQiOjE2OTk1NDk1MDcsImp0aSI6IjAyY2Q2YTVlZGY2MjQxZGZhNTU3ZTM5Y2EyNGJkZTRjIiwidXNlcl9pZCI6MX0.XqEZKSNyJvY9Xs8cPBsSONJARu74lBgDfqu0ueypr5g"
}
```

**Note**


**ALL THE BELOW APIS NEEDS bearer token TO ACCESS THE API**



`http://127.0.0.1:8000/collection/`

send a POST request with the required input data in JSON format:
```sh
{
    "title": "My Collection",
    "description": "My collection of favorite movies",
    "movies": [
        {
            "title": "Movie 1",
            "description": "Description of Movie 1",
            "genres": "Action",
            "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a9"
        },
        {
            "title": "Movie 2",
            "description": "Description of Movie 2",
            "genres": "Comedy",
            "uuid": "13ecfdcc-1680-44d8-a9e7-a0d4c6e9386a"
        }
    ]
}
```

send a GET request in return you will get
```sh
{
    "is_success": true,
    "data": {
        "collections": [
            {
                "title": "Movie 1",
                "description": "Description of Movie 1",
                "genres": "Action",
                "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a9"
            },
            {
                "title": "Movie 2",
                "description": "Description of Movie 2",
                "genres": "Comedy",
                "uuid": "13ecfdcc-1680-44d8-a9e7-a0d4c6e9386a"
            },
            {
                "title": "Movie 9",
                "description": "Description of Movie 9",
                "genres": "Action",
                "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a0"
            }
        ],
        "favourite_genres": "Action, Comedy"
    }
}
```
`http://localhost:8000/collection/<collection_uuid>/`
GET, PUT & DELETE API

PUT
```
title = <Optional updated title>
description = <Optional updated description>
movies = <Optional updated movies>
```
sample input data in JSON format for PUT
```sh
{
    "title": "My Collection",
    "description": "My collection of favorite movies",
    "movies": [
        {
            "title": "Movie 1",
            "description": "Description of Movie 1",
            "genres": "Action",
            "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a9"
        },
        {
            "title": "Movie 2",
            "description": "Description of Movie 2",
            "genres": "Comedy",
            "uuid": "13ecfdcc-1680-44d8-a9e7-a0d4c6e9386a"
        }
    ]
}
```


`http://localhost:8000/collection/<collection_uuid>/`

send a GET request in return you will get

```sh
{
    "movies": [
        {
            "title": "Movie 1",
            "description": "Description of Movie 1",
            "genres": "Action",
            "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a9"
        },
        {
            "title": "Movie 2",
            "description": "Description of Movie 2",
            "genres": "Comedy",
            "uuid": "13ecfdcc-1680-44d8-a9e7-a0d4c6e9386a"
        }
    ],
    "title": "My Collection",
    "description": "My collection of favorite movies"
}
```


`http://127.0.0.1:8000/request-count/`

send a GET request in return you will get
this endpoint is used to return count of total requests done in project
```sh
{
    "requests": 3
}
```


`http://127.0.0.1:8000/request-count/reset/`

send a POST request in return you will get
this endpoint is used to reset count of requests done in project
```sh
{
    "requests": "request count reset successfully"
}
```