import requests

firstToken = "1786136347163443200-8xjrI11sJOAyXpXkIlD1y4Ne39wKO1"
secondToken = "Z2KqHi5cZD5PHqve865FaBHkhIIusXZO4nbXNDvKhthFw"

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACfH3QEAAAAAqNrCg8F3TTyI8cM1%2BdFi3zd%2FA%2BE%3DFAOsTeMniuhoUxaezzRULDdDRqguQrmYDugeA1IjKhVB5epNDT"

username = "MnhmPynhs2957"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

url = f"https://api.twitter.com/2/users/by/username/{username}"

response = requests.get(url, headers=headers)
user_data = response.json()

print(user_data)
