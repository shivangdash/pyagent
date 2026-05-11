"""
Base class for all tools used by the agent.
Defines the interface that all tools must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseTool(ABC):
    """
    Abstract base class for all agent tools.
    
    Every tool that can be used by the agent must inherit from this class
    and implement the required methods.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize a tool with a name and description.
        
        Args:
            name: Unique identifier for the tool
            description: Human-readable description of what the tool does
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Returns:
            Dictionary containing:
                - 'success': bool indicating if the operation succeeded
                - 'data': The result of the tool execution
                - 'error': Error message if success is False
                - 'metadata': Optional metadata about the execution
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """Get tool information for the agent."""
        return {
            'name': self.name,
            'description': self.description
        }
