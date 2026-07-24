# Contributing Guidelines

## How to Contribute

Thank you for your interest in improving this EDA analysis project! Here are the guidelines for contributing.

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-day3-eda-javeria.git
   cd ai-day3-eda-javeria
   ```
3. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pytest  # Verify tests pass
   ```

### Code Standards

#### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints for all function parameters and returns

#### Documentation
- Add docstrings to all functions and classes
- Use Google-style docstring format
- Include examples in module docstrings
- Update README if adding new functionality

#### Example Function:
```python
def analyze_correlation(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """
    Compute correlation matrix for numeric features.
    
    Args:
        df (pd.DataFrame): Input dataframe with numeric columns
        method (str): Correlation method ('pearson', 'spearman', 'kendall')
    
    Returns:
        pd.DataFrame: Correlation matrix with features as rows and columns
    
    Example:
        >>> df = pd.read_csv('data.csv')
        >>> corr_matrix = analyze_correlation(df, method='pearson')
        >>> print(corr_matrix)
    """
    return df.corr(method=method)
```

### Testing

All contributions must include tests. Run tests before submitting:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_eda_analysis.py

# Run with coverage report
pytest --cov=src tests/
```

### Submitting Changes

1. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: descriptive commit message"
   ```

2. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to any related issues
   - Screenshots/examples if applicable

### Pull Request Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass (`pytest`)
- [ ] New functions have docstrings
- [ ] README updated if needed
- [ ] No hardcoded values (use config.py)
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

### Types of Contributions

#### 🐛 Bug Reports
- Use GitHub Issues with the "bug" label
- Include reproducible steps
- Attach error messages and stack traces
- Specify Python and package versions

#### ✨ Feature Requests
- Use GitHub Issues with the "enhancement" label
- Describe the use case and desired behavior
- Suggest implementation approach if possible
- Discuss before starting major work

#### 📚 Documentation
- Fix typos and unclear explanations
- Add examples and use cases
- Improve code comments
- Update API documentation

#### 🧪 Tests
- Add test coverage for new features
- Fix failing tests
- Improve test quality and clarity

### Development Workflow Example

```bash
# 1. Create feature branch
git checkout -b feature/add-data-quality-report

# 2. Make changes and test
python -m pytest tests/

# 3. Commit changes
git commit -m "Add data quality report module with comprehensive metrics"

# 4. Push to fork
git push origin feature/add-data-quality-report

# 5. Create Pull Request on GitHub
# (Include description, testing notes, any breaking changes)
```

### Code Review Process

- At least one maintainer review required
- Constructive feedback will be provided
- Please respond to review comments
- Updates push automatically to PR
- Squash commits before merging (if requested)

### Questions?

- 💬 Open an Issue for questions
- 📧 Email: waqarjaveria333@gmail.com
- 🔗 GitHub: [Javeria033](https://github.com/Javeria033)

Thank you for contributing! 🙏