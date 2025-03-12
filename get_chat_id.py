import requests

TOKEN = "7635928850:AAHEK1R9na9MRbw1vJHuXyyHcXmN00Nzx-M"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
print(response.json())  # Look for 'chat' -> 'id' in the output
