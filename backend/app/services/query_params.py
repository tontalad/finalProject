from typing import Dict, List, Optional
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from models.query_params import QueryParams


class QueryParamsService:
    def __init__(self, collection: Collection):
        self.collection = collection

    async def build_and_execute_query(
        self,
        query_params: QueryParams
    ) -> List[Dict]:

        filter_query = query_params.filter_query or {}
        sort = query_params.sort
        skip = query_params.skip
        limit = query_params.limit
        projection = query_params.projection 
 
        print("filter_query", query_params)   
        sort_query = []
        if sort:
            for field, order in sort.items():
                sort_order_value = ASCENDING if order == "asc" else DESCENDING
                sort_query.append((field, sort_order_value))

        query = self.collection.find(filter_query, projection) 
        if sort_query:
            query = query.sort(sort_query)
        if skip is not None:
            query = query.skip(skip)
        if limit is not None:
            query = query.limit(limit)

        return await query.to_list(None)