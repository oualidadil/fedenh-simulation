#!/usr/bin/env python3
"""
Script de lancement pour l'interface graphique FedEnh
Lance l'application Streamlit avec configuration optimisée
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Packages manquants détectés:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Installez les packages manquants avec:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def generate_sample_datasets():
    """Générer des datasets d'exemple si nécessaire"""
    sample_files = ['tcd_sample.csv', 'gmsc_sample.csv', 'hc_sample.csv']
    missing_samples = [f for f in sample_files if not Path(f).exists()]
    
    if missing_samples:
        print("🔄 Génération des datasets d'exemple...")
        try:
            from demo_datasets import create_sample_datasets, save_datasets_to_csv
            datasets = create_sample_datasets()
            save_datasets_to_csv(datasets)
            print("✅ Datasets d'exemple générés avec succès!")
        except Exception as e:
            print(f"⚠️ Erreur lors de la génération des datasets: {e}")
            print("   L'application fonctionnera toujours, mais sans datasets d'exemple.")

def launch_streamlit():
    """Lancer l'application Streamlit"""
    print("🚀 Lancement de l'interface graphique FedEnh...")
    print("=" * 60)
    
    # Configuration Streamlit
    streamlit_config = {
        'server.port': 8501,
        'server.address': 'localhost',
        'browser.gatherUsageStats': 'false',
        'theme.base': 'light',
        'theme.primaryColor': '#1f4e79',
        'theme.backgroundColor': '#ffffff',
        'theme.secondaryBackgroundColor': '#f0f2f6',
        'theme.textColor': '#262730'
    }
    
    # Créer le fichier de configuration Streamlit
    config_dir = Path.home() / '.streamlit'
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w') as f:
        f.write('[server]\n')
        f.write('port = 8501\n')
        f.write('address = "localhost"\n')
        f.write('gatherUsageStats = false\n')
        f.write('\n[theme]\n')
        f.write('base = "light"\n')
        f.write('primaryColor = "#1f4e79"\n')
        f.write('backgroundColor = "#ffffff"\n')
        f.write('secondaryBackgroundColor = "#f0f2f6"\n')
        f.write('textColor = "#262730"\n')
    
    # Lancer Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'gui_application.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement de Streamlit: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
        return True
    
    return True

def main():
    """Fonction principale"""
    print("🏦 FedEnh Simulation - Interface Graphique")
    print("=" * 60)
    
    # Vérifier les dépendances
    print("🔍 Vérification des dépendances...")
    if not check_dependencies():
        print("\n❌ Veuillez installer les dépendances manquantes avant de continuer.")
        return 1
    
    print("✅ Toutes les dépendances sont installées")
    
    # Générer les datasets d'exemple
    generate_sample_datasets()
    
    # Lancer l'application
    print("\n🌐 Ouverture de l'interface web...")
    print("📱 L'application sera accessible à l'adresse: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter l'application")
    print("=" * 60)
    
    success = launch_streamlit()
    
    if success:
        print("\n🎉 Application fermée avec succès!")
        return 0
    else:
        print("\n❌ Erreur lors de l'exécution de l'application")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
