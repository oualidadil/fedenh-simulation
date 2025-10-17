#!/usr/bin/env python3
"""
Lancement simple de l'interface FedEnh sans configuration
"""

import subprocess
import sys
import os
import time

def main():
    print("🚀 Lancement de l'interface graphique FedEnh...")
    print("=" * 50)
    
    # Tuer les processus Streamlit existants
    try:
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
        time.sleep(2)
    except:
        pass
    
    # Créer le fichier de configuration Streamlit pour éviter les prompts
    config_dir = os.path.expanduser("~/.streamlit")
    os.makedirs(config_dir, exist_ok=True)
    
    config_file = os.path.join(config_dir, "config.toml")
    with open(config_file, 'w') as f:
        f.write("""[server]
port = 8501
address = "localhost"
gatherUsageStats = false
enableCORS = false
enableXsrfProtection = false

[theme]
base = "light"
primaryColor = "#1f4e79"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
""")
    
    print("📱 L'application sera accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Lancer Streamlit avec configuration
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'gui_application.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
