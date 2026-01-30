import requests

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_alert(self, message):
        """Sends a real-time message to your Telegram app."""
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self.base_url, data=payload)
            return response.json()
        except Exception as e:
            print(f"Telegram Error: {e}")
            return None