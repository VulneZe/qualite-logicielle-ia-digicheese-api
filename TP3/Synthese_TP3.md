# Synthèse TP3 - Performance, Dette Technique et CI/CD

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 3  
**Date** : 3 février 2026  

---

## 🎯 Objectifs pédagogiques atteints

À la fin de ce TP3, vous serez capables de :
- ✅ Exécuter des tests de charge simples avec k6
- ✅ Mesurer les principaux KPI : latence, taux d'erreur, throughput
- ✅ Identifier les points critiques de l'API
- ✅ Utiliser l'IA pour analyser les résultats et proposer des seuils cibles
- ✅ Analyser la dette technique avec des outils spécialisés
- ✅ Construire un plan d'action priorisé pour réduire la dette technique

---

## 📊 Résultats principaux obtenus

### Partie 1 - Analyse Dette Technique (TP 3.1)

#### 📈 Métriques de qualité mesurées
- **flake8** : 267 violations PEP8 détectées
- **radon** : Complexité moyenne A (1.80) sur 422 blocs
- **pylint** : Score global 6.22/10

#### 🔍 Problèmes critiques identifiés
1. **Imports cycliques (R0401)** : 20+ occurrences - **Priorité Haute**
2. **Middleware JWT complexe** : Complexité C (11) - **Priorité Haute**
3. **Code dupliqué (R0801)** : 5+ blocs - **Priorité Moyenne**
4. **Docstrings manquants** : 50+ occurrences - **Priorité Moyenne**

#### 📋 Tableau KPI final

| Endpoint | Complexité cyclomatique | Code smells | Duplication / longueur | Actions / Priorité |
|---|---|---|---|---|
| **/login** (middleware JWT) | **C (11)** | Imports cycliques, code dupliqué | 15+ violations E501 | **Haute** |
| **/users** (/items) | **A (1-4)** | Variables non utilisées, docstrings | 20+ violations E501 | **Moyenne** |
| **/orders** (/order_items) | **A (1-4)** | Code dupliqué, docstrings | 25+ violations E501 | **Moyenne** |

### Partie 2 - Tests de Performance (TP 3.2)

#### 🚀 Tests de charge exécutés
- **Outil** : k6 (CLI pour automatisation)
- **Requêtes totales** : 3000
- **Durée** : 10m30s avec charge progressive (10→50→100 VUs)
- **Taux d'erreur global** : 0.00%

#### 📊 KPI Performance mesurés

| Endpoint | Latence moyenne | Temps max | Taux d'erreur | Throughput |
|---|---|---|---|---|
| **/health** | 45ms | 85ms | 0.00% | 4.8 req/s |
| **/items** | 125ms | 450ms | 0.00% | 4.8 req/s |
| **/order_items** | 180ms | 1250ms | 0.00% | 4.8 req/s |

#### 🔍 Goulets d'étranglement identifiés
1. **/order_items** : Latence max 1250ms à 100 VUs - **Critique**
2. **/items** : Dégradation 4.7x sous charge - **Moyen**
3. **/health** : Performances stables - **Correct**

---

## 🎯 Plans d'action prioritisés

### 📋 Plan Dette Technique (TP 3.1)

#### 🔴 Actions Haute Priorité (1-2 semaines)
1. **Corriger les imports cycliques**
   - Impact : Fort (maintenabilité)
   - Effort : Élevé
   - Action : Restructurer l'architecture

2. **Optimiser jwt_validation_middleware**
   - Impact : Fort (sécurité)
   - Effort : Moyen
   - Action : Décomposer en fonctions simples

#### 🟡 Actions Moyenne Priorité (1 mois)
3. **Éliminer le code dupliqué**
   - Impact : Moyen
   - Effort : Faible
   - Action : Créer utilitaires partagés

4. **Ajouter les docstrings**
   - Impact : Moyen
   - Effort : Moyen
   - Action : Documenter classes et fonctions

### 📋 Plan Performance (TP 3.2)

#### 🔴 Actions Haute Priorité (Immédiat)
1. **Optimiser /order_items**
   - Ajouter indexes SQL
   - Implémenter eager loading
   - Mettre en cache les résultats

2. **Paginer /items**
   - Ajouter skip/limit
   - Limiter résultats par requête
   - Ajouter filtres

#### 🟡 Actions Moyenne Priorité (1-2 semaines)
3. **Mise en cache généralisée**
   - Redis pour données fréquentes
   - Cache côté client
   - Stratégie d'invalidation

---

## 📈 Métriques cibles et progression

### 📊 Dette Technique

| Métrique | Actuel | Cible | Délai |
|---|---|---|---|
| Score pylint | 6.22/10 | 8.0/10 | 1 mois |
| Violations flake8 | 267 | <50 | 2 semaines |
| Complexité moyenne | A (1.80) | A (1.5) | 1 mois |
| Couverture docstring | ~20% | 90% | 1 mois |

### 📊 Performance

| Métrique | Actuel | Cible | Délai |
|---|---|---|---|
| Latence /health | 45ms | <50ms | Maintenu |
| Latence /items | 125ms | <100ms | 2 semaines |
| Latence /order_items | 180ms | <150ms | 1 mois |
| Taux d'erreur | 0.00% | <1% | Maintenu |
| Throughput | 4.8 req/s | 10+ req/s | 1 mois |

---

## 🎯 Leçons apprises

### Techniques et Outils

1. **Outils de qualité complémentaires**
   - **flake8** : Style et conventions PEP8
   - **radon** : Complexité cyclomatique
   - **pylint** : Code smells et qualité globale
   - **k6** : Tests de charge automatisés

2. **Analyse de performance**
   - Tests de charge progressifs essentiels
   - Seuils critiques : latence >500ms, erreur >5%
   - Monitoring continu nécessaire

3. **Dette technique mesurable**
   - Score pylint comme indicateur global
   - Complexité radon pour identifier les points critiques
   - Violations flake8 pour la lisibilité

### Méthodologiques

1. **Approche progressive**
   - Analyse → Mesure → Plan → Action
   - Prioriser les actions à fort impact
   - Mesurer avant et après optimisation

2. **IA comme assistant**
   - Analyse rapide des résultats complexes
   - Génération de plans d'action structurés
   - Recommandations basées sur les métriques

3. **Qualité continue**
   - CI/CD avec qualité gates
   - Monitoring en production
   - Réductions de dette technique itératives

---

## 🚀 Recommandations futures

### Court terme (1 mois)
- ✅ Implémenter les corrections de formatage (black, flake8)
- ✅ Ajouter les docstrings essentiels
- ✅ Optimiser les requêtes SQL critiques
- ✅ Mettre en place monitoring de base

### Moyen terme (3 mois)
- ✅ Refactoriser l'architecture cyclique
- ✅ Implémenter la pagination sur tous les endpoints
- ✅ Mettre en place cache Redis
- ✅ Configurer CI/CD avec tests de performance

### Long terme (6 mois)
- ✅ Architecture microservices si nécessaire
- ✅ Monitoring avancé avec Grafana
- ✅ Tests de charge automatisés en CI/CD
- ✅ Documentation complète et maintenue

---

## 🏆 Succès du TP3

### ✅ Objectifs atteints
1. **Analyse dette technique** : Identification précise des problèmes
2. **Tests de performance** : Mesure réaliste des capacités
3. **Plans d'action** : Priorisés et réalisables
4. **Utilisation IA** : Analyse pertinente des résultats

### 📊 Améliorations quantifiables
- **Qualité code** : 6.22/10 → Objectif 8.0/10
- **Violations** : 267 → Objectif <50
- **Performance** : 1250ms max → Objectif <500ms
- **Documentation** : 20% → Objectif 90%

### 🎯 Compétences développées
- Analyse de dette technique avec outils spécialisés
- Tests de charge avec k6
- Interprétation des métriques de performance
- Planification d'optimisation priorisée
- Utilisation de l'IA pour l'analyse technique

---

## 📝 Conclusion

Le TP3 a permis de lier théorie et pratique de manière exceptionnelle. L'analyse de la dette technique a révélé des problèmes d'architecture importants mais traitables, tandis que les tests de performance ont identifié des goulets d'étranglement critiques. L'utilisation de l'IA a permis d'accélérer l'analyse et de générer des plans d'action pertinents.

**Point clé** : La qualité et la performance ne sont pas des options mais des investissements continus qui nécessitent des outils, des processus et une discipline rigoureuse.

---

*Abdelali IRKHA - 3 février 2026*
