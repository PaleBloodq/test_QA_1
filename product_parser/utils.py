import os
from dataclasses import dataclass
import re
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
    platforms: list[str]
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
        if self.original_price and self.offer_ends:
            self.original_price = self.normalize_price(self.original_price)
            self.offer_ends = datetime.strptime(self.offer_ends, r'Offer ends %d/%m/%Y %I:%M %p %Z')
            self.discount = int(round(self.original_price / self.final_price * 100 - 100, 0))
        else:
            self.original_price = self.final_price


async def send_publications(session: aiohttp.ClientSession, product_id: str, editions: list[Edition]):
    url = f'{os.environ.get("BACKEND_HOST")}/api/product/{product_id}/publications/update/'
    data = {
        'publications': [
            {
                'title': edition.title,
                'platforms': edition.platforms,
                'final_price': edition.final_price,
                'original_price': edition.original_price,
                'offer_ends': edition.offer_ends.isoformat() if edition.offer_ends else None,
                'discount': edition.discount,
            } for edition in editions
        ]
    }
    await session.post(url, json=data)


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
                    product_platforms = soup.find('dd', {'data-qa': re.compile('platform-value')}).text.split(', ')
                    for soup_edition in soup.find_all('article'):
                        title = soup_edition.find('h3', {'data-qa': re.compile('editionName')}).text
                        final_price = soup_edition.find('span', {'data-qa': re.compile('finalPrice')}).text
                        if final_price == 'Free':
                            continue
                        platforms = [soup_platform.text for soup_platform in soup_edition.find_all('span', {'data-qa': re.compile('productTag')})] or product_platforms
                        original_price = soup_edition.find('span', {'data-qa': re.compile('originalPrice')})
                        original_price = original_price.text if original_price else None
                        offer_ends = soup_edition.find('span', {'data-qa': re.compile('discountDescriptor')})
                        offer_ends = offer_ends.text if offer_ends else None
                        editions.append(Edition(title, final_price, platforms, original_price, offer_ends))
                    if editions:
                        await send_publications(session, str(product.product_id), editions)
            except aiohttp.client_exceptions.ClientConnectionError:
                pass
