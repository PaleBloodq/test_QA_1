from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup


@dataclass
class Edition:
    product_id: str
    title: str
    final_price: int
    offer: list = None
    original_price: int = None
    offer_ends: datetime = None
    discount: int = None
    
    def normalize_price(self, price: str):
        price = float(price.split('\xa0')[0].replace('.', '').replace(',', '.'))
        if price <= 899:
            exchange_rate = 5.5
        elif 900 <= price <= 1699:
            exchange_rate = 5
        else:
            exchange_rate = 4.5
        price *= exchange_rate
        if price >= 1000 and price % 1000 < 25:
            price -= price % 1000 + 5
        if price % 5 > 0:
            price -= price % 5
        return int(price)
    
    def __post_init__(self):
        self.final_price = self.normalize_price(self.final_price)
        if self.offer:
            self.original_price = self.normalize_price(self.offer[0].text)
            self.offer_ends = datetime.strptime(self.offer[1].text, r'Offer ends %d/%m/%Y %I:%M %p %Z')
            self.discount = int(round(self.original_price / self.final_price * 100 - 100, 0))
        else:
            self.original_price = self.final_price
    
    # TODO: Прописать отправку издания в API
    def send(self):
        pass


def parse(product_id: str, url: str):
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        for soup_edition in soup.find_all('article'):
            try:
                title = soup_edition.find('h3').text
                final_price = soup_edition.find('span', {'class': 'psw-t-title-m'}).text
                if final_price == 'Free':
                    continue
                Edition(
                    product_id,
                    title,
                    final_price,
                    soup_edition.find_all('span', {'class': 'psw-c-t-2'}),
                ).send()
            except:
                pass
    except:
        pass
