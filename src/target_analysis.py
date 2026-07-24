"""Target variable analysis and categorization module."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class TargetAnalysis:
    """Analyze and categorize target variable."""
    
    def __init__(self, df, clv_column='customer_lifetime_value'):
        """Initialize target analysis.
        
        Args:
            df: Input DataFrame
            clv_column: Name of customer lifetime value column
        """
        self.df = df.copy()
        self.clv_column = clv_column
        self.target_col = 'purchase_category'
    
    def categorize_customers(self, high_threshold=3500, low_threshold=1500):
        """Categorize customers based on CLV thresholds.
        
        Args:
            high_threshold: CLV threshold for high-value customers
            low_threshold: CLV threshold for low-value customers
            
        Returns:
            pd.DataFrame: DataFrame with new target column
        """
        print("\n" + "=" * 80)
        print("--- TARGET VARIABLE CATEGORIZATION ---")
        print("=" * 80)
        
        conditions = [
            (self.df[self.clv_column] > high_threshold),
            (self.df[self.clv_column] >= low_threshold) & (self.df[self.clv_column] <= high_threshold),
            (self.df[self.clv_column] < low_threshold)
        ]
        choices = ['High Value Customer', 'Medium Value Customer', 'Low Value Customer']
        
        self.df[self.target_col] = np.select(conditions, choices, default='Medium Value Customer')
        
        print(f"\nThresholds:")
        print(f"  High Value:   CLV > {high_threshold}")
        print(f"  Medium Value: {low_threshold} ≤ CLV ≤ {high_threshold}")
        print(f"  Low Value:    CLV < {low_threshold}")
        
        print("\n" + "=" * 80 + "\n")
        
        return self.df
    
    def print_class_distribution(self):
        """Print class distribution statistics."""
        print("\n" + "=" * 80)
        print("--- TARGET CLASS DISTRIBUTION ---")
        print("=" * 80)
        
        class_counts = self.df[self.target_col].value_counts()
        class_percentages = self.df[self.target_col].value_counts(normalize=True) * 100
        
        print(f"\nClass Counts:")
        for cls, count in class_counts.items():
            pct = class_percentages[cls]
            print(f"  {cls:<25} {count:4d} ({pct:5.2f}%)")
        
        print(f"\nTotal Samples: {len(self.df)}")
        print("=" * 80 + "\n")
        
        return class_counts, class_percentages
    
    def plot_class_distribution(self, figsize=(10, 6), save_path=None):
        """Create visualizations of class distribution.
        
        Args:
            figsize: Figure size tuple
            save_path: Optional path to save figure
        """
        print("Creating class distribution plots...")
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Bar plot
        class_counts = self.df[self.target_col].value_counts()
        colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red
        
        axes[0].bar(class_counts.index, class_counts.values, color=colors, edgecolor='black')
        axes[0].set_title('Purchase Category Distribution', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Count')
        axes[0].set_xlabel('Category')
        for i, v in enumerate(class_counts.values):
            axes[0].text(i, v + 5, str(v), ha='center', fontweight='bold')
        
        # Pie chart
        class_percentages = self.df[self.target_col].value_counts(normalize=True) * 100
        axes[1].pie(
            class_percentages.values,
            labels=class_percentages.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        axes[1].set_title('Purchase Category Proportion', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Class distribution plots saved to {save_path}")
        
        plt.show()
    
    def check_class_imbalance(self):
        """Check and report on class imbalance."""
        print("\n" + "=" * 80)
        print("--- CLASS IMBALANCE ANALYSIS ---")
        print("=" * 80)
        
        class_counts = self.df[self.target_col].value_counts()
        imbalance_ratio = class_counts.max() / class_counts.min()
        
        print(f"\nImbalance Ratio: {imbalance_ratio:.2f}x")
        
        if imbalance_ratio > 3:
            print("⚠ Significant class imbalance detected!")
            print("  Recommendation: Use stratified sampling, SMOTE, or class weights")
        elif imbalance_ratio > 1.5:
            print("⚠ Moderate class imbalance detected")
            print("  Recommendation: Monitor model performance on minority class")
        else:
            print("✓ Classes are relatively balanced")
        
        print("=" * 80 + "\n")
        
        return imbalance_ratio
    
    def get_dataframe(self):
        """Return DataFrame with target column.
        
        Returns:
            pd.DataFrame: DataFrame with categorized target variable
        """
        return self.df
