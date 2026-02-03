# Routes pour la gestion des rôles des utilisateurs (Admin uniquement)
# Ajouté le 19/01/2026 : Activation des décorateurs @is_granted pour sécuriser l'accès admin
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from src.config.database import get_session
from src.enum.role_enum import RoleEnum
from src.models.role import Role
from src.models.user import User
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter()

@router.post("/users/{user_id}/roles/{role}")
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut ajouter des rôles
def add_role_to_user(
    user_id: int,
    role: RoleEnum,
    session: Session = Depends(get_session),
):
    """
    Ajouter un rôle à un utilisateur.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut gérer les rôles de tous les utilisateurs
    - OP_COLIS: Ne peut PAS gérer les rôles (accès refusé)
    - OP_STOCK: Ne peut PAS gérer les rôles (accès refusé)
    """
    # 1) récupérer l'utilisateur
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # 2) récupérer le rôle en base
    db_role = session.exec(select(Role).where(Role.name == role.value)).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rôle introuvable en base")

    # 3) ajouter si pas déjà présent
    if db_role not in user.roles:
        user.roles.append(db_role)
        session.add(user)
        session.commit()

    return {"user_id": user_id, "added": role.value}


@router.delete("/users/{user_id}/roles/{role}")
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut supprimer des rôles
def remove_role_from_user(
    user_id: int,
    role: RoleEnum,
    session: Session = Depends(get_session),
):
    """
    Supprimer un rôle d'un utilisateur.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut gérer les rôles de tous les utilisateurs
    - OP_COLIS: Ne peut PAS gérer les rôles (accès refusé)
    - OP_STOCK: Ne peut PAS gérer les rôles (accès refusé)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    db_role = session.exec(select(Role).where(Role.name == role)).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Rôle introuvable en base")

    if db_role in user.roles:
        user.roles.remove(db_role)
        session.add(user)
        session.commit()

    return {"user_id": user_id, "removed": role.name}

@router.patch("/users/{user_id}/roles")
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut définir les rôles
def set_roles_for_user(
    user_id: int,
    roles: str = Query(..., description="CSV ex: ADMIN,OP_STOCK"),
    session: Session = Depends(get_session),
):
    """
    Définir les rôles d'un utilisateur (remplace tous les rôles existants).
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut gérer les rôles de tous les utilisateurs
    - OP_COLIS: Ne peut PAS gérer les rôles (accès refusé)
    - OP_STOCK: Ne peut PAS gérer les rôles (accès refusé)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # 1) Parser "ADMIN,OP_STOCK" -> [RoleEnum.ADMIN, RoleEnum.OP_STOCK]
    wanted: list[RoleEnum] = []
    for part in roles.split(","):
        name = part.strip().upper()
        if not name:
            continue
        if name not in RoleEnum.__members__:
            raise HTTPException(status_code=400, detail=f"Rôle invalide: {name}")
        wanted.append(RoleEnum[name])

    # 2) Charger les rôles en DB
    db_roles = session.exec(select(Role).where(Role.name.in_(wanted))).all()

    if len(db_roles) != len(set(wanted)):
        raise HTTPException(status_code=400, detail="Un ou plusieurs rôles n'existent pas en base")

    # 3) Remplacer complètement
    user.roles = db_roles
    session.add(user)
    session.commit()

    return {"user_id": user_id, "roles": [r.name for r in wanted]}

@router.get("/users/{user_id}/roles")
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut voir les rôles
def get_user_roles(
    user_id: int,
    session: Session = Depends(get_session),
):
    """
    Consulter les rôles d'un utilisateur.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut voir les rôles de tous les utilisateurs
    - OP_COLIS: Ne peut PAS voir les rôles (accès refusé)
    - OP_STOCK: Ne peut PAS voir les rôles (accès refusé)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return {
        "user_id": user_id,
        "roles": [r.name for r in user.roles],  # ex: ["ADMIN", "OP_STOCK"]
    }