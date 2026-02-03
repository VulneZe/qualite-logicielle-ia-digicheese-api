# TP1 - Exercice 1 : Classification des problèmes de qualité

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 1  
**Date** : 3 février 2026  

---

## 📋 Consignes

Pour chaque problème listé ci-dessous :
1. Identifiez la dimension de qualité concernée (interne, externe, perçue)
2. Associez la ou les caractéristiques ISO/IEC 25010 correspondantes
3. Indiquez quelle(s) partie(s) prenante(s) serait(ent) impactée(s)

---

## 📊 Tableau de travail

| Problème | Dimension | Caractéristique ISO | Parties prenantes impactées |
|---|---|---|---|
| Méthode Python très longue et complexe | | | |
| Temps de réponse élevé d'un service | | | |
| Interface utilisateur peu intuitive | | | |
| Application instable en production | | | |
| Absence de tests automatisés | | | |

---

## 🔍 Analyse adaptée à digicheese-api

### Contexte du projet
- **API FastAPI** pour gestion de fromages
- **Endpoints** : CRUD produits, gestion stock, commandes
- **Technologies** : Python, FastAPI, SQLAlchemy, PostgreSQL

### Problèmes identifiés dans le code

#### 1. Méthode Python très longue et complexe
**Exemple concret dans digicheese-api :**
```python
# src/services/conditionnement_item_service.py - Fonctions complexes

def create_link(session: Session, payload: ConditionnementItemCreate) -> ConditionnementItem:
    """
    Crée un lien conditionnement-item avec validation complexe
    - 110 caractères de ligne (dépassement PEP8)
    - Logique de validation imbriquée
    - Plusieurs responsabilités
    """
    # Validation conditionnement existe
    conditionnement = session.get(Conditionnement, payload.conditionnement_id)
    if not conditionnement:
        raise ConditionnementNotFoundError(f"Conditionnement id={payload.conditionnement_id} not found.")
    
    # Validation item existe  
    item = session.get(Item, payload.item_id)
    if not item:
        raise ItemNotFoundError(f"Item id={payload.item_id} not found.")
        
    # Validation quantité
    if payload.quantity <= 0 or payload.quantity > 1000:
        raise QuantityRangeError("Quantity must be between 1 and 1000")
        
    # Vérification doublon
    stmt = select(ConditionnementItem).where(
        ConditionnementItem.conditionnement_id == payload.conditionnement_id,
        ConditionnementItem.item_id == payload.item_id
    )
    existing = session.exec(stmt).first()
    if existing:
        raise ConditionnementItemAlreadyExistsError("Link already exists")
        
    # Création et sauvegarde
    link = ConditionnementItem(**_dump(payload))
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
```

**Analyse :**
- **Dimension** : Interne
- **Caractéristiques ISO/IEC 25010** : 
  - Maintenabilité (Modifiabilité, Testabilité)
  - Réutilisabilité
- **Parties prenantes** : Développeurs, Équipe maintenance, Architectes

#### 2. Temps de réponse élevé d'un service
**Exemple concret dans digicheese-api :**
```python
# src/services/client_service.py - Requêtes N+1 potentielles

def get_clients(self, skip: int = 0, limit: int = 50) -> list[Client]:
    """
    Liste paginée simple - RISQUE N+1
    """
    stmt = select(Client).order_by(Client.id).offset(skip).limit(limit)
    clients = list(session.exec(stmt))
    
    # PROBLÈME : Pour chaque client, on pourrait faire des requêtes supplémentaires
    # si on charge les relations (commandes, adresses, etc.)
    return clients

# src/routers/item_router.py - Endpoint sans optimisation
@router.get("", response_model=list[ItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def list_all(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 50,
    current_user=Depends(get_current_user),
):
    # Pas de cache, pas de pagination optimisée
    return list_items(session, skip=skip, limit=limit)
```

**Analyse :**
- **Dimension** : Externe
- **Caractéristiques ISO/IEC 25010** :
  - Performance (Temps de réponse, Utilisation des ressources)
  - Efficacité
- **Parties prenantes** : Utilisateurs finaux, Client API, Équipe production

#### 3. Interface utilisateur peu intuitive
**Exemple concret dans digicheese-api :**
```python
# Réponses API mal structurées et documentation incomplète

# src/routers/item_router.py - Endpoints sans descriptions détaillées
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Pas de description dans le décorateur
    # Messages d'erreur génériques
    try:
        return create_item(session, payload)
    except ItemCodeAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

# Erreurs HTTP non standardisées
# 409 pour doublon (correct) mais messages d'erreur inconsistants
# Pas de documentation sur les formats d'erreur
# Swagger généré automatiquement mais sans descriptions métier
```

**Analyse :**
- **Dimension** : Perçue
- **Caractéristiques ISO/IEC 25010** :
  - Utilisabilité (Compréhensibilité, Apprenabilité)
  - Accessibilité
- **Parties prenantes** : Développeurs API, Clients API, Utilisateurs finaux

#### 4. Application instable en production
**Exemple concret dans digicheese-api :**
```python
# src/services/conditionnement_service.py - Gestion d'erreurs manquante

def update_conditionnement(self, conditionnement_id: int, payload: ConditionnementUpdate) -> Conditionnement:
    """
    Mise à jour conditionnement - PROBLÈMES DE FIABILITÉ
    """
    conditionnement = self.get_conditionnement_by_id(conditionnement_id)
    
    # PROBLÈME 1 : Pas de validation des données entrantes
    data = _dump(payload, exclude_unset=True)
    for key, value in data.items():
        setattr(conditionnement, key, value)
    
    # PROBLÈME 2 : Pas de transaction rollback en cas d'erreur
    session.add(conditionnement)
    session.commit()  # Si erreur ici, état inconsistant
    
    session.refresh(conditionnement)
    return conditionnement

# src/security/middleware.py - Middleware complexe avec complexité C
def jwt_validation_middleware(request: Request, call_next):
    # Complexité cyclomatique élevée (C)
    # Gestion d'erreurs partielle
    # Pas de logging approprié
    pass
```

**Analyse :**
- **Dimension** : Externe
- **Caractéristiques ISO/IEC 25010** :
  - Fiabilité (Maturité, Tolérance aux fautes)
  - Disponibilité
- **Parties prenantes** : Utilisateurs finaux, Équipe production, Support client

#### 5. Absence de tests automatisés
**Exemple concret dans digicheese-api :**
```python
# Structure tests actuelle :
# tests/ - DOSSIER EXISTANT MAIS PEU STRUCTURÉ

# tests/conftest.py - Configuration minimale
# tests/test_auth.py - Quelques tests basiques
# tests/test_items.py - Tests incomplets

# MANQUES CRITIQUES :
# 1. Pas de tests pour les services complexes (ConditionnementItemService)
# 2. Pas de tests d'intégration API
# 3. Pas de tests de charge
# 4. Pas de tests de sécurité
# 5. Couverture de code probablement faible

# Exemple de service non testé :
# src/services/conditionnement_item_service.py - 127 lignes, 0 tests
# src/services/stock_line_service.py - Complexité B, 0 tests
# src/security/auth.py - Complexité B, tests minimaux
```

**Analyse :**
- **Dimension** : Interne
- **Caractéristiques ISO/IEC 25010** :
  - Fiabilité (Testabilité)
  - Maintenabilité (Modifiabilité)
- **Parties prenantes** : Développeurs, Équipe QA, Architectes, Chef de projet

---

## 📈 Tableau complété

| Problème | Dimension | Caractéristique ISO | Parties prenantes impactées |
|---|---|---|---|
| Méthode Python très longue et complexe | **Interne** | Maintenabilité, Réutilisabilité | Développeurs, Maintenance, Architectes |
| Temps de réponse élevé d'un service | **Externe** | Performance, Efficacité | Utilisateurs, Client API, Production |
| Interface utilisateur peu intuitive | **Perçue** | Utilisabilité, Accessibilité | Développeurs API, Clients API, Utilisateurs |
| Application instable en production | **Externe** | Fiabilité, Disponibilité | Utilisateurs, Production, Support |
| Absence de tests automatisés | **Interne** | Fiabilité, Maintenabilité | Développeurs, QA, Architectes, Chef de projet |

---

## 🎯 Synthèse spécifique à digicheese-api

### Problèmes prioritaires identifiés
1. **Absence de tests automatisés** - Bloquant pour la qualité
2. **Application instable en production** - Critique pour les utilisateurs
3. **Temps de réponse élevé** - Impact direct l'expérience utilisateur

### Actions recommandées
1. **Immédiat** : Mettre en place tests unitaires pour les services critiques
2. **Court terme** : Améliorer la gestion d'erreurs et les transactions
3. **Moyen terme** : Optimiser les requêtes et refactoriser les méthodes complexes

---

*Document de référence pour l'audit qualité de digicheese-api*
