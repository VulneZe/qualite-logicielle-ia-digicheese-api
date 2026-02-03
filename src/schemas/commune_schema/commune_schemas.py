# Schémas de validation pour les communes
from pydantic import Field
from sqlmodel import SQLModel
from typing import Optional

from src import ZipCode
from src.models.base.commune_base import CommuneBase
from src.schemas.zip_code_schema.zip_code_response import ZipCodeResponse


class CommuneCreate(SQLModel):
    """
    Schéma pour créer une nouvelle commune.
    
    Modifications par rapport à la version précédente :
    - Remplacement du champ 'code_postal' par 'code_postal_id' de type CodePostalEnum
    - Suppression du champ 'ville' (le nom de la commune suffit)
    - Conservation du nom et du statut actif
    """
    
    # Nom de la commune (obligatoire)
    nom: str = Field(min_length=2)
    
    # Code postal (ENUM pour validation stricte)
    zip_code_id: int

class CommuneUpdate(SQLModel):
    """
    Schéma pour modifier une commune existante.
    
    Modifications par rapport à la version précédente :
    - Remplacement du champ 'code_postal' par 'code_postal_id' de type CodePostalEnum
    - Suppression du champ 'ville' (le nom de la commune suffit)
    - Conservation du nom et du statut actif
    """
    
    # Nom de la commune (optionnel)
    nom: Optional[str] = Field(min_length=2, default=None)
    
    # Code postal (ENUM pour validation stricte)
    zip_code_id: Optional[int] = Field(default=None)

class CommuneResponse(CommuneBase):
    """
    Schéma pour les réponses API (retour des données commune).
    
    Modifications par rapport à la version précédente :
    - Remplacement du champ 'code_postal' par 'code_postal_id' de type CodePostalEnum
    - Suppression du champ 'ville' (le nom de la commune suffit)
    - Conservation du nom et du statut actif
    """
    id: int
    zip_code: ZipCodeResponse

