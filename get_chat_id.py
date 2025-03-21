import requests

TOKEN = "7635928850:AAHEK1R9na9MRbw1vJHuXyyHcXmN00Nzx-M"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
data = response.json()

cleaned_data = set()

for result in data.get('result', []):
    # Check 'message' updates
    message = result.get('message')
    if message:
        chat = message.get('chat')
        if chat and chat['type'] in ('group', 'supergroup'):
            cleaned_data.add((chat['title'], chat['id']))

    # Check 'my_chat_member' updates
    my_chat_member = result.get('my_chat_member')
    if my_chat_member:
        chat = my_chat_member.get('chat')
        if chat and chat['type'] in ('group', 'supergroup'):
            cleaned_data.add((chat['title'], chat['id']))

# Print cleaned data
for title, chat_id in cleaned_data:
    print({"group_name": title, "chat_id": chat_id})