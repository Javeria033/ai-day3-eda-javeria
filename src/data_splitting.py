"""Data splitting and sampling strategy module."""

import pandas as pd
from sklearn.model_selection import train_test_split


class DataSplitter:
    """Handle train-validation-test split strategies."""
    
    def __init__(self, df, random_state=42):
        """Initialize DataSplitter.
        
        Args:
            df: Input DataFrame
            random_state: Random seed for reproducibility
        """
        self.df = df
        self.random_state = random_state
        self.train_data = None
        self.val_data = None
        self.test_data = None
    
    def split_data(self, train_size=0.70, val_size=0.15, test_size=0.15):
        """Split data into train, validation, and test sets.
        
        Args:
            train_size: Proportion for training (default: 0.70)
            val_size: Proportion for validation (default: 0.15)
            test_size: Proportion for testing (default: 0.15)
            
        Returns:
            tuple: (train_data, val_data, test_data)
        """
        print("\n" + "=" * 80)
        print("--- DATA SPLITTING STRATEGY ---")
        print("=" * 80)
        
        # Verify proportions sum to 1
        assert abs(train_size + val_size + test_size - 1.0) < 0.001, \
            "Train, val, and test sizes must sum to 1.0"
        
        # First split: separate training data
        self.train_data, temp_data = train_test_split(
            self.df, 
            test_size=(1 - train_size), 
            random_state=self.random_state
        )
        
        # Second split: separate validation and test data
        val_test_split = test_size / (val_size + test_size)
        self.val_data, self.test_data = train_test_split(
            temp_data,
            test_size=val_test_split,
            random_state=self.random_state
        )
        
        # Print results
        total = len(self.df)
        print(f"Training Set:   {len(self.train_data):4d} rows ({len(self.train_data)/total*100:5.1f}%)")
        print(f"Validation Set: {len(self.val_data):4d} rows ({len(self.val_data)/total*100:5.1f}%)")
        print(f"Testing Set:    {len(self.test_data):4d} rows ({len(self.test_data)/total*100:5.1f}%)")
        print(f"Total:          {total:4d} rows")
        print("=" * 80 + "\n")
        
        return self.train_data, self.val_data, self.test_data
    
    def get_splits(self):
        """Get the current splits.
        
        Returns:
            tuple: (train_data, val_data, test_data)
        """
        if self.train_data is None:
            raise ValueError("Data has not been split yet. Call split_data() first.")
        
        return self.train_data, self.val_data, self.test_data
    
    def print_class_distribution(self, target_col):
        """Print class distribution across splits.
        
        Args:
            target_col: Name of target column
        """
        if self.train_data is None:
            raise ValueError("Data has not been split yet. Call split_data() first.")
        
        print("\n" + "=" * 80)
        print("--- CLASS DISTRIBUTION ACROSS SPLITS ---")
        print("=" * 80)
        
        for name, data in [('Training', self.train_data), 
                          ('Validation', self.val_data), 
                          ('Testing', self.test_data)]:
            print(f"\n{name} Set:")
            dist = data[target_col].value_counts(normalize=True) * 100
            for cls, pct in dist.items():
                print(f"  {cls}: {pct:6.2f}%")
        
        print("=" * 80 + "\n")
