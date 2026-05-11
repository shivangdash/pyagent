#!/usr/bin/env python3
"""
Quick demonstration script for PyAgent system.
Shows the agent in action with a complete workflow.
"""

from src.agent import DataAnalysisAgent

def demo():
    """Run a demonstration of the agent system."""
    print("=" * 80)
    print("PyAgent - Data Analysis Agent System - DEMONSTRATION")
    print("=" * 80)
    
    # Create agent
    agent = DataAnalysisAgent()
    
    print("\n1. Agent Initialization - Available Tools:")
    print("-" * 80)
    for tool in agent.get_tool_list():
        print(f"   ✓ {tool['name']}: {tool['description']}")
    
    # Demo 1: Analyze clean data
    print("\n\n2. Analyzing Clean Data (sales_data.csv)")
    print("-" * 80)
    result = agent.analyze_file('data/sales_data.csv')
    
    if result['success']:
        print("✓ Analysis completed successfully!")
        print(f"  - Rows: {result['report']['sections'][0]['content'].get('row_count', 'N/A')}")
        print(f"  - Status: {result['report']['sections'][0]['status']}")
    
    # Demo 2: Analyze messy data
    print("\n\n3. Analyzing Messy Data (messy_data.csv)")
    print("-" * 80)
    result = agent.quick_validate('data/messy_data.csv')
    
    if result['success']:
        val = result['validation']
        print(f"✓ Validation complete")
        print(f"  - Rows: {result['rows']}")
        print(f"  - Quality: {'GOOD' if val.get('valid') else 'ISSUES DETECTED'}")
        print(f"  - Issues found: {len(val.get('issues', []))}")
        
        if val.get('issues'):
            print("  - Issue types:")
            issue_types = set(i['type'] for i in val.get('issues', []))
            for issue_type in issue_types:
                print(f"    • {issue_type}")
    
    # Demo 3: Statistics from JSON
    print("\n\n4. Analyzing JSON Data (inventory.json)")
    print("-" * 80)
    result = agent.get_statistics('data/inventory.json')
    
    if result['success']:
        print("✓ Statistics computed")
        print(f"  - Columns analyzed: {len(result.get('statistics', {}))}")
        
        # Show one example
        first_col = list(result.get('statistics', {}).keys())[0]
        first_stats = result['statistics'][first_col]
        print(f"  - Sample: {first_col} ({first_stats.get('type')})")
    
    # Demo 4: Agent Execution Log
    print("\n\n5. Execution Log")
    print("-" * 80)
    log = agent.get_execution_log()
    print(f"✓ Total actions logged: {len(log)}")
    print("  Last 5 actions:")
    for entry in log[-5:]:
        print(f"    • {entry['message']}")
    
    print("\n" + "=" * 80)
    print("Demonstration Complete!")
    print("=" * 80)
    print("\nTo use interactively, run: python -m src.main")
    print()

if __name__ == '__main__':
    demo()
