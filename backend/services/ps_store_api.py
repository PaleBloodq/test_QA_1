import logging
import re
import requests
from api.serializers import ps_api as serializers


class PS_StoreAPI:
    API_URL = 'https://web.np.playstation.com/api/graphql/v1/'
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers['x-psn-store-locale-override'] = 'en-tr'
    
    def _get_by_product_id(self, product_id: str) -> dict:
        response = self.session.get(self.API_URL+f'op?operationName=metGetConceptByProductIdQuery&variables={{"productId":"{product_id}"}}&extensions={{"persistedQuery":{{"version":1,"sha256Hash":"0a4c9f3693b3604df1c8341fdc3e481f42eeecf961a996baaa65e65a657a6433"}}}}')
        return response.json()
    
    def _get_by_concept_id(self, concept_id: int) -> dict:
        response = self.session.get(self.API_URL+f'op?operationName=metGetPricingDataByConceptId&variables={{"conceptId":"{concept_id}"}}&extensions={{"persistedQuery":{{"version":1,"sha256Hash":"abcb311ea830e679fe2b697a27f755764535d825b24510ab1239a4ca3092bd09"}}}}')
        return response.json()
    
    def get_by_url(self, url: str) -> list[serializers.Edition]:
        logging.warning(f'Parse {url=}')
        if url:
            data = None
            match = re.match(r'https://store.playstation.com/en-tr/concept/(\d*)/?', url)
            if match:
                data = self._get_by_concept_id(match.group(1)).get('data')
                logging.warning('Concept found.')
            match = re.match(r'https://store.playstation.com/en-tr/product/([a-zA-Z0-9\-\_]*)/?', url)
            if match:
                data = self._get_by_product_id(match.group(1)).get('data')
                logging.warning('Product found.')
            if data:
                serializer = serializers.Data(data=data)
                if serializer.is_valid():
                    return serializer.get_editions()
            logging.warning('Data not found.')
        return []
