#!/usr/bin/env python3
"""
Script principal pour exécuter la simulation FedEnh
Point d'entrée pour l'application de simulation
"""

import argparse
import json
import time
from pathlib import Path
from fedenh_simulation import SimulationConfig, FedEnhSimulation
from visualization import FedEnhVisualizer
from enhanced_features import run_tests, PerformanceBenchmark, LocalPersonalization

def parse_arguments():
    """Parser les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Simulation FedEnh - Open Banking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python run_simulation.py --clients 10 --rounds 50
  python run_simulation.py --config config.json --output results.json
  python run_simulation.py --benchmark --visualize
  python run_simulation.py --test
        """
    )
    
    # Paramètres de simulation
    parser.add_argument('--clients', type=int, default=10,
                       help='Nombre de clients (défaut: 10)')
    parser.add_argument('--rounds', type=int, default=50,
                       help='Nombre de rounds (défaut: 50)')
    parser.add_argument('--fraction', type=float, default=0.3,
                       help='Fraction de clients par round (défaut: 0.3)')
    parser.add_argument('--epochs', type=int, default=3,
                       help='Époques locales (défaut: 3)')
    parser.add_argument('--lr', type=float, default=0.01,
                       help='Taux d\'apprentissage (défaut: 0.01)')
    parser.add_argument('--noise', type=float, default=1.1,
                       help='Multiplicateur de bruit DP (défaut: 1.1)')
    
    # Fichiers
    parser.add_argument('--config', type=str,
                       help='Fichier de configuration JSON')
    parser.add_argument('--output', type=str,
                       help='Fichier de sortie pour les résultats')
    
    # Options
    parser.add_argument('--test', action='store_true',
                       help='Exécuter les tests unitaires')
    parser.add_argument('--benchmark', action='store_true',
                       help='Exécuter un benchmark de performance')
    parser.add_argument('--visualize', action='store_true',
                       help='Générer les visualisations')
    parser.add_argument('--streamlit', action='store_true',
                       help='Lancer l\'interface Streamlit')
    parser.add_argument('--verbose', action='store_true',
                       help='Mode verbeux')
    
    return parser.parse_args()

def load_config(config_file: str) -> SimulationConfig:
    """Charger la configuration depuis un fichier JSON"""
    with open(config_file, 'r') as f:
        config_dict = json.load(f)
    
    return SimulationConfig(**config_dict)

def save_results(results: dict, output_file: str):
    """Sauvegarder les résultats dans un fichier JSON"""
    # Convertir les defaultdict en dict pour la sérialisation
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, dict):
            serializable_results[key] = dict(value)
        else:
            serializable_results[key] = value
    
    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"💾 Résultats sauvegardés dans {output_file}")

def run_benchmark():
    """Exécuter un benchmark de performance"""
    print("🏁 Démarrage du benchmark de performance...")
    
    benchmark = PerformanceBenchmark()
    
    # Configurations à tester
    configs = [
        {
            'num_clients': 5,
            'num_rounds': 30,
            'client_fraction': 0.2,
            'local_epochs': 2,
            'learning_rate': 0.01
        },
        {
            'num_clients': 10,
            'num_rounds': 30,
            'client_fraction': 0.3,
            'local_epochs': 3,
            'learning_rate': 0.01
        },
        {
            'num_clients': 15,
            'num_rounds': 30,
            'client_fraction': 0.4,
            'local_epochs': 3,
            'learning_rate': 0.01
        },
        {
            'num_clients': 10,
            'num_rounds': 30,
            'client_fraction': 0.3,
            'local_epochs': 5,
            'learning_rate': 0.005
        }
    ]
    
    # Exécuter le benchmark
    results = benchmark.run_benchmark(configs, num_runs=3)
    
    # Analyser les résultats
    analysis = benchmark.analyze_benchmark_results()
    
    print("\n📊 Résultats du Benchmark:")
    for config_name, metrics in analysis.items():
        print(f"\n{config_name}:")
        print(f"  Précision: {metrics['mean_accuracy']:.4f} ± {metrics['std_accuracy']:.4f}")
        print(f"  Loss: {metrics['mean_loss']:.4f} ± {metrics['std_loss']:.4f}")
        print(f"  Convergence: {metrics['mean_convergence_rounds']:.1f} ± {metrics['std_convergence_rounds']:.1f} rounds")
    
    # Générer les graphiques
    benchmark.plot_benchmark_comparison("benchmark_results.png")
    print("📈 Graphiques de benchmark sauvegardés dans benchmark_results.png")
    
    return results

def run_visualization(results: dict):
    """Générer les visualisations"""
    print("🎨 Génération des visualisations...")
    
    visualizer = FedEnhVisualizer(results)
    
    # Graphiques statiques
    visualizer.plot_global_metrics("global_metrics.png")
    visualizer.plot_client_participation("client_participation.png")
    visualizer.plot_client_metrics_evolution("client_metrics.png")
    visualizer.plot_convergence_analysis("convergence_analysis.png")
    
    # Tableau de bord interactif
    fig = visualizer.create_interactive_dashboard()
    fig.write_html("interactive_dashboard.html")
    
    # Rapport de synthèse
    report = visualizer.generate_summary_report()
    with open("simulation_report.md", "w") as f:
        f.write(report)
    
    print("📊 Visualisations générées:")
    print("  - global_metrics.png")
    print("  - client_participation.png")
    print("  - client_metrics.png")
    print("  - convergence_analysis.png")
    print("  - interactive_dashboard.html")
    print("  - simulation_report.md")

def main():
    """Fonction principale"""
    args = parse_arguments()
    
    print("🏦 Simulation FedEnh - Open Banking")
    print("=" * 50)
    
    # Exécuter les tests si demandé
    if args.test:
        print("\n🧪 Exécution des tests unitaires...")
        success = run_tests()
        if not success:
            print("❌ Les tests ont échoué. Arrêt de l'exécution.")
            return
        print("✅ Tous les tests sont passés!")
    
    # Exécuter le benchmark si demandé
    if args.benchmark:
        benchmark_results = run_benchmark()
        if not args.visualize:
            return
    
    # Lancer Streamlit si demandé
    if args.streamlit:
        print("🌐 Lancement de l'interface Streamlit...")
        import subprocess
        subprocess.run(["streamlit", "run", "visualization.py"])
        return
    
    # Configuration de la simulation
    if args.config:
        config = load_config(args.config)
        print(f"📋 Configuration chargée depuis {args.config}")
    else:
        config = SimulationConfig(
            num_clients=args.clients,
            num_rounds=args.rounds,
            client_fraction=args.fraction,
            local_epochs=args.epochs,
            learning_rate=args.lr,
            noise_multiplier=args.noise
        )
        print(f"📋 Configuration: {args.clients} clients, {args.rounds} rounds, "
              f"{args.fraction*100:.1f}% par round")
    
    # Exécuter la simulation
    print("\n🚀 Démarrage de la simulation...")
    start_time = time.time()
    
    simulation = FedEnhSimulation(config)
    simulation.setup_simulation()
    results = simulation.run_simulation()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Afficher les résultats finaux
    print(f"\n🎉 Simulation terminée en {execution_time:.2f} secondes")
    print(f"📈 Résultats finaux:")
    print(f"   Loss finale: {results['global_losses'][-1]:.4f}")
    print(f"   Précision finale: {results['global_accuracies'][-1]:.4f}")
    print(f"   Rounds exécutés: {len(results['rounds'])}")
    
    # Sauvegarder les résultats
    if args.output:
        save_results(results, args.output)
    
    # Générer les visualisations
    if args.visualize:
        run_visualization(results)
    
    # Afficher un résumé de participation
    print(f"\n👥 Participation des clients:")
    for client_id, count in results['participation_counts'].items():
        print(f"   Client {client_id}: {count} participations")
    
    print(f"\n✨ Simulation FedEnh terminée avec succès!")

if __name__ == "__main__":
    main()
