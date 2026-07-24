"""
Unit Tests for EDA Analysis Modules

Tests core functionality of:
- Data generation and loading
- Descriptive statistics computation
- Data splitting and stratification
- Correlation analysis
- Outlier detection
- Target variable analysis
- Leakage detection
"""

import sys
from pathlib import Path
import unittest
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_generation import generate_sample_data
from descriptive_stats import DescriptiveStats
from data_splitting import DataSplitter
from correlation_analysis import CorrelationAnalysis
from outlier_detection import OutlierDetector
from target_analysis import TargetAnalysis
from leakage_detection import LeakageDetector


class TestDataGeneration(unittest.TestCase):
    """Test data generation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.n_samples = 100
        self.random_state = 42
    
    def test_generate_data_shape(self):
        """Test that generated data has correct shape"""
        df = generate_sample_data(self.n_samples, self.random_state)
        self.assertEqual(len(df), self.n_samples)
        self.assertGreater(len(df.columns), 0)
    
    def test_generate_data_no_missing(self):
        """Test that generated data has no missing values"""
        df = generate_sample_data(self.n_samples, self.random_state)
        self.assertEqual(df.isnull().sum().sum(), 0)
    
    def test_generate_data_reproducible(self):
        """Test that same seed produces same data"""
        df1 = generate_sample_data(50, 42)
        df2 = generate_sample_data(50, 42)
        pd.testing.assert_frame_equal(df1, df2)


class TestDescriptiveStats(unittest.TestCase):
    """Test descriptive statistics computation"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(100, 42)
        self.stats = DescriptiveStats(self.df)
    
    def test_summary_statistics_shape(self):
        """Test that summary statistics have correct shape"""
        summary = self.stats.get_summary_statistics()
        self.assertGreater(len(summary), 0)
        self.assertIn('mean', summary.columns.str.lower().values)
    
    def test_numeric_columns_identified(self):
        """Test that numeric columns are correctly identified"""
        numeric_cols = self.stats.numeric_columns
        self.assertGreater(len(numeric_cols), 0)
        for col in numeric_cols:
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df[col]))


class TestDataSplitting(unittest.TestCase):
    """Test data splitting and stratification"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(200, 42)
        self.splitter = DataSplitter(self.df, test_size=0.30, random_state=42)
    
    def test_split_sizes(self):
        """Test that splits have correct sizes"""
        X_train, X_val, X_test = self.splitter.split_stratified()
        total = len(X_train) + len(X_val) + len(X_test)
        self.assertEqual(total, len(self.df))
    
    def test_split_ratios(self):
        """Test that split ratios are approximately correct"""
        X_train, X_val, X_test = self.splitter.split_stratified()
        train_ratio = len(X_train) / len(self.df)
        self.assertAlmostEqual(train_ratio, 0.70, delta=0.05)


class TestCorrelationAnalysis(unittest.TestCase):
    """Test correlation analysis functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(100, 42)
        self.corr_analysis = CorrelationAnalysis(self.df)
    
    def test_correlation_matrix_shape(self):
        """Test correlation matrix has correct shape"""
        corr_matrix = self.corr_analysis.compute_correlation_matrix()
        self.assertEqual(corr_matrix.shape[0], corr_matrix.shape[1])
    
    def test_correlation_values_in_range(self):
        """Test that correlation values are between -1 and 1"""
        corr_matrix = self.corr_analysis.compute_correlation_matrix()
        self.assertTrue((corr_matrix >= -1).all().all())
        self.assertTrue((corr_matrix <= 1).all().all())
    
    def test_diagonal_equals_one(self):
        """Test that diagonal of correlation matrix equals 1"""
        corr_matrix = self.corr_analysis.compute_correlation_matrix()
        np.testing.assert_array_almost_equal(np.diag(corr_matrix), np.ones(len(corr_matrix)))


class TestOutlierDetection(unittest.TestCase):
    """Test outlier detection functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(100, 42)
        self.detector = OutlierDetector(self.df)
    
    def test_outlier_detection_returns_dataframe(self):
        """Test that outlier detection returns a DataFrame"""
        numeric_col = self.df.select_dtypes(include=[np.number]).columns[0]
        outliers = self.detector.detect_iqr_outliers(numeric_col)
        self.assertIsInstance(outliers, pd.DataFrame)
    
    def test_outlier_count_reasonable(self):
        """Test that outlier count is reasonable (< 50%)"""
        numeric_col = self.df.select_dtypes(include=[np.number]).columns[0]
        outliers = self.detector.detect_iqr_outliers(numeric_col)
        outlier_ratio = len(outliers) / len(self.df)
        self.assertLess(outlier_ratio, 0.5)


class TestTargetAnalysis(unittest.TestCase):
    """Test target variable analysis"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(100, 42)
        self.target_analysis = TargetAnalysis(self.df)
    
    def test_categorization_creates_categories(self):
        """Test that categorization creates valid categories"""
        categorized = self.target_analysis.categorize_customer_value()
        self.assertGreater(len(categorized.unique()), 0)
    
    def test_no_missing_categories(self):
        """Test that categorization produces no missing values"""
        categorized = self.target_analysis.categorize_customer_value()
        self.assertEqual(categorized.isnull().sum(), 0)


class TestLeakageDetection(unittest.TestCase):
    """Test data leakage detection"""
    
    def setUp(self):
        """Set up test data"""
        self.df = generate_sample_data(100, 42)
        self.detector = LeakageDetector(self.df)
    
    def test_leakage_assessment_returns_dict(self):
        """Test that leakage assessment returns a dictionary"""
        report = self.detector.assess_leakage()
        self.assertIsInstance(report, dict)
    
    def test_leakage_report_has_findings(self):
        """Test that leakage report contains findings"""
        report = self.detector.assess_leakage()
        self.assertGreater(len(report), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete pipeline"""
    
    def test_complete_pipeline(self):
        """Test complete EDA pipeline execution"""
        # Generate data
        df = generate_sample_data(100, 42)
        
        # Run all analyses
        stats = DescriptiveStats(df)
        summary = stats.get_summary_statistics()
        
        splitter = DataSplitter(df, test_size=0.30, random_state=42)
        splits = splitter.split_stratified()
        
        corr_analysis = CorrelationAnalysis(df)
        corr_matrix = corr_analysis.compute_correlation_matrix()
        
        detector = OutlierDetector(df)
        numeric_col = df.select_dtypes(include=[np.number]).columns[0]
        outliers = detector.detect_iqr_outliers(numeric_col)
        
        target_analysis = TargetAnalysis(df)
        categorized = target_analysis.categorize_customer_value()
        
        leakage_detector = LeakageDetector(df)
        leakage_report = leakage_detector.assess_leakage()
        
        # Verify all outputs exist
        self.assertIsNotNone(summary)
        self.assertEqual(len(splits), 3)
        self.assertIsNotNone(corr_matrix)
        self.assertIsInstance(outliers, pd.DataFrame)
        self.assertGreater(len(categorized), 0)
        self.assertGreater(len(leakage_report), 0)


if __name__ == '__main__':
    unittest.main()