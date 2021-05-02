# Calendar API

## Running the app locally
- create a virtual env based on requirements.txt
- run `python3 manage.py migrate`
- run `python3 manage.py runsslserver 127.0.0.1:8000`

## API
### Users
First you need to create a user. You can either do that using django admin page, or with user endpoint:
```
curl --location --request POST 'https://127.0.0.1:8000/api/user/' \

--form 'email="asd@test.com"' \

--form 'password="asdasddsa"' \

--form 'username="testuser"' \
```

In the response you're going to get a token. Save it for further usage.

### Locations
Create a room:
```
curl --location --request POST 'https://127.0.0.1:8000/api/room/' \

--form 'manager="1"' \

--form 'name="Room1"' \

--form 'address="Address"'
```
### Events
Creating events:
****Enter the token you got earlier on to the headers****
```
curl --location --request POST 'https://127.0.0.1:8000/api/event/' \

--header 'Authorization: Token **your token** \

--header 'Content-Type: application/json' \

--data-raw '{

"name": "Meeting name",

"agenda": "Talking about important stuff",

"start": "2021-02-09 11:00",

"end": "2021-02-09 14:00",

"participants": ["asd@test.com"],

"location": 1

}'
```

Filtering events by location:
```https://127.0.0.1:8000/api/event?location_id=1```
Filtering by day:
```https://127.0.0.1:8000/api/day=2021-02-09```
Search events by name/agenda:
```https://127.0.0.1:8000/api/event?query=important+meeting```


### Tests
To run tests, run
```python3 manage.py test```


