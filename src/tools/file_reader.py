"""
DataFileReader Tool - Reads and loads data from CSV and JSON files.
"""

import json
import csv
from pathlib import Path
from typing import Any, Dict, List
from .base_tool import BaseTool


class DataFileReader(BaseTool):
    """
    Tool for reading data from CSV and JSON files.
    
    Supports:
    - CSV format with automatic header detection
    - JSON format (both single objects and arrays)
    """
    
    def __init__(self):
        super().__init__(
            name="DataFileReader",
            description="Reads and parses CSV and JSON data files"
        )
    
    def execute(self, file_path: str) -> Dict[str, Any]:
        """
        Read a data file (CSV or JSON).
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Result dictionary with loaded data
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {
                    'success': False,
                    'data': None,
                    'error': f"File not found: {file_path}",
                    'metadata': {}
                }
            
            if path.suffix.lower() == '.csv':
                return self._read_csv(path)
            elif path.suffix.lower() == '.json':
                return self._read_json(path)
            else:
                return {
                    'success': False,
                    'data': None,
                    'error': f"Unsupported file format: {path.suffix}. Supported: .csv, .json",
                    'metadata': {}
                }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"Error reading file: {str(e)}",
                'metadata': {}
            }
    
    def _read_csv(self, path: Path) -> Dict[str, Any]:
        """Read a CSV file and return as list of dictionaries."""
        try:
            data = []
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            return {
                'success': True,
                'data': {
                    'format': 'csv',
                    'rows': data,
                    'column_count': len(data[0].keys()) if data else 0,
                    'row_count': len(data)
                },
                'error': None,
                'metadata': {
                    'file_path': str(path),
                    'file_size_bytes': path.stat().st_size
                }
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"CSV parsing error: {str(e)}",
                'metadata': {}
            }
    
    def _read_json(self, path: Path) -> Dict[str, Any]:
        """Read a JSON file and return its content."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Normalize to list of records
            if isinstance(raw_data, list):
                records = raw_data
            elif isinstance(raw_data, dict):
                records = [raw_data]
            else:
                records = [raw_data]
            
            return {
                'success': True,
                'data': {
                    'format': 'json',
                    'rows': records,
                    'column_count': len(records[0].keys()) if isinstance(records[0], dict) else 0,
                    'row_count': len(records)
                },
                'error': None,
                'metadata': {
                    'file_path': str(path),
                    'file_size_bytes': path.stat().st_size
                }
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'data': None,
                'error': f"JSON parsing error: {str(e)}",
                'metadata': {}
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"JSON reading error: {str(e)}",
                'metadata': {}
            }
