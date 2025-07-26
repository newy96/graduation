# Стойности на ангажираност/печалба за всяка стратегия
PAYOFF_MATRIX = {
    "Share": 1.0,    # висока видимост, но риск от невярна информация
    "Ignore": 0.1,   # пасивно поведение
    "Report": 0.7    # етично, умерен ефект
}

# Функция за получаване на оценка
def get_payoff(strategy: str) -> float:
    return PAYOFF_MATRIX.get(strategy, 0.0)

if __name__ == "__main__":
    # Тестов код – ще се изпълни само ако се стартира директно файла payoff.py
    for s in ["Share", "Ignore", "Report", "Unknown"]:
        print(f"Payoff for {s}: {get_payoff(s)}")
