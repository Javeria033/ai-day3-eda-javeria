"""Descriptive statistics and data summary module."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class DescriptiveStats:
    """Calculate and visualize descriptive statistics."""
    
    def __init__(self, df, features=None):
        """Initialize with DataFrame and features.
        
        Args:
            df: Input DataFrame
            features: List of numeric features to analyze
        """
        self.df = df
        self.features = features or [
            'customer_age', 'income', 'purchase_amount', 
            'number_of_purchases', 'customer_lifetime_value'
        ]
    
    def get_summary_statistics(self):
        """Generate summary statistics table.
        
        Returns:
            pd.DataFrame: Summary statistics for all features
        """
        print("\n" + "=" * 80)
        print("--- DESCRIPTIVE STATISTICS ---")
        print("=" * 80)
        
        summary_data = []
        for col in self.features:
            summary_data.append({
                'Feature': col,
                'Mean': round(self.df[col].mean(), 2),
                'Median': round(self.df[col].median(), 2),
                'Minimum': round(self.df[col].min(), 2),
                'Maximum': round(self.df[col].max(), 2),
                'Std Dev': round(self.df[col].std(), 2),
                'Observation (Count)': self.df[col].count()
            })
        
        summary_df = pd.DataFrame(summary_data)
        print(summary_df.to_string(index=False))
        print("=" * 80 + "\n")
        
        return summary_df
    
    def plot_distributions(self, figsize=(15, 10), save_path=None):
        """Create histograms for all features.
        
        Args:
            figsize: Figure size tuple
            save_path: Optional path to save figure
        """
        print("Creating distribution plots...")
        
        plt.figure(figsize=figsize)
        sns.set_theme(style="whitegrid")
        
        n_features = len(self.features)
        n_cols = 2
        n_rows = (n_features + n_cols - 1) // n_cols
        
        for i, col in enumerate(self.features, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.histplot(self.df[col], kde=True, bins=30, color='royalblue')
            plt.title(f'Distribution of {col}', fontsize=12, fontweight='bold')
            plt.xlabel(col)
            plt.ylabel('Frequency')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Distribution plots saved to {save_path}")
        
        plt.show()
    
    def print_basic_info(self):
        """Print basic dataset information."""
        print("\n" + "=" * 80)
        print("--- DATASET INFORMATION ---")
        print("=" * 80)
        print(f"Total Rows: {self.df.shape[0]}")
        print(f"Total Columns: {self.df.shape[1]}")
        print(f"\nColumn Names & Types:")
        for col, dtype in self.df.dtypes.items():
            print(f"  {col}: {dtype}")
        print(f"\nMissing Values:")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            print("  ✓ No missing values detected")
        else:
            print(missing[missing > 0])
        print(f"\nFirst 5 rows:")
        print(self.df.head())
        print("=" * 80 + "\n")
