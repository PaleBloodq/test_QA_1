import os
from dataclasses import dataclass
import aiohttp.client_exceptions
from pydantic import BaseModel, HttpUrl, UUID4
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup


class Product(BaseModel):
    product_id: UUID4
    url: HttpUrl


class Data(BaseModel):
    data: list[Product]


@dataclass
class Edition:
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


async def send_publications(session: aiohttp.ClientSession, product_id: str, editions: list[Edition]):
    url = f'{os.environ.get("BACKEND_HOST")}/api/product/{product_id}/publications/update/'
    data = {
        'publications': [
            {
                'title': edition.title,
                'final_price': edition.final_price,
                'original_price': edition.original_price,
                'offer_ends': edition.offer_ends.isoformat() if edition.offer_ends else None,
                'discount': edition.discount,
            } for edition in editions
        ]
    }
    await session.post(url, data=data)


async def parse_product(data: Data):
    async with aiohttp.ClientSession() as session:
        for product in data.data:
            try:
                async with session.get(str(product.url)) as response:
                    editions = []
                    if str(response.url) != str(product.url):
                        continue
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    for soup_edition in soup.find_all('article'):
                        title = soup_edition.find('h3').text
                        final_price = soup_edition.find('span', {'class': 'psw-t-title-m'}).text
                        if final_price == 'Free':
                            continue
                        editions.append(Edition(title, final_price, soup_edition.find_all('span', {'class': 'psw-c-t-2'})))
                    if editions:
                        await send_publications(session, str(product.product_id), editions)
            except aiohttp.client_exceptions.ClientConnectionError:
                pass
