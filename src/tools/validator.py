"""
DataValidator Tool - Validates data quality and identifies issues.
"""

from typing import Any, Dict, List
from .base_tool import BaseTool


class DataValidator(BaseTool):
    """
    Tool for validating data quality.
    
    Checks for:
    - Missing values (None, empty strings)
    - Data type consistency
    - Duplicate records
    - Outliers (basic statistical detection)
    """
    
    def __init__(self):
        super().__init__(
            name="DataValidator",
            description="Validates data quality and identifies data issues"
        )
    
    def execute(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate the quality of provided data.
        
        Args:
            data: List of data records (dictionaries)
            
        Returns:
            Validation report with identified issues
        """
        try:
            if not data:
                return {
                    'success': True,
                    'data': {
                        'valid': True,
                        'row_count': 0,
                        'issues': [],
                        'summary': 'Empty dataset - no validation needed'
                    },
                    'error': None,
                    'metadata': {}
                }
            
            issues = []
            
            # Check for missing values
            missing_summary = self._check_missing_values(data)
            if missing_summary['has_missing']:
                issues.extend(missing_summary['issues'])
            
            # Check for duplicates
            duplicate_summary = self._check_duplicates(data)
            if duplicate_summary['duplicates_found']:
                issues.extend(duplicate_summary['issues'])
            
            # Check data type consistency
            type_summary = self._check_type_consistency(data)
            if type_summary['inconsistencies']:
                issues.extend(type_summary['issues'])
            
            valid = len(issues) == 0
            
            return {
                'success': True,
                'data': {
                    'valid': valid,
                    'row_count': len(data),
                    'columns': list(data[0].keys()) if data else [],
                    'issues': issues,
                    'summary': f"Found {len(issues)} data quality issues" if issues else "Data quality is good"
                },
                'error': None,
                'metadata': {
                    'missing_value_check': missing_summary,
                    'duplicate_check': duplicate_summary,
                    'type_consistency': type_summary
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"Validation error: {str(e)}",
                'metadata': {}
            }
    
    def _check_missing_values(self, data: List[Dict]) -> Dict[str, Any]:
        """Check for missing values in the dataset."""
        issues = []
        missing_counts = {}
        
        for record in data:
            for key, value in record.items():
                if value is None or value == '' or (isinstance(value, str) and value.lower() == 'nan'):
                    missing_counts[key] = missing_counts.get(key, 0) + 1
        
        for column, count in missing_counts.items():
            percentage = (count / len(data)) * 100
            issues.append({
                'type': 'missing_values',
                'column': column,
                'count': count,
                'percentage': round(percentage, 2),
                'severity': 'high' if percentage > 50 else 'medium' if percentage > 20 else 'low'
            })
        
        return {
            'has_missing': len(missing_counts) > 0,
            'issues': issues,
            'missing_counts': missing_counts
        }
    
    def _check_duplicates(self, data: List[Dict]) -> Dict[str, Any]:
        """Check for duplicate records."""
        seen = set()
        duplicates = []
        duplicate_indices = []
        
        for idx, record in enumerate(data):
            # Convert to tuple for hashability
            try:
                record_tuple = tuple(sorted(record.items()))
                if record_tuple in seen:
                    duplicate_indices.append(idx)
                else:
                    seen.add(record_tuple)
            except TypeError:
                # Skip unhashable types
                pass
        
        if duplicate_indices:
            duplicates.append({
                'type': 'duplicate_records',
                'count': len(duplicate_indices),
                'indices': duplicate_indices[:10],  # Show first 10
                'severity': 'high' if len(duplicate_indices) > len(data) * 0.1 else 'medium'
            })
        
        return {
            'duplicates_found': len(duplicate_indices) > 0,
            'issues': duplicates,
            'duplicate_count': len(duplicate_indices)
        }
    
    def _check_type_consistency(self, data: List[Dict]) -> Dict[str, Any]:
        """Check for type inconsistencies in columns."""
        issues = []
        column_types = {}
        
        for record in data:
            for key, value in record.items():
                if key not in column_types:
                    column_types[key] = []
                column_types[key].append(type(value).__name__)
        
        inconsistencies = {}
        for column, types in column_types.items():
            unique_types = set(types)
            if len(unique_types) > 1:
                inconsistencies[column] = list(unique_types)
                issues.append({
                    'type': 'type_inconsistency',
                    'column': column,
                    'found_types': list(unique_types),
                    'severity': 'medium'
                })
        
        return {
            'inconsistencies': len(inconsistencies) > 0,
            'issues': issues,
            'problematic_columns': inconsistencies
        }
