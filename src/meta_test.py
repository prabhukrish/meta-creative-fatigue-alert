import requests

ACCESS_TOKEN = "EAAR8gWxErEwBQHpRXnIbYKfd5Are4r7zDaZArqWGRWe38vCE3O1F9hNz5QlHzwXd3KRdQEU1LMZB98TwTq6ZBk6XXuAUYSn6BLHbn1AS3dFWPDSgEQzenj8IzG7IfcwGoesyiRzGptVTZBCgJgKttakIoxZAZCLhWybolE27bE6HVAq9ypgz3q2p6JmPTimK2T28rYvIVT7XlZAFIuGjMrLFQkS3GK1iRpzAE8tjauRFpslHvIZBpeAniTD5ufMobnqAap4n4JZCT7uQgSUcXUTcj"
AD_ACCOUNT_ID = "act_2038695363582581"

url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/ads"

params = {
    "fields": "id,name",
    "limit": 5,
    "access_token": ACCESS_TOKEN
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print("Response:", response.text)
