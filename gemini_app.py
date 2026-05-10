import os
import platform
from dotenv import load_dotenv
from google import genai

# Завантаження ключа з файлу .env
load_dotenv()

# Тарифи для моделі Gemini 1.5 Flash (ціна за 1 млн токенів)
PRICE_INPUT_1M = 0.075  # $
PRICE_OUTPUT_1M = 0.30  # $

def print_system_info():
    print(f"Операційна система: {platform.system()} {platform.release()}")
    print(f"Версія ядра/системи: {platform.version()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 40)

def calculate_usage(usage_metadata):
    # Отримання кількості токенів
    prompt_tokens = usage_metadata.prompt_token_count
    candidate_tokens = usage_metadata.candidates_token_count
    total_tokens = usage_metadata.total_token_count

    # Розрахунок вартості
    cost_in = (prompt_tokens / 1_000_000) * PRICE_INPUT_1M
    cost_out = (candidate_tokens / 1_000_000) * PRICE_OUTPUT_1M
    total_cost = cost_in + cost_out

    print(f"\n--- Статистика токенів ---")
    print(f"Токенів у запиті: {prompt_tokens}")
    print(f"Токенів у відповіді: {candidate_tokens}")
    print(f"Загальна кількість: {total_tokens}")
    print(f"Загальна вартість запиту: ${total_cost:.6f}")

def ask_gemini(client, text_query):
    print(f"\nЗапит: {text_query}")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=text_query
        )
        print(f"Відповідь:\n{response.text}")
        calculate_usage(response.usage_metadata)
    except Exception as e:
        print(f"Помилка API: {e}")

def main():
    print_system_info()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Помилка: GEMINI_API_KEY не знайдено в .env!")
        return

    client = genai.Client(api_key=api_key)

    # 1. Запит українською мовою
    ua_query = "Що таке штучний інтелект? В кінці відповіді наведіть список джерел із посиланнями."
    ask_gemini(client, ua_query)

    print("\n" + "="*50 + "\n")

    # 2. Запит англійською мовою
    en_query = "What is artificial intelligence? At the end of your answer, provide a list of sources with references."
    ask_gemini(client, en_query)

if __name__ == "__main__":
    main()