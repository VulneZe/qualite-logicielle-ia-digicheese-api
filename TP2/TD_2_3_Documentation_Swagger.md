# TD 2.3 — Documentation automatique avec Swagger/OpenAPI

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 2  
**Date** : 3 février 2026  

---

## 🎯 Objectif du TP

Apprendre à générer, lire et analyser la documentation automatique d'une API FastAPI avec Swagger/OpenAPI, et utiliser l'IA pour résumer et identifier les améliorations possibles.

---

## 🔍 Accéder à la documentation Swagger

### 1. Démarrage de l'application

```bash
# Démarrer l'API digicheese-api
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Accès à la documentation
# Swagger UI : http://localhost:8000/docs
# OpenAPI JSON : http://localhost:8000/openapi.json
# ReDoc : http://localhost:8000/redoc
```

### 2. Vérification des endpoints

L'application digicheese-api expose les endpoints suivants :

```python
# src/main.py - Configuration des routers
app.include_router(api_router)
app.include_router(item_router)          # /items
app.include_router(price_router)         # /prices  
app.include_router(stock_router)          # /stocks
app.include_router(stock_line_router)     # /stock_lines
app.include_router(update_item_router)    # /update_items
app.include_router(update_router)         # /updates
app.include_router(shop_router)           # /shops
app.include_router(order_item_router)     # /order_items
app.include_router(conditionnement_item_router)  # /conditionnement_items
```

---

## 📊 Analyse des endpoints

### Endpoints principaux analysés

#### 1. Items Management (`/items`)

```python
# src/routers/item_router.py
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    """Créer un nouvel item"""

@router.get("", response_model=list[ItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)  
def list_all(session: Session = Depends(get_session), skip: int = 0, limit: int = 50, current_user=Depends(get_current_user)):
    """Lister tous les items avec pagination"""

@router.get("/{item_id}", response_model=ItemRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def get_one(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    """Récupérer un item par son ID"""

@router.patch("/{item_id}", response_model=ItemRead)
@is_granted(RoleEnum.ADMIN)
def patch_one(item_id: int, patch: ItemUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    """Mettre à jour partiellement un item"""

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_one(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    """Supprimer un item"""
```

#### 2. Stocks Management (`/stocks`)

```python
# src/routers/stock_router.py
@router.post("", response_model=StockRead, status_code=status.HTTP_201_CREATED)
def create(payload: StockCreate, session: Session = Depends(get_session)):
    """Créer un stock"""

@router.get("", response_model=list[StockRead])
def list_all(session: Session = Depends(get_session)):
    """Lister tous les stocks"""

@router.get("/{stock_id}", response_model=StockRead)
def get_one(stock_id: int, session: Session = Depends(get_session)):
    """Récupérer un stock par ID"""

@router.patch("/{stock_id}", response_model=StockRead)
def patch_one(stock_id: int, patch: StockUpdate, session: Session = Depends(get_session)):
    """Mettre à jour un stock"""

@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(stock_id: int, session: Session = Depends(get_session)):
    """Supprimer un stock"""
```

#### 3. Authentication (si disponible)

```python
# src/routers/auth_router.py (hypothétique)
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginCredentials, session: Session = Depends(get_session)):
    """Authentifier un utilisateur et retourner un token JWT"""

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: RefreshTokenRequest, session: Session = Depends(get_session)):
    """Rafraîchir un token JWT"""
```

---

## 📋 Tableau de synthèse des endpoints

| Endpoint | Méthode | Paramètres | Réponses | Commentaires / Tests |
|---|---|---|---|---|
| **/health** | GET | - | 200 OK + status | ✅ Endpoint de santé fonctionnel |
| **/items** | POST | ItemCreate (body) | 201 Created, 401 Unauthorized, 422 Validation, 409 Conflict | ✅ Création item, validation code unique |
| **/items** | GET | skip, limit (query) | 200 OK + liste items | ✅ Pagination, filtres |
| **/items/{id}** | GET | item_id (path) | 200 OK + item, 404 Not Found | ✅ Récupération par ID |
| **/items/{id}** | PATCH | item_id (path), ItemUpdate (body) | 200 OK + item, 401 Unauthorized, 404 Not Found, 409 Conflict | ✅ Mise à jour partielle |
| **/items/{id}** | DELETE | item_id (path) | 204 No Content, 401 Unauthorized, 404 Not Found | ✅ Suppression item |
| **/stocks** | POST | StockCreate (body) | 201 Created, 422 Validation | ✅ Création stock |
| **/stocks** | GET | - | 200 OK + liste stocks | ✅ Liste stocks |
| **/stocks/{id}** | GET | stock_id (path) | 200 OK + stock, 404 Not Found | ✅ Détail stock |
| **/stocks/{id}** | PATCH | stock_id (path), StockUpdate (body) | 200 OK + stock, 404 Not Found | ✅ Mise à jour stock |
| **/stocks/{id}** | DELETE | stock_id (path) | 204 No Content, 404 Not Found | ✅ Suppression stock |
| **/prices** | POST | PriceCreate (body) | 201 Created, 409 Conflict | ⚠️ Prix unique par item |
| **/prices** | GET | - | 200 OK + liste prices | ✅ Liste prix |
| **/shops** | POST | ShopCreate (body) | 201 Created | ✅ Création magasin |
| **/order_items** | POST | OrderItemCreate (body) | 201 Created, 422 Validation | ⚠️ Complexité validation |

---

## 🤖 Utilisation de l'IA pour résumer la documentation

### Prompt IA pour analyse OpenAPI

```prompt
Rôle : Expert en documentation API et OpenAPI
Contexte : J'ai une API FastAPI pour la gestion de fromages (digicheese-api)
Objectif : Analyser la spécification OpenAPI et générer un résumé structuré

Spécification OpenAPI fournie :
- Endpoint /items : CRUD complet avec authentification
- Endpoint /stocks : Gestion des stocks  
- Endpoint /prices : Gestion des prix
- Endpoint /shops : Gestion des magasins
- Endpoint /order_items : Gestion des commandes
- Endpoint /health : Health check

Contraintes :
- Résumer les endpoints, méthodes, paramètres
- Identifier les formats de réponse et codes d'erreur
- Détecter les incohérences ou manques
- Proposer des améliorations de documentation
- Identifier les tests manquants
- Présenter sous forme de tableau clair

Format de sortie :
- Tableau synthétique par endpoint
- Liste des problèmes identifiés
- Recommandations d'amélioration
- Tests unitaires/intégration manquants
```

### Résumé IA généré

```markdown
## Analyse OpenAPI - DigiCheese API

### Résumé des endpoints

| Endpoint | Méthodes | Authentification | Validation | Complexité |
|---|---|---|---|---|
| **/items** | CRUD complet | ADMIN/OP_COLIS | Code unique, Pydantic | Élevée |
| **/stocks** | CRUD complet | Aucune | Quantité valide | Moyenne |
| **/prices** | CRUD simple | Aucune | Unicité par item | Moyenne |
| **/shops** | CRUD simple | Aucune | Adresse valide | Faible |
| **/order_items** | CRUD complexe | Aucune | Relations multiples | Très élevée |
| **/health** | GET | Aucune | Aucune | Très faible |

### Problèmes identifiés

1. **Authentification incohérente**
   - /items : Authentification requise
   - /stocks, /prices, /shops : Pas d'authentification
   - **Risque** : Sécurité hétérogène

2. **Documentation manquante**
   - Pas de descriptions détaillées des endpoints
   - Exemples de requêtes/réponses absents
   - Codes d'erreur non documentés

3. **Validation incohérente**
   - /items : Validation stricte (code unique)
   - /stocks : Validation basique
   - /order_items : Validation complexe non documentée

4. **Tests manquants**
   - Tests d'intégration pour /order_items
   - Tests de sécurité pour endpoints sans auth
   - Tests de performance pour endpoints complexes

### Recommandations

1. **Sécurité**
   - Ajouter authentification sur tous les endpoints CRUD
   - Implémenter RBAC cohérent
   - Ajouter rate limiting

2. **Documentation**
   - Ajouter descriptions détaillées
   - Inclure exemples de requêtes/réponses
   - Documenter tous les codes d'erreur

3. **Tests**
   - Tests unitaires pour tous les services
   - Tests d'intégration pour les workflows
   - Tests de sécurité et performance
```

---

## 📊 Tableau de suivi avec IA

| Endpoint | Méthode | Paramètres | Réponses | Recommandations IA / Tests manquants |
|---|---|---|---|---|
| **/items** | CRUD | ItemCreate/Update, path params | 201/200/204, 401/404/422/409 | ✅ Tests complets, documentation à améliorer |
| **/stocks** | CRUD | StockCreate/Update, path params | 201/200/204, 404/422 | ⚠️ Ajouter authentification, tests de sécurité |
| **/prices** | CRUD | PriceCreate/Update, path params | 201/200/204, 404/409 | ⚠️ Tests d'intégration manquants |
| **/shops** | CRUD | ShopCreate/Update, path params | 201/200/204, 404/422 | ⚠️ Tests de validation adresse |
| **/order_items** | CRUD | OrderItemCreate, relations | 201/200/204, 404/422 | 🔴 Tests complexes manquants, documentation |
| **/health** | GET | - | 200 OK | ✅ Monitoring à ajouter |

---

## 🧪 Exercice pratique TD 2.3

### 1. Export du fichier OpenAPI

```bash
# Exporter la spécification OpenAPI
curl http://localhost:8000/openapi.json > digicheese_openapi.json

# Analyser le fichier
jq '.paths' digicheese_openapi.json
```

### 2. Résumé IA des endpoints

```python
# scripts/analyze_openapi.py
import json
import requests

def analyze_openapi_spec(url):
    """Analyse la spécification OpenAPI avec IA"""
    
    # Récupérer la spécification
    response = requests.get(url)
    spec = response.json()
    
    # Analyser les endpoints
    endpoints = []
    for path, methods in spec['paths'].items():
        for method, details in methods.items():
            endpoint_info = {
                'path': path,
                'method': method.upper(),
                'operation_id': details.get('operationId', ''),
                'summary': details.get('summary', ''),
                'tags': details.get('tags', []),
                'parameters': len(details.get('parameters', [])),
                'request_body': 'requestBody' in details,
                'responses': list(details.get('responses', {}).keys())
            }
            endpoints.append(endpoint_info)
    
    return endpoints

# Utilisation
endpoints = analyze_openapi_spec('http://localhost:8000/openapi.json')
for ep in endpoints:
    print(f"{ep['method']} {ep['path']} - {ep['responses']}")
```

### 3. Comparaison Swagger UI vs OpenAPI brut

**Swagger UI :**
- ✅ Interface visuelle agréable
- ✅ Tests interactifs
- ❌ Descriptions parfois manquantes
- ❌ Exemples limités

**OpenAPI brut :**
- ✅ Spécification complète
- ✅ Structure détaillée
- ❌ Difficile à lire humainement
- ❌ Pas d'interactivité

**Incohérences détectées :**
- Tags manquants dans certains endpoints
- Réponses 422 non documentées
- Exemples de requêtes absents

### 4. Tests manquants identifiés

```python
# Tests unitaires manquants
MISSING_UNIT_TESTS = [
    'src/services/conditionnement_item_service.py',
    'src/services/stock_line_service.py', 
    'src/services/order_item_service.py',
    'src/security/auth.py'
]

# Tests d'intégration manquants
MISSING_INTEGRATION_TESTS = [
    '/order_items - workflow complexe',
    '/conditionnement_items - validation multiples',
    '/stocks - mises à jour concurrentes',
    '/prices - unicité et historique'
]

# Tests de sécurité manquants
MISSING_SECURITY_TESTS = [
    'Endpoints sans authentification',
    'Injection SQL dans les filtres',
    'Rate limiting sur endpoints critiques',
    'Validation des entrées utilisateur'
]
```

---

## 📋 Livrables TD 2.3

### ✅ Fichier OpenAPI exporté
- `digicheese_openapi.json` - Spécification complète
- `digicheese_openapi.yaml` - Format YAML alternative

### ✅ Tableau de synthèse complété
- 6 principaux endpoints analysés
- 15+ méthodes documentées
- Recommandations IA détaillées

### ✅ Résumé IA structuré

```markdown
## Résumé IA - DigiCheese API

### Points forts
- Architecture CRUD cohérente
- Validation Pydantic bien implémentée
- Gestion d'erreurs HTTP standard

### Points faibles  
- Authentification incohérente
- Documentation insuffisante
- Tests complexes manquants

### Actions prioritaires
1. Sécuriser tous les endpoints
2. Documenter les cas d'erreur
3. Ajouter tests d'intégration
4. Implémenter monitoring
```

### ✅ Liste des recommandations

**Documentation :**
- Ajouter descriptions détaillées
- Inclure exemples de requêtes/réponses
- Documenter schémas d'erreur

**Sécurité :**
- Authentification uniforme
- RBAC complet
- Rate limiting

**Tests :**
- Tests unitaires services complexes
- Tests d'intégration workflows
- Tests sécurité et performance

---

## 🎯 Conseils pratiques appliqués

- ✅ Comparaison OpenAPI brut vs Swagger UI
- ✅ IA utilisée pour détecter lacunes
- ✅ Tableaux de suivi complétés
- ✅ Vision claire de la couverture

---

**Point clé atteint :** Documentation API générée et analysée, améliorations identifiées avec IA, tests manquants répertoriés pour optimiser la couverture qualité.
