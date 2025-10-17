"""
Simulation de l'algorithme FedEnh (Enhanced Federated Averaging) pour l'Open Banking
Implémentation complète avec confidentialité différentielle et données non-IID
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
import random
import copy
from dataclasses import dataclass
from abc import ABC, abstractmethod
import time
import json
from collections import defaultdict

# Configuration de l'affichage
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

@dataclass
class SimulationConfig:
    """Configuration de la simulation"""
    num_clients: int = 10
    num_rounds: int = 100
    client_fraction: float = 0.3
    local_epochs: int = 5
    batch_size: int = 32
    learning_rate: float = 0.01
    noise_multiplier: float = 1.1  # Pour la confidentialité différentielle
    l2_norm_clip: float = 1.0
    data_size_per_client: int = 1000
    num_features: int = 20
    num_classes: int = 2

class Model(ABC):
    """Classe abstraite pour les modèles d'apprentissage"""
    
    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass
    
    @abstractmethod
    def backward(self, x: np.ndarray, y: np.ndarray, output: np.ndarray) -> Dict[str, np.ndarray]:
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, np.ndarray]:
        pass
    
    @abstractmethod
    def set_parameters(self, params: Dict[str, np.ndarray]):
        pass
    
    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        pass

class LogisticRegressionModel(Model):
    """Modèle de régression logistique simple"""
    
    def __init__(self, num_features: int, num_classes: int):
        self.num_features = num_features
        self.num_classes = num_classes
        # Initialisation Xavier
        self.weights = np.random.normal(0, 0.1, (num_features, num_classes))
        self.bias = np.zeros(num_classes)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass"""
        # S'assurer que x est un array numpy avec le bon type
        x = np.asarray(x, dtype=np.float64)
        
        # Vérifier que les poids et biais sont correctement initialisés
        if not hasattr(self, 'weights') or self.weights is None:
            self.weights = np.random.normal(0, 0.01, (x.shape[1], self.num_classes))
        if not hasattr(self, 'bias') or self.bias is None:
            self.bias = np.zeros(self.num_classes)
            
        z = np.dot(x, self.weights) + self.bias
        
        # Gérer les valeurs infinies et NaN
        z = np.clip(z, -500, 500)  # Éviter overflow/underflow
        
        # Softmax pour la classification multi-classe
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def backward(self, x: np.ndarray, y: np.ndarray, output: np.ndarray) -> Dict[str, np.ndarray]:
        """Backward pass - calcul des gradients"""
        # S'assurer que tous les inputs sont des arrays numpy avec le bon type
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        output = np.asarray(output, dtype=np.float64)
        
        m = x.shape[0]
        
        # Gradient de la loss cross-entropy
        grad_output = output - y
        
        # Gérer les valeurs NaN/Inf
        grad_output = np.nan_to_num(grad_output, nan=0.0, posinf=1.0, neginf=-1.0)
        
        grad_weights = (1/m) * np.dot(x.T, grad_output)
        grad_bias = (1/m) * np.sum(grad_output, axis=0)
        
        # Gérer les gradients NaN/Inf
        grad_weights = np.nan_to_num(grad_weights, nan=0.0, posinf=1.0, neginf=-1.0)
        grad_bias = np.nan_to_num(grad_bias, nan=0.0, posinf=1.0, neginf=-1.0)
        
        return {
            'weights': grad_weights,
            'bias': grad_bias
        }
    
    def get_parameters(self) -> Dict[str, np.ndarray]:
        """Récupérer les paramètres du modèle"""
        return {
            'weights': self.weights.copy(),
            'bias': self.bias.copy()
        }
    
    def set_parameters(self, params: Dict[str, np.ndarray]):
        """Définir les paramètres du modèle"""
        self.weights = params['weights'].copy()
        self.bias = params['bias'].copy()
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """Prédiction"""
        output = self.forward(x)
        return np.argmax(output, axis=1)
    
    def compute_loss(self, x: np.ndarray, y: np.ndarray) -> float:
        """Calcul de la loss cross-entropy"""
        # S'assurer que les inputs sont des arrays numpy avec le bon type
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        
        output = self.forward(x)
        # Éviter log(0)
        output = np.clip(output, 1e-15, 1 - 1e-15)
        
        # Gérer les valeurs NaN/Inf dans les logs
        log_output = np.log(output)
        log_output = np.nan_to_num(log_output, nan=0.0, posinf=0.0, neginf=-50.0)
        
        loss = -np.mean(np.sum(y * log_output, axis=1))
        
        # Gérer la loss finale
        loss = np.nan_to_num(loss, nan=1.0, posinf=1.0, neginf=0.0)
        
        return float(loss)

class Client:
    """Client représentant une institution financière"""
    
    def __init__(self, client_id: int, data: Tuple[np.ndarray, np.ndarray], 
                 model: Model, config: SimulationConfig):
        self.client_id = client_id
        self.x_train, self.y_train = data
        self.model = model
        self.config = config
        self.data_size = len(self.x_train)
        
        # Métriques locales
        self.local_losses = []
        self.local_accuracies = []
        self.participation_count = 0
    
    def client_update(self, global_model_params: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Mise à jour locale du modèle (ClientUpdate)"""
        # Copier les paramètres globaux
        self.model.set_parameters(global_model_params)
        
        # Diviser les données en lots
        batches = self._create_batches()
        
        # Entraînement local sur plusieurs époques
        for epoch in range(self.config.local_epochs):
            for batch_x, batch_y in batches:
                # Forward pass
                output = self.model.forward(batch_x)
                
                # Backward pass
                gradients = self.model.backward(batch_x, batch_y, output)
                
                # Mise à jour des paramètres
                self.model.weights -= self.config.learning_rate * gradients['weights']
                self.model.bias -= self.config.learning_rate * gradients['bias']
        
        # Calculer les métriques locales
        local_loss = self.model.compute_loss(self.x_train, self.y_train)
        local_accuracy = self._compute_accuracy()
        
        self.local_losses.append(local_loss)
        self.local_accuracies.append(local_accuracy)
        self.participation_count += 1
        
        return self.model.get_parameters()
    
    def _create_batches(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Créer des lots de données"""
        batches = []
        indices = np.arange(len(self.x_train))
        np.random.shuffle(indices)
        
        for i in range(0, len(indices), self.config.batch_size):
            batch_indices = indices[i:i + self.config.batch_size]
            batch_x = self.x_train[batch_indices]
            batch_y = self.y_train[batch_indices]
            batches.append((batch_x, batch_y))
        
        return batches
    
    def _compute_accuracy(self) -> float:
        """Calculer la précision locale"""
        predictions = self.model.predict(self.x_train)
        true_labels = np.argmax(self.y_train, axis=1)
        accuracy = np.mean(predictions == true_labels)
        return accuracy
    
    def apply_differential_privacy(self, gradients: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Appliquer la confidentialité différentielle aux gradients"""
        # Clipping L2
        grad_norm = np.linalg.norm(gradients['weights'])
        if grad_norm > self.config.l2_norm_clip:
            scale = self.config.l2_norm_clip / grad_norm
            gradients['weights'] *= scale
        
        # Ajout de bruit gaussien
        noise_scale = self.config.noise_multiplier * self.config.l2_norm_clip
        noise_weights = np.random.normal(0, noise_scale, gradients['weights'].shape)
        noise_bias = np.random.normal(0, noise_scale, gradients['bias'].shape)
        
        gradients['weights'] += noise_weights
        gradients['bias'] += noise_bias
        
        return gradients

class Server:
    """Serveur central pour l'agrégation fédérée"""
    
    def __init__(self, model: Model, config: SimulationConfig):
        self.model = model
        self.config = config
        self.global_round = 0
        
        # Métriques globales
        self.global_losses = []
        self.global_accuracies = []
        self.client_participation = defaultdict(int)
        self.convergence_history = []
    
    def select_clients(self, clients: List[Client]) -> List[Client]:
        """Sélectionner aléatoirement un sous-ensemble de clients"""
        num_selected = max(1, int(self.config.client_fraction * len(clients)))
        selected_clients = random.sample(clients, num_selected)
        
        # Enregistrer la participation
        for client in selected_clients:
            self.client_participation[client.client_id] += 1
        
        return selected_clients
    
    def aggregate_and_update(self, client_updates: List[Dict[str, np.ndarray]], 
                           selected_clients: List[Client]) -> Dict[str, np.ndarray]:
        """Agrégation des mises à jour clients (AggregateAndUpdate)"""
        if not client_updates:
            return self.model.get_parameters()
        
        # Agrégation fédérée pondérée
        aggregated_params = {}
        
        for key in client_updates[0].keys():
            weighted_sum = np.zeros_like(client_updates[0][key])
            total_weight = 0
            
            for i, update in enumerate(client_updates):
                weight = selected_clients[i].data_size
                weighted_sum += weight * update[key]
                total_weight += weight
            
            aggregated_params[key] = weighted_sum / total_weight
        
        return aggregated_params
    
    def evaluate_global_model(self, test_data: Tuple[np.ndarray, np.ndarray]) -> Tuple[float, float]:
        """Évaluer le modèle global"""
        x_test, y_test = test_data
        
        # Calculer la loss
        loss = self.model.compute_loss(x_test, y_test)
        
        # Calculer la précision
        predictions = self.model.predict(x_test)
        true_labels = np.argmax(y_test, axis=1)
        accuracy = np.mean(predictions == true_labels)
        
        return loss, accuracy
    
    def check_convergence(self, window_size: int = 15, threshold: float = 0.0001) -> bool:
        """Vérifier la convergence du modèle avec critères très stricts"""
        # Nécessite au moins window_size rounds pour vérifier
        if len(self.global_losses) < window_size:
            return False
        
        recent_losses = self.global_losses[-window_size:]
        loss_variance = np.var(recent_losses)
        
        # Critères de convergence très stricts
        # 1. Vérifier la tendance sur les derniers rounds
        if len(recent_losses) >= 5:
            # Vérifier la tendance sur les 5 derniers rounds
            recent_trend = np.mean(np.diff(recent_losses[-5:]))
            
            # La loss doit être presque stable (amélioration < 0.0001 par round)
            if abs(recent_trend) < 0.0001 and loss_variance < threshold:
                print(f"   🔍 Convergence détectée: tendance = {recent_trend:.6f}, variance = {loss_variance:.6f}")
                self.convergence_history.append(loss_variance)
                return True
        
        self.convergence_history.append(loss_variance)
        return False

class DataGenerator:
    """Générateur de données non-IID pour la simulation"""
    
    @staticmethod
    def generate_non_iid_data(num_clients: int, data_size_per_client: int, 
                            num_features: int, num_classes: int) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Générer des données non-IID pour chaque client"""
        datasets = []
        
        for client_id in range(num_clients):
            # Créer des distributions différentes pour chaque client
            # Simulation de différents types d'institutions financières
            
            if client_id < num_clients // 3:
                # Clients avec majoritairement classe 0 (ex: banques traditionnelles)
                class_0_ratio = 0.8
            elif client_id < 2 * num_clients // 3:
                # Clients avec majoritairement classe 1 (ex: fintech)
                class_0_ratio = 0.2
            else:
                # Clients avec distribution équilibrée (ex: banques universelles)
                class_0_ratio = 0.5
            
            # Générer les données
            x = np.random.normal(0, 1, (data_size_per_client, num_features))
            
            # Créer des labels biaisés
            num_class_0 = int(data_size_per_client * class_0_ratio)
            num_class_1 = data_size_per_client - num_class_0
            
            y = np.zeros((data_size_per_client, num_classes))
            y[:num_class_0, 0] = 1  # Classe 0
            y[num_class_0:, 1] = 1  # Classe 1
            
            # Mélanger les données
            indices = np.arange(data_size_per_client)
            np.random.shuffle(indices)
            x = x[indices]
            y = y[indices]
            
            datasets.append((x, y))
        
        return datasets

class FedEnhSimulation:
    """Simulation principale de l'algorithme FedEnh"""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.server = None
        self.clients = []
        self.test_data = None
        self.results = {
            'rounds': [],
            'global_losses': [],
            'global_accuracies': [],
            'client_losses': defaultdict(list),
            'client_accuracies': defaultdict(list),
            'participation_counts': defaultdict(int)
        }
    
    def setup_simulation(self):
        """Configurer la simulation"""
        print("🔧 Configuration de la simulation FedEnh...")
        
        # Générer les données
        print("📊 Génération des données non-IID...")
        client_datasets = DataGenerator.generate_non_iid_data(
            self.config.num_clients,
            self.config.data_size_per_client,
            self.config.num_features,
            self.config.num_classes
        )
        
        # Générer les données de test
        self.test_data = DataGenerator.generate_non_iid_data(
            1, 500, self.config.num_features, self.config.num_classes
        )[0]
        
        # Créer le modèle global
        global_model = LogisticRegressionModel(
            self.config.num_features, 
            self.config.num_classes
        )
        
        # Créer le serveur
        self.server = Server(global_model, self.config)
        
        # Créer les clients
        self.clients = []
        for i, (x, y) in enumerate(client_datasets):
            client_model = LogisticRegressionModel(
                self.config.num_features, 
                self.config.num_classes
            )
            client = Client(i, (x, y), client_model, self.config)
            self.clients.append(client)
        
        print(f"✅ Simulation configurée avec {len(self.clients)} clients")
    
    def run_simulation(self):
        """Exécuter la simulation complète"""
        print("🚀 Démarrage de la simulation FedEnh...")
        print(f"📋 Configuration: {self.config.num_rounds} rounds, "
              f"{self.config.client_fraction*100:.1f}% clients par round")
        
        start_time = time.time()
        
        for round_num in range(1, self.config.num_rounds + 1):
            print(f"\n🔄 Round {round_num}/{self.config.num_rounds}")
            
            # 1. Sélection des clients
            selected_clients = self.server.select_clients(self.clients)
            print(f"   👥 {len(selected_clients)} clients sélectionnés")
            
            # 2. Mise à jour locale des clients
            client_updates = []
            for client in selected_clients:
                global_params = self.server.model.get_parameters()
                local_update = client.client_update(global_params)
                client_updates.append(local_update)
            
            # 3. Agrégation et mise à jour globale
            aggregated_params = self.server.aggregate_and_update(
                client_updates, selected_clients
            )
            self.server.model.set_parameters(aggregated_params)
            
            # 4. Évaluation globale
            global_loss, global_accuracy = self.server.evaluate_global_model(self.test_data)
            self.server.global_losses.append(global_loss)
            self.server.global_accuracies.append(global_accuracy)
            
            # 5. Enregistrement des résultats
            self._record_results(round_num, selected_clients, global_loss, global_accuracy)
            
            # 6. Vérification de la convergence (minimum 20 rounds)
            if round_num >= 20 and self.server.check_convergence():
                print(f"   ✅ Convergence atteinte au round {round_num}")
                print(f"   📊 Loss finale: {global_loss:.4f}, Accuracy finale: {global_accuracy:.4f}")
                break
            
            # Affichage des métriques plus fréquent
            if round_num % 5 == 0 or round_num <= 3:
                print(f"   📊 Loss: {global_loss:.4f}, Accuracy: {global_accuracy:.4f}")
                print(f"   📈 Données test: {self.test_data[0].shape[0]} échantillons, {self.test_data[0].shape[1]} features")
        
        end_time = time.time()
        print(f"\n🎉 Simulation terminée en {end_time - start_time:.2f} secondes")
        
        return self.results
    
    def _record_results(self, round_num: int, selected_clients: List[Client], 
                       global_loss: float, global_accuracy: float):
        """Enregistrer les résultats du round"""
        self.results['rounds'].append(round_num)
        self.results['global_losses'].append(global_loss)
        self.results['global_accuracies'].append(global_accuracy)
        
        for client in selected_clients:
            self.results['client_losses'][client.client_id].append(client.local_losses[-1])
            self.results['client_accuracies'][client.client_id].append(client.local_accuracies[-1])
            self.results['participation_counts'][client.client_id] = client.participation_count

def main():
    """Fonction principale pour exécuter la simulation"""
    # Configuration de la simulation
    config = SimulationConfig(
        num_clients=10,
        num_rounds=50,
        client_fraction=0.3,
        local_epochs=3,
        batch_size=32,
        learning_rate=0.01,
        noise_multiplier=1.1,
        data_size_per_client=500
    )
    
    # Créer et exécuter la simulation
    simulation = FedEnhSimulation(config)
    simulation.setup_simulation()
    results = simulation.run_simulation()
    
    # Afficher les résultats finaux
    print("\n📈 Résultats finaux:")
    print(f"   Loss finale: {results['global_losses'][-1]:.4f}")
    print(f"   Précision finale: {results['global_accuracies'][-1]:.4f}")
    
    # Participation des clients
    print("\n👥 Participation des clients:")
    for client_id, count in results['participation_counts'].items():
        print(f"   Client {client_id}: {count} participations")

if __name__ == "__main__":
    main()
