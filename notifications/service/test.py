import time
import requests


while True:

    url = 'http://localhost:5555/start_alarm'
    data = {
        "event_name": "test_event_name",
        "secret_token": "my_super_secret_notifications_token"
    }

    response = requests.post(url, json=data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    delay = 3
    for i in range(delay):
        time.sleep(1)
        print (delay-i)


    url = 'http://localhost:5555/stop_alarm'
    data = {
        "event_name": "test_event_name",
        "secret_token": "my_super_secret_notifications_token"
    }

    response = requests.post(url, json=data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    delay = 3
    for i in range(delay):
        time.sleep(1)
        print (delay-i)

