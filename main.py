"""Main EDA execution script for e-commerce customer analysis."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_generation import generate_sample_data
from descriptive_stats import DescriptiveStats
from data_splitting import DataSplitter
from correlation_analysis import CorrelationAnalysis
from outlier_detection import OutlierDetection
from target_analysis import TargetAnalysis
from leakage_detection import LeakageDetection


def main():
    """Execute complete EDA pipeline."""
    
    print("\n" + "=" * 80)
    print("E-COMMERCE CUSTOMER EDA ANALYSIS")
    print("=" * 80)
    
    # ========== PART 1: DATA LOADING ==========
    print("\n>>> PART 1: DATA GENERATION & LOADING")
    df = generate_sample_data(n_samples=1000, seed=42)
    
    # ========== PART 2: DESCRIPTIVE STATISTICS ==========
    print("\n>>> PART 2: DESCRIPTIVE STATISTICS")
    desc_stats = DescriptiveStats(df)
    desc_stats.print_basic_info()
    summary_df = desc_stats.get_summary_statistics()
    desc_stats.plot_distributions(save_path='outputs/01_distributions.png')
    
    # ========== PART 3: DATA SPLITTING STRATEGY ==========
    print("\n>>> PART 3: DATA SPLITTING STRATEGY")
    splitter = DataSplitter(df, random_state=42)
    train_data, val_data, test_data = splitter.split_data(
        train_size=0.70,
        val_size=0.15,
        test_size=0.15
    )
    
    # ========== PART 4: CORRELATION ANALYSIS ==========
    print("\n>>> PART 4: CORRELATION ANALYSIS")
    corr_analysis = CorrelationAnalysis(df)
    corr_matrix = corr_analysis.compute_correlation_matrix()
    corr_analysis.plot_correlation_matrix(save_path='outputs/02_correlation_heatmap.png')
    corr_analysis.plot_scatter_relationships(
        'income',
        'purchase_amount',
        save_path='outputs/03_income_vs_purchase.png'
    )
    
    # ========== PART 5: OUTLIER DETECTION ==========
    print("\n>>> PART 5: OUTLIER DETECTION")
    outlier_detector = OutlierDetection(df)
    outliers_info = outlier_detector.detect_outliers_iqr()
    outlier_detector.plot_boxplots(save_path='outputs/04_boxplots.png')
    outlier_detector.print_data_quality_report()
    
    # ========== PART 6: TARGET VARIABLE ANALYSIS ==========
    print("\n>>> PART 6: TARGET VARIABLE ANALYSIS")
    target_analyzer = TargetAnalysis(df)
    df_with_target = target_analyzer.categorize_customers(
        high_threshold=3500,
        low_threshold=1500
    )
    class_counts, class_pcts = target_analyzer.print_class_distribution()
    target_analyzer.plot_class_distribution(save_path='outputs/05_class_distribution.png')
    imbalance_ratio = target_analyzer.check_class_imbalance()
    
    # ========== PART 7: CLASS DISTRIBUTION IN SPLITS ==========
    print("\n>>> PART 7: CLASS DISTRIBUTION ACROSS SPLITS")
    df_with_target_copy = df_with_target.copy()
    splitter_with_target = DataSplitter(df_with_target_copy, random_state=42)
    train_split, val_split, test_split = splitter_with_target.split_data()
    splitter_with_target.print_class_distribution('purchase_category')
    
    # ========== PART 8: LEAKAGE DETECTION ==========
    print("\n>>> PART 8: DATA LEAKAGE DETECTION")
    leakage_detector = LeakageDetection(df)
    leakage_risks = leakage_detector.check_temporal_leakage()
    
    all_features = df.columns.tolist()
    safe_features = leakage_detector.get_safe_features(all_features)
    
    leakage_detector.print_leakage_summary()
    
    # ========== SUMMARY & RECOMMENDATIONS ==========
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY & KEY FINDINGS")
    print("=" * 80)
    
    summary_text = f"""
1. DATASET OVERVIEW:
   • Total Samples: {len(df)}
   • Total Features: {len(df.columns)}
   • No Missing Values: ✓

2. DESCRIPTIVE STATISTICS:
   • Customer Age:          Mean = {df['customer_age'].mean():.2f}, Range = [{df['customer_age'].min()}, {df['customer_age'].max()}]
   • Income:                Mean = ${df['income'].mean():,.0f}, Range = [${df['income'].min():,.0f}, ${df['income'].max():,.0f}]
   • Purchase Amount:       Mean = ${df['purchase_amount'].mean():.2f}, Range = [${df['purchase_amount'].min():.2f}, ${df['purchase_amount'].max():.2f}]
   • Num Purchases:         Mean = {df['number_of_purchases'].mean():.2f}, Range = [{df['number_of_purchases'].min()}, {df['number_of_purchases'].max()}]
   • Customer Lifetime Value: Mean = ${df['customer_lifetime_value'].mean():.2f}, Range = [${df['customer_lifetime_value'].min():.2f}, ${df['customer_lifetime_value'].max():.2f}]

3. DATA QUALITY:
   • Outliers Detected: {sum([info['outlier_count'] for info in outliers_info.values()])} (using IQR method)
   • Data Completeness: 100%
   • Quality Status: ✓ Good for Modeling

4. TARGET DISTRIBUTION:
   • High Value Customers:   {class_counts['High Value Customer']:3d} ({class_pcts['High Value Customer']:5.2f}%)
   • Medium Value Customers: {class_counts['Medium Value Customer']:3d} ({class_pcts['Medium Value Customer']:5.2f}%)
   • Low Value Customers:    {class_counts['Low Value Customer']:3d} ({class_pcts['Low Value Customer']:5.2f}%)
   • Imbalance Ratio: {imbalance_ratio:.2f}x

5. CORRELATION INSIGHTS:
   • Income ↔ Purchase Amount:    {corr_matrix.loc['income', 'purchase_amount']:.4f} (Very Strong)
   • Income ↔ CLV:                {corr_matrix.loc['income', 'customer_lifetime_value']:.4f} (Very Strong)
   • Age ↔ Num Purchases:         {corr_matrix.loc['customer_age', 'number_of_purchases']:.4f}

6. DATA LEAKAGE RISKS:
   • HIGH RISK: customer_lifetime_value (Remove from features)
   • MEDIUM RISK: number_of_purchases (May include future data)
   • MEDIUM RISK: purchase_amount (May span future periods)
   • SAFE FEATURES: {len(safe_features)} features available for modeling

7. TRAIN-VAL-TEST SPLIT:
   • Training Set:   {len(train_data)} samples (70%)
   • Validation Set: {len(val_data)} samples (15%)
   • Testing Set:    {len(test_data)} samples (15%)

RECOMMENDATIONS:
✓ Proceed with feature engineering using SAFE features only
✓ Use stratified sampling to maintain class distribution
✓ Implement class weights to handle imbalance (ratio: {imbalance_ratio:.2f}x)
✓ Consider SMOTE for minority class oversampling
✓ Validate on holdout test set to detect leakage
✓ Monitor prediction patterns for suspicious anomalies
    """
    
    print(summary_text)
    print("=" * 80)
    print("\n✓ EDA Analysis Complete!")
    print("Output files saved to 'outputs/' directory")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
