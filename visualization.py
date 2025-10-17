"""
Module de visualisation pour la simulation FedEnh
Interface utilisateur avec graphiques et métriques en temps réel
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Any
import pandas as pd
from collections import defaultdict
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

class FedEnhVisualizer:
    """Visualiseur pour la simulation FedEnh"""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
        self.setup_style()
    
    def setup_style(self):
        """Configurer le style des graphiques"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configuration des couleurs
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'warning': '#C73E1D',
            'info': '#6A994E'
        }
    
    def plot_global_metrics(self, save_path: str = None):
        """Tracer les métriques globales (loss et accuracy)"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        rounds = self.results['rounds']
        losses = self.results['global_losses']
        accuracies = self.results['global_accuracies']
        
        # Graphique de la loss
        ax1.plot(rounds, losses, color=self.colors['primary'], linewidth=2, marker='o', markersize=4)
        ax1.set_xlabel('Rounds', fontsize=12)
        ax1.set_ylabel('Loss Globale', fontsize=12)
        ax1.set_title('Évolution de la Loss Globale', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(bottom=0)
        
        # Graphique de l'accuracy
        ax2.plot(rounds, accuracies, color=self.colors['success'], linewidth=2, marker='s', markersize=4)
        ax2.set_xlabel('Rounds', fontsize=12)
        ax2.set_ylabel('Précision Globale', fontsize=12)
        ax2.set_title('Évolution de la Précision Globale', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_client_participation(self, save_path: str = None):
        """Visualiser la participation des clients"""
        participation_counts = self.results['participation_counts']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graphique en barres de la participation
        client_ids = list(participation_counts.keys())
        counts = list(participation_counts.values())
        
        bars = ax1.bar(client_ids, counts, color=self.colors['info'], alpha=0.7)
        ax1.set_xlabel('ID Client', fontsize=12)
        ax1.set_ylabel('Nombre de Participations', fontsize=12)
        ax1.set_title('Participation des Clients', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Ajouter les valeurs sur les barres
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        # Graphique en camembert de la distribution
        total_participations = sum(counts)
        percentages = [count/total_participations * 100 for count in counts]
        
        wedges, texts, autotexts = ax2.pie(counts, labels=[f'Client {cid}' for cid in client_ids],
                                          autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribution de la Participation', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_client_metrics_evolution(self, save_path: str = None):
        """Tracer l'évolution des métriques par client"""
        client_losses = self.results['client_losses']
        client_accuracies = self.results['client_accuracies']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Graphique des losses par client
        for client_id, losses in client_losses.items():
            if losses:  # Vérifier que le client a participé
                rounds = list(range(1, len(losses) + 1))
                ax1.plot(rounds, losses, label=f'Client {client_id}', 
                        marker='o', markersize=3, alpha=0.7)
        
        ax1.set_xlabel('Rounds de Participation', fontsize=12)
        ax1.set_ylabel('Loss Locale', fontsize=12)
        ax1.set_title('Évolution de la Loss par Client', fontsize=14, fontweight='bold')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Graphique des accuracies par client
        for client_id, accuracies in client_accuracies.items():
            if accuracies:  # Vérifier que le client a participé
                rounds = list(range(1, len(accuracies) + 1))
                ax2.plot(rounds, accuracies, label=f'Client {client_id}', 
                        marker='s', markersize=3, alpha=0.7)
        
        ax2.set_xlabel('Rounds de Participation', fontsize=12)
        ax2.set_ylabel('Précision Locale', fontsize=12)
        ax2.set_title('Évolution de la Précision par Client', fontsize=14, fontweight='bold')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_convergence_analysis(self, save_path: str = None):
        """Analyser la convergence de l'algorithme"""
        rounds = self.results['rounds']
        losses = self.results['global_losses']
        accuracies = self.results['global_accuracies']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Loss avec moyenne mobile
        window_size = min(5, len(losses) // 4)
        if window_size > 1:
            moving_avg = np.convolve(losses, np.ones(window_size)/window_size, mode='valid')
            moving_rounds = rounds[window_size-1:]
            ax1.plot(moving_rounds, moving_avg, color=self.colors['warning'], 
                    linewidth=3, label=f'Moyenne mobile ({window_size})')
        
        ax1.plot(rounds, losses, color=self.colors['primary'], alpha=0.6, label='Loss originale')
        ax1.set_xlabel('Rounds')
        ax1.set_ylabel('Loss')
        ax1.set_title('Convergence de la Loss')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Dérivée de la loss (vitesse de convergence)
        if len(losses) > 1:
            loss_derivative = np.diff(losses)
            ax2.plot(rounds[1:], loss_derivative, color=self.colors['secondary'], linewidth=2)
            ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax2.set_xlabel('Rounds')
            ax2.set_ylabel('Variation de Loss')
            ax2.set_title('Vitesse de Convergence')
            ax2.grid(True, alpha=0.3)
        
        # 3. Accuracy avec moyenne mobile
        if window_size > 1:
            moving_avg_acc = np.convolve(accuracies, np.ones(window_size)/window_size, mode='valid')
            ax3.plot(moving_rounds, moving_avg_acc, color=self.colors['success'], 
                    linewidth=3, label=f'Moyenne mobile ({window_size})')
        
        ax3.plot(rounds, accuracies, color=self.colors['info'], alpha=0.6, label='Accuracy originale')
        ax3.set_xlabel('Rounds')
        ax3.set_ylabel('Précision')
        ax3.set_title('Convergence de la Précision')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 1)
        
        # 4. Distribution des améliorations
        if len(accuracies) > 1:
            improvements = np.diff(accuracies)
            ax4.hist(improvements, bins=20, color=self.colors['warning'], alpha=0.7, edgecolor='black')
            ax4.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Pas d\'amélioration')
            ax4.set_xlabel('Amélioration de Précision')
            ax4.set_ylabel('Fréquence')
            ax4.set_title('Distribution des Améliorations')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_dashboard(self):
        """Créer un tableau de bord interactif avec Plotly"""
        # Créer des sous-graphiques
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Loss Globale', 'Précision Globale', 
                          'Participation des Clients', 'Convergence'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        rounds = self.results['rounds']
        losses = self.results['global_losses']
        accuracies = self.results['global_accuracies']
        
        # 1. Loss globale
        fig.add_trace(
            go.Scatter(x=rounds, y=losses, mode='lines+markers',
                      name='Loss Globale', line=dict(color='#2E86AB', width=3)),
            row=1, col=1
        )
        
        # 2. Précision globale
        fig.add_trace(
            go.Scatter(x=rounds, y=accuracies, mode='lines+markers',
                      name='Précision Globale', line=dict(color='#F18F01', width=3)),
            row=1, col=2
        )
        
        # 3. Participation des clients
        participation_counts = self.results['participation_counts']
        client_ids = list(participation_counts.keys())
        counts = list(participation_counts.values())
        
        fig.add_trace(
            go.Bar(x=client_ids, y=counts, name='Participations',
                  marker_color='#6A994E'),
            row=2, col=1
        )
        
        # 4. Analyse de convergence (moyenne mobile)
        window_size = min(5, len(losses) // 4)
        if window_size > 1:
            moving_avg = np.convolve(losses, np.ones(window_size)/window_size, mode='valid')
            moving_rounds = rounds[window_size-1:]
            fig.add_trace(
                go.Scatter(x=moving_rounds, y=moving_avg, mode='lines',
                          name='Moyenne Mobile', line=dict(color='#A23B72', width=3)),
                row=2, col=2
            )
        
        # Mise à jour de la mise en page
        fig.update_layout(
            title_text="Tableau de Bord FedEnh - Simulation Open Banking",
            title_x=0.5,
            height=800,
            showlegend=True
        )
        
        # Mise à jour des axes
        fig.update_xaxes(title_text="Rounds", row=1, col=1)
        fig.update_yaxes(title_text="Loss", row=1, col=1)
        fig.update_xaxes(title_text="Rounds", row=1, col=2)
        fig.update_yaxes(title_text="Précision", row=1, col=2)
        fig.update_xaxes(title_text="ID Client", row=2, col=1)
        fig.update_yaxes(title_text="Participations", row=2, col=1)
        fig.update_xaxes(title_text="Rounds", row=2, col=2)
        fig.update_yaxes(title_text="Loss (Moyenne Mobile)", row=2, col=2)
        
        return fig
    
    def generate_summary_report(self) -> str:
        """Générer un rapport de synthèse"""
        rounds = self.results['rounds']
        losses = self.results['global_losses']
        accuracies = self.results['global_accuracies']
        participation_counts = self.results['participation_counts']
        
        report = f"""
# 📊 Rapport de Simulation FedEnh - Open Banking

## 🎯 Résultats Globaux
- **Rounds exécutés**: {len(rounds)}
- **Loss finale**: {losses[-1]:.4f}
- **Précision finale**: {accuracies[-1]:.4f}
- **Amélioration de la loss**: {((losses[0] - losses[-1]) / losses[0] * 100):.2f}%
- **Amélioration de la précision**: {((accuracies[-1] - accuracies[0]) / accuracies[0] * 100):.2f}%

## 👥 Participation des Clients
- **Nombre total de clients**: {len(participation_counts)}
- **Participations moyennes**: {np.mean(list(participation_counts.values())):.1f}
- **Participations max**: {max(participation_counts.values())}
- **Participations min**: {min(participation_counts.values())}

## 📈 Analyse de Convergence
- **Convergence atteinte**: {'Oui' if len(rounds) < 100 else 'Non'}
- **Rounds pour convergence**: {len(rounds)}
- **Stabilité finale**: {np.std(losses[-5:]) if len(losses) >= 5 else 'N/A'}

## 🏆 Top 3 Clients les Plus Actifs
"""
        
        sorted_participation = sorted(participation_counts.items(), key=lambda x: x[1], reverse=True)
        for i, (client_id, count) in enumerate(sorted_participation[:3], 1):
            report += f"{i}. Client {client_id}: {count} participations\n"
        
        return report

def create_streamlit_app():
    """Créer une application Streamlit pour l'interface utilisateur"""
    st.set_page_config(
        page_title="FedEnh Simulation - Open Banking",
        page_icon="🏦",
        layout="wide"
    )
    
    st.title("🏦 Simulation FedEnh - Open Banking")
    st.markdown("**Algorithme d'Apprentissage Fédéré Amélioré pour les Institutions Financières**")
    
    # Sidebar pour la configuration
    st.sidebar.header("⚙️ Configuration")
    
    num_clients = st.sidebar.slider("Nombre de clients", 5, 20, 10)
    num_rounds = st.sidebar.slider("Nombre de rounds", 10, 100, 50)
    client_fraction = st.sidebar.slider("Fraction de clients par round", 0.1, 1.0, 0.3)
    learning_rate = st.sidebar.slider("Taux d'apprentissage", 0.001, 0.1, 0.01)
    
    # Bouton pour lancer la simulation
    if st.sidebar.button("🚀 Lancer la Simulation"):
        with st.spinner("Exécution de la simulation..."):
            # Import et exécution de la simulation
            from fedenh_simulation import SimulationConfig, FedEnhSimulation
            
            config = SimulationConfig(
                num_clients=num_clients,
                num_rounds=num_rounds,
                client_fraction=client_fraction,
                learning_rate=learning_rate
            )
            
            simulation = FedEnhSimulation(config)
            simulation.setup_simulation()
            results = simulation.run_simulation()
            
            # Stocker les résultats dans la session
            st.session_state.results = results
    
    # Affichage des résultats
    if 'results' in st.session_state:
        results = st.session_state.results
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Loss Finale", f"{results['global_losses'][-1]:.4f}")
        
        with col2:
            st.metric("Précision Finale", f"{results['global_accuracies'][-1]:.4f}")
        
        with col3:
            st.metric("Rounds Exécutés", len(results['rounds']))
        
        with col4:
            total_participations = sum(results['participation_counts'].values())
            st.metric("Total Participations", total_participations)
        
        # Graphiques
        st.header("📊 Visualisations")
        
        # Créer le visualiseur
        visualizer = FedEnhVisualizer(results)
        
        # Graphiques avec Plotly
        fig = visualizer.create_interactive_dashboard()
        st.plotly_chart(fig, use_container_width=True)
        
        # Rapport de synthèse
        st.header("📋 Rapport de Synthèse")
        report = visualizer.generate_summary_report()
        st.markdown(report)
        
        # Téléchargement des résultats
        st.header("💾 Export des Résultats")
        
        # Convertir en JSON pour le téléchargement
        results_json = json.dumps(results, default=str, indent=2)
        
        st.download_button(
            label="📥 Télécharger les Résultats (JSON)",
            data=results_json,
            file_name="fedenh_simulation_results.json",
            mime="application/json"
        )

if __name__ == "__main__":
    # Exemple d'utilisation
    print("🎨 Module de visualisation FedEnh chargé")
    print("Pour utiliser l'interface Streamlit, exécutez: streamlit run visualization.py")
