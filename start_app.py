#!/usr/bin/env python3
"""
Script de lancement simple pour l'interface graphique FedEnh
"""

import subprocess
import sys
import os

def main():
    print("🚀 Lancement de l'interface graphique FedEnh...")
    print("=" * 50)
    print("📱 L'application sera accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Lancer Streamlit directement
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'gui_application.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
