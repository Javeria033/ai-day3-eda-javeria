"""Data leakage detection and prevention module."""

import pandas as pd
import numpy as np


class LeakageDetection:
    """Identify and document potential data leakage risks."""
    
    def __init__(self, df, target_col='customer_lifetime_value'):
        """Initialize leakage detection.
        
        Args:
            df: Input DataFrame
            target_col: Target variable column name
        """
        self.df = df
        self.target_col = target_col
        self.leakage_risks = []
    
    def check_temporal_leakage(self):
        """Check for temporal data leakage risks.
        
        Returns:
            list: List of identified leakage risks
        """
        print("\n" + "=" * 80)
        print("--- DATA LEAKAGE DETECTION ---")
        print("=" * 80)
        
        leakage_risks = {
            'customer_lifetime_value': {
                'risk': 'HIGH',
                'description': 'CLV includes future purchase information not available at prediction time',
                'impact': 'Model will appear accurate but fail in production',
                'mitigation': 'Remove CLV from features; use only early transaction data'
            },
            'number_of_purchases': {
                'risk': 'MEDIUM',
                'description': 'If includes future purchases, leaks information about customer value',
                'impact': 'Overstated model performance on minority class',
                'mitigation': 'Use only purchases from first 3 months for prediction'
            },
            'purchase_amount': {
                'risk': 'MEDIUM',
                'description': 'Total purchase amount might include future transactions',
                'impact': 'Features may be too predictive, inflating accuracy metrics',
                'mitigation': 'Segment data by time period; use only baseline period'
            }
        }
        
        for feature, risk_info in leakage_risks.items():
            if feature in self.df.columns:
                print(f"\n{feature}:")
                print(f"  Risk Level: {risk_info['risk']}")
                print(f"  Description: {risk_info['description']}")
                print(f"  Impact: {risk_info['impact']}")
                print(f"  Mitigation: {risk_info['mitigation']}")
                self.leakage_risks.append(feature)
        
        return leakage_risks
    
    def get_safe_features(self, all_features):
        """Get list of features safe from leakage.
        
        Args:
            all_features: List of all features in dataset
            
        Returns:
            list: List of features safe to use for modeling
        """
        risky_features = {
            'customer_lifetime_value',
            'number_of_purchases',
            'purchase_amount'
        }
        
        safe_features = [f for f in all_features if f not in risky_features]
        
        print("\n" + "=" * 80)
        print("--- RECOMMENDED FEATURES FOR MODELING ---")
        print("=" * 80)
        print(f"\nSafe Features ({len(safe_features)}):")
        for feat in safe_features:
            print(f"  ✓ {feat}")
        
        print(f"\nFeatures to EXCLUDE ({len(risky_features)}):")
        for feat in risky_features:
            if feat in all_features:
                print(f"  ✗ {feat} (Data leakage risk)")
        
        print("=" * 80 + "\n")
        
        return safe_features
    
    def print_leakage_summary(self):
        """Print comprehensive leakage detection summary."""
        print("\n" + "=" * 80)
        print("--- LEAKAGE PREVENTION STRATEGY ---")
        print("=" * 80)
        
        print("""
KEY FINDINGS:
1. Customer Lifetime Value (CLV) - HIGH RISK
   • This metric is calculated using FUTURE purchase data
   • It would not be available at prediction time in production
   • Using it inflates model accuracy unrealistically

2. Number of Purchases - MEDIUM RISK
   • If this includes future transactions, it's leakage
   • Should only count baseline period purchases

3. Purchase Amount - MEDIUM RISK
   • Total purchases might span future time periods
   • Need to segment by time window

RECOMMENDATIONS:
• Immediate: Remove CLV from modeling features
• Use only demographic data + early purchase behavior
• Implement strict time-based validation strategy
• Document feature availability at prediction time
• Regular leakage audits during model development

NEXT STEPS:
1. Create a feature engineering pipeline that removes CLV
2. Use stratified sampling to maintain class distribution
3. Test model with only safe features
4. Monitor for any suspicious patterns in predictions
        """)
        
        print("=" * 80 + "\n")
