# Énumération pour les statuts de commandes
from enum import Enum

class StatutEnum(Enum):
    """Statuts possibles pour une commande."""
    
    EN_ATTENTE = "en_attente"
    EN_PREPARATION = "en_preparation"
    PRETE = "prete"
    EN_LIVRAISON = "en_livraison"
    LIVREE = "livree"
    ANNULEE = "annulee"
