"""Data generation and loading module for e-commerce customer analysis."""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_sample_data(n_samples=1000, seed=42):
    """Generate sample e-commerce customer dataset.
    
    Args:
        n_samples: Number of customer samples to generate
        seed: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Generated customer dataset
    """
    np.random.seed(seed)
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'customer_age': np.random.randint(18, 70, size=n_samples),
        'income': np.random.randint(20000, 150000, size=n_samples),
        'purchase_amount': np.random.uniform(10, 500, size=n_samples),
        'number_of_purchases': np.random.randint(1, 20, size=n_samples),
        'customer_lifetime_value': np.random.uniform(100, 5000, size=n_samples)
    }
    
    df = pd.DataFrame(data)
    return df


def load_data(filepath):
    """Load customer dataset from CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"✓ Dataset loaded successfully from {filepath}")
    print(f"  Shape: {df.shape}")
    return df


def save_data(df, filepath):
    """Save dataset to CSV file.
    
    Args:
        df: DataFrame to save
        filepath: Destination file path
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"✓ Dataset saved to {filepath}")
