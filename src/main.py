"""
Data Analysis Agent - Main Application Module
Entry point for the data analysis system.
"""

import json
import sys
from pathlib import Path
from typing import Optional
from src.agent import DataAnalysisAgent


class DataAnalysisApp:
    """
    Main application class for the Data Analysis Agent.
    Handles user interaction and coordinates the agent's workflow.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.agent = DataAnalysisAgent()
        self.current_file = None
    
    def run_interactive(self):
        """Run the application in interactive mode."""
        print("\n" + "=" * 70)
        print("DATA ANALYSIS AGENT - Interactive Mode")
        print("=" * 70)
        print("\nAvailable Tools:")
        for tool in self.agent.get_tool_list():
            print(f"  - {tool['name']}: {tool['description']}")
        
        print("\nCommands:")
        print("  1. analyze <file_path>    - Perform full analysis on a file")
        print("  2. validate <file_path>   - Quick validation of a file")
        print("  3. stats <file_path>      - Get statistics for a file")
        print("  4. help                   - Show this help message")
        print("  5. quit                   - Exit the application")
        print("\n" + "-" * 70 + "\n")
        
        while True:
            try:
                command = input("Enter command: ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                if command.lower() == 'help':
                    self._print_help()
                    continue
                
                parts = command.split(None, 1)
                cmd = parts[0].lower()
                param = parts[1] if len(parts) > 1 else None
                
                if cmd == 'analyze':
                    if not param:
                        print("Error: Please provide a file path")
                        continue
                    self._handle_analyze(param)
                
                elif cmd == 'validate':
                    if not param:
                        print("Error: Please provide a file path")
                        continue
                    self._handle_validate(param)
                
                elif cmd == 'stats':
                    if not param:
                        print("Error: Please provide a file path")
                        continue
                    self._handle_stats(param)
                
                else:
                    print(f"Unknown command: {cmd}")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _handle_analyze(self, file_path: str):
        """Handle analyze command."""
        print(f"\nAnalyzing file: {file_path}")
        result = self.agent.analyze_file(file_path)
        
        if result['success']:
            print("\n✓ Analysis completed successfully!")
            print(result['formatted_report'])
            
            # Save report to file
            output_file = f"{Path(file_path).stem}_report.json"
            with open(output_file, 'w') as f:
                json.dump(result['report'], f, indent=2)
            print(f"\nReport saved to: {output_file}")
        else:
            print(f"\n✗ Analysis failed: {result['error']}")
    
    def _handle_validate(self, file_path: str):
        """Handle validate command."""
        print(f"\nValidating file: {file_path}")
        result = self.agent.quick_validate(file_path)
        
        if result['success']:
            val = result['validation']
            print(f"\n✓ File Information:")
            print(f"  Rows: {result['rows']}")
            print(f"  Columns: {result['columns']}")
            print(f"  Data Quality: {'GOOD' if val.get('valid') else 'ISSUES FOUND'}")
            print(f"  Issues: {len(val.get('issues', []))}")
            if val.get('issues'):
                print("\n  Issues found:")
                for issue in val.get('issues', [])[:5]:
                    print(f"    - {issue['type']}: {issue}")
        else:
            print(f"\n✗ Validation failed: {result['error']}")
    
    def _handle_stats(self, file_path: str):
        """Handle stats command."""
        print(f"\nComputing statistics for: {file_path}")
        result = self.agent.get_statistics(file_path)
        
        if result['success']:
            print("\n✓ Statistics computed:")
            for col, stats in result['statistics'].items():
                print(f"\n  {col}:")
                for key, value in stats.items():
                    if key != 'type':
                        print(f"    {key}: {value}")
        else:
            print(f"\n✗ Statistics failed: {result['error']}")
    
    def _print_help(self):
        """Print help message."""
        print("\nCOMMAND HELP:")
        print("\n  analyze <file_path>")
        print("    Performs complete analysis of a data file")
        print("    - Reads the file (CSV or JSON)")
        print("    - Validates data quality")
        print("    - Computes statistics")
        print("    - Generates comprehensive report")
        print("    Example: analyze data/sales_data.csv")
        
        print("\n  validate <file_path>")
        print("    Quick validation of a file without full analysis")
        print("    - Checks data quality")
        print("    - Reports issues")
        print("    Example: validate data/customers.json")
        
        print("\n  stats <file_path>")
        print("    Computes only statistical metrics")
        print("    Example: stats data/metrics.csv")
        
        print("\n  help")
        print("    Shows this help message")
        
        print("\n  quit")
        print("    Exits the application")
        print()


def main():
    """Main entry point."""
    app = DataAnalysisApp()
    app.run_interactive()


if __name__ == '__main__':
    main()
