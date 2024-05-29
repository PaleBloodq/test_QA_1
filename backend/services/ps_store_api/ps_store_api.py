import logging
import re
import requests
from . import serializers


class PS_StoreAPI:
    API_URL = 'https://web.np.playstation.com/api/graphql/v1/'
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers['x-psn-store-locale-override'] = 'en-tr'
    
    def _get_by_product_id(self, product_id: str) -> list[dict]:
        response = self.session.get(self.API_URL+f'op?operationName=metGetConceptByProductIdQuery&variables={{"productId":"{product_id}"}}&extensions={{"persistedQuery":{{"version":1,"sha256Hash":"0a4c9f3693b3604df1c8341fdc3e481f42eeecf961a996baaa65e65a657a6433"}}}}')
        return response.json().get('data', {}).get('productRetrieve', {}).get('concept', {}).get('selectableProducts', {}).get('purchasableProducts', [])
    
    def _get_by_concept_id(self, concept_id: int) -> list[dict]:
        response = self.session.get(self.API_URL+f'op?operationName=metGetPricingDataByConceptId&variables={{"conceptId":"{concept_id}"}}&extensions={{"persistedQuery":{{"version":1,"sha256Hash":"abcb311ea830e679fe2b697a27f755764535d825b24510ab1239a4ca3092bd09"}}}}')
        return response.json().get('data', {}).get('conceptRetrieve', {}).get('selectableProducts', {}).get('purchasableProducts', [])
    
    def _get_editions(self, data: list[dict]) -> list[serializers.Edition]:
        serializer = serializers.ProductSerializer(data=data, many=True)
        if serializer.is_valid():
            return serializer.create(serializer.validated_data)
        logging.warning(serializer.errors)
        return []
    
    def get_by_url(self, url: str) -> list[serializers.Edition]:
        logging.warning(f'Parse {url=}')
        match = re.match(r'https://store.playstation.com/en-tr/(product|concept)/([a-zA-Z0-9\-\_]*)/?', url)
        if match:
            element_type = match.group(1)
            element_id = match.group(2)
        data = {
            'product': self._get_by_product_id,
            'concept': self._get_by_concept_id
        }.get(element_type)(element_id) if match else []
        return [
            edition
            for edition in self._get_editions(data) if all((
                edition.price.discounted_price,
                edition.price.base_price
            ))
        ]
