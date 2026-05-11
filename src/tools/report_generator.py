"""
ReportGenerator Tool - Generates reports and insights from data analysis.
"""

import json
from typing import Any, Dict, List
from .base_tool import BaseTool


class ReportGenerator(BaseTool):
    """
    Tool for generating reports and insights.
    
    Generates:
    - Summary reports
    - Data quality reports
    - Statistical summaries
    - Recommendations and insights
    """
    
    def __init__(self):
        super().__init__(
            name="ReportGenerator",
            description="Generates reports and insights from data analysis"
        )
    
    def execute(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a report from analysis results.
        
        Args:
            analysis_results: Dictionary containing analysis data
            
        Returns:
            Generated report with insights and recommendations
        """
        try:
            report = {
                'title': 'Data Analysis Report',
                'sections': []
            }
            
            if 'validation' in analysis_results:
                report['sections'].append(
                    self._generate_validation_section(analysis_results['validation'])
                )
            
            if 'statistics' in analysis_results:
                report['sections'].append(
                    self._generate_statistics_section(analysis_results['statistics'])
                )
            
            if 'metadata' in analysis_results:
                report['sections'].append(
                    self._generate_metadata_section(analysis_results['metadata'])
                )
            
            # Add insights and recommendations
            report['sections'].append(
                self._generate_insights_section(analysis_results)
            )
            
            return {
                'success': True,
                'data': {
                    'report': report,
                    'formatted_text': self._format_report_text(report),
                    'json_export': json.dumps(report, indent=2)
                },
                'error': None,
                'metadata': {'report_type': 'comprehensive'}
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"Report generation error: {str(e)}",
                'metadata': {}
            }
    
    def _generate_validation_section(self, validation: Dict) -> Dict[str, Any]:
        """Generate data quality validation section."""
        issues = validation.get('issues', [])
        valid = validation.get('valid', True)
        
        return {
            'name': 'Data Quality Assessment',
            'status': 'PASS' if valid else 'ISSUES FOUND',
            'content': {
                'overall_quality': 'Good' if valid else 'Needs Attention',
                'issue_count': len(issues),
                'issues': issues[:10],  # Show top 10
                'recommendation': self._get_quality_recommendation(valid, issues)
            }
        }
    
    def _generate_statistics_section(self, statistics: Dict) -> Dict[str, Any]:
        """Generate statistics summary section."""
        numeric_cols = []
        categorical_cols = []
        
        for col, stats in statistics.items():
            if stats.get('type') == 'numeric':
                numeric_cols.append({
                    'name': col,
                    'mean': stats.get('mean'),
                    'std_dev': stats.get('std_dev'),
                    'range': f"{stats.get('min')} to {stats.get('max')}"
                })
            else:
                categorical_cols.append({
                    'name': col,
                    'unique_values': stats.get('unique_values'),
                    'most_common': stats.get('most_common')
                })
        
        return {
            'name': 'Statistical Summary',
            'content': {
                'numeric_columns': numeric_cols,
                'categorical_columns': categorical_cols,
                'total_columns': len(statistics)
            }
        }
    
    def _generate_metadata_section(self, metadata: Dict) -> Dict[str, Any]:
        """Generate metadata section."""
        return {
            'name': 'Dataset Information',
            'content': metadata
        }
    
    def _generate_insights_section(self, analysis: Dict) -> Dict[str, Any]:
        """Generate insights and recommendations."""
        insights = []
        
        # Data quality insights
        if 'validation' in analysis and not analysis['validation'].get('valid'):
            insights.append(
                'Data quality issues detected - recommend data cleaning before analysis'
            )
        
        # Statistical insights
        if 'statistics' in analysis:
            numeric_found = any(
                s.get('type') == 'numeric' 
                for s in analysis['statistics'].values()
            )
            if numeric_found:
                insights.append(
                    'Dataset contains numeric data - consider statistical analysis and visualization'
                )
        
        insights.append('Regular data monitoring recommended to maintain data quality')
        insights.append('Consider establishing data governance policies')
        
        return {
            'name': 'Insights & Recommendations',
            'content': {
                'insights': insights,
                'next_steps': [
                    'Review data quality issues',
                    'Perform deeper statistical analysis if needed',
                    'Establish data validation rules',
                    'Schedule regular data audits'
                ]
            }
        }
    
    def _get_quality_recommendation(self, valid: bool, issues: List) -> str:
        """Get recommendation based on data quality."""
        if valid:
            return 'Data quality is good. Safe to proceed with analysis.'
        
        high_severity = sum(1 for i in issues if i.get('severity') == 'high')
        if high_severity > 0:
            return 'Critical data quality issues found. Data cleaning is recommended before use.'
        
        return 'Some data quality issues found. Review and address before critical analysis.'
    
    def _format_report_text(self, report: Dict) -> str:
        """Format report as readable text."""
        lines = []
        lines.append('=' * 80)
        lines.append(report.get('title', 'Report'))
        lines.append('=' * 80)
        lines.append('')
        
        for section in report.get('sections', []):
            lines.append(f"\n{section.get('name', 'Section')}")
            lines.append('-' * 70)
            
            content = section.get('content', {})
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, (list, dict)):
                        lines.append(f"{key}:")
                        lines.append(f"  {json.dumps(value, indent=2)}")
                    else:
                        lines.append(f"{key}: {value}")
            else:
                lines.append(str(content))
        
        lines.append('\n' + '=' * 80)
        return '\n'.join(lines)
