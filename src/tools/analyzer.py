"""
StatisticalAnalyzer Tool - Computes statistical metrics and measures.
"""

from typing import Any, Dict, List
from .base_tool import BaseTool


class StatisticalAnalyzer(BaseTool):
    """
    Tool for computing statistical metrics from data.
    
    Calculates:
    - Descriptive statistics (mean, median, std dev, min, max)
    - Data distribution
    - Correlations
    - Categorical summaries
    """
    
    def __init__(self):
        super().__init__(
            name="StatisticalAnalyzer",
            description="Computes statistical metrics and measures from data"
        )
    
    def execute(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze data and compute statistical metrics.
        
        Args:
            data: List of data records (dictionaries)
            
        Returns:
            Dictionary containing statistical analysis results
        """
        try:
            if not data:
                return {
                    'success': True,
                    'data': {'statistics': {}, 'summary': 'Empty dataset'},
                    'error': None,
                    'metadata': {}
                }
            
            statistics = {}
            
            # Analyze each column
            for column in data[0].keys():
                values = [record.get(column) for record in data]
                
                # Try numeric analysis
                numeric_values = self._extract_numeric_values(values)
                if numeric_values:
                    statistics[column] = self._compute_numeric_stats(column, numeric_values)
                else:
                    # Categorical analysis
                    statistics[column] = self._compute_categorical_stats(column, values)
            
            return {
                'success': True,
                'data': {
                    'statistics': statistics,
                    'row_count': len(data),
                    'column_count': len(data[0].keys()) if data else 0,
                    'summary': f"Analyzed {len(data)} records with {len(statistics)} columns"
                },
                'error': None,
                'metadata': {
                    'columns_analyzed': len(statistics)
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"Analysis error: {str(e)}",
                'metadata': {}
            }
    
    def _extract_numeric_values(self, values: List[Any]) -> List[float]:
        """Extract numeric values from a list, handling various formats."""
        numeric = []
        for val in values:
            if val is None or val == '':
                continue
            try:
                numeric.append(float(val))
            except (ValueError, TypeError):
                continue
        return numeric
    
    def _compute_numeric_stats(self, column: str, values: List[float]) -> Dict[str, Any]:
        """Compute statistics for numeric column."""
        if not values:
            return {'type': 'numeric', 'status': 'no_valid_values'}
        
        sorted_values = sorted(values)
        count = len(values)
        mean = sum(values) / count
        
        # Median
        if count % 2 == 0:
            median = (sorted_values[count // 2 - 1] + sorted_values[count // 2]) / 2
        else:
            median = sorted_values[count // 2]
        
        # Standard deviation
        variance = sum((x - mean) ** 2 for x in values) / count
        std_dev = variance ** 0.5
        
        return {
            'type': 'numeric',
            'count': count,
            'mean': round(mean, 4),
            'median': round(median, 4),
            'std_dev': round(std_dev, 4),
            'min': round(min(values), 4),
            'max': round(max(values), 4),
            'range': round(max(values) - min(values), 4),
            'sum': round(sum(values), 4)
        }
    
    def _compute_categorical_stats(self, column: str, values: List[Any]) -> Dict[str, Any]:
        """Compute statistics for categorical column."""
        # Count occurrences
        value_counts = {}
        for val in values:
            if val is None or val == '':
                val = 'NULL'
            val_str = str(val)
            value_counts[val_str] = value_counts.get(val_str, 0) + 1
        
        # Get top categories
        sorted_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_counts[:5]
        
        total_non_null = sum(1 for v in values if v not in [None, ''])
        
        return {
            'type': 'categorical',
            'unique_values': len(value_counts),
            'total_count': len(values),
            'non_null_count': total_non_null,
            'top_values': {k: v for k, v in top_5},
            'most_common': top_5[0][0] if top_5 else None
        }
