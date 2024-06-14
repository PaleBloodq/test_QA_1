import logging
import requests
from . import serializers, models


class PS_StoreAPI:
    API_URL = 'https://web.np.playstation.com/api/graphql/v1/'
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers['x-psn-store-locale-override'] = 'en-tr'
    
    def _get_response(self, operation_name: str, variables: dict, sha256Hash: str) -> dict:
        url = self.API_URL
        url += f'op?operationName={operation_name}'
        url += f'&variables={variables}'
        url += f'&extensions={{"persistedQuery":{{"version":1,"sha256Hash":"{sha256Hash}"}}}}'
        url = url.replace(' ', '').replace('\'', '\"')
        return self.session.get(url).json()
    
    def _get_add_ons(self, product: models.Product, limit: int, offset: int) -> dict:
        return self._get_response(
            'metGetAddOnsByTitleId',
            {
                'npTitleId': product.np_title_id,
                'pageArgs': {
                    'size': limit,
                    'offset': offset
                }
            },
            'e98d01ff5c1854409a405a5f79b5a9bcd36a5c0679fb33f4e18113c157d4d916'
        ).get('data', {}).get('addOnProductsByTitleIdRetrieve', {})
    
    def _get_add_ons_amount(self, product: models.Product) -> int:
        return self._get_add_ons(product, 1, 0).get('pageInfo', {}).get('totalCount', 0)
    
    def _parse_add_ons(self, product: models.Product):
        add_ons_amount = self._get_add_ons_amount(product)
        if add_ons_amount == 0:
            return
        for add_on in self._get_add_ons(product, add_ons_amount, 0).get('addOnProducts'):
            serializer = serializers.AddOnSerializer(
                instance=models.AddOn.objects.filter(concept=product.concept, id=add_on.get('id')).first(),
                data=add_on
            )
            if serializer.is_valid():
                serializer.save(concept=product.concept)
            else:
                logging.warning(serializer.errors)
    
    def _parse_products(self, concept: models.Concept):
        for product in self._get_response(
            'metGetPricingDataByConceptId',
            {
                'conceptId': f'{concept.id}'
            },
            'abcb311ea830e679fe2b697a27f755764535d825b24510ab1239a4ca3092bd09'
        ).get('data').get('conceptRetrieve').get('selectableProducts').get('purchasableProducts'):
            serializer = serializers.ProductSerializer(
                instance=models.Product.objects.filter(concept=concept, id=product.get('id')).first(),
                data=product
            )
            if serializer.is_valid():
                self._parse_add_ons(serializer.save(concept=concept))
            else:
                logging.warning(serializer.errors)
    
    def parse_by_concept_id(self, concept_id: int) -> models.Concept | None:
        serializer = serializers.ConceptSerializer(
            instance=models.Concept.objects.filter(id=concept_id).first(),
            data=self._get_response(
                'metGetConceptById',
                {
                    'conceptId': str(concept_id)
                },
                'cc90404ac049d935afbd9968aef523da2b6723abfb9d586e5f77ebf7c5289006'
            ).get('data').get('conceptRetrieve'),
        )
        if serializer.is_valid():
            concept = serializer.save()
            self._parse_products(concept)
            return concept
        logging.warning(serializer.errors)
    
    def parse_by_product_id(self, product_id: str) -> models.Concept | None:
        concept_id = self._get_response(
            'metGetProductById',
            {
                'productId': product_id
            },
            'a128042177bd93dd831164103d53b73ef790d56f51dae647064cb8f9d9fc9d1a'
        ).get('data').get('productRetrieve').get('concept').get('id')
        return self.parse_by_concept_id(concept_id)
