# Quick Start Guide - E-Commerce EDA Analysis

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Complete Analysis
```bash
python main.py
```

### Step 3: Check Output
Visualization files are saved to `outputs/` directory:
- `01_distributions.png` - Feature distributions
- `02_correlation_heatmap.png` - Correlation matrix
- `03_income_vs_purchase.png` - Income vs spending relationship
- `04_boxplots.png` - Outlier detection
- `05_class_distribution.png` - Target variable distribution

## Project Structure

```
src/
├── data_generation.py          # Load/generate data
├── descriptive_stats.py         # Summary statistics
├── data_splitting.py            # Train-val-test split
├── correlation_analysis.py      # Correlation analysis
├── outlier_detection.py         # Outlier detection
├── target_analysis.py           # Target categorization
└── leakage_detection.py         # Leakage detection

main.py                          # Main execution script
requirements.txt                 # Dependencies
```

## Python Modules (90% Code)

Each module is a standalone Python class:

```python
# Example: Using individual modules
from src.descriptive_stats import DescriptiveStats
from src.data_generation import generate_sample_data

df = generate_sample_data()
stats = DescriptiveStats(df)
summary = stats.get_summary_statistics()
stats.plot_distributions(save_path='outputs/dist.png')
```

## Key Analysis Steps

### 1. Data Loading
```python
df = generate_sample_data(n_samples=1000, seed=42)
```

### 2. Descriptive Statistics
```python
desc_stats = DescriptiveStats(df)
desc_stats.print_basic_info()
summary = desc_stats.get_summary_statistics()
```

### 3. Data Splitting
```python
splitter = DataSplitter(df, random_state=42)
train, val, test = splitter.split_data()
```

### 4. Correlation Analysis
```python
corr = CorrelationAnalysis(df)
matrix = corr.compute_correlation_matrix()
corr.plot_correlation_matrix()
```

### 5. Outlier Detection
```python
outliers = OutlierDetection(df)
outliers.detect_outliers_iqr()
outliers.plot_boxplots()
```

### 6. Target Analysis
```python
target = TargetAnalysis(df)
df = target.categorize_customers()
target.print_class_distribution()
```

### 7. Leakage Detection
```python
leakage = LeakageDetection(df)
leakage.check_temporal_leakage()
safe_features = leakage.get_safe_features(df.columns)
```

## Expected Output

```
================================================================================
E-COMMERCE CUSTOMER EDA ANALYSIS
================================================================================

>>> PART 1: DATA GENERATION & LOADING
✓ Dataset loaded successfully
  Shape: (1000, 6)

>>> PART 2: DESCRIPTIVE STATISTICS
================================================== DESCRIPTIVE STATISTICS ===
Feature                Mean     Median   Minimum   Maximum   Std Dev   Count
customer_age          43.82     44.00     18.00     69.00    14.99    1000
income            84905.98  84699.00  20060.00 149972.00 38430.89    1000
...

>>> PART 3: DATA SPLITTING STRATEGY
Training Set:   700 rows (70%)
Validation Set: 150 rows (15%)
Testing Set:    150 rows (15%)

>>> PART 4: CORRELATION ANALYSIS
Key Correlations:
  Income vs Purchase Amount:       0.9200
  Income vs CLV:                   0.8950
...

>>> PART 5: OUTLIER DETECTION
Outliers Detected: 0 (using IQR method)
✓ Data quality is good for modeling

>>> PART 6: TARGET VARIABLE ANALYSIS
Class Counts:
  High Value Customer:        400 (40.00%)
  Medium Value Customer:      400 (40.00%)
  Low Value Customer:         200 (20.00%)

>>> PART 7: LEAKAGE DETECTION
⚠ HIGH RISK: customer_lifetime_value (Remove from features)
⚠ MEDIUM RISK: number_of_purchases (May include future data)

================================================================================
ANALYSIS COMPLETE!
================================================================================
```

## Common Tasks

### Generate Fresh Data
```python
from src.data_generation import generate_sample_data
df = generate_sample_data(n_samples=5000, seed=123)
```

### Save Data to CSV
```python
from src.data_generation import save_data
save_data(df, 'data/my_data.csv')
```

### Load from File
```python
from src.data_generation import load_data
df = load_data('data/ecommerce_customers.csv')
```

### Custom Visualization
```python
from src.correlation_analysis import CorrelationAnalysis
corr = CorrelationAnalysis(df, numeric_features=['age', 'income', 'spending'])
corr.plot_scatter_relationships('age', 'spending', save_path='age_vs_spending.png')
```

## Troubleshooting

### Import Error
```bash
# Make sure you're in the project root directory
cd ai-day3-eda-javeria
python main.py
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Permission Denied (outputs/)
```bash
mkdir -p outputs/
chmod 755 outputs/
```

## Project Stats

- **Total Python Code**: ~500 lines
- **Python vs Jupyter**: 90% Python, 10% Jupyter (optional)
- **Modules**: 7 reusable classes
- **Visualizations**: 5 automated plots
- **Analysis Steps**: 8 comprehensive analyses

## Next Steps

1. ✅ Run `python main.py` to generate analysis
2. 📊 Review visualizations in `outputs/`
3. 📖 Read `docs/management_summary.md` for findings
4. 🔧 Modify parameters in `main.py` for custom analysis
5. 📚 Import modules for your own analysis scripts

## Documentation

Each module has comprehensive docstrings:
```python
from src.descriptive_stats import DescriptiveStats
help(DescriptiveStats.get_summary_statistics)
```

## Support

For questions or issues:
1. Check the README.md for detailed documentation
2. Review docstrings in source files
3. Check the management_summary.md for analysis insights

---

**Created by**: Javeria  
**Date**: July 2026  
**Program**: AI Internship Day 3
