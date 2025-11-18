# services/chat_service.py
import requests

def send_chat(message):
    
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAqOd00nE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=B2p6UxNVx1tww6eGVTMWggsFtPUSrAirIz_rINEgsD4https://chat.googleapis.com/v1/spaces/AAQAqOd00nE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=B2p6UxNVx1tww6eGVTMWggsFtPUSrAirIz_rINEgsD4"
    
    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)

        if response.status_code != 200:
            print("Chat webhook error:", response.text)

    except Exception as e:
        print("Chat Webhook Exception:", e)