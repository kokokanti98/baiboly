"""
Bible API endpoints using Flask-RESTful.
Provides REST API for accessing Bible books, chapters, and verses.
"""
from flask import Blueprint, request
from flask_restful import Api, Resource
from src.app import db
from src.services.bible_service import BibleService
from src.services.search_service import SearchService

# Create blueprint
bible_bp = Blueprint('bible', __name__)
api = Api(bible_bp)


class LivresResource(Resource):
    """Resource for listing all Bible books."""

    def get(self):
        """
        GET /api/bible/livres
        Query params:
            testament: Filter by testament (AT or NT)
        """
        testament = request.args.get('testament')
        service = BibleService(db.session)
        livres = service.get_all_livres(testament=testament)
        return livres, 200


class LivreResource(Resource):
    """Resource for a specific Bible book."""

    def get(self, livre_id):
        """GET /api/bible/livres/<id>"""
        service = BibleService(db.session)
        livre = service.get_livre_by_id(livre_id)

        if not livre:
            return {"error": "Tsy hita ny boky"}, 404

        return livre, 200


class LivreChapitresResource(Resource):
    """Resource for chapters of a specific book."""

    def get(self, livre_id):
        """GET /api/bible/livres/<id>/chapitres"""
        service = BibleService(db.session)

        # Verify livre exists
        livre = service.get_livre_by_id(livre_id)
        if not livre:
            return {"error": "Tsy hita ny boky"}, 404

        chapitres = service.get_chapitres_by_livre(livre_id)
        return chapitres, 200


class ChapitreResource(Resource):
    """Resource for a specific chapter."""

    def get(self, chapitre_id):
        """GET /api/bible/chapitres/<id>"""
        service = BibleService(db.session)
        chapitre = service.get_chapitre_by_id(chapitre_id)

        if not chapitre:
            return {"error": "Tsy hita ny toko"}, 404

        return chapitre, 200


class ChapitreVersetsResource(Resource):
    """Resource for verses of a specific chapter."""

    def get(self, chapitre_id):
        """GET /api/bible/chapitres/<id>/versets"""
        service = BibleService(db.session)

        # Verify chapitre exists
        chapitre = service.get_chapitre_by_id(chapitre_id)
        if not chapitre:
            return {"error": "Tsy hita ny toko"}, 404

        versets = service.get_versets_by_chapitre(chapitre_id)
        return versets, 200


class VersetResource(Resource):
    """Resource for a specific verse."""

    def get(self, verset_id):
        """GET /api/bible/versets/<id>"""
        service = BibleService(db.session)
        verset = service.get_verset_by_id(verset_id)

        if not verset:
            return {"error": "Tsy hita ny andininy"}, 404

        return verset, 200


class BibleReferenceResource(Resource):
    """Resource for getting verse by reference (e.g., Gen 1:1)."""

    def get(self):
        """
        GET /api/bible/reference
        Query params:
            livre: Book abbreviation (e.g., "Gen")
            chapitre: Chapter number
            verset: Verse number
        """
        livre_abbrev = request.args.get('livre')
        chapitre_numero = request.args.get('chapitre', type=int)
        verset_numero = request.args.get('verset', type=int)

        # Validate required parameters
        if not livre_abbrev or not chapitre_numero or not verset_numero:
            return {
                "error": "Ilaina ny 'livre', 'chapitre', ary 'verset'"
            }, 400

        service = BibleService(db.session)
        verset = service.get_verset_by_reference(
            livre_abbrev, chapitre_numero, verset_numero
        )

        if not verset:
            return {"error": "Tsy hita ny andininy"}, 404

        return verset, 200


class BibleReferenceRangeResource(Resource):
    """Resource for getting verses by reference range (e.g., Gen 1:1-5)."""

    def get(self):
        """
        GET /api/bible/reference-range
        Query params:
            ref: Full reference (e.g., "Genesis 1:5-7", "Gen 1:5-7")
        OR:
            livre: Book name or abbreviation
            chapitre: Chapter number
            verset_debut: Starting verse number
            verset_fin: Ending verse number (optional, defaults to verset_debut)
        """
        # Try to parse full reference string
        ref = request.args.get('ref', '').strip()

        if ref:
            # Parse reference like "Genesis 1:5-7" or "Gen 1:5-7"
            service = BibleService(db.session)
            result = service.parse_and_get_verse_range(ref)

            if result.get('error'):
                return result, 400

            return result, 200

        # Alternative: use separate parameters
        livre_param = request.args.get('livre')
        chapitre_numero = request.args.get('chapitre', type=int)
        verset_debut = request.args.get('verset_debut', type=int)
        verset_fin = request.args.get('verset_fin', type=int)

        if not livre_param or not chapitre_numero or not verset_debut:
            return {
                "error": "Ilaina ny 'ref' na 'livre', 'chapitre', 'verset_debut'"
            }, 400

        # If no end verse specified, use start verse
        if not verset_fin:
            verset_fin = verset_debut

        service = BibleService(db.session)
        versets = service.get_verse_range(
            livre_param, chapitre_numero, verset_debut, verset_fin
        )

        if not versets or len(versets) == 0:
            return {"error": "Tsy hita ny andininy"}, 404

        return {
            "versets": versets,
            "reference": f"{livre_param} {chapitre_numero}:{verset_debut}-{verset_fin}",
            "count": len(versets)
        }, 200


class BibleSearchResource(Resource):
    """Resource for searching verses by text."""

    def get(self):
        """
        GET /api/bible/search
        Query params:
            q: Search query (required)
            livre_id: Filter by book ID (optional)
            testament: Filter by testament (optional)
            limit: Results per page (default: 20)
            offset: Pagination offset (default: 0)
        """
        query = request.args.get('q', '').strip()

        if not query:
            return {"error": "Ilaina ny query 'q'"}, 400

        livre_id = request.args.get('livre_id', type=int)
        testament = request.args.get('testament')
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Limit pagination
        limit = min(limit, 100)  # Max 100 results per page

        service = SearchService(db.session)
        results = service.search_versets(
            query=query,
            livre_id=livre_id,
            testament=testament,
            limit=limit,
            offset=offset
        )

        # Get total count for pagination
        total = service.count_search_results(
            query=query,
            livre_id=livre_id,
            testament=testament
        )

        return {
            "results": results,
            "total": total,
            "limit": limit,
            "offset": offset,
            "query": query
        }, 200


# Register resources
api.add_resource(LivresResource, '/livres')
api.add_resource(LivreResource, '/livres/<int:livre_id>')
api.add_resource(LivreChapitresResource, '/livres/<int:livre_id>/chapitres')
api.add_resource(ChapitreResource, '/chapitres/<int:chapitre_id>')
api.add_resource(ChapitreVersetsResource, '/chapitres/<int:chapitre_id>/versets')
api.add_resource(VersetResource, '/versets/<int:verset_id>')
api.add_resource(BibleReferenceResource, '/reference')
api.add_resource(BibleReferenceRangeResource, '/reference-range')
api.add_resource(BibleSearchResource, '/search')
