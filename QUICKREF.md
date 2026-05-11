#!/usr/bin/env python3
"""
QUICK REFERENCE - PyAgent Usage Guide
Execute this file to see all usage examples and command reference
"""

import sys

QUICK_REFERENCE = """
╔════════════════════════════════════════════════════════════════════════════╗
║                          PYAGENT - QUICK REFERENCE                        ║
║                  AI-Powered Data Analysis Agent System                     ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 INSTALLATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  $ pip install -r requirements.txt
  $ python -m pytest tests/test_all.py -v    # Verify installation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 INTERACTIVE MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  $ python -m src.main

  Then use these commands:
  
    analyze <file>    Full analysis (read → validate → analyze → report)
    validate <file>   Quick validation only
    stats <file>      Statistics extraction only
    help              Show command help
    quit              Exit application

  Examples:
    >>> analyze data/sales_data.csv
    >>> validate data/customer_data.csv
    >>> stats data/inventory.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PROGRAMMATIC USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  from src.agent import DataAnalysisAgent
  
  # Create agent
  agent = DataAnalysisAgent()
  
  # Full analysis
  result = agent.analyze_file('data/sales_data.csv')
  if result['success']:
      print(result['formatted_report'])
  
  # Quick validation
  result = agent.quick_validate('data/customer_data.csv')
  
  # Get statistics
  result = agent.get_statistics('data/inventory.json')
  print(result['statistics'])
  
  # Transform data
  result = agent.transform_data(
      data=data_list,
      operation='filter',
      column='region',
      value='North',
      operator='=='
  )

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AVAILABLE TOOLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. DataFileReader
     Purpose:  Read and parse CSV and JSON files
     Input:    File path (str)
     Output:   List of dictionaries
     
  2. DataValidator
     Purpose:  Check data quality and identify issues
     Input:    Data list
     Output:   Quality report with issues and severity
     
  3. StatisticalAnalyzer
     Purpose:  Compute statistics and metrics
     Input:    Data list
     Output:   Statistics for each column (numeric and categorical)
     
  4. DataTransformer
     Purpose:  Clean and transform data
     Input:    Data + operation + parameters
     Output:   Transformed data
     
  5. ReportGenerator
     Purpose:  Synthesize analysis into insights and reports
     Input:    Analysis results
     Output:   Formatted report with recommendations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 TRANSFORMATION OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  agent.transform_data(data, operation='remove_duplicates')
  
  agent.transform_data(data, operation='remove_nulls')
  
  agent.transform_data(data, 
      operation='filter',
      column='region',
      value='North',
      operator='==')  # operators: ==, >, <, contains
  
  agent.transform_data(data,
      operation='aggregate',
      group_by='product')  # optionally add metric='sum', metric_column='sales'
  
  agent.transform_data(data,
      operation='extract_columns',
      columns=['name', 'email', 'age'])

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SAMPLE DATA FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  data/sales_data.csv       - 20 clean sales transactions
  data/customer_data.csv    - 12 customer records
  data/inventory.json       - 8 inventory items (JSON format)
  data/messy_data.csv       - 10 records with quality issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Run all tests
  $ python -m pytest tests/test_all.py -v
  
  # Run specific test class
  $ python -m pytest tests/test_all.py::TestDataFileReader -v
  
  # Run with coverage
  $ python -m pytest tests/test_all.py --cov=src
  
  # Run demonstration
  $ python demo.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PROJECT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  src/
    ├── agent/              Agent orchestration
    ├── tools/              Tool implementations
    └── main.py             CLI interface
  
  tests/
    └── test_all.py         Comprehensive test suite (32 tests)
  
  data/
    ├── sales_data.csv      Sample CSV data
    ├── customer_data.csv   Customer data
    ├── inventory.json      JSON format data
    └── messy_data.csv      Data with quality issues
  
  README.md                 User documentation
  JOURNAL.md               Development journal
  DELIVERY_SUMMARY.md      Project completion summary
  requirements.txt         Python dependencies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Issue: ModuleNotFoundError
  → Run from project root: cd /workspaces/pyagent
  
  Issue: File not found
  → Ensure paths are relative to project root
  
  Issue: pytest not found
  → Install: pip install pytest
  
  Issue: Tests fail
  → Check sample data files exist in /data/
  → Run: python -m pytest tests/test_all.py -v
  
  Issue: Import errors
  → Verify Python is 3.8+: python --version
  → Check PYTHONPATH includes src/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DOCUMENTATION FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  README.md              → Complete user guide (start here!)
  JOURNAL.md            → Development progress (all stages 1-3)
  DELIVERY_SUMMARY.md   → Project completion details
  demo.py               → Runnable demonstration script
  QUICKREF.md           → This file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Install:  pip install -r requirements.txt
  2. Test:     python -m pytest tests/test_all.py -v
  3. Demo:     python demo.py
  4. Run:      python -m src.main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 KEY FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ Intelligent agent orchestration
  ✓ Multi-format data support (CSV, JSON)
  ✓ Comprehensive data validation
  ✓ Statistical analysis
  ✓ Data transformation and cleaning
  ✓ Automated report generation
  ✓ 32 passing test cases
  ✓ Zero external dependencies
  ✓ Production-ready error handling
  ✓ Full documentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For complete documentation, see README.md
For development details, see JOURNAL.md
For more information, see DELIVERY_SUMMARY.md

PyAgent v1.0.0 - Ready for Production
"""

if __name__ == '__main__':
    print(QUICK_REFERENCE)
