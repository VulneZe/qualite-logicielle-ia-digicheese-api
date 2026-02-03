# TP1 - Travail de synthèse : Préparation au Jour 2

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 1  
**Date** : 3 février 2026  

---

## 🎯 Objectifs

- Réaliser un premier squelette de test unitaire Python pour le code audité
- Identifier les fonctions critiques à tester et les critères de qualité associés
- Préparer des prompts pour générer des tests automatiques via IA
- Compléter les tableaux des exercices pour avoir un document de référence

---

## 🧪 Squelette de test unitaire Python

### Structure de tests pour digicheese-api

```python
# tests/test_cheese_service.py
"""
Tests unitaires pour le service de gestion des fromages
Critères : Maintenabilité, Performance, Fiabilité
"""
import pytest
from unittest.mock import Mock, patch
from app.services.cheese_service import CheeseService
from app.models.cheese import Cheese, CheeseCreate
from app.schemas.cheese import CheeseResponse


class TestCheeseService:
    """Tests unitaires du service CheeseService"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.cheese_service = CheeseService()
        self.mock_db = Mock()
    
    def test_create_cheese_success(self):
        """Test création fromage avec données valides"""
        # Arrange
        cheese_data = CheeseCreate(
            name="Camembert",
            price=5.99,
            description="Fromage normand",
            stock_quantity=100
        )
        
        # Act
        result = self.cheese_service.create_cheese(cheese_data)
        
        # Assert
        assert result.name == "Camembert"
        assert result.price == 5.99
        assert result.stock_quantity == 100
        assert isinstance(result, CheeseResponse)
    
    def test_create_cheese_invalid_price(self):
        """Test création fromage avec prix invalide"""
        # Arrange
        cheese_data = CheeseCreate(
            name="Camembert",
            price=-1.0,  # Prix invalide
            description="Fromage normand",
            stock_quantity=100
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Price must be positive"):
            self.cheese_service.create_cheese(cheese_data)
    
    def test_get_cheese_by_id_found(self):
        """Test récupération fromage par ID existant"""
        # Arrange
        cheese_id = 1
        expected_cheese = Cheese(
            id=cheese_id,
            name="Camembert",
            price=5.99
        )
        
        # Act
        result = self.cheese_service.get_cheese_by_id(cheese_id)
        
        # Assert
        assert result.id == cheese_id
        assert result.name == "Camembert"
    
    def test_get_cheese_by_id_not_found(self):
        """Test récupération fromage par ID inexistant"""
        # Arrange
        cheese_id = 999
        
        # Act & Assert
        with pytest.raises(ValueError, match="Cheese not found"):
            self.cheese_service.get_cheese_by_id(cheese_id)
    
    @pytest.mark.performance
    def test_get_all_cheeses_performance(self):
        """Test performance récupération liste fromages"""
        import time
        
        # Act
        start_time = time.time()
        result = self.cheese_service.get_all_cheeses()
        end_time = time.time()
        
        # Assert
        assert end_time - start_time < 0.1  # < 100ms
        assert len(result) >= 0
    
    def test_update_cheese_stock_success(self):
        """Test mise à jour stock fromage"""
        # Arrange
        cheese_id = 1
        new_stock = 150
        
        # Act
        result = self.cheese_service.update_stock(cheese_id, new_stock)
        
        # Assert
        assert result.stock_quantity == new_stock
    
    def test_update_cheese_stock_invalid_quantity(self):
        """Test mise à jour stock avec quantité invalide"""
        # Arrange
        cheese_id = 1
        invalid_stock = -10
        
        # Act & Assert
        with pytest.raises(ValueError, match="Stock must be positive"):
            self.cheese_service.update_stock(cheese_id, invalid_stock)


# tests/test_cheese_routes.py
"""
Tests unitaires pour les routes API fromages
Critères : Fiabilité, Sécurité, Performance
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestCheeseRoutes:
    """Tests des endpoints API fromages"""
    
    def setup_method(self):
        """Initialisation client de test"""
        self.client = TestClient(app)
    
    def test_get_cheeses_endpoint_success(self):
        """Test endpoint GET /cheeses"""
        response = self.client.get("/cheeses")
        
        assert response.status_code == 200
        assert "data" in response.json()
        assert isinstance(response.json()["data"], list)
    
    def test_create_cheese_endpoint_success(self):
        """Test endpoint POST /cheeses"""
        cheese_data = {
            "name": "Brie",
            "price": 4.99,
            "description": "Fromage français",
            "stock_quantity": 50
        }
        
        response = self.client.post("/cheeses", json=cheese_data)
        
        assert response.status_code == 201
        assert response.json()["name"] == "Brie"
        assert response.json()["price"] == 4.99
    
    def test_create_cheese_endpoint_invalid_data(self):
        """Test endpoint POST /cheeses avec données invalides"""
        invalid_data = {
            "name": "",
            "price": -1.0,
            "description": "",
            "stock_quantity": -10
        }
        
        response = self.client.post("/cheeses", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.performance
    def test_get_cheese_by_id_performance(self):
        """Test performance endpoint GET /cheeses/{id}"""
        import time
        
        # Act
        start_time = time.time()
        response = self.client.get("/cheeses/1")
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200
        assert end_time - start_time < 0.05  # < 50ms


# tests/conftest.py
"""
Configuration fixtures pour les tests
"""
import pytest
from app.database import get_db
from app.main import app


@pytest.fixture
def test_db():
    """Fixture base de données de test"""
    # Configuration DB de test
    pass


@pytest.fixture
def client():
    """Fixture client FastAPI pour les tests"""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def sample_cheese():
    """Fixture fromage échantillon pour les tests"""
    return {
        "id": 1,
        "name": "Camembert",
        "price": 5.99,
        "description": "Fromage normand",
        "stock_quantity": 100
    }
```

---

## 🎯 Fonctions critiques à tester

### 1. CheeseService.create_cheese()
**Critères de qualité :**
- **Maintenabilité** : Code clair, testable
- **Fiabilité** : Gestion erreurs, validation
- **Performance** : Temps réponse <100ms

**Tests requis :**
- Succès création fromage valide
- Échec avec données invalides
- Gestion doublons
- Performance sous charge

### 2. CheeseService.update_stock()
**Critères de qualité :**
- **Fiabilité** : Cohérence des données
- **Sécurité** : Pas de négatifs
- **Performance** : Mise à jour rapide

**Tests requis :**
- Mise à jour réussie
- Rejet quantités négatives
- Gestion stock insuffisant
- Concurrence (race conditions)

### 3. CheeseRoutes.get_cheeses()
**Critères de qualité :**
- **Performance** : <200ms réponse
- **Fiabilité** : Format réponse constant
- **Sécurité** : Pas d'exposition données sensibles

**Tests requis :**
- Réponse correcte
- Format JSON valide
- Performance
- Gestion erreurs

### 4. CheeseService.calculate_price()
**Critères de qualité :**
- **Maintenabilité** : Logique modulaire
- **Performance** : Calculs rapides
- **Fiabilité** : Résultats cohérents

**Tests requis :**
- Calculs corrects
- Gestion promotions
- Performance
- Edge cases (prix nuls, négatifs)

---

## 🤖 Prompts IA pour génération de tests automatiques

### Prompt 1 : Tests unitaires service
```
Rôle : Expert en tests Python et FastAPI
Contexte : Je développe une API FastAPI pour la gestion de fromages (digicheese-api)
Objectif : Générer des tests unitaires complets pour la classe CheeseService
Format de sortie : Code Python avec pytest, incluant arrange-act-assert pattern

Critères de qualité requis :
- Couverture >80% du code
- Tests edge cases et erreurs
- Tests performance (<100ms)
- Tests concurrence et race conditions
- Mock des dépendances externes

Code à tester :
```python
class CheeseService:
    def create_cheese(self, cheese_data: CheeseCreate) -> CheeseResponse:
        # Validation des données
        if cheese_data.price <= 0:
            raise ValueError("Price must be positive")
        
        # Création en base
        cheese = Cheese(**cheese_data.dict())
        db.add(cheese)
        db.commit()
        
        return CheeseResponse.from_orm(cheese)
    
    def update_stock(self, cheese_id: int, new_quantity: int) -> CheeseResponse:
        if new_quantity < 0:
            raise ValueError("Stock must be positive")
        
        cheese = db.query(Cheese).filter(Cheese.id == cheese_id).first()
        if not cheese:
            raise ValueError("Cheese not found")
        
        cheese.stock_quantity = new_quantity
        db.commit()
        
        return CheeseResponse.from_orm(cheese)
```

Génère le fichier test_cheese_service.py complet avec tous les tests nécessaires.
```

### Prompt 2 : Tests API endpoints
```
Rôle : Spécialiste en tests d'API REST
Contexte : API FastAPI digicheese-api avec endpoints CRUD pour les fromages
Objectif : Générer des tests d'intégration pour tous les endpoints
Format de sortie : Code Python avec TestClient FastAPI

Critères de qualité requis :
- Tests tous les codes HTTP (200, 201, 400, 404, 422, 500)
- Validation des schémas de réponse
- Tests de sécurité (injection, authentification)
- Tests de performance (<200ms)
- Tests de pagination et filtrage

Endpoints à tester :
- GET /cheeses (liste, pagination, filtrage)
- POST /cheeses (création, validation)
- GET /cheeses/{id} (détail, not found)
- PUT /cheeses/{id} (mise à jour, validation)
- DELETE /cheeses/{id} (suppression, cascade)

Génère test_cheese_routes.py avec couverture complète de tous les scénarios.
```

### Prompt 3 : Tests de charge
```
Rôle : Expert en performance et tests de charge
Contexte : API digicheese-api devant supporter 1000 requêtes/secondes
Objectif : Générer scripts k6 pour tests de charge réalistes
Format de sortie : Scripts JavaScript k6 avec scénarios variés

Critères de qualité requis :
- Scénarios : pic charge, charge soutenue, montée en charge
- Métriques : temps réponse, taux d'erreur, throughput
- Simulation : utilisateurs réels avec comportements variés
- Seuils : <200ms réponse, <1% erreur, 1000 req/s

Scénarios à simuler :
1. Navigation catalogue (GET /cheeses)
2. Recherche fromages (GET /cheeses/search)
3. Création commandes (POST /orders)
4. Mise à jour panier (PUT /cart)

Génère scripts k6 complets avec rapports de performance.
```

### Prompt 4 : Tests de sécurité
```
Rôle : Expert en sécurité applicative
Contexte : API digicheese-api avec données sensibles (prix, stock, commandes)
Objectif : Générer tests de sécurité automatisés
Format de sortie : Scripts Python avec sécurité checks

Critères de qualité requis :
- Tests injection SQL, XSS, CSRF
- Tests authentification et autorisation
- Tests validation entrées (input validation)
- Tests rate limiting et DoS
- Tests exposition données sensibles

Sécurité à tester :
- Injection dans paramètres de recherche
- Tentatives de modification prix non autorisées
- Accès données autres utilisateurs
- Rate limiting sur endpoints critiques
- Validation formats entrées

Génère suite de tests sécurité complète avec exploitation tentatives.
```

---

## 📊 Tableaux récapitulatifs complétés

### Résumé exercice 1 - Classification problèmes
| Problème | Dimension | Caractéristique ISO | Parties prenantes |
|---|---|---|---|
| Méthode Python complexe | Interne | Maintenabilité | Développeurs |
| Temps réponse élevé | Externe | Performance | Utilisateurs |
| Interface peu intuitive | Perçue | Utilisabilité | Clients API |
| Application instable | Externe | Fiabilité | Production |
| Absence tests | Interne | Fiabilité | Équipe QA |

### Résumé exercice 2 - Facteurs influence
| Facteur | Type |
|---|---|
| Revue de code | Mixte |
| Conventions codage | Mixte |
| Documentation | Mixte |
| Intégration continue | Mixte |
| Choix framework | Technique |

### Résumé exercice 3 - Cycle de vie
| Phase | Livrables qualité | Action clé | Risque principal |
|---|---|---|---|
| Inception | Vision qualité | Définir SLA | Exigences floues |
| Élaboration | Architecture | Configurer CI/CD | Architecture non scalable |
| Construction | Tests unitaires | Tests pytest | Dette technique |
| Transition | Tests charge | Monitoring production | Performance dégradée |

---

## 🚀 Préparation Jour 2

### Checklist pour la suite
- [ ] Implémenter squelette de tests dans projet digicheese-api
- [ ] Exécuter premiers tests unitaires
- [ ] Utiliser prompts IA pour générer tests additionnels
- [ ] Configurer pipeline CI/CD avec tests automatiques
- [ ] Mesurer couverture de code et améliorer

### Objectifs Jour 2
1. **Mise en pratique** : Implémenter les tests conçus
2. **Automatisation** : CI/CD avec qualité gates
3. **Amélioration** : Utiliser retours tests pour refactoriser
4. **Documentation** : Documenter processus qualité

---

*Document de préparation complet pour le Jour 2 - Tests et Qualité*
