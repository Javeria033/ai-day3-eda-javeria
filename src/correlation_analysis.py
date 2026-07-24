"""Correlation and relationship analysis module."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class CorrelationAnalysis:
    """Analyze correlations between features."""
    
    def __init__(self, df, numeric_features=None):
        """Initialize correlation analysis.
        
        Args:
            df: Input DataFrame
            numeric_features: List of numeric columns to analyze
        """
        self.df = df
        self.numeric_features = numeric_features or [
            'customer_age', 'income', 'purchase_amount',
            'number_of_purchases', 'customer_lifetime_value'
        ]
        self.corr_matrix = None
    
    def compute_correlation_matrix(self):
        """Compute Pearson correlation matrix.
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        print("\n" + "=" * 80)
        print("--- CORRELATION ANALYSIS ---")
        print("=" * 80)
        
        self.corr_matrix = self.df[self.numeric_features].corr()
        
        # Print key correlations
        print("\nKey Correlations:")
        print(f"  Income vs Purchase Amount:       {self.corr_matrix.loc['income', 'purchase_amount']:7.4f}")
        print(f"  Income vs CLV:                   {self.corr_matrix.loc['income', 'customer_lifetime_value']:7.4f}")
        print(f"  Age vs Number of Purchases:     {self.corr_matrix.loc['customer_age', 'number_of_purchases']:7.4f}")
        print(f"  Purchase Amount vs CLV:          {self.corr_matrix.loc['purchase_amount', 'customer_lifetime_value']:7.4f}")
        print("=" * 80 + "\n")
        
        return self.corr_matrix
    
    def plot_correlation_matrix(self, figsize=(8, 6), save_path=None):
        """Plot correlation matrix heatmap.
        
        Args:
            figsize: Figure size tuple
            save_path: Optional path to save figure
        """
        if self.corr_matrix is None:
            self.compute_correlation_matrix()
        
        print("Creating correlation heatmap...")
        
        plt.figure(figsize=figsize)
        sns.heatmap(
            self.corr_matrix,
            annot=True,
            cmap='coolwarm',
            center=0,
            fmt='.2f',
            square=True,
            linewidths=0.5
        )
        plt.title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Correlation heatmap saved to {save_path}")
        
        plt.show()
    
    def plot_scatter_relationships(self, x_col, y_col, save_path=None):
        """Create scatter plot for two features.
        
        Args:
            x_col: Column for x-axis
            y_col: Column for y-axis
            save_path: Optional path to save figure
        """
        print(f"Creating scatter plot: {x_col} vs {y_col}...")
        
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            x=x_col,
            y=y_col,
            data=self.df,
            alpha=0.6,
            color='purple',
            s=50
        )
        plt.title(f'{x_col} vs {y_col}', fontsize=14, fontweight='bold')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Scatter plot saved to {save_path}")
        
        plt.show()
    
    def get_high_correlations(self, threshold=0.8):
        """Get pairs of features with high correlation.
        
        Args:
            threshold: Correlation threshold (default: 0.8)
            
        Returns:
            list: List of tuples with high correlations
        """
        if self.corr_matrix is None:
            self.compute_correlation_matrix()
        
        high_corr = []
        for i in range(len(self.corr_matrix.columns)):
            for j in range(i+1, len(self.corr_matrix.columns)):
                if abs(self.corr_matrix.iloc[i, j]) > threshold:
                    high_corr.append((
                        self.corr_matrix.columns[i],
                        self.corr_matrix.columns[j],
                        self.corr_matrix.iloc[i, j]
                    ))
        
        return high_corr
