"""
Générateur de datasets de démonstration pour la simulation FedEnh
Simulation des datasets TCD, GMSC et HC avec caractéristiques réalistes
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import io

class CreditDatasetGenerator:
    """Générateur de datasets de crédit pour démonstration"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        np.random.seed(random_state)
    
    def generate_taiwan_credit_dataset(self, n_samples: int = 30000) -> pd.DataFrame:
        """Générer le Taiwan Credit Dataset (TCD) simulé"""
        
        # Paramètres basés sur le vrai dataset TCD
        n_default = int(n_samples * 0.22)  # 22% de défauts
        n_no_default = n_samples - n_default
        
        # Variables du dataset TCD
        data = {}
        
        # Variables démographiques
        data['LIMIT_BAL'] = np.random.exponential(100000, n_samples).astype(int)  # Limite de crédit
        data['SEX'] = np.random.choice([1, 2], n_samples)  # Sexe (1=male, 2=female)
        data['EDUCATION'] = np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.1, 0.3, 0.3, 0.2, 0.05, 0.05])
        data['MARRIAGE'] = np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.4, 0.1])
        data['AGE'] = np.random.normal(35, 10, n_samples).astype(int)
        data['AGE'] = np.clip(data['AGE'], 21, 80)
        
        # Variables de paiement (6 mois)
        for i in range(1, 7):
            data[f'PAY_AMT{i}'] = np.random.exponential(5000, n_samples).astype(int)
            data[f'BILL_AMT{i}'] = np.random.normal(40000, 20000, n_samples).astype(int)
            data[f'PAY_{i}'] = np.random.choice([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8], n_samples, 
                                              p=[0.1, 0.3, 0.2, 0.15, 0.1, 0.05, 0.03, 0.02, 0.02, 0.03])
        
        # Créer le DataFrame
        df = pd.DataFrame(data)
        
        # Générer la variable cible basée sur les patterns de paiement
        # Plus de retards de paiement = plus de risque de défaut
        payment_delays = df[['PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']].sum(axis=1)
        bill_ratio = df['BILL_AMT1'] / (df['LIMIT_BAL'] + 1)
        
        # Score de risque basé sur les variables
        risk_score = (
            payment_delays * 0.4 +
            bill_ratio * 0.3 +
            (df['AGE'] < 25) * 0.1 +
            (df['EDUCATION'] == 1) * 0.1 +
            (df['MARRIAGE'] == 3) * 0.1
        )
        
        # Générer les défauts
        default_prob = 1 / (1 + np.exp(-(risk_score - 2)))
        df['default'] = np.random.binomial(1, default_prob, n_samples)
        
        # Ajuster pour avoir le bon ratio
        current_default_ratio = df['default'].mean()
        target_ratio = 0.22
        
        if current_default_ratio > target_ratio:
            # Réduire les défauts
            threshold = np.percentile(default_prob, (1 - target_ratio) * 100)
            df.loc[default_prob < threshold, 'default'] = 0
        else:
            # Augmenter les défauts
            threshold = np.percentile(default_prob, target_ratio * 100)
            df.loc[default_prob > threshold, 'default'] = 1
        
        return df
    
    def generate_give_me_some_credit_dataset(self, n_samples: int = 150000) -> pd.DataFrame:
        """Générer le Give Me Some Credit Dataset simulé"""
        
        # Variables du dataset GMSC
        data = {}
        
        # Variables principales
        data['RevolvingUtilizationOfUnsecuredLines'] = np.random.beta(2, 5, n_samples)
        data['age'] = np.random.normal(45, 15, n_samples).astype(int)
        data['age'] = np.clip(data['age'], 18, 100)
        
        data['NumberOfTime30-59DaysPastDueNotWorse'] = np.random.poisson(0.5, n_samples)
        data['DebtRatio'] = np.random.beta(2, 3, n_samples)
        data['MonthlyIncome'] = np.random.lognormal(8.5, 0.8, n_samples).astype(int)
        data['NumberOfOpenCreditLinesAndLoans'] = np.random.poisson(8, n_samples)
        data['NumberOfTimes90DaysLate'] = np.random.poisson(0.2, n_samples)
        data['NumberRealEstateLoansOrLines'] = np.random.poisson(1, n_samples)
        data['NumberOfTime60-89DaysPastDueNotWorse'] = np.random.poisson(0.3, n_samples)
        data['NumberOfDependents'] = np.random.poisson(1, n_samples)
        
        # Créer le DataFrame
        df = pd.DataFrame(data)
        
        # Générer la variable cible
        risk_factors = (
            df['RevolvingUtilizationOfUnsecuredLines'] * 0.3 +
            df['NumberOfTime30-59DaysPastDueNotWorse'] * 0.2 +
            df['NumberOfTimes90DaysLate'] * 0.2 +
            df['DebtRatio'] * 0.15 +
            (df['age'] < 25) * 0.1 +
            (df['MonthlyIncome'] < 2000) * 0.05
        )
        
        default_prob = 1 / (1 + np.exp(-(risk_factors - 1.5)))
        df['SeriousDlqin2yrs'] = np.random.binomial(1, default_prob, n_samples)
        
        return df
    
    def generate_home_credit_dataset(self, n_samples: int = 300000) -> pd.DataFrame:
        """Générer le Home Credit Dataset simulé"""
        
        # Variables du dataset HC
        data = {}
        
        # Variables principales
        data['SK_ID_CURR'] = range(n_samples)
        data['TARGET'] = np.random.binomial(1, 0.08, n_samples)  # 8% de défauts
        
        # Variables démographiques
        data['NAME_CONTRACT_TYPE'] = np.random.choice(['Cash loans', 'Revolving loans'], n_samples, p=[0.7, 0.3])
        data['CODE_GENDER'] = np.random.choice(['M', 'F'], n_samples, p=[0.6, 0.4])
        data['FLAG_OWN_CAR'] = np.random.choice(['Y', 'N'], n_samples, p=[0.4, 0.6])
        data['FLAG_OWN_REALTY'] = np.random.choice(['Y', 'N'], n_samples, p=[0.6, 0.4])
        data['CNT_CHILDREN'] = np.random.poisson(1, n_samples)
        data['AMT_INCOME_TOTAL'] = np.random.lognormal(9, 0.8, n_samples).astype(int)
        data['AMT_CREDIT'] = np.random.lognormal(10, 0.5, n_samples).astype(int)
        data['AMT_ANNUITY'] = np.random.lognormal(8, 0.6, n_samples).astype(int)
        data['AMT_GOODS_PRICE'] = np.random.lognormal(9.5, 0.7, n_samples).astype(int)
        
        # Variables catégorielles
        data['NAME_TYPE_SUITE'] = np.random.choice(['Unaccompanied', 'Family', 'Spouse, partner', 'Children', 'Other_A', 'Other_B'], 
                                                  n_samples, p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
        data['NAME_INCOME_TYPE'] = np.random.choice(['Working', 'Commercial associate', 'Pensioner', 'State servant', 'Unemployed', 'Student'], 
                                                   n_samples, p=[0.7, 0.1, 0.1, 0.05, 0.03, 0.02])
        data['NAME_EDUCATION_TYPE'] = np.random.choice(['Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree'], 
                                                      n_samples, p=[0.5, 0.3, 0.1, 0.08, 0.02])
        data['NAME_FAMILY_STATUS'] = np.random.choice(['Married', 'Single / not married', 'Civil marriage', 'Separated', 'Widow', 'Unknown'], 
                                                     n_samples, p=[0.5, 0.3, 0.1, 0.05, 0.03, 0.02])
        data['NAME_HOUSING_TYPE'] = np.random.choice(['House / apartment', 'With parents', 'Municipal apartment', 'Rented apartment', 'Office apartment', 'Co-op apartment'], 
                                                    n_samples, p=[0.6, 0.15, 0.1, 0.1, 0.03, 0.02])
        
        # Variables numériques
        data['REGION_POPULATION_RELATIVE'] = np.random.beta(2, 5, n_samples)
        data['DAYS_BIRTH'] = -np.random.normal(35*365, 10*365, n_samples).astype(int)
        data['DAYS_EMPLOYED'] = -np.random.exponential(5*365, n_samples).astype(int)
        data['DAYS_REGISTRATION'] = -np.random.exponential(3*365, n_samples).astype(int)
        data['DAYS_ID_PUBLISH'] = -np.random.exponential(2*365, n_samples).astype(int)
        
        # Variables de contact
        data['OWN_CAR_AGE'] = np.random.exponential(5, n_samples)
        data['FLAG_MOBIL'] = np.random.choice([0, 1], n_samples, p=[0.05, 0.95])
        data['FLAG_EMP_PHONE'] = np.random.choice([0, 1], n_samples, p=[0.1, 0.9])
        data['FLAG_WORK_PHONE'] = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
        data['FLAG_CONT_MOBILE'] = np.random.choice([0, 1], n_samples, p=[0.02, 0.98])
        data['FLAG_PHONE'] = np.random.choice([0, 1], n_samples, p=[0.1, 0.9])
        data['FLAG_EMAIL'] = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
        
        # Variables de bureau
        data['CNT_FAM_MEMBERS'] = np.random.poisson(2, n_samples)
        data['REGION_RATING_CLIENT'] = np.random.choice([1, 2, 3], n_samples, p=[0.2, 0.5, 0.3])
        data['REGION_RATING_CLIENT_W_CITY'] = np.random.choice([1, 2, 3], n_samples, p=[0.2, 0.5, 0.3])
        data['WEEKDAY_APPR_PROCESS_START'] = np.random.choice(['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], 
                                                             n_samples, p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.1, 0.15])
        # Probabilités pour les heures (normalisées)
        hour_probs = [0.02]*12 + [0.04]*8 + [0.02]*4  # Total = 0.24 + 0.32 + 0.08 = 0.64
        hour_probs = [p/0.64 for p in hour_probs]  # Normaliser à 1.0
        data['HOUR_APPR_PROCESS_START'] = np.random.choice(range(24), n_samples, p=hour_probs)
        
        # Variables externes
        data['EXT_SOURCE_1'] = np.random.beta(2, 2, n_samples)
        data['EXT_SOURCE_2'] = np.random.beta(2, 2, n_samples)
        data['EXT_SOURCE_3'] = np.random.beta(2, 2, n_samples)
        
        # Variables calculées
        data['APARTMENTS_AVG'] = np.random.beta(2, 5, n_samples)
        data['BASEMENTAREA_AVG'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BEGINEXPLUATATION_AVG'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BUILD_AVG'] = np.random.beta(2, 5, n_samples)
        data['COMMONAREA_AVG'] = np.random.beta(2, 5, n_samples)
        data['ELEVATORS_AVG'] = np.random.beta(2, 5, n_samples)
        data['ENTRANCES_AVG'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMAX_AVG'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMIN_AVG'] = np.random.beta(2, 5, n_samples)
        data['LANDAREA_AVG'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAPARTMENTS_AVG'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAREA_AVG'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAPARTMENTS_AVG'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAREA_AVG'] = np.random.beta(2, 5, n_samples)
        
        # Variables de bureau
        data['APARTMENTS_MODE'] = np.random.beta(2, 5, n_samples)
        data['BASEMENTAREA_MODE'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BEGINEXPLUATATION_MODE'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BUILD_MODE'] = np.random.beta(2, 5, n_samples)
        data['COMMONAREA_MODE'] = np.random.beta(2, 5, n_samples)
        data['ELEVATORS_MODE'] = np.random.beta(2, 5, n_samples)
        data['ENTRANCES_MODE'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMAX_MODE'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMIN_MODE'] = np.random.beta(2, 5, n_samples)
        data['LANDAREA_MODE'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAPARTMENTS_MODE'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAREA_MODE'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAPARTMENTS_MODE'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAREA_MODE'] = np.random.beta(2, 5, n_samples)
        
        # Variables de bureau
        data['APARTMENTS_MEDI'] = np.random.beta(2, 5, n_samples)
        data['BASEMENTAREA_MEDI'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BEGINEXPLUATATION_MEDI'] = np.random.beta(2, 5, n_samples)
        data['YEARS_BUILD_MEDI'] = np.random.beta(2, 5, n_samples)
        data['COMMONAREA_MEDI'] = np.random.beta(2, 5, n_samples)
        data['ELEVATORS_MEDI'] = np.random.beta(2, 5, n_samples)
        data['ENTRANCES_MEDI'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMAX_MEDI'] = np.random.beta(2, 5, n_samples)
        data['FLOORSMIN_MEDI'] = np.random.beta(2, 5, n_samples)
        data['LANDAREA_MEDI'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAPARTMENTS_MEDI'] = np.random.beta(2, 5, n_samples)
        data['LIVINGAREA_MEDI'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAPARTMENTS_MEDI'] = np.random.beta(2, 5, n_samples)
        data['NONLIVINGAREA_MEDI'] = np.random.beta(2, 5, n_samples)
        
        # Variables de bureau
        data['TOTALAREA_MODE'] = np.random.beta(2, 5, n_samples)
        data['OBS_30_CNT_SOCIAL_CIRCLE'] = np.random.poisson(2, n_samples)
        data['DEF_30_CNT_SOCIAL_CIRCLE'] = np.random.poisson(0.5, n_samples)
        data['OBS_60_CNT_SOCIAL_CIRCLE'] = np.random.poisson(2, n_samples)
        data['DEF_60_CNT_SOCIAL_CIRCLE'] = np.random.poisson(0.5, n_samples)
        data['DAYS_LAST_PHONE_CHANGE'] = -np.random.exponential(365, n_samples).astype(int)
        
        # Variables de bureau
        data['FLAG_DOCUMENT_2'] = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
        data['FLAG_DOCUMENT_3'] = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
        data['FLAG_DOCUMENT_4'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_5'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_6'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_7'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_8'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_9'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_10'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_11'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_12'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_13'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_14'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_15'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_16'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_17'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_18'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_19'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        data['FLAG_DOCUMENT_20'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        data['FLAG_DOCUMENT_21'] = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
        
        # Variables de bureau
        data['AMT_REQ_CREDIT_BUREAU_HOUR'] = np.random.poisson(0.5, n_samples)
        data['AMT_REQ_CREDIT_BUREAU_DAY'] = np.random.poisson(1, n_samples)
        data['AMT_REQ_CREDIT_BUREAU_WEEK'] = np.random.poisson(2, n_samples)
        data['AMT_REQ_CREDIT_BUREAU_MON'] = np.random.poisson(5, n_samples)
        data['AMT_REQ_CREDIT_BUREAU_QRT'] = np.random.poisson(10, n_samples)
        data['AMT_REQ_CREDIT_BUREAU_YEAR'] = np.random.poisson(20, n_samples)
        
        # Créer le DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    def get_dataset_info(self, dataset_name: str) -> Dict:
        """Obtenir les informations sur un dataset"""
        info = {
            'TCD': {
                'name': 'Taiwan Credit Dataset',
                'description': 'Dataset UCI avec 30,000 échantillons et 23 variables',
                'samples': 30000,
                'features': 23,
                'target_ratio': 0.22,
                'source': 'UCI Machine Learning Repository'
            },
            'GMSC': {
                'name': 'Give Me Some Credit',
                'description': 'Dataset Kaggle avec 150,000 échantillons',
                'samples': 150000,
                'features': 11,
                'target_ratio': 0.067,
                'source': 'Kaggle Competition'
            },
            'HC': {
                'name': 'Home Credit',
                'description': 'Dataset Kaggle avec 300,000 échantillons et 122 variables',
                'samples': 300000,
                'features': 122,
                'target_ratio': 0.08,
                'source': 'Kaggle Competition'
            }
        }
        return info.get(dataset_name, {})

def create_sample_datasets():
    """Créer des datasets d'exemple pour la démonstration"""
    generator = CreditDatasetGenerator()
    
    # Générer les datasets
    tcd_data = generator.generate_taiwan_credit_dataset(5000)  # Version réduite pour la démo
    gmsc_data = generator.generate_give_me_some_credit_dataset(10000)  # Version réduite
    hc_data = generator.generate_home_credit_dataset(15000)  # Version réduite
    
    return {
        'TCD': tcd_data,
        'GMSC': gmsc_data,
        'HC': hc_data
    }

def save_datasets_to_csv(datasets: Dict[str, pd.DataFrame], output_dir: str = "."):
    """Sauvegarder les datasets en CSV"""
    for name, df in datasets.items():
        filename = f"{output_dir}/{name.lower()}_sample.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Dataset {name} sauvegardé: {filename}")

if __name__ == "__main__":
    # Générer et sauvegarder les datasets d'exemple
    print("🔄 Génération des datasets de démonstration...")
    datasets = create_sample_datasets()
    
    print("💾 Sauvegarde des datasets...")
    save_datasets_to_csv(datasets)
    
    print("📊 Résumé des datasets générés:")
    for name, df in datasets.items():
        info = CreditDatasetGenerator().get_dataset_info(name)
        print(f"\n{name}:")
        print(f"  - Échantillons: {df.shape[0]:,}")
        print(f"  - Variables: {df.shape[1]:,}")
        if 'default' in df.columns:
            default_ratio = df['default'].mean()
            print(f"  - Ratio de défaut: {default_ratio:.3f}")
        elif 'SeriousDlqin2yrs' in df.columns:
            default_ratio = df['SeriousDlqin2yrs'].mean()
            print(f"  - Ratio de défaut: {default_ratio:.3f}")
        elif 'TARGET' in df.columns:
            default_ratio = df['TARGET'].mean()
            print(f"  - Ratio de défaut: {default_ratio:.3f}")
    
    print("\n🎉 Datasets de démonstration générés avec succès!")
