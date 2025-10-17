# 🚀 Guide d'Installation - Simulation FedEnh

## 📋 Prérequis

### Système d'Exploitation
- **macOS** 10.14+ (recommandé)
- **Linux** Ubuntu 18.04+ / CentOS 7+
- **Windows** 10+ (avec WSL recommandé)

### Python
- **Python 3.8+** (recommandé: Python 3.9 ou 3.10)
- **pip** (gestionnaire de paquets Python)

### Mémoire et Stockage
- **RAM**: Minimum 4GB, recommandé 8GB+
- **Stockage**: 2GB d'espace libre
- **CPU**: Processeur multi-cœurs recommandé

## 🔧 Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/votre-repo/fedenh_simulation.git
cd fedenh_simulation
```

### 2. Créer un Environnement Virtuel
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Vérifier l'Installation
```bash
python run_simulation.py --test
```

## 🐛 Résolution de Problèmes

### Problème: "externally-managed-environment"
**Solution**: Utiliser un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problème: Erreurs de compilation matplotlib
**Solution**: Installer les dépendances système
```bash
# Sur macOS avec Homebrew:
brew install pkg-config freetype

# Sur Ubuntu/Debian:
sudo apt-get install python3-dev pkg-config libfreetype6-dev

# Sur CentOS/RHEL:
sudo yum install python3-devel pkgconfig freetype-devel
```

### Problème: Erreurs de mémoire
**Solution**: Réduire la taille des données
```bash
python run_simulation.py --clients 5 --rounds 20
```

### Problème: Streamlit ne se lance pas
**Solution**: Vérifier l'installation
```bash
pip install --upgrade streamlit
streamlit --version
```

## 🔍 Tests de Validation

### Test Rapide
```bash
python run_simulation.py --clients 3 --rounds 5
```

### Test Complet
```bash
python demo.py
```

### Test des Tests Unitaires
```bash
python run_simulation.py --test
```

## 📊 Vérification des Performances

### Test de Scalabilité
```bash
python run_simulation.py --benchmark
```

### Test avec Configuration Avancée
```bash
python run_simulation.py --config config_advanced.json
```

## 🌐 Interface Web

### Lancer Streamlit
```bash
streamlit run visualization.py
```

### Accéder à l'Interface
- Ouvrir: http://localhost:8501
- Interface interactive disponible

## 📁 Structure des Fichiers

```
fedenh_simulation/
├── fedenh_simulation.py      # Simulation principale
├── visualization.py          # Visualisations et interface
├── enhanced_features.py      # Fonctionnalités avancées
├── run_simulation.py         # Script principal
├── demo.py                   # Démonstration complète
├── requirements.txt          # Dépendances Python
├── README.md                # Documentation principale
├── INSTALLATION.md          # Ce guide
├── config_example.json      # Configuration simple
├── config_advanced.json     # Configuration avancée
└── venv/                    # Environnement virtuel
```

## 🚀 Première Utilisation

### 1. Simulation de Base
```bash
python run_simulation.py --clients 10 --rounds 50
```

### 2. Avec Visualisations
```bash
python run_simulation.py --clients 10 --rounds 50 --visualize
```

### 3. Interface Web
```bash
streamlit run visualization.py
```

### 4. Démonstration Complète
```bash
python demo.py
```

## 🔧 Configuration Avancée

### Variables d'Environnement
```bash
export FEDENH_LOG_LEVEL=INFO
export FEDENH_MAX_CLIENTS=50
export FEDENH_CACHE_DIR=/tmp/fedenh
```

### Configuration Personnalisée
Créer un fichier `my_config.json`:
```json
{
  "num_clients": 20,
  "num_rounds": 100,
  "client_fraction": 0.3,
  "learning_rate": 0.01
}
```

Utiliser avec:
```bash
python run_simulation.py --config my_config.json
```

## 📞 Support

### Problèmes Courants
1. **ImportError**: Vérifier l'activation de l'environnement virtuel
2. **MemoryError**: Réduire le nombre de clients ou la taille des données
3. **TimeoutError**: Augmenter les timeouts ou réduire la complexité

### Logs et Debug
```bash
# Mode verbeux
python run_simulation.py --verbose

# Logs détaillés
python run_simulation.py --clients 5 --rounds 10 2>&1 | tee simulation.log
```

### Contact
- **Issues GitHub**: [Créer une issue](https://github.com/votre-repo/issues)
- **Documentation**: Consulter README.md
- **Email**: support@fedenh-simulation.com

## ✅ Checklist d'Installation

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Tests unitaires passent (`python run_simulation.py --test`)
- [ ] Simulation de base fonctionne
- [ ] Interface Streamlit accessible
- [ ] Visualisations générées correctement

## 🎉 Félicitations !

Votre installation de la simulation FedEnh est maintenant complète ! 

**Prochaines étapes:**
1. Explorez les exemples dans `demo.py`
2. Consultez la documentation dans `README.md`
3. Lancez l'interface web avec `streamlit run visualization.py`
4. Expérimentez avec différentes configurations

---

**Développé avec ❤️ pour l'Open Banking et l'Apprentissage Fédéré**
