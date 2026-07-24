"""Outlier detection and data quality module."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class OutlierDetection:
    """Detect and handle outliers in the dataset."""
    
    def __init__(self, df, numeric_features=None):
        """Initialize outlier detection.
        
        Args:
            df: Input DataFrame
            numeric_features: List of numeric columns to check
        """
        self.df = df
        self.numeric_features = numeric_features or [
            'customer_age', 'income', 'purchase_amount',
            'number_of_purchases', 'customer_lifetime_value'
        ]
        self.outliers_info = {}
    
    def detect_outliers_iqr(self):
        """Detect outliers using IQR (Interquartile Range) method.
        
        Returns:
            dict: Outlier information for each feature
        """
        print("\n" + "=" * 80)
        print("--- OUTLIER DETECTION (IQR METHOD) ---")
        print("=" * 80)
        
        for col in self.numeric_features:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            
            self.outliers_info[col] = {
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': len(outliers),
                'outlier_percentage': (len(outliers) / len(self.df)) * 100
            }
            
            print(f"\n{col}:")
            print(f"  Lower Bound: {lower_bound:.2f}")
            print(f"  Upper Bound: {upper_bound:.2f}")
            print(f"  Outliers: {len(outliers)} ({self.outliers_info[col]['outlier_percentage']:.2f}%)")
        
        print("=" * 80 + "\n")
        
        return self.outliers_info
    
    def plot_boxplots(self, figsize=(15, 10), save_path=None):
        """Create box plots for outlier visualization.
        
        Args:
            figsize: Figure size tuple
            save_path: Optional path to save figure
        """
        print("Creating box plots...")
        
        plt.figure(figsize=figsize)
        n_features = len(self.numeric_features)
        n_cols = 2
        n_rows = (n_features + n_cols - 1) // n_cols
        
        for i, col in enumerate(self.numeric_features, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.boxplot(y=self.df[col], color='lightblue')
            plt.title(f'Box Plot: {col}', fontweight='bold')
            plt.ylabel(col)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Box plots saved to {save_path}")
        
        plt.show()
    
    def print_data_quality_report(self):
        """Print comprehensive data quality report."""
        print("\n" + "=" * 80)
        print("--- DATA QUALITY REPORT ---")
        print("=" * 80)
        
        total_outliers = sum([info['outlier_count'] for info in self.outliers_info.values()])
        
        print(f"\nTotal Outliers Detected: {total_outliers}")
        
        if total_outliers == 0:
            print("✓ No significant outliers detected using IQR method")
            print("✓ Data quality is good for modeling")
        else:
            print(f"⚠ {total_outliers} outlier(s) detected")
            print("  Recommendation: Investigate and decide on handling strategy")
        
        print("\nMissing Values Check:")
        missing = self.df.isnull().sum().sum()
        if missing == 0:
            print("✓ No missing values detected")
        else:
            print(f"⚠ {missing} missing value(s) detected")
        
        print("\nData Completeness:")
        for col in self.df.columns:
            completeness = (self.df[col].notna().sum() / len(self.df)) * 100
            print(f"  {col}: {completeness:.2f}%")
        
        print("=" * 80 + "\n")
