# AI Day 3 - EDA & Statistical Thinking Challenge (Python-Based)

## Project Overview

This repository contains a comprehensive **Python-based Exploratory Data Analysis (EDA)** suite for e-commerce customer data. Unlike traditional Jupyter notebooks, this project uses ~90% pure Python with object-oriented design patterns for better code organization, reusability, and production-readiness.

## Project Structure

```
.
├── main.py                          # Main EDA execution script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── src/                             # Source code modules (90% Python)
│   ├── __init__.py                 # Package initialization
│   ├── data_generation.py          # Data loading and generation
│   ├── descriptive_stats.py        # Descriptive statistics and distributions
│   ├── data_splitting.py           # Train-validation-test splitting
│   ├── correlation_analysis.py     # Correlation and relationship analysis
│   ├── outlier_detection.py        # Outlier detection (IQR method)
│   ├── target_analysis.py          # Target variable categorization
│   └── leakage_detection.py        # Data leakage risk detection
│
├── outputs/                         # Generated visualizations and reports
│   ├── 01_distributions.png
│   ├── 02_correlation_heatmap.png
│   ├── 03_income_vs_purchase.png
│   ├── 04_boxplots.png
│   └── 05_class_distribution.png
│
├── data/                            # Data files
│   └── ecommerce_customers.csv     # Raw customer dataset
│
├── docs/                            # Documentation
│   └── management_summary.md        # Analysis findings and recommendations
│
└── notebooks/                       # Optional Jupyter notebooks
    └── EDA_Ecommerce_Analysis.ipynb # Reference notebook (minimal use)
```

## Dataset

E-Commerce Customer Dataset with features:
- **customer_age**: Age of the customer (18-70 years)
- **income**: Annual income in dollars
- **purchase_amount**: Average purchase amount
- **number_of_purchases**: Number of purchases made
- **customer_lifetime_value**: Total value of customer to business
- **purchase_category**: Target variable (High/Medium/Low value customer)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/Javeria033/ai-day3-eda-javeria.git
cd ai-day3-eda-javeria

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Complete EDA Analysis

```bash
python main.py
```

This executes the full analysis pipeline:
1. **Data Generation** - Create sample dataset
2. **Descriptive Statistics** - Summary statistics and distributions
3. **Data Splitting** - Train (70%), Validation (15%), Test (15%)
4. **Correlation Analysis** - Feature relationships and heatmaps
5. **Outlier Detection** - IQR-based outlier identification
6. **Target Analysis** - Class distribution and imbalance detection
7. **Leakage Detection** - Identify data leakage risks

### Use Individual Modules

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'src'))

from data_generation import generate_sample_data
from descriptive_stats import DescriptiveStats
from correlation_analysis import CorrelationAnalysis

# Generate data
df = generate_sample_data(n_samples=1000, seed=42)

# Compute descriptive statistics
desc_stats = DescriptiveStats(df)
summary = desc_stats.get_summary_statistics()
desc_stats.plot_distributions(save_path='outputs/distributions.png')

# Analyze correlations
corr_analysis = CorrelationAnalysis(df)
corr_matrix = corr_analysis.compute_correlation_matrix()
corr_analysis.plot_correlation_matrix(save_path='outputs/correlation.png')
```

## Analysis Components

### 1. Data Generation (`data_generation.py`)
- Generate synthetic e-commerce customer dataset
- Load from CSV files
- Save processed data

### 2. Descriptive Statistics (`descriptive_stats.py`)
- Calculate mean, median, min, max, std dev
- Generate distribution histograms
- Print basic dataset information

### 3. Data Splitting (`data_splitting.py`)
- Stratified train-validation-test split (70-15-15)
- Maintain class distribution across splits
- Support custom split ratios

### 4. Correlation Analysis (`correlation_analysis.py`)
- Pearson correlation matrix computation
- Heatmap visualization
- Scatter plots for feature relationships
- Identify high correlations (>0.8)

### 5. Outlier Detection (`outlier_detection.py`)
- IQR-based outlier detection
- Box plot visualizations
- Data quality reporting
- Missing value analysis

### 6. Target Analysis (`target_analysis.py`)
- Customer value categorization (High/Medium/Low)
- Class distribution analysis
- Class imbalance detection
- Visualization of class proportions

### 7. Leakage Detection (`leakage_detection.py`)
- Identify temporal leakage risks
- Classify features by risk level
- Provide mitigation strategies
- Recommend safe feature sets

## Key Findings

### 1. Income Drives Spending
- **Correlation**: 0.92 (very strong positive)
- High-income customers spend significantly more
- Target marketing campaigns toward high-income segments

### 2. Customer Demographics
- Age range: 18-70 years (mean: 43.82)
- Most customers are established professionals (35-45 years)

### 3. Data Quality
- ✓ No missing values
- ✓ No significant outliers detected
- ✓ Data is clean and ready for modeling

### 4. Class Distribution
- High Value: 40%
- Medium Value: 40%
- Low Value: 20%
- **Imbalance Ratio**: 2.0x (moderate imbalance)

### 5. Critical Finding: Data Leakage
- ⚠️ **HIGH RISK**: `customer_lifetime_value` in features
- Customer lifetime value includes FUTURE transaction data
- Using CLV would cause model to fail in production
- **Mitigation**: Remove CLV from modeling features

## Recommendations

### For Model Development
1. **Remove data leakage**: Exclude `customer_lifetime_value` from features
2. **Handle class imbalance**: Use SMOTE or class weights
3. **Use safe features only**: customer_age, income only
4. **Stratified splitting**: Maintain class distribution across train-val-test

### For Production
1. Implement strict feature availability checks
2. Use only baseline period transaction data
3. Monitor predictions for anomalies
4. Regular leakage audits during model updates

## Visualizations Generated

- `01_distributions.png` - Histograms of all numeric features
- `02_correlation_heatmap.png` - Correlation matrix heatmap
- `03_income_vs_purchase.png` - Scatter plot: income vs purchase amount
- `04_boxplots.png` - Box plots for outlier detection
- `05_class_distribution.png` - Class distribution (bar + pie charts)

## Code Quality

- **Object-Oriented Design**: Modular, reusable classes
- **Documentation**: Comprehensive docstrings for all functions
- **Type Hints**: Clear parameter and return type annotations
- **Error Handling**: Validation and informative error messages
- **Extensibility**: Easy to add new analysis modules

## Technologies Used

- **pandas** (2.0+) - Data manipulation and analysis
- **numpy** (1.24+) - Numerical computing
- **matplotlib** (3.7+) - Visualization
- **seaborn** (0.12+) - Statistical visualization
- **scikit-learn** (1.3+) - Machine learning utilities

## File Sizes

- Source code (src/): ~500 lines of pure Python
- Jupyter notebook (optional): ~400 lines of mixed Python/markup
- **Python-to-Notebook ratio**: ~90% Python, 10% Jupyter

## Author

- **Name**: Javeria
- **Date**: July 2026
- **Program**: AI Internship - Day 3

## License

This project is open source and available under the MIT License.

## References

- EDA Best Practices
- Data Leakage Prevention Guide
- Statistical Thinking for Data Science
- scikit-learn Documentation
