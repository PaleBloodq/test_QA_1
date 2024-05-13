import asyncio
import logging
import os
import random
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

import aiohttp
import aiohttp.client_exceptions
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pydantic import BaseModel, HttpUrl, UUID4

ua = UserAgent()
BACKEND_URL = f'{os.environ.get("BACKEND_SCHEMA")}://{os.environ.get("BACKEND_HOST")}'
if os.environ.get("BACKEND_PORT"):
    BACKEND_URL += f':{os.environ.get("BACKEND_PORT")}'


class Product(BaseModel):
    product_id: UUID4
    url: HttpUrl


class Data(BaseModel):
    data: list[Product]
    need_notify: bool


@dataclass
class Edition:
    title: str
    final_price: str
    platforms: List[str]
    original_price: Optional[str] = None
    offer_ends: Optional[str] = None
    discount: Optional[int] = None
    image: Optional[str] = None
    release_date: Optional[str] = None

    final_price_int: int = field(init=False, repr=False)
    original_price_int: Optional[int] = field(init=False, repr=False)

    def __post_init__(self):
        self.final_price_int = self._normalize_price(self.final_price)
        self.original_price_int = self._normalize_price(self.original_price) if self.original_price else None
        self.final_price = self.final_price_int
        self.original_price = self.original_price_int if self.original_price_int else self.final_price_int
        self.offer_ends = self._parse_offer_ends(self.offer_ends)
        self.discount = self._calculate_discount(self.original_price_int, self.final_price_int)
        self.release_date = self._parse_release_date(self.release_date)

    @staticmethod
    def _normalize_price(price: Optional[str]) -> int:
        if not price or price == "Free":
            return 0
        normalized_price = float(price.split("\xa0")[0].replace(".", "").replace(",", "."))
        if normalized_price <= 899:
            exchange_rate = 5.5
        elif 900 <= normalized_price <= 1699:
            exchange_rate = 5.0
        else:
            exchange_rate = 4.5
        normalized_price *= exchange_rate
        normalized_price = round(normalized_price / 1000) * 1000 if normalized_price >= 1000 else normalized_price
        normalized_price = normalized_price - normalized_price % 5
        return int(normalized_price)

    @staticmethod
    def _parse_offer_ends(offer_ends: Optional[str]) -> Optional[str]:
        if offer_ends:
            return datetime.strptime(offer_ends, r"Offer ends %d/%m/%Y %I:%M %p %Z").isoformat()
        return None
    
    @staticmethod
    def _parse_release_date(release_date: Optional[str]) -> Optional[str]:
        if release_date:
            parsed_date = datetime.strptime(release_date, r"%d/%m/%Y")
            return parsed_date.date().isoformat()
        return None

    @staticmethod
    def _calculate_discount(original_price: Optional[int], final_price: int) -> Optional[int]:
        if original_price and original_price > final_price:
            return round((original_price / final_price - 1) * 100)
        return None


class Parser:
    processing_urls = set()
    _user_agent = lambda: ua.random
    headers = {
        "User-Agent": _user_agent()
    }

    def __init__(self):
        self.lock = asyncio.Lock()
        self.current_self_urls = set()
    async def parse_product(self, data: Data):
        async with self.lock:
            self.data = data
            for product in data.data:
                self.processing_urls.add(str(product.url))
                self.current_self_urls.add(str(product.url))
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for product in data.data:
                url = str(product.url)
                if url not in self.processing_urls or url in self.processing_urls:
                    try:
                        await self._parse_url(session, url, product.product_id)
                        await asyncio.sleep(random.randint(1, 4) - random.random())
                    except (
                            aiohttp.client_exceptions.ClientConnectionError,
                            AttributeError,
                            ValueError,
                    ) as e:
                        logging.error(f"Error parsing {url}: {e}")
                    finally:
                        async with self.lock:
                            self.processing_urls.remove(url)
                            self.current_self_urls.remove(url)

    async def _parse_url(self, session: aiohttp.ClientSession, url: str, product_id: UUID4):
        async with session.get(url) as response:
            if str(response.url) != url:
                return

            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            product_platforms = (
                soup.find("dd", {"data-qa": re.compile("platform-value")}).text.split(", ")
            )
            release_date = soup.find("dd", {"data-qa": re.compile("releaseDate-value")}).text
            editions = [
                self._parse_edition(soup_edition, product_platforms, release_date)
                for soup_edition in soup.find_all("article")
                if soup_edition.find("span", {"data-qa": re.compile("finalPrice")}).text != "Free"
            ]

            if editions:
                await self.send_publications(session, str(product_id), editions)

    @staticmethod
    def _parse_edition(soup_edition, product_platforms: List[str], release_date: str) -> Edition:
        title = soup_edition.find("h3", {"data-qa": re.compile("editionName")}).text
        final_price = soup_edition.find("span", {"data-qa": re.compile("finalPrice")}).text
        platforms = [
                        soup_platform.text
                        for soup_platform in soup_edition.find_all("span", {"data-qa": re.compile("productTag")})
                    ] or product_platforms
        original_price_tag = soup_edition.find("span", {"data-qa": re.compile("originalPrice")})
        original_price = original_price_tag.text if original_price_tag else None
        offer_ends_tag = soup_edition.find("span", {"data-qa": re.compile("discountDescriptor")})
        offer_ends = offer_ends_tag.text if offer_ends_tag else None
        image = soup_edition.find("img", {"data-qa": re.compile("media#image")}).get("src")
        return Edition(
            title=title,
            final_price=final_price,
            platforms=platforms,
            original_price=original_price,
            offer_ends=offer_ends,
            image=image,
            release_date=release_date,
        )

    async def send_publications(self, session: aiohttp.ClientSession, product_id: str, editions: List[Edition]):
        url = f"{BACKEND_URL}/api/product/{product_id}/publications/update/"
        data = {"publications": [edition.__dict__ for edition in editions], 'need_notify': self.data.need_notify}
        for _ in range(3):
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    break
                else:
                    await asyncio.sleep(1)
                    logging.error(f"Failed to send publications for product {product_id}")
