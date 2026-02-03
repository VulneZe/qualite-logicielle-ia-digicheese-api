# Modèle de base pour les communes
from sqlmodel import SQLModel, Field

class CommuneBase(SQLModel):
    """
    Modèle de base pour les communes.
    
    Modifications par rapport à la version précédente :
    - Remplacement du champ 'code_postal' par 'code_postal_id' de type CodePostalEnum
    - Suppression du champ 'ville' (le nom de la commune suffit)
    - Conservation du nom et du statut actif
    """
    
    # Nom de la commune (obligatoire)
    nom: str = Field(nullable=False, min_length=2)
