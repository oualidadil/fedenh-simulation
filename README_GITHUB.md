# 🏦 FedEnh Simulation - Apprentissage Fédéré pour l'Open Banking

## 📖 Description

Application web interactive pour simuler l'algorithme **FedEnh** (Enhanced Federated Averaging) appliqué au domaine bancaire. Cette application permet de démontrer comment plusieurs institutions financières peuvent collaborer pour créer un modèle de prédiction de risque de crédit performant, tout en préservant la confidentialité des données de leurs clients.

## ✨ Fonctionnalités

- 🔐 **Confidentialité Différentielle** : Protection de la vie privée intégrée
- 📊 **Visualisations Interactives** : Graphiques dynamiques avec Plotly
- 🎯 **Métriques Spécialisées** : Accuracy, Precision, Recall, F1-Score, KS Score
- 🏦 **Datasets de Crédit** : Support pour datasets Taiwan Credit, GMSC, Home Credit
- ⚙️ **Configuration Flexible** : Tous les paramètres sont ajustables
- 📈 **Analyse Comparative** : Comparaison avec d'autres méthodes fédérées

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le repository
git clone https://github.com/votre-username/fedenh_simulation.git
cd fedenh_simulation

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement de l'Application

```bash
# Lancer l'interface web
streamlit run gui_application.py
```

L'application sera accessible à l'adresse : **http://localhost:8501**

## 📋 Utilisation

### 1. Upload de Données
- Téléchargez votre fichier CSV/Excel
- Ou sélectionnez un dataset prédéfini

### 2. Configuration
- Ajustez les paramètres de simulation
- Configurez le nombre de clients, rounds, etc.

### 3. Simulation
- Lancez la simulation d'apprentissage fédéré
- Suivez la progression en temps réel

### 4. Résultats
- Analysez les performances du modèle
- Explorez les visualisations interactives
- Exportez les résultats

## 📊 Datasets Inclus

- **Taiwan Credit Dataset (TCD)** : 5,000 échantillons, 24 variables
- **Give Me Some Credit (GMSC)** : 10,000 échantillons, 11 variables
- **Home Credit (HC)** : 15,000 échantillons, 110 variables

## 🛠️ Technologies

- **Python 3.12+**
- **Streamlit** : Interface web interactive
- **NumPy** : Calculs numériques
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **Scikit-learn** : Métriques d'évaluation

## 📚 Documentation

- `QUICK_START.md` : Guide de démarrage rapide
- `GUI_GUIDE.md` : Guide complet de l'interface
- `INSTALLATION.md` : Instructions d'installation détaillées

## 🎓 Contexte Académique

Cette application a été développée dans le cadre d'un projet de recherche sur l'apprentissage fédéré appliqué au scoring de crédit dans le contexte de l'Open Banking.

**Auteur :** © Adil OUALID

## 📄 Licence

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à créer une issue sur GitHub.

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile sur GitHub !**

