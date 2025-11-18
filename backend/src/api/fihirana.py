"""
Fihirana API endpoints using Flask-RESTful.
Provides REST API for accessing hymns (fihirana).
"""
from flask import Blueprint, request
from flask_restful import Api, Resource
from src.app import db
from src.services.fihirana_service import FihiranaService

# Create blueprint
fihirana_bp = Blueprint('fihirana', __name__)
api = Api(fihirana_bp)


class FihiranaListResource(Resource):
    """Resource for listing fihirana."""

    def get(self):
        """
        GET /api/fihirana
        Query params:
            collection: Filter by collection (FFPM, Fanampiny, Antema)
            limit: Results per page (default: 100)
            offset: Pagination offset (default: 0)
        """
        collection = request.args.get('collection')
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Limit pagination
        limit = min(limit, 200)  # Max 200 results per page

        service = FihiranaService(db.session)
        fihiranas = service.get_all_fihirana(
            collection=collection, limit=limit, offset=offset
        )

        total = service.count_by_collection(collection=collection)

        return {
            "fihiranas": fihiranas,
            "total": total,
            "limit": limit,
            "offset": offset,
            "collection": collection,
        }, 200


class FihiranaResource(Resource):
    """Resource for a specific fihirana."""

    def get(self, fihirana_id):
        """GET /api/fihirana/<id>"""
        service = FihiranaService(db.session)
        fihirana = service.get_fihirana_by_id(fihirana_id)

        if not fihirana:
            return {"error": "Tsy hita ny fihirana"}, 404

        return fihirana, 200


class FihiranaByNumberResource(Resource):
    """Resource for getting fihirana by number."""

    def get(self):
        """
        GET /api/fihirana/numero
        Query params:
            numero: Hymn number (required)
            collection: Collection name (optional)
        """
        numero = request.args.get('numero', type=int)

        if not numero:
            return {"error": "Ilaina ny 'numero'"}, 400

        collection = request.args.get('collection')

        service = FihiranaService(db.session)
        fihirana = service.get_fihirana_by_number(numero, collection)

        if not fihirana:
            return {"error": "Tsy hita ny fihirana"}, 404

        return fihirana, 200


class FihiranaSearchResource(Resource):
    """Resource for searching fihirana by text."""

    def get(self):
        """
        GET /api/fihirana/search
        Query params:
            q: Search query (required)
            collection: Filter by collection (optional)
            limit: Results per page (default: 20)
            offset: Pagination offset (default: 0)
        """
        query = request.args.get('q', '').strip()

        if not query:
            return {"error": "Ilaina ny query 'q'"}, 400

        collection = request.args.get('collection')
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Limit pagination
        limit = min(limit, 100)  # Max 100 results per page

        service = FihiranaService(db.session)
        results = service.search_fihirana(
            query_text=query, collection=collection, limit=limit, offset=offset
        )

        # Get total count for pagination
        total = service.count_search_results(query_text=query, collection=collection)

        return {
            "results": results,
            "total": total,
            "limit": limit,
            "offset": offset,
            "query": query,
            "collection": collection,
        }, 200


# Register resources
api.add_resource(FihiranaListResource, '')
api.add_resource(FihiranaResource, '/<int:fihirana_id>')
api.add_resource(FihiranaByNumberResource, '/numero')
api.add_resource(FihiranaSearchResource, '/search')
