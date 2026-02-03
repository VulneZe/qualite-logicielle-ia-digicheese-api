# Instructions pour créer le repository GitHub

## 📋 Étapes à suivre

### 1. Créer le repository sur GitHub
1. Allez sur [github.com](https://github.com)
2. Cliquez sur **"New repository"** (vert en haut à droite)
3. Remplissez les informations :
   - **Repository name** : `qualite-logicielle-ia-digicheese-api`
   - **Description** : `Projet de qualité logicielle assistée par l'IA - Analyse du projet digicheese-api`
   - **Visibility** : Choisissez **Private** ou **Public**
   - **Ne cochez pas** "Add a README file" (nous en avons déjà un)
   - **Ne cochez pas** "Add .gitignore" (nous en avons déjà un)
4. Cliquez sur **"Create repository"**

### 2. Connecter le dossier local au repo GitHub
Ouvrez un terminal PowerShell dans le dossier `RENDU_FINAL` :

```powershell
# Ajouter le remote (remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub)
git remote add origin https://github.com/VOTRE_USERNAME/qualite-logicielle-ia-digicheese-api.git

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Projet qualité logicielle IA complet

✅ Jour 1 : Fondamentaux qualité (classification, facteurs, cycle de vie)
✅ Jour 2 : Tests et IA (unitaires, intégration, documentation)
✅ Jour 3 : Performance et dette technique (flake8, pylint, radon, k6)
✅ Vérification IA vs réalité avec rapports JSON
✅ Synthèse complète avec KPI et plans d'action

Étudiant : Baptiste Rouault
Cours : IA Pour la qualité de code
Date : 3 février 2026"

# Pousser vers GitHub
git push -u origin main
```

### 3. Si vous rencontrez des erreurs
Si vous avez une erreur d'authentification :
```powershell
# Configurer Git avec vos informations GitHub
git config --global user.name "Baptiste Rouault"
git config --global user.email "votre-email@example.com"

# Ou utiliser un token GitHub si vous avez 2FA
git remote set-url origin https://VOTRE_USERNAME:VOTRE_TOKEN@github.com/VOTRE_USERNAME/qualite-logicielle-ia-digicheese-api.git
```

---

## 📁 Contenu du repository

### Structure finale
```
qualite-logicielle-ia-digicheese-api/
├── README.md                     # Vue d'ensemble du projet
├── TP1/                          # Jour 1 - Fondamentaux qualité
│   ├── Exercice1_Classification_Problèmes.md
│   ├── Exercice2_Facteurs_Influence.md
│   ├── Exercice3_Cycle_Vie_Livrables.md
│   └── Travail_Synthèse_Préparation_Jour2.md
├── TP2/                          # Jour 2 - Tests et IA
│   ├── TD_2_1_Tests_Unitaires_IA.md
│   ├── TD_2_2_Tests_Integration_Postman.md
│   ├── TD_2_3_Documentation_Swagger.md
│   └── Synthese_Jour2_KPI.md
├── TP3/                          # Jour 3 - Performance & Dette Technique
│   ├── TP_3_1_Analyse_Dette_Technique.md
│   ├── TP_3_2_Tests_Performance.md
│   └── Synthese_TP3.md
├── TD/                           # Vérification & Synthèse
│   ├── SYNTHESE_COMPLETE.md
│   ├── TD_2_Verification_Referentiel_IA.md
│   ├── référentiel_IA_TD1.md
│   ├── pytest_rapport.json
│   ├── pylint_rapport.json
│   ├── flake8_rapport.json
│   ├── radon_rapport.json
│   └── performance_rapport.json
├── .gitignore                    # Fichiers à ignorer
└── INSTRUCTIONS_GITHUB.md        # Ce fichier
```

---

## 🎯 Points clés du projet

### ✅ Réalisations principales
- **23 tests unitaires** générés avec IA (86% couverture)
- **12 endpoints** testés en intégration
- **267 violations** PEP8 identifiées et analysées
- **Tests de charge** k6 (3000 requêtes, 0.00% erreur)
- **Analyse IA vs réalité** avec validation croisée

### 📊 Métriques qualité
- **Couverture tests** : 86%
- **Score pylint** : 6.22/10
- **Complexité** : A (1.80)
- **Performance** : 156ms latence moyenne
- **Documentation** : 70% des endpoints

### 🚀 Compétences démontrées
- **Outils qualité** : flake8, pylint, radon, pytest, k6
- **Tests automatisés** : Unitaires, intégration, performance
- **IA assistée** : Génération et validation de tests
- **Analyse critique** : Comparaison IA vs réalité

---

## 🏆 Une fois sur GitHub

Votre repository sera accessible à l'URL :
`https://github.com/VOTRE_USERNAME/qualite-logicielle-ia-digicheese-api`

Vous pourrez :
- ✅ Partager le lien avec votre professeur
- ✅ Ajouter des collaborateurs si nécessaire
- ✅ Créer des Issues pour le suivi
- ✅ Utiliser les Projects pour la gestion

---

**Bon courage pour la création du repository !** 🚀
