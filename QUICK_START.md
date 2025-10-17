# ⚡ Guide de Démarrage Rapide - Simulation FedEnh

## 🚀 Démarrage en 5 Minutes

### 1. Installation Rapide
```bash
# Cloner et installer
git clone <votre-repo>
cd fedenh_simulation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Immédiat
```bash
# Simulation rapide (30 secondes)
python run_simulation.py --clients 5 --rounds 10

# Avec visualisations
python run_simulation.py --clients 5 --rounds 10 --visualize
```

### 3. Interface Web
```bash
# Lancer l'interface interactive
streamlit run visualization.py
# Ouvrir http://localhost:8501
```

## 🎯 Commandes Essentielles

### Simulation de Base
```bash
# Configuration simple
python run_simulation.py --clients 10 --rounds 50

# Avec fichier de configuration
python run_simulation.py --config config_example.json

# Mode verbeux
python run_simulation.py --clients 10 --rounds 50 --verbose
```

### Tests et Validation
```bash
# Tests unitaires
python run_simulation.py --test

# Benchmark de performance
python run_simulation.py --benchmark

# Démonstration complète
python demo.py
```

### Export des Résultats
```bash
# Sauvegarder les résultats
python run_simulation.py --clients 10 --rounds 50 --output results.json

# Générer les visualisations
python run_simulation.py --clients 10 --rounds 50 --visualize
```

## 📊 Exemples de Configuration

### Configuration Minimaliste
```bash
python run_simulation.py --clients 3 --rounds 5 --fraction 0.5
```

### Configuration Réaliste
```bash
python run_simulation.py --clients 15 --rounds 100 --fraction 0.3 --epochs 5
```

### Configuration Avancée
```bash
python run_simulation.py --config config_advanced.json --visualize
```

## 🎨 Visualisations Disponibles

### Graphiques Statiques
- `global_metrics.png` - Évolution des métriques globales
- `client_participation.png` - Participation des clients
- `convergence_analysis.png` - Analyse de convergence

### Interface Interactive
- `interactive_dashboard.html` - Tableau de bord Plotly
- Interface Streamlit - http://localhost:8501

### Rapports
- `simulation_report.md` - Rapport de synthèse détaillé

## 🔧 Paramètres Principaux

| Paramètre | Description | Valeur par Défaut | Exemple |
|-----------|-------------|-------------------|---------|
| `--clients` | Nombre de clients | 10 | `--clients 15` |
| `--rounds` | Nombre de rounds | 50 | `--rounds 100` |
| `--fraction` | Fraction de clients/round | 0.3 | `--fraction 0.5` |
| `--epochs` | Époques locales | 3 | `--epochs 5` |
| `--lr` | Taux d'apprentissage | 0.01 | `--lr 0.02` |
| `--noise` | Bruit DP | 1.1 | `--noise 1.5` |

## 📈 Interprétation des Résultats

### Métriques Clés
- **Loss finale** < 0.5 : Bonne convergence
- **Précision finale** > 0.7 : Performance acceptable
- **Rounds de convergence** < 50 : Convergence rapide

### Signaux d'Alerte
- **Loss qui augmente** : Taux d'apprentissage trop élevé
- **Pas de convergence** : Trop peu de rounds ou clients
- **Précision faible** : Données non-IID trop extrêmes

## 🚨 Résolution de Problèmes Rapide

### Erreur: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erreur: "Memory error"
```bash
python run_simulation.py --clients 3 --rounds 10
```

### Streamlit ne démarre pas
```bash
pip install --upgrade streamlit
streamlit run visualization.py
```

### Tests qui échouent
```bash
python run_simulation.py --test --verbose
```

## 🎯 Cas d'Usage Typiques

### 1. Démonstration Rapide
```bash
python demo.py
```

### 2. Recherche et Développement
```bash
python run_simulation.py --benchmark --visualize
```

### 3. Production/Évaluation
```bash
python run_simulation.py --config config_advanced.json --output production_results.json
```

### 4. Formation/Enseignement
```bash
streamlit run visualization.py
# Interface interactive pour l'apprentissage
```

## 📚 Ressources Supplémentaires

### Documentation Complète
- `README.md` - Documentation principale
- `INSTALLATION.md` - Guide d'installation détaillé
- `simulation_report.md` - Exemple de rapport

### Fichiers de Configuration
- `config_example.json` - Configuration simple
- `config_advanced.json` - Configuration avancée

### Exemples et Démonstrations
- `demo.py` - Démonstration complète
- `run_simulation.py` - Script principal avec options

## 🎉 Félicitations !

Vous êtes maintenant prêt à utiliser la simulation FedEnh ! 

**Prochaines étapes recommandées:**
1. 🚀 Lancez `python demo.py` pour voir toutes les fonctionnalités
2. 🌐 Ouvrez l'interface web avec `streamlit run visualization.py`
3. 🔬 Expérimentez avec différentes configurations
4. 📊 Analysez les résultats avec les visualisations

---

**Besoin d'aide ?** Consultez `README.md` ou créez une issue sur GitHub.
