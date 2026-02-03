# TP 3.1 — Analyse détaillée de la dette technique

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault
**Cours** : IA Pour la qualité de code - Jour 3  
**Date** : 3 février 2026  

---

## 🎯 Objectif TP

Analyser la dette technique sur les endpoints existants (/login, /users, /orders) et construire un plan d'action priorisé.

---

## 📊 Étape 1 - Exécution des outils de qualité

### Installation des outils
```bash
pip install flake8 pylint radon
```

### Résultats obtenus sur digicheese-api

#### 1. flake8 - Conventions PEP8
**Total : 267 violations détectées**

**Violations principales :**
- **E501** : Lignes trop longues (>79 caractères) - 120+ occurrences
- **W293** : Lignes vides avec espaces - 50+ occurrences  
- **E302** : Manque de lignes vides - 15+ occurrences
- **E712** : Comparaison incorrecte (is True) - 2 occurrences
- **F841** : Variables non utilisées - 3 occurrences

**Exemples concrets :**
```
src/services/conditionnement_item_service.py:45:80: E501 line too long (86 > 79 characters)
src/services/conditionnement_service.py:18:77: E712 comparison to True should be 'if cond is True:'
src/services/commune_service.py:55:9: F841 local variable 'commune' is assigned to but never used
```

#### 2. radon - Complexité cyclomatique
**422 blocs analysés**
**Complexité moyenne : A (1.80)** - Bonne

**Fonctions avec complexité élevée :**
- **C (11-20)** : 1 fonction
  - `jwt_validation_middleware` - C (complexité élevée)
- **B (6-10)** : 5 fonctions
  - `get_current_user` - B
  - `Auth.refresh_token` - B
  - `ClientService.create_client` - B
  - `ClientService.update_client` - B
  - `UserService.update_user` - B
  - `stock_line_service.update_stock_line` - B

#### 3. pylint - Code smells et qualité globale
**Score global : 6.22/10** - Moyen

**Problèmes critiques identifiés :**
- **R0401** : Imports cycliques - 20+ occurrences
- **R0801** : Code dupliqué - 5+ occurrences
- **C0114** : Docstring module manquant
- **C0115** : Docstring classe manquant
- **C0116** : Docstring fonction manquant
- **W0622** : Redéfinition de built-in 'id'

**Exemples concrets :**
```
src/services/__init__.py:1:0: R0401: Cyclic import (src -> src.routers -> src.security.auth)
src/services/conditionnement_service.py:18:77: E712 comparison to True should be 'if cond is True:'
src/services/commune_service.py:55:9: F841 local variable 'commune' is assigned to but never used
```

---

## 📋 Étape 2 - Analyse par endpoint

### Problème : Les endpoints /login, /users, /orders n'existent pas dans digicheese-api

**Endpoints réels du projet :**
- `/items` - CRUD items (remplace /users)
- `/stocks` - Gestion stocks 
- `/orders` - Non existant (utilise /order_items)
- `/login` - Non existant (middleware JWT)

**Adaptation pour l'analyse :**
- **/login** → Analyse du middleware JWT et auth_service
- **/users** → Analyse de `/items` (logique similaire)
- **/orders** → Analyse de `/order_items` (logique équivalente)

---

## 📊 Tableau KPI à remplir

| Endpoint | Complexité cyclomatique (radon) | Code smells (pylint) | Duplication / longueur | Actions / Priorité |
|---|---|---|---|---|
| **/login** (middleware JWT) | **C (11)** | Imports cycliques, code dupliqué | 15+ violations E501 | **Haute** |
| **/users** (/items) | **A (1-4)** | Variables non utilisées, docstrings | 20+ violations E501 | **Moyenne** |
| **/orders** (/order_items) | **A (1-4)** | Code dupliqué, docstrings | 25+ violations E501 | **Moyenne** |

---

## 🤖 Étape 3 - Prompt IA pour analyse

```prompt
Rôle : Expert en qualité logicielle et analyse de dette technique
Contexte : J'ai analysé mon projet FastAPI digicheese-api avec flake8, pylint et radon
Objectif : Analyser les résultats et proposer un plan d'action priorisé

Résultats complets :

flake8 (267 violations) :
- E501: Lignes trop longues (>79 caractères) - 120+ occurrences
- W293: Lignes vides avec espaces - 50+ occurrences  
- E302: Manque de lignes vides - 15+ occurrences
- E712: Comparaison incorrecte (is True) - 2 occurrences
- F841: Variables non utilisées - 3 occurrences

radon (422 blocs analysés, complexité moyenne A (1.80)) :
- C (11-20): jwt_validation_middleware
- B (6-10): get_current_user, Auth.refresh_token, ClientService.create_client, ClientService.update_client, UserService.update_user, stock_line_service.update_stock_line

pylint (score 6.22/10) :
- R0401: Imports cycliques - 20+ occurrences
- R0801: Code dupliqué - 5+ occurrences
- C0114/C0115/C0116: Docstrings manquants - 50+ occurrences
- W0622: Redéfinition built-in 'id' - 4 occurrences

Endpoints analysés :
- /login: middleware JWT (complexité C, imports cycliques)
- /users: /items (complexité A, variables inutilisées)
- /orders: /order_items (complexité A, code dupliqué)

Pour chaque endpoint, indique :
- Les points critiques à corriger en priorité
- Les fonctions les plus complexes
- Les zones de duplication ou code smells
- Un plan d'action clair, structuré et priorisé pour réduire la dette technique

Présente les informations dans un tableau clair et priorisé.
```

---

## 📈 Étape 4 - Résultats de l'analyse IA

### Plan d'action priorisé généré par IA

#### 🔴 Actions Haute Priorité (Critiques)

1. **Corriger les imports cycliques (R0401)**
   - **Endpoint** : Tous (affecte tout le projet)
   - **Problème** : 20+ imports cycliques bloquent la maintenance
   - **Solution** : Restructurer l'architecture, utiliser les imports tardifs
   - **Impact** : Fort
   - **Effort** : Élevé

2. **Optimiser jwt_validation_middleware (Complexité C)**
   - **Endpoint** : /login
   - **Problème** : Complexité 11, point critique de sécurité
   - **Solution** : Décomposer en fonctions plus simples, extraire la logique
   - **Impact** : Fort
   - **Effort** : Moyen

3. **Éliminer le code dupliqué (R0801)**
   - **Endpoint** : Tous
   - **Problème** : 5+ blocs de code dupliqués
   - **Solution** : Créer des fonctions utilitaires partagées
   - **Impact** : Moyen
   - **Effort** : Faible

#### 🟡 Actions Moyenne Priorité

4. **Ajouter les docstrings manquants (C0114/C0115/C0116)**
   - **Endpoint** : Tous
   - **Problème** : 50+ docstrings manquants
   - **Solution** : Documenter classes, fonctions et modules
   - **Impact** : Moyen
   - **Effort** : Moyen

5. **Corriger les lignes trop longues (E501)**
   - **Endpoint** : Tous
   - **Problème** : 120+ lignes >79 caractères
   - **Solution** : Reformater le code, utiliser black
   - **Impact** : Faible
   - **Effort** : Faible

#### 🟢 Actions Faible Priorité

6. **Nettoyer les variables non utilisées (F841)**
   - **Endpoint** : /users, /orders
   - **Problème** : 3 variables non utilisées
   - **Solution** : Supprimer ou utiliser les variables
   - **Impact** : Faible
   - **Effort** : Faible

---

## 📋 Étape 5 - Tableau KPI final complété

| Endpoint | Complexité cyclomatique (radon) | Code smells (pylint) | Duplication / longueur | Actions / Priorité |
|---|---|---|---|---|
| **/login** (middleware JWT) | **C (11)** | Imports cycliques, code dupliqué | 15+ violations E501 | **Haute** |
| **/users** (/items) | **A (1-4)** | Variables non utilisées, docstrings | 20+ violations E501 | **Moyenne** |
| **/orders** (/order_items) | **A (1-4)** | Code dupliqué, docstrings | 25+ violations E501 | **Moyenne** |

---

## 📝 Notes personnelles sur les améliorations possibles

### 🎯 Points critiques identifiés

1. **Architecture cyclique** : Le plus gros problème, affecte la maintenabilité
2. **Middleware JWT complexe** : Point de sécurité critique à optimiser
3. **Code dupliqué** : Indicateur de mauvaise conception
4. **Documentation absente** : Impact sur la maintenabilité

### 🚀 Améliorations prioritaires

1. **Court terme (1-2 semaines)**
   - Corriger les lignes trop longues avec black
   - Ajouter docstrings essentiels
   - Nettoyer les variables inutilisées

2. **Moyen terme (1 mois)**
   - Restructurer les imports cycliques
   - Créer des utilitaires partagés
   - Optimiser le middleware JWT

3. **Long terme (2-3 mois)**
   - Refactoriser l'architecture complète
   - Mettre en place CI/CD avec qualité gates
   - Documenter complètement le code

### 📊 Métriques cibles

| Métrique | Actuel | Cible | Délai |
|---|---|---|---|
| Score pylint | 6.22/10 | 8.0/10 | 1 mois |
| Violations flake8 | 267 | <50 | 2 semaines |
| Complexité moyenne | A (1.80) | A (1.5) | 1 mois |
| Couverture docstring | ~20% | 90% | 1 mois |

---

## 🏆 Livrables attendus

### ✅ Tableau KPI complété pour chaque endpoint
- Analyse détaillée des 3 endpoints
- Métriques de complexité et code smells
- Actions prioritaires identifiées

### ✅ Rapport IA : plan d'action priorisé
- Plan structuré en 3 niveaux de priorité
- Solutions concrètes pour chaque problème
- Estimation d'impact et d'effort

### ✅ Notes personnelles sur les améliorations possibles
- Analyse critique de l'architecture actuelle
- Recommandations pratiques et réalistes
- Planning par étapes avec métriques cibles

---

## 🎯 Conseils et bonnes pratiques appliqués

- ✅ **Analyse des endpoints critiques** : /login (middleware JWT) priorisé
- ✅ **Vérification réaliste** : Complexité et code smells adaptés au projet réel
- ✅ **Prompts IA complets** : Toutes les métriques et erreurs incluses
- ✅ **Actions simples mais impactantes** : Formatage et documentation en premier

---

**Conclusion** : Le projet digicheese-api présente une dette technique modérée (score 6.22/10) avec des problèmes d'architecture cyclique et de documentation. Le plan d'action priorisé permettra d'améliorer significativement la qualité et la maintenabilité du code.
