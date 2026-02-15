import requests
import sys

# Адрес, на котором запущен сервис (по умолчанию localhost:5000)
BASE_URL = "http://localhost:5000"

def send_message(data):
    """Отправляет POST-запрос с JSON-данными на /message и возвращает ответ."""
    url = f"{BASE_URL}/message"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # выбросит исключение при HTTP-ошибке
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def test_message(data):
    """Отправляет сообщение и проверяет корректность ответа."""
    print(f"Send: {data}")
    result = send_message(data)
    if result is None:
        print(f"Error")
        return False

    print(f"Answer: {result}")

    return True

def test_root():
    """Проверяет, что корневой эндпоинт отвечает."""
    print("\nCheck root GET /")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        print(f"Answer: {response.text}")
        print("Root endpoint is OK")
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False

if __name__ == "__main__":
    print("=== Test started ===")

    test_root()
    
    test_message({"message": "Who was Ray's father?"})

    test_message({"message": "What color were Christina's eyes?"})

    test_message({"message": "How many Josephs did Ray own?"})

    test_message({"message": "How many people lived in Nina?"})

    test_message({"message": "Who created the first Joseph?"})

    test_message({"message": "Who was the biggest Joseph?"})

    test_message({"message": "Why did Stas always help Ray in dangerous situations?"})

    test_message({"message": "Who was the strongest Joseph?"})

    test_message({"message": "How does the Holy-gear work?"})