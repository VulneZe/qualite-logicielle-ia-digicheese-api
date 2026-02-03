from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from src.config.database import get_session
from src.models.conditionnement import Conditionnement
from src.schemas.conditionnement_schema.conditionnement_schemas import (
    ConditionnementCreate,
    ConditionnementUpdate,
    ConditionnementResponse
)
from src.security.guard.role_gard_decorator import is_granted
from src.enum.role_enum import RoleEnum

router = APIRouter(
    prefix="/conditionnements",
    tags=["Conditionnements"],
    responses={
        401: {"description": "Non authentifié"},
        403: {"description": "Permissions insuffisantes"},
        404: {"description": "Conditionnement non trouvé"},
        422: {"description": "Erreur de validation"}
    }
)

@router.get("/", response_model=List[ConditionnementResponse])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
def get_all_conditionnements(session: Session = Depends(get_session)):
    """Récupérer tous les conditionnements actifs.
    
    - **ADMIN** : Accès complet
    - **OP_COLIS** : Lecture autorisée
    - **OP_STOCK** : Lecture autorisée
    """
    statement = select(Conditionnement).where(Conditionnement.is_active == True)
    conditionnements = session.exec(statement).all()
    return conditionnements

@router.get("/{conditionnement_id}", response_model=ConditionnementResponse)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
def get_conditionnement(conditionnement_id: int, session: Session = Depends(get_session)):
    """Récupérer un conditionnement par son ID.
    
    - **ADMIN** : Accès complet
    - **OP_COLIS** : Lecture autorisée
    - **OP_STOCK** : Lecture autorisée
    """
    conditionnement = session.get(Conditionnement, conditionnement_id)
    if not conditionnement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conditionnement non trouvé"
        )
    return conditionnement

@router.post("/", response_model=ConditionnementResponse, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def create_conditionnement(
    conditionnement_data: ConditionnementCreate,
    session: Session = Depends(get_session)
):
    """Créer un nouveau conditionnement.
    
    - **ADMIN** : Création autorisée
    - **OP_COLIS** : Création autorisée
    - **OP_STOCK** : Création non autorisée
    
    **Champs requis** :
    - libelle: str (ex: "Boîte 500g")
    - poids: int (en grammes)
    - prix: float (en euros)
    """
    conditionnement = Conditionnement(**conditionnement_data.dict())
    session.add(conditionnement)
    session.commit()
    session.refresh(conditionnement)
    return conditionnement

@router.patch("/{conditionnement_id}", response_model=ConditionnementResponse)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def update_conditionnement(
    conditionnement_id: int,
    conditionnement_data: ConditionnementUpdate,
    session: Session = Depends(get_session)
):
    """Mettre à jour un conditionnement (mise à jour partielle).
    
    - **ADMIN** : Mise à jour autorisée
    - **OP_COLIS** : Mise à jour autorisée
    - **OP_STOCK** : Mise à jour non autorisée
    
    **Note** : Seuls les champs fournis sont mis à jour
    """
    conditionnement = session.get(Conditionnement, conditionnement_id)
    if not conditionnement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conditionnement non trouvé"
        )
    
    # Mise à jour des champs fournis
    update_data = conditionnement_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conditionnement, field, value)
    
    session.add(conditionnement)
    session.commit()
    session.refresh(conditionnement)
    return conditionnement

@router.delete("/{conditionnement_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_conditionnement(conditionnement_id: int, session: Session = Depends(get_session)):
    """Supprimer un conditionnement (désactivation).
    
    - **ADMIN** : Suppression autorisée
    - **OP_COLIS** : Suppression non autorisée
    - **OP_STOCK** : Suppression non autorisée
    
    **Note** : Le conditionnement est désactivé, pas supprimé physiquement
    """
    conditionnement = session.get(Conditionnement, conditionnement_id)
    if not conditionnement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conditionnement non trouvé"
        )
    
    # Désactivation au lieu de suppression
    conditionnement.is_active = False
    session.add(conditionnement)
    session.commit()
    return None
