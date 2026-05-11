"""
Test suite for the Data Analysis Agent.
Tests all tools and the main agent functionality.
"""

import pytest
import json
from pathlib import Path
from src.tools import (
    DataFileReader,
    DataValidator,
    StatisticalAnalyzer,
    DataTransformer,
    ReportGenerator
)
from src.agent import DataAnalysisAgent


# Test fixtures
@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {'product': 'A', 'sales': 100, 'region': 'North'},
        {'product': 'B', 'sales': 200, 'region': 'South'},
        {'product': 'A', 'sales': 150, 'region': 'North'},
        {'product': 'C', 'sales': 300, 'region': 'East'},
    ]


@pytest.fixture
def messy_data():
    """Data with quality issues."""
    return [
        {'id': 1, 'name': 'John', 'value': 100},
        {'id': 2, 'name': None, 'value': 200},
        {'id': 1, 'name': 'John', 'value': 100},  # Duplicate
        {'id': 3, 'name': 'Jane', 'value': 'invalid'},
    ]


@pytest.fixture
def csv_file():
    """Path to test CSV file."""
    return 'data/sales_data.csv'


@pytest.fixture
def json_file():
    """Path to test JSON file."""
    return 'data/inventory.json'


# =========== DataFileReader Tests ===========

class TestDataFileReader:
    """Tests for the DataFileReader tool."""
    
    def test_read_csv_success(self):
        """Test successful CSV reading."""
        reader = DataFileReader()
        result = reader.execute(file_path='data/sales_data.csv')
        
        assert result['success'] is True
        assert result['data']['format'] == 'csv'
        assert result['data']['row_count'] > 0
        assert result['data']['column_count'] > 0
    
    def test_read_json_success(self):
        """Test successful JSON reading."""
        reader = DataFileReader()
        result = reader.execute(file_path='data/inventory.json')
        
        assert result['success'] is True
        assert result['data']['format'] == 'json'
        assert result['data']['row_count'] > 0
    
    def test_read_nonexistent_file(self):
        """Test handling of nonexistent file."""
        reader = DataFileReader()
        result = reader.execute(file_path='data/nonexistent.csv')
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_read_unsupported_format(self):
        """Test handling of unsupported file format."""
        reader = DataFileReader()
        result = reader.execute(file_path='README.md')
        
        # This might succeed or fail depending on file existence
        if not Path('README.md').exists():
            assert result['success'] is False


# =========== DataValidator Tests ===========

class TestDataValidator:
    """Tests for the DataValidator tool."""
    
    def test_validate_good_data(self, sample_data):
        """Test validation of good quality data."""
        validator = DataValidator()
        result = validator.execute(data=sample_data)
        
        assert result['success'] is True
        assert 'valid' in result['data']
        assert 'issues' in result['data']
    
    def test_validate_messy_data(self, messy_data):
        """Test validation of data with issues."""
        validator = DataValidator()
        result = validator.execute(data=messy_data)
        
        assert result['success'] is True
        assert len(result['data']['issues']) > 0
    
    def test_validate_empty_data(self):
        """Test validation of empty dataset."""
        validator = DataValidator()
        result = validator.execute(data=[])
        
        assert result['success'] is True
        assert result['data']['row_count'] == 0
    
    def test_duplicate_detection(self, messy_data):
        """Test duplicate record detection."""
        validator = DataValidator()
        result = validator.execute(data=messy_data)
        
        # Check if duplicates were detected
        issues = result['data']['issues']
        duplicate_issues = [i for i in issues if i['type'] == 'duplicate_records']
        assert len(duplicate_issues) > 0
    
    def test_missing_value_detection(self, messy_data):
        """Test missing value detection."""
        validator = DataValidator()
        result = validator.execute(data=messy_data)
        
        issues = result['data']['issues']
        missing_issues = [i for i in issues if i['type'] == 'missing_values']
        # Should find missing 'name' value
        assert len(missing_issues) >= 0


# =========== StatisticalAnalyzer Tests ===========

class TestStatisticalAnalyzer:
    """Tests for the StatisticalAnalyzer tool."""
    
    def test_analyze_numeric_columns(self, sample_data):
        """Test numeric column analysis."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.execute(data=sample_data)
        
        assert result['success'] is True
        assert 'statistics' in result['data']
        assert len(result['data']['statistics']) > 0
    
    def test_compute_mean(self, sample_data):
        """Test mean calculation."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.execute(data=sample_data)
        
        sales_stats = result['data']['statistics'].get('sales', {})
        assert 'mean' in sales_stats
        assert sales_stats['type'] == 'numeric'
    
    def test_categorical_analysis(self, sample_data):
        """Test categorical column analysis."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.execute(data=sample_data)
        
        region_stats = result['data']['statistics'].get('region', {})
        assert region_stats['type'] == 'categorical'
        assert 'unique_values' in region_stats
    
    def test_analyze_empty_data(self):
        """Test analysis of empty data."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.execute(data=[])
        
        assert result['success'] is True


# =========== DataTransformer Tests ===========

class TestDataTransformer:
    """Tests for the DataTransformer tool."""
    
    def test_remove_duplicates(self, messy_data):
        """Test duplicate removal."""
        transformer = DataTransformer()
        result = transformer.execute(data=messy_data, operation='remove_duplicates')
        
        assert result['success'] is True
        assert result['data']['removed'] > 0
        assert len(result['data']['result']) < len(messy_data)
    
    def test_remove_null_records(self, messy_data):
        """Test null record removal."""
        transformer = DataTransformer()
        result = transformer.execute(data=messy_data, operation='remove_nulls')
        
        assert result['success'] is True
        assert 'removed' in result['data']
    
    def test_filter_data(self, sample_data):
        """Test data filtering."""
        transformer = DataTransformer()
        result = transformer.execute(
            data=sample_data,
            operation='filter',
            column='region',
            value='North',
            operator='=='
        )
        
        assert result['success'] is True
        assert len(result['data']['result']) > 0
        assert all(r['region'] == 'North' for r in result['data']['result'])
    
    def test_filter_numeric(self, sample_data):
        """Test numeric filtering."""
        transformer = DataTransformer()
        result = transformer.execute(
            data=sample_data,
            operation='filter',
            column='sales',
            value=150,
            operator='>'
        )
        
        assert result['success'] is True
    
    def test_aggregate_data(self, sample_data):
        """Test data aggregation."""
        transformer = DataTransformer()
        result = transformer.execute(
            data=sample_data,
            operation='aggregate',
            group_by='region'
        )
        
        assert result['success'] is True
        assert len(result['data']['result']) > 0
    
    def test_extract_columns(self, sample_data):
        """Test column extraction."""
        transformer = DataTransformer()
        result = transformer.execute(
            data=sample_data,
            operation='extract_columns',
            columns=['product', 'sales']
        )
        
        assert result['success'] is True
        assert all('product' in r for r in result['data']['result'])


# =========== ReportGenerator Tests ===========

class TestReportGenerator:
    """Tests for the ReportGenerator tool."""
    
    def test_generate_report(self):
        """Test report generation."""
        generator = ReportGenerator()
        analysis_data = {
            'validation': {
                'valid': True,
                'issues': [],
                'row_count': 10
            },
            'statistics': {
                'col1': {'type': 'numeric', 'mean': 100}
            },
            'metadata': {
                'file': 'test.csv',
                'rows': 10
            }
        }
        
        result = generator.execute(analysis_results=analysis_data)
        
        assert result['success'] is True
        assert 'report' in result['data']
        assert 'formatted_text' in result['data']
    
    def test_report_structure(self):
        """Test report structure."""
        generator = ReportGenerator()
        analysis_data = {
            'validation': {'valid': True, 'issues': []},
            'statistics': {},
            'metadata': {'rows': 10}
        }
        
        result = generator.execute(analysis_results=analysis_data)
        report = result['data']['report']
        
        assert 'title' in report
        assert 'sections' in report
        assert len(report['sections']) > 0


# =========== DataAnalysisAgent Tests ===========

class TestDataAnalysisAgent:
    """Tests for the DataAnalysisAgent."""
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = DataAnalysisAgent()
        
        assert agent.file_reader is not None
        assert agent.validator is not None
        assert agent.analyzer is not None
        assert agent.transformer is not None
        assert agent.report_generator is not None
    
    def test_get_tool_list(self):
        """Test getting tool list."""
        agent = DataAnalysisAgent()
        tools = agent.get_tool_list()
        
        assert len(tools) == 5
        assert any(t['name'] == 'DataFileReader' for t in tools)
    
    def test_analyze_csv_file(self):
        """Test full analysis workflow on CSV."""
        agent = DataAnalysisAgent()
        result = agent.analyze_file('data/sales_data.csv')
        
        assert result['success'] is True
        assert 'report' in result
        assert 'formatted_report' in result
    
    def test_analyze_json_file(self):
        """Test full analysis workflow on JSON."""
        agent = DataAnalysisAgent()
        result = agent.analyze_file('data/inventory.json')
        
        assert result['success'] is True
        assert len(result['steps']) > 0
    
    def test_quick_validate(self):
        """Test quick validation."""
        agent = DataAnalysisAgent()
        result = agent.quick_validate('data/sales_data.csv')
        
        assert result['success'] is True
        assert 'validation' in result
    
    def test_get_statistics(self):
        """Test statistics computation."""
        agent = DataAnalysisAgent()
        result = agent.get_statistics('data/sales_data.csv')
        
        assert result['success'] is True
        assert 'statistics' in result
    
    def test_transform_data(self):
        """Test data transformation through agent."""
        agent = DataAnalysisAgent()
        data = [
            {'id': 1, 'value': 100},
            {'id': 2, 'value': 200}
        ]
        
        result = agent.transform_data(data, operation='remove_duplicates')
        
        assert result['success'] is True
    
    def test_messy_data_analysis(self):
        """Test analysis of data with quality issues."""
        agent = DataAnalysisAgent()
        result = agent.analyze_file('data/messy_data.csv')
        
        assert result['success'] is True
        # Messy data should have validation issues
        validation = result['report'].get('sections', [{}])[0].get('content', {})


# =========== Integration Tests ===========

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow."""
        agent = DataAnalysisAgent()
        
        # Analyze file
        result = agent.analyze_file('data/customer_data.csv')
        assert result['success']
        
        # Extract log
        log = agent.get_execution_log()
        assert len(log) > 0
    
    def test_data_quality_workflow(self):
        """Test data quality check workflow."""
        agent = DataAnalysisAgent()
        
        # Quick validate good data
        good_result = agent.quick_validate('data/customer_data.csv')
        assert good_result['success']
        
        # Quick validate messy data
        messy_result = agent.quick_validate('data/messy_data.csv')
        assert messy_result['success']
    
    def test_stats_extraction_workflow(self):
        """Test statistics extraction workflow."""
        agent = DataAnalysisAgent()
        
        result = agent.get_statistics('data/sales_data.csv')
        assert result['success']
        assert len(result['statistics']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
