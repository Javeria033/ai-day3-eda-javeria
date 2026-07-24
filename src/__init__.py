"""E-Commerce EDA Analysis Package.

A comprehensive Python-based exploratory data analysis suite for e-commerce customer data.
"""

__version__ = '1.0.0'
__author__ = 'Javeria'

from .data_generation import generate_sample_data, load_data, save_data
from .descriptive_stats import DescriptiveStats
from .data_splitting import DataSplitter
from .correlation_analysis import CorrelationAnalysis
from .outlier_detection import OutlierDetection
from .target_analysis import TargetAnalysis
from .leakage_detection import LeakageDetection

__all__ = [
    'generate_sample_data',
    'load_data',
    'save_data',
    'DescriptiveStats',
    'DataSplitter',
    'CorrelationAnalysis',
    'OutlierDetection',
    'TargetAnalysis',
    'LeakageDetection'
]
