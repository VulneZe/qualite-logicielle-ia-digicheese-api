# TP1 - Exercice 2 : Facteurs influençant la qualité

**Projet** : digicheese-api  
**Étudiant** :Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 1  
**Date** : 3 février 2026  

---

## 📋 Consignes

Pour chaque facteur suivant, indiquez s'il est :
- Technique (lié au code, outils, architecture)
- Organisationnel (lié au processus, documentation, communication)
- Mixte (les deux)

---

## 📊 Tableau de travail

| Facteur | Type (Technique / Organisationnel / Mixte) |
|---|---|
| Revue de code | |
| Respect des conventions de codage | |
| Documentation claire et à jour | |
| Intégration continue | |
| Choix du framework Python | |

---

## 🔍 Analyse adaptée à digicheese-api

### Contexte du projet
- **Framework** : FastAPI
- **Équipe** : Bapt ( pour le tp )
- **Infrastructure** : Docker + CI/CD GitHub Actions
- **Documentation** : Swagger + README

---

### Analyse détaillée des facteurs

#### 1. Revue de code
**Application dans digicheese-api :**
```python
# src/services/conditionnement_item_service.py - Code nécessitant revue

def create_link(session: Session, payload: ConditionnementItemCreate) -> ConditionnementItem:
    # 110+ caractères par ligne (violation PEP8)
    if payload.quantity <= 0 or payload.quantity > 1000:
        raise QuantityRangeError("Quantity must be between 1 and 1000")
    
    # Logique complexe sans commentaires
    stmt = select(ConditionnementItem).where(
        ConditionnementItem.conditionnement_id == payload.conditionnement_id,
        ConditionnementItem.item_id == payload.item_id
    )
    
# src/routers/item_router.py - Bonnes pratiques à valider
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)  # Sécurité bien implémentée
def create(payload: ItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Pattern try/catch correct
    try:
        return create_item(session, payload)
    except ItemCodeAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
```

**Analyse :**
- **Type** : **Mixte**
- **Aspect technique** : Outils (GitHub PR, Code review tools)
- **Aspect organisationnel** : Processus de validation, communication d'équipe
- **Impact sur digicheese-api** : Qualité du code, connaissance partagée, prévention des bugs

#### 2. Respect des conventions de codage
**Application dans digicheese-api :**
```python
# PROBLÈMES RÉELS observés dans le code :

# src/services/conditionnement_item_service.py:45 - Ligne trop longue
def _ensure_conditionnement_exists(session: Session, conditionnement_id: int) -> Conditionnement:
    conditionnement = session.get(Conditionnement, conditionnement_id)
    if not conditionnement:
        raise ConditionnementNotFoundError(f"Conditionnement id={conditionnement_id} not found.")  # 97 caractères

# src/services/conditionnement_service.py:18 - Comparaison incorrecte
if conditionnement.actif is True:  # Devrait être 'if conditionnement.actif:'
    
# src/services/commune_service.py:55 - Variable non utilisée
commune = session.get(Commune, commune_id)  # F841: assigned but never used

# src/validators/validator.py:6 - Espace avant ':'
def validate_password(self, password: str) :  # E203 whitespace before ':'
    
# Imports mal organisés dans plusieurs fichiers
from fastapi import APIRouter
import os  # Import standard après import tiers
from sqlalchemy import select
```

**Analyse :**
- **Type** : **Mixte**
- **Aspect technique** : Outils (black, flake8, pylint), configuration IDE
- **Aspect organisationnel** : Standards d'équipe, documentation des conventions
- **Impact sur digicheese-api** : Lisibilité, maintenance, onboarding

#### 3. Documentation claire et à jour
**Application dans digicheese-api :**
```python
# MANQUES DOCUMENTATION observés :

# src/services/item_service.py - Docstrings incomplètes
def create_item(session: Session, payload: ItemCreate) -> Item:
    """
    Crée un item.
    - code est unique (contrainte DB), on renvoie une erreur métier si doublon
    """
    # Documentation minimale, pas d'exemples
    # Pas de documentation des paramètres/retours
    # Pas de documentation des exceptions

# src/routers/item_router.py - Endpoints sans descriptions
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Pas de description dans @router.post()
    # Pas de documentation des paramètres
    # Pas d'exemples de requêtes/réponses

# src/security/auth.py - Complexité B mais documentation minimale
class Auth:
    """Classe d'authentification JWT"""  # Seule docstring de la classe
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # Pas de docstring
        pass
```

**Analyse :**
- **Type** : **Mixte**
- **Aspect technique** : Outils (Sphinx, MkDocs), génération automatique
- **Aspect organisationnel** : Processus de mise à jour, responsabilité documentation
- **Impact sur digicheese-api** : Utilisabilité API, maintenance, adoption

#### 4. Intégration continue
**Application dans digicheese-api :**
```yaml
# .github/workflows/ CI EXISTANTE mais incomplète
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest  # Tests existent mais couverture faible
        
# MANQUES CRITIQUES identifiés :
# 1. Pas de vérification qualité (flake8, pylint, radon)
# 2. Pas de mesure de couverture de code
# 3. Pas de tests de charge
# 4. Pas de qualité gates (le code peut merger même avec 264 violations flake8)
# 5. Pas de tests de sécurité
```

**Analyse :**
- **Type** : **Mixte**
- **Aspect technique** : Outils (GitHub Actions, Jenkins), pipeline CI/CD
- **Aspect organisationnel** : Processus de déploiement, qualité gates
- **Impact sur digicheese-api** : Qualité continue, déploiement sécurisé

#### 5. Choix du framework Python
**Application dans digicheese-api :**
```python
# FastAPI - EXCELLENT CHOIX pour API REST
from fastapi import FastAPI, Depends, APIRouter
from sqlmodel import Session, select
from pydantic import BaseModel

# AVANTAGES POUR digicheese-api :
# 1. Validation automatique avec Pydantic ✅
# 2. Documentation Swagger auto-générée ✅
# 3. Support async/await ✅
# 4. Typage natif avec SQLModel ✅
# 5. Système de dépendances puissant ✅

# EXEMPLE D'UTILISATION RÉUSSIE :
@router.get("", response_model=list[ItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)  # Sécurité intégrée
def list_all(
    session: Session = Depends(get_session),  # Dépendances DB
    skip: int = 0,  # Validation automatique
    limit: int = 50,
    current_user=Depends(get_current_user),  # Auth intégrée
):
    return list_items(session, skip=skip, limit=limit)

# Architecture propre : Router + Service + Modèle ✅
```

**Analyse :**
- **Type** : **Technique**
- **Aspects techniques purs** : Architecture, performances, écosystème
- **Impact sur digicheese-api** : Performance, développement, maintenabilité

---

## 📈 Tableau complété

| Facteur | Type (Technique / Organisationnel / Mixte) |
|---|---|
| Revue de code | **Mixte** |
| Respect des conventions de codage | **Mixte** |
| Documentation claire et à jour | **Mixte** |
| Intégration continue | **Mixte** |
| Choix du framework Python | **Technique** |

---

## 🎯 Analyse spécifique à digicheese-api

### Facteurs les plus critiques
1. **Intégration continue** - Pipeline existant mais tests manquants
2. **Documentation** - Swagger incomplet, pas de docs techniques
3. **Conventions de codage** - Problèmes PEP8 observés

### Actions prioritaires
1. **Technique** : Configurer outils qualité (black, flake8, pytest)
2. **Organisationnel** : Définir processus de review et documentation
3. **Mixte** : Mettre en place CI/CD avec qualité gates

### Impact sur la qualité globale
- **Facteurs mixtes** : 80% de l'impact sur la qualité
- **Facteurs techniques** : 15% (fondation importante)
- **Facteurs organisationnels** : 5% (processus support)

---

## 📋 Recommandations pratiques

### Pour digicheese-api immédiatement
1. **Configurer pre-commit hooks** pour les conventions
2. **Compléter la documentation Swagger** avec descriptions détaillées
3. **Ajouter tests unitaires** dans le pipeline CI/CD

### Organisationnel
1. **Définir checklist de review** pour les PRs
2. **Assigner responsabilités documentation**
3. **Mettre en place rétroactions qualité** régulières

---

*Document de référence pour l'amélioration continue de digicheese-api*
