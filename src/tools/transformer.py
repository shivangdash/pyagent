"""
DataTransformer Tool - Transforms, cleans, and processes data.
"""

from typing import Any, Dict, List
from .base_tool import BaseTool


class DataTransformer(BaseTool):
    """
    Tool for transforming and cleaning data.
    
    Operations:
    - Remove duplicates
    - Handle missing values
    - Filter records
    - Aggregate data
    - Extract and transform columns
    """
    
    def __init__(self):
        super().__init__(
            name="DataTransformer",
            description="Transforms, cleans, and processes data"
        )
    
    def execute(self, data: List[Dict[str, Any]], operation: str, **kwargs) -> Dict[str, Any]:
        """
        Transform data using specified operation.
        
        Args:
            data: List of data records
            operation: Type of transformation ('remove_duplicates', 'remove_nulls', 'filter', 'aggregate')
            **kwargs: Operation-specific parameters
            
        Returns:
            Transformed data
        """
        try:
            if not data:
                return {
                    'success': True,
                    'data': {'result': []},
                    'error': None,
                    'metadata': {}
                }
            
            if operation == 'remove_duplicates':
                return self._remove_duplicates(data)
            elif operation == 'remove_nulls':
                return self._remove_null_records(data)
            elif operation == 'filter':
                return self._filter_data(data, kwargs)
            elif operation == 'aggregate':
                return self._aggregate_data(data, kwargs)
            elif operation == 'extract_columns':
                return self._extract_columns(data, kwargs)
            else:
                return {
                    'success': False,
                    'data': None,
                    'error': f"Unknown operation: {operation}",
                    'metadata': {}
                }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"Transform error: {str(e)}",
                'metadata': {}
            }
    
    def _remove_duplicates(self, data: List[Dict]) -> Dict[str, Any]:
        """Remove duplicate records."""
        seen = set()
        unique_data = []
        duplicates_removed = 0
        
        for record in data:
            try:
                record_tuple = tuple(sorted(record.items()))
                if record_tuple not in seen:
                    seen.add(record_tuple)
                    unique_data.append(record)
                else:
                    duplicates_removed += 1
            except TypeError:
                unique_data.append(record)
        
        return {
            'success': True,
            'data': {
                'result': unique_data,
                'original_count': len(data),
                'final_count': len(unique_data),
                'removed': duplicates_removed
            },
            'error': None,
            'metadata': {'operation': 'remove_duplicates'}
        }
    
    def _remove_null_records(self, data: List[Dict]) -> Dict[str, Any]:
        """Remove records with null/empty values."""
        cleaned = []
        removed_count = 0
        
        for record in data:
            if all(val not in [None, ''] for val in record.values()):
                cleaned.append(record)
            else:
                removed_count += 1
        
        return {
            'success': True,
            'data': {
                'result': cleaned,
                'original_count': len(data),
                'final_count': len(cleaned),
                'removed': removed_count
            },
            'error': None,
            'metadata': {'operation': 'remove_nulls'}
        }
    
    def _filter_data(self, data: List[Dict], params: Dict) -> Dict[str, Any]:
        """Filter data based on conditions."""
        column = params.get('column')
        value = params.get('value')
        operator = params.get('operator', '==')
        
        if not column:
            return {
                'success': False,
                'data': None,
                'error': "column parameter required",
                'metadata': {}
            }
        
        filtered = []
        for record in data:
            if column not in record:
                continue
            
            record_val = record[column]
            
            if operator == '==':
                if record_val == value:
                    filtered.append(record)
            elif operator == '>':
                try:
                    if float(record_val) > float(value):
                        filtered.append(record)
                except (ValueError, TypeError):
                    pass
            elif operator == '<':
                try:
                    if float(record_val) < float(value):
                        filtered.append(record)
                except (ValueError, TypeError):
                    pass
            elif operator == 'contains':
                if str(value).lower() in str(record_val).lower():
                    filtered.append(record)
        
        return {
            'success': True,
            'data': {
                'result': filtered,
                'original_count': len(data),
                'final_count': len(filtered),
                'filter_condition': f"{column} {operator} {value}"
            },
            'error': None,
            'metadata': {'operation': 'filter'}
        }
    
    def _aggregate_data(self, data: List[Dict], params: Dict) -> Dict[str, Any]:
        """Aggregate data by grouping."""
        group_by = params.get('group_by')
        metric = params.get('metric', 'count')
        metric_column = params.get('metric_column')
        
        if not group_by:
            return {
                'success': False,
                'data': None,
                'error': "group_by parameter required",
                'metadata': {}
            }
        
        groups = {}
        for record in data:
            if group_by not in record:
                continue
            
            key = str(record[group_by])
            if key not in groups:
                groups[key] = []
            groups[key].append(record)
        
        result = []
        for key, group in groups.items():
            agg_record = {f'{group_by}': key}
            
            if metric == 'count':
                agg_record['count'] = len(group)
            elif metric == 'sum' and metric_column:
                total = 0
                for record in group:
                    try:
                        total += float(record.get(metric_column, 0))
                    except (ValueError, TypeError):
                        pass
                agg_record[f'sum_{metric_column}'] = round(total, 2)
            elif metric == 'avg' and metric_column:
                values = []
                for record in group:
                    try:
                        values.append(float(record.get(metric_column, 0)))
                    except (ValueError, TypeError):
                        pass
                if values:
                    agg_record[f'avg_{metric_column}'] = round(sum(values) / len(values), 2)
            
            result.append(agg_record)
        
        return {
            'success': True,
            'data': {
                'result': result,
                'original_count': len(data),
                'groups_created': len(result),
                'aggregation': metric
            },
            'error': None,
            'metadata': {'operation': 'aggregate'}
        }
    
    def _extract_columns(self, data: List[Dict], params: Dict) -> Dict[str, Any]:
        """Extract specific columns from data."""
        columns = params.get('columns', [])
        
        if not columns:
            return {
                'success': False,
                'data': None,
                'error': "columns parameter required",
                'metadata': {}
            }
        
        result = []
        for record in data:
            extracted = {col: record.get(col) for col in columns if col in record}
            if extracted:
                result.append(extracted)
        
        return {
            'success': True,
            'data': {
                'result': result,
                'original_count': len(data),
                'final_count': len(result),
                'columns_extracted': columns
            },
            'error': None,
            'metadata': {'operation': 'extract_columns'}
        }
