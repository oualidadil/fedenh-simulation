"""
Fonctionnalités avancées pour la simulation FedEnh
- Personnalisation locale
- Évaluations de performance avancées
- Tests et validation
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional
import json
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
import unittest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

@dataclass
class PerformanceMetrics:
    """Métriques de performance détaillées"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_score: float
    loss: float
    convergence_time: float
    communication_rounds: int

class LocalPersonalization:
    """Module de personnalisation locale pour adapter le modèle global aux spécificités locales"""
    
    def __init__(self, personalization_strength: float = 0.1):
        self.personalization_strength = personalization_strength
        self.local_adaptation_history = []
    
    def adapt_global_model(self, global_params: Dict[str, np.ndarray], 
                          local_data: Tuple[np.ndarray, np.ndarray],
                          client_id: int) -> Dict[str, np.ndarray]:
        """Adapter le modèle global aux spécificités locales"""
        
        # Calculer les statistiques locales
        local_stats = self._compute_local_statistics(local_data)
        
        # Adapter les paramètres selon les statistiques locales
        adapted_params = self._adapt_parameters(global_params, local_stats)
        
        # Enregistrer l'adaptation
        self.local_adaptation_history.append({
            'client_id': client_id,
            'adaptation_strength': self.personalization_strength,
            'local_stats': local_stats,
            'timestamp': time.time()
        })
        
        return adapted_params
    
    def _compute_local_statistics(self, local_data: Tuple[np.ndarray, np.ndarray]) -> Dict[str, Any]:
        """Calculer les statistiques des données locales"""
        x, y = local_data
        
        stats = {
            'mean': np.mean(x, axis=0),
            'std': np.std(x, axis=0),
            'class_distribution': np.sum(y, axis=0),
            'data_size': len(x),
            'feature_correlation': np.corrcoef(x.T) if x.shape[1] > 1 else np.array([[1.0]])
        }
        
        return stats
    
    def _adapt_parameters(self, global_params: Dict[str, np.ndarray], 
                         local_stats: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Adapter les paramètres selon les statistiques locales"""
        adapted_params = {}
        
        for key, param in global_params.items():
            if key == 'weights':
                # Adapter les poids selon la corrélation locale
                correlation_matrix = local_stats['feature_correlation']
                adaptation_factor = np.mean(correlation_matrix) * self.personalization_strength
                adapted_params[key] = param * (1 + adaptation_factor)
            elif key == 'bias':
                # Adapter le biais selon la distribution des classes
                class_ratio = local_stats['class_distribution'] / np.sum(local_stats['class_distribution'])
                bias_adaptation = (class_ratio - 0.5) * self.personalization_strength
                adapted_params[key] = param + bias_adaptation
            else:
                adapted_params[key] = param
        
        return adapted_params

class AdvancedEvaluator:
    """Évaluateur avancé pour analyser les performances du modèle"""
    
    def __init__(self):
        self.evaluation_history = []
        self.benchmark_models = {}
    
    def comprehensive_evaluation(self, model, test_data: Tuple[np.ndarray, np.ndarray],
                               client_id: Optional[int] = None) -> PerformanceMetrics:
        """Évaluation complète des performances"""
        x_test, y_test = test_data
        
        # Prédictions
        predictions = model.predict(x_test)
        probabilities = model.forward(x_test)
        
        # Métriques de base
        accuracy = accuracy_score(np.argmax(y_test, axis=1), predictions)
        precision = precision_score(np.argmax(y_test, axis=1), predictions, average='weighted')
        recall = recall_score(np.argmax(y_test, axis=1), predictions, average='weighted')
        f1 = f1_score(np.argmax(y_test, axis=1), predictions, average='weighted')
        
        # AUC (si binaire)
        if y_test.shape[1] == 2:
            auc = roc_auc_score(y_test[:, 1], probabilities[:, 1])
        else:
            auc = 0.0  # AUC multi-classe plus complexe
        
        # Loss
        loss = model.compute_loss(x_test, y_test)
        
        # Métriques de convergence
        convergence_time = len(self.evaluation_history) if self.evaluation_history else 0
        
        metrics = PerformanceMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            auc_score=auc,
            loss=loss,
            convergence_time=convergence_time,
            communication_rounds=0  # Sera mis à jour par la simulation
        )
        
        # Enregistrer l'évaluation
        self.evaluation_history.append({
            'client_id': client_id,
            'metrics': metrics,
            'timestamp': time.time()
        })
        
        return metrics
    
    def compare_with_benchmarks(self, model, test_data: Tuple[np.ndarray, np.ndarray]) -> Dict[str, float]:
        """Comparer avec des modèles de référence"""
        x_test, y_test = test_data
        
        # Modèle aléatoire (baseline)
        random_predictions = np.random.randint(0, y_test.shape[1], len(x_test))
        random_accuracy = accuracy_score(np.argmax(y_test, axis=1), random_predictions)
        
        # Modèle majoritaire
        majority_class = np.argmax(np.sum(y_test, axis=0))
        majority_predictions = np.full(len(x_test), majority_class)
        majority_accuracy = accuracy_score(np.argmax(y_test, axis=1), majority_predictions)
        
        # Modèle actuel
        current_predictions = model.predict(x_test)
        current_accuracy = accuracy_score(np.argmax(y_test, axis=1), current_predictions)
        
        return {
            'random_baseline': random_accuracy,
            'majority_baseline': majority_accuracy,
            'current_model': current_accuracy,
            'improvement_over_random': current_accuracy - random_accuracy,
            'improvement_over_majority': current_accuracy - majority_accuracy
        }
    
    def analyze_fairness(self, model, test_data: Tuple[np.ndarray, np.ndarray],
                        sensitive_features: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Analyser l'équité du modèle"""
        x_test, y_test = test_data
        predictions = model.predict(x_test)
        true_labels = np.argmax(y_test, axis=1)
        
        if sensitive_features is not None:
            # Analyser les performances par groupe
            unique_groups = np.unique(sensitive_features)
            group_accuracies = {}
            
            for group in unique_groups:
                group_mask = sensitive_features == group
                group_accuracy = accuracy_score(true_labels[group_mask], predictions[group_mask])
                group_accuracies[f'group_{group}'] = group_accuracy
            
            # Calculer l'écart de performance
            accuracies = list(group_accuracies.values())
            fairness_gap = max(accuracies) - min(accuracies)
            
            return {
                'fairness_gap': fairness_gap,
                'group_accuracies': group_accuracies,
                'is_fair': fairness_gap < 0.1  # Seuil d'équité
            }
        else:
            return {'fairness_gap': 0.0, 'is_fair': True}

class PrivacyAnalyzer:
    """Analyseur de confidentialité pour évaluer les mécanismes de protection"""
    
    def __init__(self):
        self.privacy_metrics = []
    
    def analyze_differential_privacy(self, noise_multiplier: float, 
                                   l2_norm_clip: float, 
                                   data_size: int) -> Dict[str, float]:
        """Analyser l'efficacité de la confidentialité différentielle"""
        
        # Calculer epsilon (privacy budget)
        epsilon = self._compute_epsilon(noise_multiplier, l2_norm_clip, data_size)
        
        # Calculer delta (probabilité de fuite)
        delta = 1.0 / data_size
        
        # Évaluer la privacy-utility trade-off
        privacy_score = self._compute_privacy_score(epsilon, delta)
        
        metrics = {
            'epsilon': epsilon,
            'delta': delta,
            'privacy_score': privacy_score,
            'noise_multiplier': noise_multiplier,
            'l2_norm_clip': l2_norm_clip,
            'is_private': epsilon < 10.0  # Seuil de confidentialité
        }
        
        self.privacy_metrics.append(metrics)
        return metrics
    
    def _compute_epsilon(self, noise_multiplier: float, l2_norm_clip: float, 
                        data_size: int) -> float:
        """Calculer epsilon pour la confidentialité différentielle"""
        # Formule simplifiée pour l'analyse
        epsilon = (2 * l2_norm_clip) / (noise_multiplier * np.sqrt(data_size))
        return epsilon
    
    def _compute_privacy_score(self, epsilon: float, delta: float) -> float:
        """Calculer un score de confidentialité (0-1, plus élevé = plus privé)"""
        # Score basé sur epsilon et delta
        epsilon_score = max(0, 1 - epsilon / 10.0)  # Normaliser epsilon
        delta_score = max(0, 1 - delta * 1000)      # Normaliser delta
        
        return (epsilon_score + delta_score) / 2

class FedEnhTester(unittest.TestCase):
    """Tests unitaires pour la simulation FedEnh"""
    
    def setUp(self):
        """Configuration des tests"""
        from fedenh_simulation import SimulationConfig, LogisticRegressionModel, Client, Server
        
        self.config = SimulationConfig(
            num_clients=5,
            num_rounds=10,
            client_fraction=0.6,
            data_size_per_client=100
        )
        
        self.model = LogisticRegressionModel(10, 2)
        self.test_data = (np.random.normal(0, 1, (50, 10)), 
                         np.random.randint(0, 2, (50, 2)))
        
        # Importer les classes pour les tests
        self.Client = Client
        self.Server = Server
    
    def test_model_initialization(self):
        """Tester l'initialisation du modèle"""
        self.assertIsNotNone(self.model.weights)
        self.assertIsNotNone(self.model.bias)
        self.assertEqual(self.model.weights.shape, (10, 2))
        self.assertEqual(self.model.bias.shape, (2,))
    
    def test_forward_pass(self):
        """Tester le forward pass"""
        x = np.random.normal(0, 1, (10, 10))
        output = self.model.forward(x)
        
        self.assertEqual(output.shape, (10, 2))
        self.assertTrue(np.allclose(np.sum(output, axis=1), 1.0))  # Probabilités somment à 1
    
    def test_backward_pass(self):
        """Tester le backward pass"""
        x = np.random.normal(0, 1, (10, 10))
        y = np.random.randint(0, 2, (10, 2))
        output = self.model.forward(x)
        gradients = self.model.backward(x, y, output)
        
        self.assertIn('weights', gradients)
        self.assertIn('bias', gradients)
        self.assertEqual(gradients['weights'].shape, (10, 2))
        self.assertEqual(gradients['bias'].shape, (2,))
    
    def test_client_update(self):
        """Tester la mise à jour client"""
        client = self.Client(0, self.test_data, self.model, self.config)
        global_params = self.model.get_parameters()
        
        updated_params = client.client_update(global_params)
        
        self.assertIn('weights', updated_params)
        self.assertIn('bias', updated_params)
        self.assertEqual(len(client.local_losses), 1)
        self.assertEqual(len(client.local_accuracies), 1)
    
    def test_server_aggregation(self):
        """Tester l'agrégation serveur"""
        server = self.Server(self.model, self.config)
        
        # Simuler des mises à jour clients
        client_updates = []
        selected_clients = []
        
        for i in range(3):
            client = self.Client(i, self.test_data, self.model, self.config)
            client.data_size = 100
            selected_clients.append(client)
            client_updates.append(self.model.get_parameters())
        
        aggregated_params = server.aggregate_and_update(client_updates, selected_clients)
        
        self.assertIn('weights', aggregated_params)
        self.assertIn('bias', aggregated_params)
    
    def test_differential_privacy(self):
        """Tester la confidentialité différentielle"""
        client = self.Client(0, self.test_data, self.model, self.config)
        
        gradients = {
            'weights': np.random.normal(0, 1, (10, 2)),
            'bias': np.random.normal(0, 1, (2,))
        }
        
        # Faire une copie pour comparer
        original_gradients = {
            'weights': gradients['weights'].copy(),
            'bias': gradients['bias'].copy()
        }
        
        private_gradients = client.apply_differential_privacy(gradients)
        
        # Vérifier que le bruit a été ajouté
        self.assertFalse(np.array_equal(original_gradients['weights'], private_gradients['weights']))
        self.assertFalse(np.array_equal(original_gradients['bias'], private_gradients['bias']))

class PerformanceBenchmark:
    """Benchmark de performance pour comparer différentes configurations"""
    
    def __init__(self):
        self.benchmark_results = {}
    
    def run_benchmark(self, configs: List[Dict[str, Any]], 
                     num_runs: int = 3) -> Dict[str, List[float]]:
        """Exécuter un benchmark sur plusieurs configurations"""
        
        results = {}
        
        for config_dict in configs:
            config_name = f"config_{len(results)}"
            config_results = []
            
            print(f"🔄 Benchmark de {config_name}...")
            
            for run in range(num_runs):
                from fedenh_simulation import SimulationConfig, FedEnhSimulation
                
                config = SimulationConfig(**config_dict)
                simulation = FedEnhSimulation(config)
                simulation.setup_simulation()
                run_results = simulation.run_simulation()
                
                # Enregistrer les métriques finales
                final_accuracy = run_results['global_accuracies'][-1]
                final_loss = run_results['global_losses'][-1]
                convergence_rounds = len(run_results['rounds'])
                
                config_results.append({
                    'accuracy': final_accuracy,
                    'loss': final_loss,
                    'convergence_rounds': convergence_rounds
                })
            
            results[config_name] = config_results
        
        self.benchmark_results = results
        return results
    
    def analyze_benchmark_results(self) -> Dict[str, Any]:
        """Analyser les résultats du benchmark"""
        if not self.benchmark_results:
            return {}
        
        analysis = {}
        
        for config_name, runs in self.benchmark_results.items():
            accuracies = [run['accuracy'] for run in runs]
            losses = [run['loss'] for run in runs]
            convergence_rounds = [run['convergence_rounds'] for run in runs]
            
            analysis[config_name] = {
                'mean_accuracy': np.mean(accuracies),
                'std_accuracy': np.std(accuracies),
                'mean_loss': np.mean(losses),
                'std_loss': np.std(losses),
                'mean_convergence_rounds': np.mean(convergence_rounds),
                'std_convergence_rounds': np.std(convergence_rounds)
            }
        
        return analysis
    
    def plot_benchmark_comparison(self, save_path: str = None):
        """Visualiser la comparaison des benchmarks"""
        if not self.benchmark_results:
            print("Aucun résultat de benchmark disponible")
            return
        
        analysis = self.analyze_benchmark_results()
        
        config_names = list(analysis.keys())
        mean_accuracies = [analysis[name]['mean_accuracy'] for name in config_names]
        std_accuracies = [analysis[name]['std_accuracy'] for name in config_names]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graphique des précisions
        bars1 = ax1.bar(config_names, mean_accuracies, yerr=std_accuracies, 
                       capsize=5, alpha=0.7, color='skyblue')
        ax1.set_ylabel('Précision Moyenne')
        ax1.set_title('Comparaison des Précisions par Configuration')
        ax1.set_ylim(0, 1)
        
        # Ajouter les valeurs sur les barres
        for bar, mean, std in zip(bars1, mean_accuracies, std_accuracies):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.01,
                    f'{mean:.3f}±{std:.3f}', ha='center', va='bottom')
        
        # Graphique des rounds de convergence
        mean_rounds = [analysis[name]['mean_convergence_rounds'] for name in config_names]
        std_rounds = [analysis[name]['std_convergence_rounds'] for name in config_names]
        
        bars2 = ax2.bar(config_names, mean_rounds, yerr=std_rounds, 
                       capsize=5, alpha=0.7, color='lightcoral')
        ax2.set_ylabel('Rounds de Convergence Moyens')
        ax2.set_title('Comparaison des Rounds de Convergence')
        
        # Ajouter les valeurs sur les barres
        for bar, mean, std in zip(bars2, mean_rounds, std_rounds):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 1,
                    f'{mean:.1f}±{std:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()

def run_tests():
    """Exécuter tous les tests"""
    print("🧪 Exécution des tests FedEnh...")
    
    # Créer une suite de tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(FedEnhTester)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Afficher le résumé
    print(f"\n📊 Résumé des tests:")
    print(f"   Tests exécutés: {result.testsRun}")
    print(f"   Échecs: {len(result.failures)}")
    print(f"   Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Échecs:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Erreurs:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Exemple d'utilisation des fonctionnalités avancées
    print("🚀 Module de fonctionnalités avancées FedEnh chargé")
    
    # Exécuter les tests
    success = run_tests()
    
    if success:
        print("✅ Tous les tests sont passés avec succès!")
    else:
        print("❌ Certains tests ont échoué")
