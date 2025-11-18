"""SQLAlchemy models package."""
from src.app import db
from src.models.bible import Livre, Chapitre, Verset

# Future models
# from src.models.fihirana import Chant

__all__ = ["db", "Livre", "Chapitre", "Verset"]
