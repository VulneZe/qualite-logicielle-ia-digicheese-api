# # Router pour les détails de commande
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, select
# from typing import List
# from decimal import Decimal
#
# from src.config.database import get_session
# from src.models.detail_commande import DetailCommande
# from src.models.conditionnement import Conditionnement
# from src.schemas.detail_commande_schema.detail_commande_schemas import (
#     DetailCommandeCreate,
#     DetailCommandeUpdate,
#     DetailCommandeResponse,
#     DetailCommandeWithConditionnement
# )
# from src.security.guard.role_gard_decorator import is_granted
# from src.enum.role_enum import RoleEnum
#
# router = APIRouter(
#     responses={
#         401: {"description": "Non authentifié"},
#         403: {"description": "Permissions insuffisantes"},
#         404: {"description": "Détail de commande non trouvé"},
#         422: {"description": "Erreur de validation"}
#     }
# )
#
# def calculate_total_ligne(quantite: int, prix_unitaire: Decimal) -> Decimal:
#     """Calculer le total de la ligne."""
#     return quantite * prix_unitaire
#
# @router.get("/", response_model=List[DetailCommandeResponse])
# @is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
# def get_all_details(session: Session = Depends(get_session)):
#     """Récupérer tous les détails de commande.
#
#     - **ADMIN** : Accès complet
#     - **OP_COLIS** : Lecture autorisée
#     - **OP_STOCK** : Lecture autorisée
#     """
#     statement = select(DetailCommande)
#     details = session.exec(statement).all()
#     return details
#
# @router.get("/{detail_id}", response_model=DetailCommandeResponse)
# @is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
# def get_detail(detail_id: int, session: Session = Depends(get_session)):
#     """Récupérer un détail de commande par son ID.
#
#     - **ADMIN** : Accès complet
#     - **OP_COLIS** : Lecture autorisée
#     - **OP_STOCK** : Lecture autorisée
#     """
#     detail = session.get(DetailCommande, detail_id)
#     if not detail:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Détail de commande non trouvé"
#         )
#     return detail
#
# @router.get("/commande/{commande_id}", response_model=List[DetailCommandeWithConditionnement])
# @is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
# def get_details_by_commande(commande_id: int, session: Session = Depends(get_session)):
#     """Récupérer les détails d'une commande spécifique.
#
#     - **ADMIN** : Accès complet
#     - **OP_COLIS** : Lecture autorisée
#     - **OP_STOCK** : Lecture autorisée
#     """
#     statement = (
#         select(DetailCommande, Conditionnement)
#         .join(Conditionnement)
#         .where(DetailCommande.commande_id == commande_id)
#     )
#     results = session.exec(statement).all()
#
#     details_with_conditionnement = []
#     for detail, conditionnement in results:
#         detail_with_conditionnement = DetailCommandeWithConditionnement(
#             id=detail.id,
#             commande_id=detail.commande_id,
#             conditionnement_id=detail.conditionnement_id,
#             quantite=detail.quantite,
#             colis=detail.colis,
#             commentaire=detail.commentaire,
#             total_ligne=detail.total_ligne,
#             created_at=detail.created_at,
#             updated_at=detail.updated_at,
#             conditionnement_libelle=conditionnement.libelle,
#             conditionnement_poids=conditionnement.poids,
#             conditionnement_prix=conditionnement.prix
#         )
#         details_with_conditionnement.append(detail_with_conditionnement)
#
#     return details_with_conditionnement
#
# @router.post("/", response_model=DetailCommandeResponse, status_code=status.HTTP_201_CREATED)
# @is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
# def create_detail(
#     detail_data: DetailCommandeCreate,
#     session: Session = Depends(get_session)
# ):
#     """Créer un nouveau détail de commande.
#
#     - **ADMIN** : Création autorisée
#     - **OP_COLIS** : Création autorisée
#     - **OP_STOCK** : Création non autorisée
#
#     **Calcul automatique** : total_ligne = quantite × prix_unitaire
#     """
#     # Vérifier que le conditionnement existe
#     conditionnement = session.get(Conditionnement, detail_data.conditionnement_id)
#     if not conditionnement:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Conditionnement non trouvé"
#         )
#
#     # Calculer le total automatiquement
#     total_ligne = calculate_total_ligne(detail_data.quantite, conditionnement.prix)
#
#     # Créer le détail
#     detail = DetailCommande(
#         commande_id=detail_data.commande_id,
#         conditionnement_id=detail_data.conditionnement_id,
#         quantite=detail_data.quantite,
#         colis=detail_data.colis,
#         commentaire=detail_data.commentaire,
#         total_ligne=total_ligne
#     )
#
#     session.add(detail)
#     session.commit()
#     session.refresh(detail)
#     return detail
#
# @router.patch("/{detail_id}", response_model=DetailCommandeResponse)
# @is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
# def update_detail(
#     detail_id: int,
#     detail_data: DetailCommandeUpdate,
#     session: Session = Depends(get_session)
# ):
#     """Mettre à jour un détail de commande.
#
#     - **ADMIN** : Mise à jour autorisée
#     - **OP_COLIS** : Mise à jour autorisée
#     - **OP_STOCK** : Mise à jour non autorisée
#
#     **Calcul automatique** : Si la quantite change, total_ligne est recalculé
#     """
#     detail = session.get(DetailCommande, detail_id)
#     if not detail:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Détail de commande non trouvé"
#         )
#
#     # Mise à jour des champs fournis
#     update_data = detail_data.dict(exclude_unset=True)
#
#     # Si la quantité change, recalculer le total
#     if "quantite" in update_data:
#         conditionnement = session.get(Conditionnement, detail.conditionnement_id)
#         update_data["total_ligne"] = calculate_total_ligne(
#             update_data["quantite"],
#             conditionnement.prix
#         )
#
#     for field, value in update_data.items():
#         setattr(detail, field, value)
#
#     session.add(detail)
#     session.commit()
#     session.refresh(detail)
#     return detail
#
# @router.delete("/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
# @is_granted(RoleEnum.ADMIN)
# def delete_detail(detail_id: int, session: Session = Depends(get_session)):
#     """Supprimer un détail de commande.
#
#     - **ADMIN** : Suppression autorisée
#     - **OP_COLIS** : Suppression non autorisée
#     - **OP_STOCK** : Suppression non autorisée
#     """
#     detail = session.get(DetailCommande, detail_id)
#     if not detail:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Détail de commande non trouvé"
#         )
#
#     session.delete(detail)
#     session.commit()
#     return None
