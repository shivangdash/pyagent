"""
Data Analysis Agent - Orchestrates tools to analyze data and provide insights.

The agent receives user requests and decides which tools to use in sequence
to process data and generate meaningful insights.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from src.tools import (
    DataFileReader,
    DataValidator,
    StatisticalAnalyzer,
    DataTransformer,
    ReportGenerator
)


class DataAnalysisAgent:
    """
    Intelligent agent for data analysis.
    
    The agent can:
    1. Read data files (CSV, JSON)
    2. Validate data quality
    3. Compute statistics
    4. Transform and clean data
    5. Generate comprehensive reports
    
    The agent follows a workflow pattern where it decides which tools to use
    based on the user's request and data characteristics.
    """
    
    def __init__(self):
        """Initialize the agent with all available tools."""
        self.file_reader = DataFileReader()
        self.validator = DataValidator()
        self.analyzer = StatisticalAnalyzer()
        self.transformer = DataTransformer()
        self.report_generator = ReportGenerator()
        
        self.execution_log = []
        self.last_data = None
        self.last_validation = None
        self.last_statistics = None
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a data file with complete workflow.
        
        This is the main entry point that coordinates all tools:
        1. Read file
        2. Validate data
        3. Analyze statistics
        4. Generate report
        
        Args:
            file_path: Path to the data file to analyze
            
        Returns:
            Complete analysis report
        """
        self._log_action(f"Starting analysis of file: {file_path}")
        
        result = {
            'task': 'analyze_file',
            'file_path': file_path,
            'timestamp': datetime.now().isoformat(),
            'steps': []
        }
        
        # Step 1: Read file
        self._log_action("Step 1: Reading file")
        read_result = self.file_reader.execute(file_path=file_path)
        
        if not read_result['success']:
            result['success'] = False
            result['error'] = read_result['error']
            return result
        
        self.last_data = read_result['data']['rows']
        result['steps'].append({
            'name': 'File Read',
            'status': 'success',
            'metadata': read_result['metadata'],
            'data_summary': {
                'rows': read_result['data']['row_count'],
                'columns': read_result['data']['column_count']
            }
        })
        
        # Step 2: Validate data
        self._log_action("Step 2: Validating data quality")
        validation_result = self.validator.execute(data=self.last_data)
        self.last_validation = validation_result['data']
        
        result['steps'].append({
            'name': 'Data Validation',
            'status': 'success',
            'validation_result': {
                'valid': validation_result['data']['valid'],
                'issues': len(validation_result['data']['issues']),
                'summary': validation_result['data']['summary']
            }
        })
        
        # Step 3: Analyze statistics
        self._log_action("Step 3: Computing statistics")
        analysis_result = self.analyzer.execute(data=self.last_data)
        self.last_statistics = analysis_result['data']['statistics']
        
        result['steps'].append({
            'name': 'Statistical Analysis',
            'status': 'success',
            'columns_analyzed': analysis_result['metadata']['columns_analyzed']
        })
        
        # Step 4: Generate report
        self._log_action("Step 4: Generating report")
        report_params = {
            'validation': validation_result['data'],
            'statistics': self.last_statistics,
            'metadata': {
                'file': read_result['metadata']['file_path'],
                'file_size': read_result['metadata']['file_size_bytes'],
                'rows': read_result['data']['row_count'],
                'columns': read_result['data']['column_count']
            }
        }
        
        report_result = self.report_generator.execute(report_params)
        
        result['steps'].append({
            'name': 'Report Generation',
            'status': 'success'
        })
        
        result['success'] = True
        result['report'] = report_result['data']['report']
        result['formatted_report'] = report_result['data']['formatted_text']
        
        self._log_action("Analysis completed successfully")
        return result
    
    def quick_validate(self, file_path: str) -> Dict[str, Any]:
        """
        Quick validation of a file without full analysis.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Validation report
        """
        self._log_action(f"Quick validation of: {file_path}")
        
        # Read file
        read_result = self.file_reader.execute(file_path=file_path)
        if not read_result['success']:
            return {'success': False, 'error': read_result['error']}
        
        # Validate
        data = read_result['data']['rows']
        validation_result = self.validator.execute(data=data)
        
        return {
            'success': True,
            'file_path': file_path,
            'rows': len(data),
            'columns': len(data[0].keys()) if data else 0,
            'validation': validation_result['data']
        }
    
    def transform_data(self, data: List[Dict[str, Any]], operation: str, **kwargs) -> Dict[str, Any]:
        """
        Transform data using the transformer tool.
        
        Args:
            data: Data records to transform
            operation: Type of transformation
            **kwargs: Operation parameters
            
        Returns:
            Transformation result
        """
        self._log_action(f"Transforming data with operation: {operation}")
        return self.transformer.execute(data=data, operation=operation, **kwargs)
    
    def get_statistics(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze statistics of a file without full report generation.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Statistics dictionary
        """
        self._log_action(f"Computing statistics for: {file_path}")
        
        # Read file
        read_result = self.file_reader.execute(file_path=file_path)
        if not read_result['success']:
            return {'success': False, 'error': read_result['error']}
        
        # Analyze
        data = read_result['data']['rows']
        analysis_result = self.analyzer.execute(data=data)
        
        return {
            'success': True,
            'file_path': file_path,
            'statistics': analysis_result['data']['statistics']
        }
    
    def _log_action(self, message: str):
        """Log agent action."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.execution_log.append(log_entry)
        print(f"[Agent] {message}")
    
    def get_execution_log(self) -> List[Dict[str, str]]:
        """Get the agent's execution log."""
        return self.execution_log
    
    def get_tool_list(self) -> List[Dict[str, str]]:
        """Get list of available tools."""
        return [
            self.file_reader.get_info(),
            self.validator.get_info(),
            self.analyzer.get_info(),
            self.transformer.get_info(),
            self.report_generator.get_info()
        ]
