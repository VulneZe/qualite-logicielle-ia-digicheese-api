# TD 2 — Vérification du référentiel IA vs fichiers réels

**Projet** : digicheese-api  
**Étudiant** : Baptiste Rouault  
**Cours** : IA Pour la qualité de code - Jour 2  
**Date** : 3 février 2026  

---

## 🎯 Objectif

Comparer le référentiel qualité de départ généré automatiquement par l'IA dans le TD 1 avec les rapports réels produits par Pylint, Pytest et Coverage. L'objectif est d'identifier : pertes d'information, erreurs d'interprétation, minimisations, exagérations ou hallucinations.

---

## 📊 Étape 1 - Référentiel IA généré dans le TD 1

### Référentiel IA (extrait du TD 1)

**Problèmes identifiés par l'IA :**
1. **Score Pylint** : Actuel 6.22 → Cible 8.0
2. **Violations Flake8** : Actuel 267 → Cible <50  
3. **Couverture tests** : Actuel ~0% → Cible 80%
4. **Complexité cyclomatique** : Maintenir A (1-4)
5. **Absence de tests automatisés** : 🔴 Critique
6. **Application instable** : 🔴 Critique
7. **Temps de réponse élevé** : 🟡 Moyenne
8. **Interface peu intuitive** : 🟡 Moyenne
9. **Code complexe** : 🟢 Faible

---

## 📊 Étape 2 - Rapports réels obtenus

### Rapport Pylint réel
```bash
pylint src/ --reports=no
```

**Résultats réels :**
- **Score global** : 6.22/10 ✅ **CORRECT**
- **Violations principales** :
  - R0401 : Imports cycliques - 20+ occurrences
  - R0801 : Code dupliqué - 5+ occurrences  
  - C0114/C0115/C0116 : Docstrings manquants - 50+ occurrences
  - W0622 : Redéfinition built-in 'id' - 4 occurrences

### Rapport Flake8 réel
```bash
flake8 src/
```

**Résultats réels :**
- **Total violations** : 267 ✅ **CORRECT**
- **Types de violations** :
  - E501 : Lignes trop longues (>79) - 120+ occurrences
  - W293 : Lignes vides avec espaces - 50+ occurrences
  - E302 : Manque de lignes vides - 15+ occurrences
  - E712 : Comparaison incorrecte - 2 occurrences
  - F841 : Variables non utilisées - 3 occurrences

### Rapport Radon réel
```bash
radon cc src/ -a
```

**Résultats réels :**
- **Blocs analysés** : 422
- **Complexité moyenne** : A (1.80) ✅ **CORRECT**
- **Complexité élevée** :
  - C (11-20) : jwt_validation_middleware - C (11)
  - B (6-10) : 5 fonctions (get_current_user, Auth.refresh_token, etc.)

### Rapport Pytest réel
```bash
pytest --cov=src tests/
```

**Résultats réels :**
- **Tests passés** : 23/23 ✅ **100% réussite**
- **Couverture** : 86% ✅ **DÉPASSE L'OBJECTIF**
- **Services testés** : ItemService, ConditionnementItemService, etc.

### Rapport Performance k6 réel
```bash
k6 run test_performance.js
```

**Résultats réels :**
- **Requêtes totales** : 3000
- **Latence moyenne** : 156ms ✅ **SOUS LA LIMITE 200ms**
- **Taux d'erreur** : 0.00% ✅ **EXCELLENT**
- **Throughput** : 4.8 req/s ⚠️ **SOUS L'OBJECTIF 10 req/s**

---

## 📋 Étape 3 - Tableau de comparaison

| Élément de qualité | Référentiel IA (TD 1) | Rapports réels | Fidélité IA | Commentaire |
|---|---|---|---|---|
| **Score Pylint** | 6.22 → Cible 8.0 | 6.22/10 | ✅ **Oui** | Exactement correct |
| **Violations Flake8** | 267 → Cible <50 | 267 violations | ✅ **Oui** | Exactement correct |
| **Couverture tests** | ~0% → Cible 80% | 86% | ❌ **Non** | IA sous-estime la réalité |
| **Complexité cyclomatique** | Maintenir A (1-4) | A (1.80) | ✅ **Oui** | Correct mais moyenne 1.80 |
| **Absence de tests** | 🔴 Critique | ✅ 23 tests créés | ❌ **Non** | IA ne prévoyait pas l'amélioration |
| **Application instable** | 🔴 Critique | 0.00% erreur | ❌ **Non** | IA exagère le problème |
| **Temps de réponse** | 🟡 Moyenne | 156ms < 200ms | ❌ **Non** | IA sous-estime la performance |
| **Interface intuitive** | 🟡 Moyenne | 70% documenté | ✅ **Oui** | Correct |
| **Code complexe** | 🟢 Faible | Complexité A (1.80) | ✅ **Oui** | Correct |

---

## 📝 Étape 4 - Mini-analyse (6-10 lignes)

**Le référentiel IA est-il fidèle aux métriques réelles ?**
Partiellement. L'IA a correctement identifié les métriques statiques (pylint, flake8) mais a sous-estimé les améliorations réalisées (couverture tests 86% vs ~0% prévu) et exagéré certains problèmes (instabilité, temps de réponse).

**L'IA a-t-elle ignoré ou minimisé certaines informations ?**
Oui, l'IA a minimisé la capacité à implémenter rapidement des tests de qualité (23 tests créés) et a sous-estimé la performance réelle (156ms < 200ms).

**Y a-t-il des exagérations ou inversions de gravité ?**
Oui, l'IA a classé "Application instable" comme critique alors que le taux d'erreur est de 0.00%, et "Temps de réponse élevé" comme moyen alors que la latence est sous la limite acceptable.

**L'IA a-t-elle inventé des éléments non présents dans les rapports ?**
Non, les problèmes identifiés par l'IA existent bien dans le code, mais leur gravité a été surévaluée.

**Le référentiel IA est-il exploitable pour un audit ?**
Oui, il fournit une bonne base d'analyse mais doit être validé avec des mesures réelles pour éviter les surévaluations.

**Que faudrait-il améliorer dans le prompting ?**
Inclure les résultats réels des outils dans le prompt pour une analyse plus précise et demander à l'IA de valider ses hypothèses avec les métriques mesurées.

---

## 🏆 Livrables

### ✅ Tableau complété
- 9 éléments de qualité comparés
- Fidélité IA évaluée pour chaque élément
- Commentaires explicatifs

### ✅ Mini-analyse
- 6 lignes d'analyse critique
- Discussion de la fiabilité du référentiel IA
- Recommandations d'amélioration

---

## 🎯 Conclusion

Le référentiel IA du TD 1 est **partiellement fidèle** aux métriques réelles. Il excelle dans l'identification des problèmes statiques mais tend à **exagérer la gravité** des problèmes et **sous-estime la capacité d'amélioration**. L'IA reste un excellent outil d'analyse mais doit être **validé avec des mesures réelles** pour un audit fiable.

**Recommandation :** Utiliser l'IA comme point de départ, mais toujours valider avec les rapports réels des outils de qualité.
