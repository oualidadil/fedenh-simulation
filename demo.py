#!/usr/bin/env python3
"""
Démonstration complète de la simulation FedEnh
Script de démonstration avec exemples pratiques
"""

import numpy as np
import matplotlib.pyplot as plt
from fedenh_simulation import SimulationConfig, FedEnhSimulation
from visualization import FedEnhVisualizer
from enhanced_features import run_tests, PerformanceBenchmark, LocalPersonalization, AdvancedEvaluator

def demo_basic_simulation():
    """Démonstration de base de la simulation"""
    print("🎯 Démonstration 1: Simulation de Base")
    print("=" * 50)
    
    # Configuration simple
    config = SimulationConfig(
        num_clients=8,
        num_rounds=20,
        client_fraction=0.5,
        local_epochs=3,
        learning_rate=0.01,
        data_size_per_client=300
    )
    
    # Exécution
    simulation = FedEnhSimulation(config)
    simulation.setup_simulation()
    results = simulation.run_simulation()
    
    # Affichage des résultats
    print(f"\n📊 Résultats:")
    print(f"   Loss finale: {results['global_losses'][-1]:.4f}")
    print(f"   Précision finale: {results['global_accuracies'][-1]:.4f}")
    print(f"   Rounds exécutés: {len(results['rounds'])}")
    
    return results

def demo_visualization(results):
    """Démonstration des visualisations"""
    print("\n🎨 Démonstration 2: Visualisations")
    print("=" * 50)
    
    visualizer = FedEnhVisualizer(results)
    
    # Graphiques de base
    print("📈 Génération des graphiques...")
    visualizer.plot_global_metrics("demo_global_metrics.png")
    visualizer.plot_client_participation("demo_participation.png")
    
    # Tableau de bord interactif
    print("🌐 Création du tableau de bord interactif...")
    fig = visualizer.create_interactive_dashboard()
    fig.write_html("demo_dashboard.html")
    
    # Rapport de synthèse
    report = visualizer.generate_summary_report()
    print("\n📋 Rapport de Synthèse:")
    print(report[:500] + "..." if len(report) > 500 else report)

def demo_benchmark():
    """Démonstration du benchmark de performance"""
    print("\n🏁 Démonstration 3: Benchmark de Performance")
    print("=" * 50)
    
    benchmark = PerformanceBenchmark()
    
    # Configurations à comparer
    configs = [
        {
            'num_clients': 5,
            'num_rounds': 15,
            'client_fraction': 0.2,
            'learning_rate': 0.01
        },
        {
            'num_clients': 5,
            'num_rounds': 15,
            'client_fraction': 0.4,
            'learning_rate': 0.01
        },
        {
            'num_clients': 5,
            'num_rounds': 15,
            'client_fraction': 0.2,
            'learning_rate': 0.02
        }
    ]
    
    print("🔄 Exécution du benchmark...")
    results = benchmark.run_benchmark(configs, num_runs=2)
    
    # Analyse des résultats
    analysis = benchmark.analyze_benchmark_results()
    
    print("\n📊 Comparaison des Configurations:")
    for config_name, metrics in analysis.items():
        print(f"\n{config_name}:")
        print(f"  Précision: {metrics['mean_accuracy']:.4f} ± {metrics['std_accuracy']:.4f}")
        print(f"  Loss: {metrics['mean_loss']:.4f} ± {metrics['std_loss']:.4f}")
        print(f"  Convergence: {metrics['mean_convergence_rounds']:.1f} rounds")
    
    # Graphique de comparaison
    benchmark.plot_benchmark_comparison("demo_benchmark.png")
    print("\n📈 Graphique de benchmark sauvegardé: demo_benchmark.png")

def demo_advanced_features():
    """Démonstration des fonctionnalités avancées"""
    print("\n🚀 Démonstration 4: Fonctionnalités Avancées")
    print("=" * 50)
    
    # Personnalisation locale
    print("🎯 Test de la personnalisation locale...")
    personalizer = LocalPersonalization(personalization_strength=0.15)
    
    # Données simulées
    x = np.random.normal(0, 1, (100, 10))
    y = np.random.randint(0, 2, (100, 2))
    local_data = (x, y)
    
    # Paramètres globaux simulés
    global_params = {
        'weights': np.random.normal(0, 0.1, (10, 2)),
        'bias': np.zeros(2)
    }
    
    # Adaptation locale
    adapted_params = personalizer.adapt_global_model(global_params, local_data, client_id=0)
    
    print(f"   Adaptation appliquée avec force: {personalizer.personalization_strength}")
    print(f"   Historique d'adaptations: {len(personalizer.local_adaptation_history)}")
    
    # Évaluateur avancé
    print("\n📊 Test de l'évaluateur avancé...")
    evaluator = AdvancedEvaluator()
    
    # Modèle simulé pour l'évaluation
    from fedenh_simulation import LogisticRegressionModel
    model = LogisticRegressionModel(10, 2)
    
    # Évaluation complète
    metrics = evaluator.comprehensive_evaluation(model, local_data, client_id=0)
    
    print(f"   Précision: {metrics.accuracy:.4f}")
    print(f"   F1-Score: {metrics.f1_score:.4f}")
    print(f"   Loss: {metrics.loss:.4f}")
    
    # Comparaison avec benchmarks
    benchmark_comparison = evaluator.compare_with_benchmarks(model, local_data)
    print(f"\n📈 Comparaison avec benchmarks:")
    print(f"   Amélioration vs aléatoire: {benchmark_comparison['improvement_over_random']:.4f}")
    print(f"   Amélioration vs majoritaire: {benchmark_comparison['improvement_over_majority']:.4f}")

def demo_privacy_analysis():
    """Démonstration de l'analyse de confidentialité"""
    print("\n🔐 Démonstration 5: Analyse de Confidentialité")
    print("=" * 50)
    
    from enhanced_features import PrivacyAnalyzer
    
    analyzer = PrivacyAnalyzer()
    
    # Test de différents paramètres de confidentialité différentielle
    privacy_configs = [
        {'noise_multiplier': 0.5, 'l2_norm_clip': 1.0, 'data_size': 1000},
        {'noise_multiplier': 1.0, 'l2_norm_clip': 1.0, 'data_size': 1000},
        {'noise_multiplier': 2.0, 'l2_norm_clip': 1.0, 'data_size': 1000},
    ]
    
    print("🔍 Analyse de différents niveaux de confidentialité:")
    for i, config in enumerate(privacy_configs):
        metrics = analyzer.analyze_differential_privacy(**config)
        print(f"\nConfiguration {i+1}:")
        print(f"  Epsilon (ε): {metrics['epsilon']:.4f}")
        print(f"  Delta (δ): {metrics['delta']:.6f}")
        print(f"  Score de confidentialité: {metrics['privacy_score']:.4f}")
        print(f"  Confidentialité garantie: {'✅' if metrics['is_private'] else '❌'}")

def demo_scalability():
    """Démonstration de la scalabilité"""
    print("\n📈 Démonstration 6: Test de Scalabilité")
    print("=" * 50)
    
    # Test avec différents nombres de clients
    client_counts = [3, 5, 8, 10]
    results_scalability = {}
    
    for num_clients in client_counts:
        print(f"🔄 Test avec {num_clients} clients...")
        
        config = SimulationConfig(
            num_clients=num_clients,
            num_rounds=10,
            client_fraction=0.4,
            local_epochs=2,
            data_size_per_client=200
        )
        
        simulation = FedEnhSimulation(config)
        simulation.setup_simulation()
        results = simulation.run_simulation()
        
        results_scalability[num_clients] = {
            'final_accuracy': results['global_accuracies'][-1],
            'final_loss': results['global_losses'][-1],
            'rounds': len(results['rounds']),
            'total_participations': sum(results['participation_counts'].values())
        }
    
    # Affichage des résultats de scalabilité
    print("\n📊 Résultats de Scalabilité:")
    print("Clients | Précision | Loss    | Rounds | Participations")
    print("-" * 55)
    for num_clients, metrics in results_scalability.items():
        print(f"{num_clients:7d} | {metrics['final_accuracy']:8.4f} | {metrics['final_loss']:7.4f} | "
              f"{metrics['rounds']:6d} | {metrics['total_participations']:13d}")

def main():
    """Fonction principale de démonstration"""
    print("🏦 Démonstration Complète - Simulation FedEnh")
    print("=" * 60)
    print("Cette démonstration présente toutes les fonctionnalités")
    print("de l'application de simulation FedEnh pour l'Open Banking.")
    print("=" * 60)
    
    try:
        # 1. Simulation de base
        results = demo_basic_simulation()
        
        # 2. Visualisations
        demo_visualization(results)
        
        # 3. Benchmark de performance
        demo_benchmark()
        
        # 4. Fonctionnalités avancées
        demo_advanced_features()
        
        # 5. Analyse de confidentialité
        demo_privacy_analysis()
        
        # 6. Test de scalabilité
        demo_scalability()
        
        print("\n🎉 Démonstration terminée avec succès!")
        print("\n📁 Fichiers générés:")
        print("  - demo_global_metrics.png")
        print("  - demo_participation.png")
        print("  - demo_dashboard.html")
        print("  - demo_benchmark.png")
        print("  - simulation_report.md")
        
        print("\n💡 Prochaines étapes:")
        print("  1. Explorez les graphiques générés")
        print("  2. Ouvrez demo_dashboard.html dans votre navigateur")
        print("  3. Consultez simulation_report.md pour le rapport détaillé")
        print("  4. Lancez 'streamlit run visualization.py' pour l'interface web")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        print("Vérifiez que toutes les dépendances sont installées.")

if __name__ == "__main__":
    main()
