# PyAgent - Data Analysis Agent System

A Python-based AI agent system that intelligently analyzes data files, validates data quality, computes statistics, and generates comprehensive reports.

## Overview

**PyAgent** is an intelligent data analysis assistant built with a modular tool-based architecture. The system uses a specialized agent that orchestrates multiple tools to process data, identify quality issues, compute metrics, and provide actionable insights.

### Key Characteristics

- **AI-Based Agent**: Intelligent orchestration of tools for data analysis
- **Modular Tool Architecture**: Pluggable tools for different data operations
- **Multi-Format Support**: Works with CSV and JSON data files
- **Data Quality Focus**: Comprehensive data validation and quality checks
- **Report Generation**: Automated insight and recommendation generation
- **Error Handling**: Robust error handling and user feedback

## Project Structure

```
pyagent/
├── src/
│   ├── agent/              # Agent implementation
│   │   ├── data_analysis_agent.py
│   │   └── __init__.py
│   ├── tools/              # Tool implementations
│   │   ├── base_tool.py
│   │   ├── file_reader.py
│   │   ├── validator.py
│   │   ├── analyzer.py
│   │   ├── transformer.py
│   │   ├── report_generator.py
│   │   └── __init__.py
│   ├── main.py            # Application entry point
│   └── __init__.py
├── tests/
│   └── test_all.py        # Comprehensive test suite
├── data/                  # Sample data files
│   ├── sales_data.csv
│   ├── customer_data.csv
│   ├── inventory.json
│   └── messy_data.csv
├── docs/                  # Documentation
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── JOURNAL.md            # Development journal
```

## System Architecture

### Agent Component

The **DataAnalysisAgent** is the core intelligent component that:
1. Receives user requests
2. Decides which tools to use in sequence
3. Orchestrates tool execution
4. Aggregates results into comprehensive reports
5. Maintains execution logs

### Available Tools

1. **DataFileReader**
   - Reads CSV and JSON files
   - Extracts data into standardized format
   - Returns metadata about the loaded data

2. **DataValidator**
   - Checks for missing values
   - Detects duplicate records
   - Validates data type consistency
   - Generates quality assessment

3. **StatisticalAnalyzer**
   - Computes descriptive statistics (mean, median, std dev, etc.)
   - Analyzes categorical distributions
   - Identifies data patterns
   - Provides numerical summaries

4. **DataTransformer**
   - Removes duplicates
   - Handles missing values
   - Filters data by conditions
   - Aggregates data by groups
   - Extracts specific columns

5. **ReportGenerator**
   - Creates comprehensive analysis reports
   - Validates data and generates insights
   - Makes actionable recommendations
   - Exports reports in multiple formats

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   cd /workspaces/pyagent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -m pytest tests/ -v
   ```

## Usage

### Interactive Mode

Run the application in interactive mode:

```bash
python -m src.main
```

This starts an interactive command-line interface where you can run commands:

```
Commands:
  1. analyze <file_path>    - Perform full analysis on a file
  2. validate <file_path>   - Quick validation of a file
  3. stats <file_path>      - Get statistics for a file
  4. help                   - Show help message
  5. quit                   - Exit
```

#### Example Commands

**Analyze a CSV file:**
```
analyze data/sales_data.csv
```

**Validate data quality:**
```
validate data/customer_data.csv
```

**Get statistics:**
```
stats data/inventory.json
```

### Programmatic Usage

Use PyAgent as a library in your Python code:

```python
from src.agent import DataAnalysisAgent

# Create agent
agent = DataAnalysisAgent()

# Analyze a file
result = agent.analyze_file('data/sales_data.csv')

if result['success']:
    print(result['formatted_report'])
else:
    print(f"Error: {result['error']}")
```

#### Agent Methods

- `analyze_file(file_path)` - Full analysis workflow
- `quick_validate(file_path)` - Validate file without full analysis
- `get_statistics(file_path)` - Extract statistics only
- `transform_data(data, operation, **kwargs)` - Transform data

## Tool Usage Examples

### Using DataFileReader
```python
from src.tools import DataFileReader

reader = DataFileReader()
result = reader.execute(file_path='data/sales.csv')

if result['success']:
    data = result['data']['rows']
    print(f"Loaded {result['data']['row_count']} rows")
```

### Using DataValidator
```python
from src.tools import DataValidator

validator = DataValidator()
result = validator.execute(data=data)

print(f"Valid: {result['data']['valid']}")
print(f"Issues: {len(result['data']['issues'])}")
```

### Using DataTransformer
```python
from src.tools import DataTransformer

transformer = DataTransformer()

# Remove duplicates
result = transformer.execute(
    data=data,
    operation='remove_duplicates'
)

# Filter data
result = transformer.execute(
    data=data,
    operation='filter',
    column='region',
    value='North',
    operator='=='
)

# Aggregate data
result = transformer.execute(
    data=data,
    operation='aggregate',
    group_by='product'
)
```

## Data Formats

### Input Formats

**CSV Files:**
- Standard comma-separated format
- First row treated as header
- Automatic type detection

**JSON Files:**
- Array of objects format
- Single object format (converted to array)
- Unicode support

### Output Formats

**Analysis Report:**
- Structured JSON format
- Formatted text output
- Exportable to JSON files

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/test_all.py -v

# Run specific test class
pytest tests/test_all.py::TestDataFileReader -v

# Run with coverage report
pytest tests/test_all.py --cov=src --cov-report=html
```

### Test Coverage

The system includes 40+ test cases covering:
- All tool functionality
- Data validation scenarios
- Error handling
- Integration workflows
- Edge cases

## Data Quality Features

### Validation Checks
- Missing values detection
- Duplicate record identification
- Data type consistency validation
- Statistical outlier detection (basic)

### Data Transformation
- Null value handling
- Duplicate removal
- Conditional filtering
- Data aggregation
- Column extraction

### Quality Metrics
- Data completeness
- Unique value ratio
- Duplicate percentage
- Type consistency scores

## Configuration

The system uses sensible defaults. Configuration can be done programmatically:

```python
# Customize agent behavior
agent = DataAnalysisAgent()

# Access individual tools
reader = agent.file_reader
validator = agent.validator
analyzer = agent.analyzer
```

## Deployment

### Development Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest tests/`
3. Start application: `python -m src.main`

### Production Deployment Strategy

The system can be deployed as:

**1. Standalone CLI Application**
- Package with PyInstaller
- Distribute as executable
- Users run: `pyagent.exe analyze data.csv`

**2. Python Package**
- Publish to PyPI
- Install via: `pip install pyagent`  
- Import as library: `from pyagent import DataAnalysisAgent`

**3. Web Service**
- Wrap with Flask/FastAPI
- Deploy to cloud (AWS, GCP, Azure)
- Access via REST API

**4. Containerized Deployment**
- Docker container for consistent environment
- Easy deployment to Kubernetes
- Simplified dependency management

### Deployment Checklist

- [ ] All tests pass (pytest)
- [ ] Code follows PEP 8 style (pylint)
- [ ] Documentation complete
- [ ] Error handling comprehensive
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Logging configured
- [ ] Monitoring setup

## Programming Concepts Used

### Core Concepts

1. **Object-Oriented Programming**
   - Abstract base classes (`BaseTool`)
   - Inheritance and polymorphism
   - Encapsulation of tool functionality

2. **Design Patterns**
   - Strategy Pattern (tools framework)
   - Observer Pattern (execution logging)
   - Factory Pattern (agent orchestration)

3. **Data Structures**
   - Dictionaries for key-value data
   - Lists for collections
   - Tuples for hashable grouping

4. **Functional Programming**
   - List comprehensions
   - Filter and map operations
   - Lambda functions for sorting

5. **Error Handling**
   - Try-except blocks
   - Custom error messages
   - Graceful degradation

6. **File I/O**
   - CSV module for parsing
   - JSON module for data serialization
   - Path handling with pathlib

7. **Statistical Computing**
   - Mean, median, standard deviation
   - Frequency analysis
   - Data distribution analysis

### Advanced Concepts

- **Metaclasses and ABCs** for tool interface definition
- **Generator functions** for efficient data processing
- **Context managers** for resource handling
- **Decorators** for logging and validation
- **Type hints** for code clarity

## Data Transformation Process

The system uses a multi-stage data transformation approach:

```
Input File (CSV/JSON)
    ↓
[DataFileReader] → Standardized List of Dicts
    ↓
[DataValidator] → Quality Assessment + Issues List
    ↓
[StatisticalAnalyzer] → Statistical Metrics
    ↓
[DataTransformer] → Cleaned/Filtered Data (optional)
    ↓
[ReportGenerator] → Final Report + Insights
```

Each stage preserves data integrity and provides metadata about transformations.

## Troubleshooting

### Common Issues

**Issue: "File not found"**
- Solution: Ensure file path is correct and file exists
- Check path is relative to project root

**Issue: "Unsupported file format"**
- Solution: Only CSV and JSON are supported
- Convert your file to one of these formats

**Issue: "Type inconsistency errors"**
- Solution: Use DataValidator to identify issues
- Use DataTransformer to clean data

**Issue: Tests failing**
- Solution: Ensure all sample data files exist
- Run: `pytest tests/ -v --tb=short`

## Contributing

When extending the system:

1. Create new tools by inheriting from `BaseTool`
2. Implement the `execute()` method
3. Add tests in `test_all.py`
4. Update documentation
5. Run full test suite before committing

## Version History

- **1.0.0** (2024-05-11) - Initial release
  - 5 tools implemented
  - 40+ test cases
  - Complete documentation
  - Full data analysis workflow

## License

This project is provided as-is for educational and practical use.

## Contact & Support

For issues, feature requests, or questions:
- Review the documentation in `/docs/`
- Check the test examples in `/tests/`
- Review sample data in `/data/`

## Future Enhancements

- [ ] Add support for Excel files
- [ ] Implement machine learning classification
- [ ] Add visualization capabilities
- [ ] Create web-based interface
- [ ] Support for streaming data
- [ ] Real-time alerting system
- [ ] Database integration
- [ ] Advanced statistical models

---

**PyAgent** - Making Data Analysis Intelligent and Accessible