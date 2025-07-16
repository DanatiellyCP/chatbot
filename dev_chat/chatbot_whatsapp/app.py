import requests

url = "http://localhost:8080/message/sendText/chatbot"

payload = {
    "number": "5511966366913",
    "textMessage": {"text": "Teste da Danny"}
}
headers = {
    "apikey": "7431242",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)