"""SQLAlchemy models package."""
from src.app import db
from src.models.bible import Livre, Chapitre, Verset
from src.models.fihirana import Fihirana

__all__ = ["db", "Livre", "Chapitre", "Verset", "Fihirana"]
