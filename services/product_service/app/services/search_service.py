from elasticsearch import AsyncElasticsearch
from ..config import settings

class SearchService:
    def __init__(self):
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
    
    async def search_products(self, query: str, limit: int = 10):
        return await self.es.search(
            index="products",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description"]
                    }
                },
                "size": limit
            }
        )