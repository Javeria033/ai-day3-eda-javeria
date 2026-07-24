"""
Configuration file for EDA analysis pipeline

This module contains all configurable parameters for the analysis.
Modify these settings to customize the analysis behavior.
"""

# Data Configuration
DATA_CONFIG = {
    'n_samples': 1000,
    'random_state': 42,
    'data_path': 'data/ecommerce_customers.csv',
    'output_dir': 'outputs/',
}

# Column Configuration
COLUMN_CONFIG = {
    'numeric_columns': ['age', 'income', 'purchase_amount', 'num_purchases', 'customer_lifetime_value'],
    'categorical_columns': ['purchase_category'],
    'target_column': 'purchase_category',
}

# Splitting Configuration
SPLITTING_CONFIG = {
    'train_size': 0.70,
    'val_size': 0.15,
    'test_size': 0.15,
    'random_state': 42,
    'stratify': True,
}

# Correlation Analysis Configuration
CORRELATION_CONFIG = {
    'method': 'pearson',
    'high_correlation_threshold': 0.8,
    'figsize': (10, 8),
    'cmap': 'coolwarm',
}

# Outlier Detection Configuration
OUTLIER_CONFIG = {
    'method': 'iqr',
    'iqr_multiplier': 1.5,
    'z_score_threshold': 3.0,
    'figsize': (15, 10),
}

# Target Analysis Configuration
TARGET_CONFIG = {
    'categories': ['Low Value Customer', 'Medium Value Customer', 'High Value Customer'],
    'bins': [0, 1750, 3500, float('inf')],
    'colors': ['red', 'orange', 'green'],
    'figsize': (8, 6),
}

# Leakage Detection Configuration
LEAKAGE_CONFIG = {
    'high_risk_keywords': ['future', 'target', 'lifetime', 'total', 'cumulative'],
    'temporal_features': ['date', 'time', 'period'],
    'risk_levels': ['HIGH', 'MEDIUM', 'LOW'],
}

# Visualization Configuration
VIZ_CONFIG = {
    'style': 'seaborn',
    'dpi': 300,
    'figsize_default': (10, 6),
    'font_size': 10,
    'save_format': 'png',
}

# Analysis Pipeline Configuration
PIPELINE_CONFIG = {
    'run_data_generation': True,
    'run_descriptive_stats': True,
    'run_distribution_analysis': True,
    'run_data_splitting': True,
    'run_correlation_analysis': True,
    'run_outlier_detection': True,
    'run_target_analysis': True,
    'run_leakage_detection': True,
    'generate_visualizations': True,
    'generate_report': True,
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': 'eda_analysis.log',
}