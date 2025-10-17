# 🎨 Guide de l'Interface Graphique FedEnh

## 🌟 Interface Professionnelle Complète

L'interface graphique FedEnh offre une expérience utilisateur moderne et intuitive pour la simulation d'apprentissage fédéré avec des datasets de crédit réels.

## 🚀 Lancement de l'Application

### Méthode 1: Script de Lancement Automatique
```bash
cd ~/fedenh_simulation
source venv/bin/activate
python launch_gui.py
```

### Méthode 2: Lancement Direct Streamlit
```bash
cd ~/fedenh_simulation
source venv/bin/activate
streamlit run gui_application.py
```

### Accès à l'Interface
- **URL**: http://localhost:8501
- **Port**: 8501 (par défaut)
- **Interface**: Web responsive, compatible mobile

## 📱 Navigation de l'Interface

### 🧭 Menu de Navigation (Sidebar)
- **📁 Upload de Données**: Téléchargement et traitement des datasets
- **⚙️ Configuration**: Paramètres de simulation
- **🚀 Simulation**: Exécution de l'apprentissage fédéré
- **📊 Résultats**: Visualisation et analyse des résultats
- **ℹ️ À Propos**: Documentation et informations

## 📁 Section Upload de Données

### 📤 Upload de Fichiers
- **Formats supportés**: CSV, Excel (.xlsx), JSON
- **Taille maximale**: 200MB (configurable)
- **Validation automatique**: Vérification du format et structure

### 🏷️ Datasets Prédéfinis
- **Taiwan Credit Dataset (TCD)**: 30,000 échantillons, 23 variables
- **Give Me Some Credit (GMSC)**: 150,000 échantillons, 11 variables  
- **Home Credit (HC)**: 300,000 échantillons, 122 variables

### 🔧 Configuration du Prétraitement
- **Variable cible**: Sélection de la variable à prédire
- **Seuil de corrélation**: Suppression des variables fortement corrélées (>0.97)
- **Traitement automatique**:
  - Gestion des valeurs manquantes
  - Encodage one-hot des variables catégorielles
  - Normalisation [0,1] des variables numériques
  - Suppression de la multicolinéarité

### 👀 Aperçu des Données
- **Métriques de base**: Échantillons, variables, valeurs manquantes
- **Tableau de données**: Premières lignes avec pagination
- **Types de données**: Analyse des types et valeurs uniques
- **Statistiques descriptives**: Résumé automatique

## ⚙️ Section Configuration

### 🏦 Paramètres des Clients
- **Nombre de clients**: 3-20 institutions financières
- **Fraction par round**: 10%-100% des clients sélectionnés
- **Taille des données**: 100-2000 échantillons par client

### 🔄 Paramètres d'Entraînement
- **Nombre de rounds**: 10-200 cycles d'apprentissage
- **Époques locales**: 1-10 époques par client
- **Taille des lots**: 16, 32, 64, 128 échantillons
- **Taux d'apprentissage**: 0.001-0.1 (ajustable)

### 🔐 Confidentialité et Sécurité
- **Multiplicateur de bruit**: 0.5-3.0 (confidentialité différentielle)
- **Seuil de clipping L2**: 0.1-2.0 (stabilité des gradients)
- **Mécanismes de protection**: Automatiques

### 🎯 Options Avancées
- **Personnalisation locale**: Adaptation aux spécificités locales
- **Métriques avancées**: Évaluation détaillée des performances
- **Analyse de convergence**: Détection automatique

## 🚀 Section Simulation

### 🎬 Lancement de la Simulation
- **Bouton principal**: Lancement avec un clic
- **Barre de progression**: Suivi en temps réel
- **Statut détaillé**: Messages informatifs
- **Arrêt d'urgence**: Possibilité d'interrompre

### 📊 Métriques en Temps Réel
- **Loss globale**: Évolution de la fonction de perte
- **Précision**: Taux de classification correcte
- **Convergence**: Détection automatique de la stabilité
- **Participation**: Suivi des clients actifs

## 📊 Section Résultats

### 📈 Métriques Principales
- **Loss finale**: Valeur de convergence
- **Précision finale**: Performance du modèle
- **Rounds exécutés**: Nombre de cycles
- **Total participations**: Activité des clients

### 🎨 Visualisations Interactives
- **Graphiques Plotly**: Zoom, pan, sélection
- **Évolution des métriques**: Loss et précision
- **Participation des clients**: Distribution et activité
- **Analyse de convergence**: Moyennes mobiles

### 🔍 Métriques Détaillées
- **Par client**: Performance individuelle
- **Historique**: Évolution temporelle
- **Comparaisons**: Benchmarks et références
- **Analyse de variance**: Stabilité des résultats

### 💾 Export des Résultats
- **Format JSON**: Résultats complets
- **Format CSV**: Métriques tabulaires
- **Rapports PDF**: Documentation automatique
- **Graphiques PNG**: Visualisations haute résolution

## 🎯 Fonctionnalités Spécialisées

### 📊 Métriques de Crédit
- **Accuracy**: Proportion de classifications correctes
- **Recall**: Détection des défauts de paiement
- **F1-Score**: Équilibre précision/rappel
- **KS (Kolmogorov-Smirnov)**: Capacité discriminative

### 🔐 Confidentialité Différentielle
- **Epsilon (ε)**: Budget de confidentialité
- **Delta (δ)**: Probabilité de fuite
- **Score de confidentialité**: Évaluation globale (0-1)
- **Trade-off privacy-utility**: Analyse automatique

### 🏦 Simulation Réaliste
- **Données non-IID**: Hétérogénéité des institutions
- **Types d'institutions**: Banques traditionnelles, fintech, universelles
- **Distributions biaisées**: Réalisme des données
- **Scénarios multiples**: Configurations variées

## 🎨 Design et Expérience Utilisateur

### 🎨 Interface Moderne
- **Design responsive**: Adaptation mobile/desktop
- **Thème professionnel**: Couleurs cohérentes
- **Navigation intuitive**: Menu sidebar
- **Feedback visuel**: Messages et animations

### 📱 Compatibilité
- **Navigateurs**: Chrome, Firefox, Safari, Edge
- **Appareils**: Desktop, tablette, mobile
- **Résolutions**: Adaptatif automatique
- **Accessibilité**: Standards WCAG

### ⚡ Performance
- **Chargement rapide**: Optimisation des assets
- **Mémoire efficace**: Gestion des datasets
- **Calculs parallèles**: Traitement optimisé
- **Cache intelligent**: Réutilisation des résultats

## 🔧 Configuration Avancée

### ⚙️ Paramètres Streamlit
```toml
[server]
port = 8501
address = "localhost"
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#1f4e79"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### 🎛️ Variables d'Environnement
```bash
export FEDENH_LOG_LEVEL=INFO
export FEDENH_MAX_CLIENTS=50
export FEDENH_CACHE_DIR=/tmp/fedenh
export STREAMLIT_SERVER_PORT=8501
```

## 🚨 Résolution de Problèmes

### ❌ Erreurs Courantes

#### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### "Port already in use"
```bash
# Changer le port
streamlit run gui_application.py --server.port 8502
```

#### "Memory error"
- Réduire la taille des datasets
- Diminuer le nombre de clients
- Augmenter la mémoire disponible

#### "Upload failed"
- Vérifier le format du fichier
- Réduire la taille du fichier
- Vérifier la connexion internet

### 🔍 Debug et Logs
```bash
# Mode debug
streamlit run gui_application.py --logger.level debug

# Logs détaillés
export STREAMLIT_LOGGER_LEVEL=debug
```

## 📚 Exemples d'Utilisation

### 🎯 Cas d'Usage Typiques

#### 1. Démonstration Rapide
1. Lancer l'application
2. Sélectionner un dataset prédéfini
3. Configuration par défaut
4. Lancer la simulation
5. Analyser les résultats

#### 2. Recherche et Développement
1. Upload d'un dataset personnalisé
2. Configuration avancée
3. Simulation avec métriques détaillées
4. Export des résultats
5. Analyse comparative

#### 3. Formation et Enseignement
1. Utilisation des datasets d'exemple
2. Exploration des paramètres
3. Visualisation des concepts
4. Comparaison des configurations
5. Discussion des résultats

### 📊 Workflow Recommandé
1. **Préparation**: Upload et prétraitement des données
2. **Configuration**: Ajustement des paramètres
3. **Simulation**: Exécution de l'apprentissage fédéré
4. **Analyse**: Exploration des résultats
5. **Export**: Sauvegarde pour analyse approfondie

## 🎉 Fonctionnalités Avancées

### 🔬 Analyse Comparative
- **Benchmarks automatiques**: Comparaison de configurations
- **Métriques statistiques**: Moyennes, écarts-types, intervalles
- **Tests de significativité**: Validation des résultats
- **Visualisations comparatives**: Graphiques multi-configurations

### 📈 Monitoring en Temps Réel
- **Métriques live**: Mise à jour automatique
- **Alertes de convergence**: Notifications intelligentes
- **Historique complet**: Traçabilité des expériences
- **Export automatique**: Sauvegarde périodique

### 🎨 Personnalisation
- **Thèmes**: Couleurs et styles personnalisables
- **Layouts**: Disposition adaptative
- **Widgets**: Composants interactifs
- **Extensions**: Modules complémentaires

---

## 🎊 Conclusion

L'interface graphique FedEnh offre une expérience complète et professionnelle pour l'apprentissage fédéré appliqué au crédit. Elle combine facilité d'utilisation, fonctionnalités avancées et visualisations interactives pour une recherche et un développement efficaces.

**🚀 Prêt à explorer l'apprentissage fédéré avec style !**
