# Énumération des types de conditionnement pour fromagerie
from enum import Enum

class TypeConditionnementEnum(str, Enum):
    """Types de conditionnement disponibles pour les produits fromagers."""
    
    BOITE = "BOITE"
    SAC = "SAC"
    VACUUM = "VACUUM"
    ORIGINAL = "ORIGINAL"
    CAISSE = "CAISSE"
    PLATEAU = "PLATEAU"
    POT = "POT"
