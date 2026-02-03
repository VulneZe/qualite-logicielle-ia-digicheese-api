from enum import Enum

class ParcelTypeEnum(str, Enum):
    LETTRE = "lettre"
    PETIT_COLIS = "petit_colis"
    MOYEN_COLIS = "moyen_colis"
    GRAND_COLIS = "grand_colis"