import requests
import json

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

def test_message(data, expected):
    """Отправляет сообщение и проверяет корректность ответа."""
    result = send_message(data)

    print(json.dumps({
        "request": data,
        "result": {
            "answer": result,
            "isCorrect": result.get('success') is expected
        }
    }))

def test_root():
    """Проверяет, что корневой эндпоинт отвечает."""
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False

if __name__ == "__main__":
    print("=== Test started ===")

    test_root()
    
    test_message({"message": "Who was Ray's father?"}, True)

    test_message({"message": "What color were Christina's eyes?"}, True)

    test_message({"message": "How many Josephs did Ray own?"}, True)

    test_message({"message": "How many people lived in Nina?"}, False)

    test_message({"message": "Who created the first Joseph?"}, False)

    test_message({"message": "Who was the biggest Joseph?"}, False)

    test_message({"message": "Why did Stas always help Ray in dangerous situations?"}, True)

    test_message({"message": "Who was the strongest Joseph?"}, True)

    test_message({"message": "How does the Holy-gear work?"}, True)