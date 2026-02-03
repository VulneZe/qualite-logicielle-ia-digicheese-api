# TP1 - Exercice 3 : Cycle de vie et livrables qualité

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 1  
**Date** : 3 février 2026  

---

## 📋 Consignes

Pour chaque phase du RUP, indiquez :
- Les livrables qualité principaux
- Un exemple concret d'action à réaliser pour garantir la qualité
- Un risque qualité potentiel

---

## 📊 Tableau de travail

| Phase | Livrables qualité | Exemple d'action | Risque qualité |
|---|---|---|---|
| Inception | | | |
| Élaboration | | | |
| Construction | | | |
| Transition | | | |

---

## 🔍 Analyse adaptée à digicheese-api

### Contexte du projet
- **Type** : API REST pour gestion fromages
- **Méthodologie** : Approche agile avec inspirations RUP
- **Équipe** : 2-3 développeurs Python
- **Durée estimée** : 3-4 mois

---

## 📈 Tableau complété

| Phase | Livrables qualité | Exemple d'action | Risque qualité |
|---|---|---|---|
| **Inception** | - Vision qualité<br>- Exigences qualité<br>- Plan de tests haut niveau | - Définir SLA (99.9% uptime)<br>- Identifier métriques clés<br>- Workshop qualité avec stakeholders | - Exigences floues<br>- Métriques irréalistes<br>- Manque d'adhésion stakeholders |
| **Élaboration** | - Architecture qualité<br>- Plan de tests détaillé<br>- Standards de codage<br>- Pipeline CI/CD | - Concevoir architecture scalable<br>- Écrire tests d'intégration<br>- Configurer GitHub Actions<br>- Définir conventions PEP8 | - Architecture non scalable<br>- Tests incomplets<br>- Pipeline inefficace<br>- Conventions non respectées |
| **Construction** | - Tests unitaires<br>- Tests d'intégration<br>- Documentation API<br>- Rapports qualité | - Tests pytest avec 80%+ couverture<br>- Tests endpoints CRUD<br>- Documentation Swagger complète<br>- Rapports pylint/flake8 quotidiens | - Dette technique accumulée<br>- Tests oubliés<br>- Documentation obsolète<br>- Qualité dépriorisée |
| **Transition** | - Tests de charge<br>- Documentation utilisateur<br>- Monitoring production<br>- Rapport qualité final | - Tests k6 avec 1000 req/s<br>- Guides API clients<br>- Monitoring Prometheus/Grafana<br>- Audit qualité complet | - Performance dégradée<br>- Documentation incomplète<br>- Monitoring insuffisant<br>- Non-conformité exigences |

---

## 🎯 Application spécifique à digicheese-api

### Phase Inception (Semaines 1-2)
**Livrables qualité :**
- Vision qualité : API performante, sécurisée, documentée
- Exigences qualité : <200ms réponse, 99.9% uptime, documentation complète
- Plan de tests : Tests unitaires, intégration, charge, sécurité

**Action concrète :**
```python
# Document : QUALITY_REQUIREMENTS.md (basé sur digicheese-api réel)
SLA Requirements:
- Response time: <200ms for 95% of requests
- Availability: 99.9% uptime
- Error rate: <0.1%
- Documentation: 100% endpoints documented

Quality Metrics:
- Code coverage: >80%
- Pylint score: >8.0/10
- Performance: <100ms average response
- Flake8 violations: <10

Critical Endpoints (observés dans digicheese-api):
- /items (CRUD principal)
- /stocks (gestion inventaire)
- /auth (sécurité)
```

**Risques identifiés :**
- SLA trop ambitieux pour MVP (264 violations flake8 déjà présentes)
- Métriques difficiles à mesurer sans monitoring
- Équipe petite pour qualité élevée pour qualité élevée

### Phase Élaboration (Semaines 3-6)
**Livrables qualité :**
- Architecture qualité (basée sur digicheese-api réel)
- Plan de tests détaillé
- Standards de codage PEP8 + black
- Pipeline CI/CD amélioré

**Action concrète :**
```yaml
# .github/workflows/quality.yml (amélioration CI existante)
name: Quality Gates
on: [push, pull_request]
jobs:
 quality:
   runs-on: ubuntu-latest
   steps:
     - name: Code Quality
       run: |
         black --check .
         flake8 . --max-line-length=79
         pylint src/ --fail-under=8.0
         pytest --cov=src tests/ --cov-fail-under=80
         radon cc src/ --min B
         coverage report --fail-under=80
```

**Architecture basée sur digicheese-api :**
- ✅ Router + Service + Model (déjà bien fait)
- ❌ Manque : Tests complets, qualité gates
- ❌ Manque : Monitoring, logging

**Risques identifiés :**
- Architecture existante bonne mais qualité faible
- Pipeline CI/CD existant mais incomplet
- Standards PEP8 non respectés (264 violations) par l'équipe

### Phase Construction (Semaines 7-12)
**Livrables qualité :**
- Tests unitaires avec couverture >80%
- Tests d'intégration pour tous endpoints (observés dans digicheese-api)
- Documentation Swagger complète
- Rapports qualité hebdomadaires

**Action concrète :**
```python
# tests/test_item_service.py (basé sur services réels)
class TestItemService:
    def test_create_item_success(self):
        """Test création item avec données valides"""
        item_data = ItemCreate(code="CHEESE001", name="Camembert", price=5.99)
        result = create_item(session, item_data)
        assert result.code == "CHEESE001"
        assert result.name == "Camembert"
    
    def test_create_item_duplicate_code(self):
        """Test création item avec code en double"""
        item_data = ItemCreate(code="CHEESE001", name="Camembert", price=5.99)
        create_item(session, item_data)  # Premier item
        
        # Tentative doublon
        with pytest.raises(ItemCodeAlreadyExistsError):
            create_item(session, item_data)
    
    def test_get_item_not_found(self):
        """Test récupération item inexistant"""
        with pytest.raises(ItemNotFoundError):
            get_item(session, 999)

# tests/test_conditionnement_item_service.py (service complexe non testé)
class TestConditionnementItemService:
    def test_create_link_success(self):
        """Test création lien conditionnement-item"""
        # Basé sur la fonction complexe de 127 lignes
        pass
```

**Risques identifiés :**
- Services complexes non testés (ConditionnementItemService)
- Dette technique accumulée (264 violations flake8)
- Documentation non maintenue

### Phase Transition (Semaines 13-16)
**Livrables qualité :**
- Tests de charge (1000 req/s)
- Documentation utilisateur complète
- Monitoring production configuré
- Audit qualité final

**Action concrète :**
```javascript
// k6/script.js - Tests de charge (basé sur endpoints réels)
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 500 },
    { duration: '10m', target: 1000 },  // Objectif digicheese-api
    { duration: '5m', target: 500 },
    { duration: '2m', target: 0 },
  ],
};

export default function () {
  // Tests endpoints critiques de digicheese-api
  let response = http.get('https://api.digicheese.com/items');
  check(response, {
    'status was 200': (r) => r.status == 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  
  // Test création item
  response = http.post('https://api.digicheese.com/items', JSON.stringify({
    code: 'TEST001',
    name: 'Test Cheese',
    price: 4.99
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

**Monitoring basé sur problèmes réels :**
- Surveillance middleware JWT (complexité C)
- Monitoring services complexes (ConditionnementItem)
- Alertes sur temps de réponse >200ms
- Surveillance erreurs 409 (doublons)

**Risques identifiés :**
- Performance dégradée (middleware JWT complexe)
- Monitoring insuffisant (pas de logging structuré)
- Documentation utilisateur incomplète

---

## 📊 Plan de suivi qualité pour digicheese-api

### Métriques par phase
| Phase | Couverture tests | Score pylint | Performance | Documentation |
|---|---|---|---|---|
| Inception | 0% | N/A | N/A | 10% |
| Élaboration | 20% | 6.0/10 | 500ms | 30% |
| Construction | 80% | 8.0/10 | 200ms | 90% |
| Transition | 85% | 8.5/10 | 100ms | 100% |

### Points de contrôle qualité
- **Hebdomadaire** : Revue code, métriques qualité
- **Mensuel** : Audit architecture, tests de charge
- **Fin de phase** : Validation livrables qualité

---

## 🚀 Recommandations finales

### Pour digicheese-api
1. **Commencer tôt** : Tests et documentation dès la phase Élaboration
2. **Automatiser** : Pipeline CI/CD avec qualité gates strictes
3. **Surveiller** : Monitoring et alertes en production
4. **Documenter** : Documentation maintenue automatiquement

### Leçons apprises
- La qualité se construit progressivement
- Les tests doivent accompagner le développement
- L'architecture doit évoluer avec les besoins
- La documentation est aussi importante que le code

---

*Document de référence pour le cycle de vie qualité de digicheese-api*
