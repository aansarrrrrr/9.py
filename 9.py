import requests
from html.parser import HTMLParser

# Класс для парсинга HTML и извлечения курса доллара
class CurrencyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_in_usd_row = False
        self.usd_rate = None

    def handle_starttag(self, tag, attrs):
        # Ищем начало строки с курсом доллара
        if tag == 'td' and ('data-currency', 'USD') in attrs:
            self.is_in_usd_row = True

    def handle_endtag(self, tag):
        if tag == 'td' and self.is_in_usd_row:
            self.is_in_usd_row = False

    def handle_data(self, data):
        if self.is_in_usd_row:
            # Сохраняем курс, когда находим нужный элемент
            self.usd_rate = data.strip().replace(',', '.')
    
    def get_usd_rate(self):
        return float(self.usd_rate) if self.usd_rate else None

# Функция для получения курса доллара с сайта Национального банка Казахстана
def get_usd_rate():
    url = 'https://www.nationalbank.kz/cont/print.php?docid=144&lang=rus'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Не удалось загрузить страницу.")
        return None
    
    html_data = response.text
    parser = CurrencyHTMLParser()
    parser.feed(html_data)
    
    return parser.get_usd_rate()


# Пример класса конвертера валют
class CurrencyConverter:
    def __init__(self, exchange_rate):
        self.exchange_rate = exchange_rate  # Курс валюты

    def convert_to_usd(self, amount):
        return amount / self.exchange_rate  # Конвертируем валюту в доллары США

    def convert_from_usd(self, amount):
        return amount * self.exchange_rate  # Конвертируем доллары США в национальную валюту

# Пример использования
if __name__ == "__main__":
    try:
        usd_rate = get_usd_rate()  # Получаем текущий курс доллара
        if usd_rate:
            print(f"Текущий курс доллара США: {usd_rate} KZT за 1 USD")

            # Создаем объект конвертера
            converter = CurrencyConverter(usd_rate)

            # Получаем количество валюты от пользователя
            amount_in_local_currency = float(input("Введите сумму в вашей валюте: "))
            amount_in_usd = converter.convert_to_usd(amount_in_local_currency)
            print(f"{amount_in_local_currency} вашей валюты = {amount_in_usd:.2f} USD")
        else:
            print("Не удалось получить курс доллара.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
