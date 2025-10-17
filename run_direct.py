#!/usr/bin/env python3
"""
Lancement direct de l'interface FedEnh
"""

import subprocess
import sys
import os

def main():
    print("🚀 Lancement direct de l'interface FedEnh...")
    print("=" * 50)
    
    # Vérifier que le fichier existe
    if not os.path.exists('gui_application.py'):
        print("❌ Fichier gui_application.py non trouvé")
        return
    
    print("📱 L'application sera accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Lancer Streamlit directement avec les paramètres minimaux
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 
            'gui_application.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'true'
        ]
        
        print(f"🔧 Commande: {' '.join(cmd)}")
        print("🚀 Lancement en cours...")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("💡 Essayez de lancer manuellement:")
        print("   streamlit run gui_application.py --server.port 8501")

if __name__ == "__main__":
    main()
