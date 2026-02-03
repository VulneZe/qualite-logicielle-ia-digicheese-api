# Rendu Final - Qualité Logicielle Assistée par l'IA

**Étudiant** : Baptiste Rouault  
**Cours** : IA Pour la qualité de code  
**Date** : 3 février 2026  
**Projet** : digicheese-api  

---

## 📁 Structure du rendu

```
RENDU_FINAL/
├── TP1/                           # Jour 1 - Fondamentaux qualité
│   ├── Exercice1_Classification_Problèmes.md
│   ├── Exercice2_Facteurs_Influence.md
│   ├── Exercice3_Cycle_Vie_Livrables.md
│   └── Travail_Synthèse_Préparation_Jour2.md
├── TP2/                           # Jour 2 - Tests et IA
│   ├── TD_2_1_Tests_Unitaires_IA.md
│   ├── TD_2_2_Tests_Integration_Postman.md
│   ├── TD_2_3_Documentation_Swagger.md
│   └── Synthese_Jour2_KPI.md
├── TP3/                           # Jour 3 - Performance & Dette Technique
│   ├── TP_3_1_Analyse_Dette_Technique.md
│   ├── TP_3_2_Tests_Performance.md
│   └── Synthese_TP3.md
└── TD/                            # Vérification & Synthèse
    ├── SYNTHESE_COMPLETE.md
    ├── TD_2_Verification_Referentiel_IA.md
    ├── référentiel_IA_TD1.md
    ├── pytest_rapport.json
    ├── pylint_rapport.json
    ├── flake8_rapport.json
    ├── radon_rapport.json
    └── performance_rapport.json
```

---

## 🎯 Réalisations principales

### 📊 Jour 1 - Fondamentaux de la Qualité
- **3 exercices** sur la classification des problèmes de qualité
- **Analyse** des facteurs influençant la qualité
- **Cycle de vie** RUP avec livrables qualité
- **Synthèse** préparatoire pour le Jour 2

### 🧪 Jour 2 - Tests et IA
- **23 tests unitaires** générés avec IA (86% couverture)
- **12 endpoints** testés en intégration avec Postman
- **Documentation** Swagger/OpenAPI analysée (70%)
- **KPI mesurés** et suivis

### 🔍 Jour 3 - Performance & Dette Technique
- **267 violations** PEP8 identifiées avec flake8
- **Complexité** cyclomatique A (1.80) avec radon
- **Score pylint** 6.22/10 avec analyse détaillée
- **Tests de charge** k6 (3000 requêtes, 0.00% erreur)

### 📈 Vérification & Synthèse
- **Comparaison** référentiel IA vs rapports réels
- **Tableau de fidélité** IA (4/9 éléments corrects)
- **Synthèse complète** des 3 jours
- **Rapports JSON** pour tous les outils

---

## 🏆 Résultats clés

### 📊 Métriques qualité atteintes
- **Couverture tests** : 0% → 86% ✅
- **Score pylint** : 6.22/10 (objectif 8.0) ⚠️
- **Violations flake8** : 267 (objectif <50) ⚠️
- **Complexité** : A (1.80) ✅

### 🚀 Performance mesurée
- **Latence moyenne** : 156ms (<200ms) ✅
- **Taux d'erreur** : 0.00% ✅
- **Throughput** : 4.8 req/s (objectif 10) ⚠️
- **Requêtes testées** : 3000 ✅

### 📋 Documentation
- **Endpoints documentés** : 70% (objectif 90%) ⚠️
- **Tests unitaires** : 23 créés ✅
- **Tests intégration** : 12 créés ✅

---

## 🎯 Plans d'action prioritaires

### 🔴 Actions Immédiates (1-2 semaines)
1. **Corriger imports cycliques** (R0401)
2. **Optimiser /order_items** (latence 1250ms)
3. **Paginer /items** (dégradation sous charge)

### 🟡 Actions Court Terme (1 mois)
1. **Éliminer code dupliqué** (R0801)
2. **Ajouter docstrings** (50+ manquants)
3. **Mise en cache Redis** (performance)

### 🟢 Actions Long Terme (2-3 mois)
1. **Refactoriser architecture** (imports cycliques)
2. **CI/CD complet** (tests automatisés)
3. **Monitoring avancé** (Grafana)

---

## 📊 Analyse IA vs Réalité

### ✅ Points forts de l'IA
- **Métriques statiques** : pylint, flake8 correctement identifiées
- **Analyse structurée** : Classification ISO/IEC 25010 pertinente
- **Priorisation** : Actions concrètes et réalisables

### ⚠️ Limitations de l'IA
- **Sous-estimation** : Couverture tests (86% vs ~0% prévu)
- **Exagération** : Instabilité critique (0.00% erreur)
- **Validation nécessaire** : Toujours vérifier avec outils réels

---

## 🏆 Compétences développées

### ✅ Techniques
- **Outils qualité** : flake8, pylint, radon, pytest, k6
- **Tests automatisés** : Unitaires, intégration, performance
- **Documentation API** : Swagger/OpenAPI
- **Analyse IA** : Génération et validation de tests

### ✅ Méthodologiques
- **Approche progressive** : Analyse → Mesure → Action
- **Priorisation** : Impact vs Effort
- **Qualité continue** : CI/CD et monitoring
- **Validation croisée** : IA vs outils réels

---

## 📝 Conclusion

Les 3 jours de TP sur la qualité logicielle assistée par l'IA ont permis de transformer radicalement l'approche de développement du projet digicheese-api :

- **Tests complets** : 86% couverture, 0.00% erreur
- **Qualité mesurée** : Outils automatisés et KPI suivis
- **Performance évaluée** : Tests de charge et optimisations
- **Documentation structurée** : Swagger/OpenAPI analysé

**La qualité logicielle assistée par l'IA n'est plus une théorie mais une pratique concrète, mesurable et efficace.**

---

*Ce dossier contient l'intégralité des travaux réalisés et est prêt pour évaluation.*
