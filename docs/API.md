# E-Commerce Customer EDA - API Documentation

## Overview

This document describes the public API for the EDA analysis modules. All classes and functions are designed to be easily integrated into other projects.

---

## Table of Contents

1. [Data Generation](#data-generation)
2. [Descriptive Statistics](#descriptive-statistics)
3. [Data Splitting](#data-splitting)
4. [Correlation Analysis](#correlation-analysis)
5. [Outlier Detection](#outlier-detection)
6. [Target Analysis](#target-analysis)
7. [Leakage Detection](#leakage-detection)

---

## Data Generation

### Module: `src/data_generation.py`

#### Function: `generate_sample_data()`

Generate synthetic e-commerce customer data.

```python
def generate_sample_data(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame
```

**Parameters:**
- `n_samples` (int): Number of samples to generate. Default: 1000
- `seed` (int): Random seed for reproducibility. Default: 42

**Returns:**
- `pd.DataFrame`: Generated dataset with columns: age, income, purchase_amount, num_purchases, customer_lifetime_value, purchase_category

**Example:**
```python
from src.data_generation import generate_sample_data

df = generate_sample_data(n_samples=500, seed=42)
print(f"Generated {len(df)} samples")
print(df.head())
```

**Features:**
- Realistic distributions based on e-commerce domain
- No missing values
- Reproducible with seed parameter
- Includes categorical target variable

---

## Descriptive Statistics

### Module: `src/descriptive_stats.py`

#### Class: `DescriptiveStats`

Compute and visualize descriptive statistics for dataset.

```python
class DescriptiveStats:
    def __init__(self, df: pd.DataFrame)
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe

**Methods:**

##### `get_summary_statistics() -> pd.DataFrame`

Get summary statistics (mean, median, std, min, max, etc.)

```python
from src.descriptive_stats import DescriptiveStats

stats = DescriptiveStats(df)
summary = stats.get_summary_statistics()
print(summary)
```

Returns DataFrame with statistical measures for each numeric column.

##### `plot_distributions(save_path: str = None) -> None`

Generate histograms for all numeric features.

```python
stats.plot_distributions(save_path='outputs/distributions.png')
```

**Parameters:**
- `save_path` (str): Path to save figure. Optional.

**Properties:**

##### `numeric_columns: List[str]`

Get list of numeric column names.

```python
numeric_cols = stats.numeric_columns
```

---

## Data Splitting

### Module: `src/data_splitting.py`

#### Class: `DataSplitter`

Stratified train-validation-test splitting.

```python
class DataSplitter:
    def __init__(
        self,
        df: pd.DataFrame,
        test_size: float = 0.30,
        random_state: int = 42
    )
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe
- `test_size` (float): Proportion for validation+test. Default: 0.30
- `random_state` (int): Random seed. Default: 42

**Methods:**

##### `split_stratified() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]`

Perform stratified split into train (70%), validation (15%), test (15%).

```python
splitter = DataSplitter(df, test_size=0.30, random_state=42)
X_train, X_val, X_test = splitter.split_stratified()

print(f"Train: {len(X_train)} samples")
print(f"Val: {len(X_val)} samples")
print(f"Test: {len(X_test)} samples")
```

**Returns:**
- Tuple of three DataFrames: (X_train, X_val, X_test)

**Guarantees:**
- Stratification maintains class distribution across splits
- No data leakage between splits
- Reproducible with random_state

---

## Correlation Analysis

### Module: `src/correlation_analysis.py`

#### Class: `CorrelationAnalysis`

Compute and visualize feature correlations.

```python
class CorrelationAnalysis:
    def __init__(self, df: pd.DataFrame, method: str = 'pearson')
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe
- `method` (str): Correlation method ('pearson', 'spearman', 'kendall'). Default: 'pearson'

**Methods:**

##### `compute_correlation_matrix() -> pd.DataFrame`

Get correlation matrix for numeric features.

```python
corr_analysis = CorrelationAnalysis(df)
corr_matrix = corr_analysis.compute_correlation_matrix()

# Find high correlations
high_corr = corr_matrix[(corr_matrix > 0.8) & (corr_matrix < 1.0)]
print(high_corr)
```

**Returns:**
- `pd.DataFrame`: Correlation matrix (square, symmetric)

##### `plot_correlation_matrix(save_path: str = None) -> None`

Generate heatmap visualization of correlations.

```python
corr_analysis.plot_correlation_matrix(save_path='outputs/correlation_heatmap.png')
```

**Parameters:**
- `save_path` (str): Path to save figure. Optional.

##### `get_high_correlations(threshold: float = 0.8) -> List[Tuple]`

Get pairs of features with high correlation.

```python
high_pairs = corr_analysis.get_high_correlations(threshold=0.8)
for feat1, feat2, corr in high_pairs:
    print(f"{feat1} - {feat2}: {corr:.3f}")
```

---

## Outlier Detection

### Module: `src/outlier_detection.py`

#### Class: `OutlierDetector`

Detect and visualize outliers using IQR method.

```python
class OutlierDetector:
    def __init__(self, df: pd.DataFrame, iqr_multiplier: float = 1.5)
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe
- `iqr_multiplier` (float): IQR multiplier for bounds. Default: 1.5

**Methods:**

##### `detect_iqr_outliers(column: str) -> pd.DataFrame`

Detect outliers in a specific column.

```python
detector = OutlierDetector(df)
outliers = detector.detect_iqr_outliers('income')

print(f"Found {len(outliers)} outliers")
print(outliers)
```

**Parameters:**
- `column` (str): Column name to analyze

**Returns:**
- `pd.DataFrame`: Rows identified as outliers

##### `plot_boxplots(save_path: str = None) -> None`

Generate box plots for all numeric columns.

```python
detector.plot_boxplots(save_path='outputs/boxplots.png')
```

**Parameters:**
- `save_path` (str): Path to save figure. Optional.

##### `get_outlier_summary() -> Dict`

Get summary of outliers in all numeric columns.

```python
summary = detector.get_outlier_summary()
for col, count in summary.items():
    print(f"{col}: {count} outliers")
```

---

## Target Analysis

### Module: `src/target_analysis.py`

#### Class: `TargetAnalysis`

Analyze and categorize target variable.

```python
class TargetAnalysis:
    def __init__(self, df: pd.DataFrame)
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe

**Methods:**

##### `categorize_customer_value() -> pd.Series`

Categorize customers by value level.

```python
target = TargetAnalysis(df)
categories = target.categorize_customer_value()

print(categories.value_counts())
```

**Returns:**
- `pd.Series`: Customer value categories (High/Medium/Low)

**Categories:**
- High Value: CLV ≥ $3,500
- Medium Value: $1,750 ≤ CLV < $3,500
- Low Value: CLV < $1,750

##### `plot_distribution(save_path: str = None) -> None`

Generate distribution plot for target variable.

```python
target.plot_distribution(save_path='outputs/class_distribution.png')
```

##### `get_class_imbalance() -> float`

Get class imbalance ratio.

```python
imbalance = target.get_class_imbalance()
print(f"Imbalance ratio: {imbalance:.2f}")
```

---

## Leakage Detection

### Module: `src/leakage_detection.py`

#### Class: `LeakageDetector`

Assess data leakage risks in dataset.

```python
class LeakageDetector:
    def __init__(self, df: pd.DataFrame)
```

**Constructor Parameters:**
- `df` (pd.DataFrame): Input dataframe

**Methods:**

##### `assess_leakage() -> Dict[str, str]`

Assess leakage risk for all features.

```python
detector = LeakageDetector(df)
report = detector.assess_leakage()

for feature, risk_level in report.items():
    print(f"{feature}: {risk_level}")
```

**Returns:**
- `Dict[str, str]`: Feature names mapped to risk levels (HIGH/MEDIUM/LOW)

**Risk Levels:**
- 🔴 HIGH: Feature includes future/target data
- 🟡 MEDIUM: Temporal ambiguity or derived features
- 🟢 LOW: Safe demographic/baseline data

##### `get_safe_features() -> List[str]`

Get list of features safe to use in modeling.

```python
safe_features = detector.get_safe_features()
print("Safe features:", safe_features)
```

**Returns:**
- `List[str]`: Feature names with LOW risk level

##### `generate_report(save_path: str = None) -> None`

Generate detailed leakage report.

```python
detector.generate_report(save_path='outputs/leakage_report.txt')
```

---

## Complete Example

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'src'))

from data_generation import generate_sample_data
from descriptive_stats import DescriptiveStats
from data_splitting import DataSplitter
from correlation_analysis import CorrelationAnalysis
from outlier_detection import OutlierDetector
from target_analysis import TargetAnalysis
from leakage_detection import LeakageDetector

# Step 1: Generate data
df = generate_sample_data(n_samples=1000, seed=42)

# Step 2: Descriptive statistics
stats = DescriptiveStats(df)
summary = stats.get_summary_statistics()
stats.plot_distributions(save_path='outputs/01_distributions.png')

# Step 3: Data splitting
splitter = DataSplitter(df, test_size=0.30, random_state=42)
X_train, X_val, X_test = splitter.split_stratified()

# Step 4: Correlation analysis
corr_analysis = CorrelationAnalysis(df)
corr_matrix = corr_analysis.compute_correlation_matrix()
corr_analysis.plot_correlation_matrix(save_path='outputs/02_correlation.png')

# Step 5: Outlier detection
detector = OutlierDetector(df)
detector.plot_boxplots(save_path='outputs/04_boxplots.png')

# Step 6: Target analysis
target = TargetAnalysis(df)
categories = target.categorize_customer_value()
target.plot_distribution(save_path='outputs/05_class_distribution.png')

# Step 7: Leakage detection
leakage_detector = LeakageDetector(df)
safe_features = leakage_detector.get_safe_features()
leakage_detector.generate_report(save_path='outputs/leakage_report.txt')

print("✅ Complete EDA analysis finished!")
```

---

## Error Handling

All modules include error handling and validation:

```python
try:
    df = generate_sample_data(n_samples=-100)  # Invalid
except ValueError as e:
    print(f"Error: {e}")

try:
    stats = DescriptiveStats(None)  # Invalid
except TypeError as e:
    print(f"Error: {e}")
```

---

## Performance

| Operation | Time (1000 samples) |
|-----------|--------------------|
| Data generation | < 100ms |
| Descriptive stats | < 50ms |
| Correlation analysis | < 100ms |
| Outlier detection | < 75ms |
| Target analysis | < 25ms |
| Leakage detection | < 50ms |

---

## Version

Current version: **1.0.0**

---

## Support

- 📧 Email: waqarjaveria333@gmail.com
- 🐛 Report bugs: https://github.com/Javeria033/ai-day3-eda-javeria/issues
- 💬 Discussions: https://github.com/Javeria033/ai-day3-eda-javeria/discussions