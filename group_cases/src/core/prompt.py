"""
Prompt module for managing and formatting prompts.
"""
from typing import Dict, Any, Optional

class Prompt:
    """A class for managing and formatting prompts."""
    
    def __init__(self, template: str, variables: Optional[Dict[str, Any]] = None):
        """
        Initialize prompt.
        
        Args:
            template (str): Template string with variables in {variable_name} format
            variables (Dict[str, Any], optional): Variables to format the template with. Defaults to None.
        """
        self.template = template
        self.variables = variables or {}
        
    def format(self, **kwargs) -> str:
        """
        Format the prompt with the given variables.
        
        Args:
            **kwargs: Variables to format the template with
            
        Returns:
            str: Formatted prompt
        """
        # Combine stored variables with new ones, new ones take precedence
        variables = {**self.variables, **kwargs}
        return self.template.format(**variables)
        
    def add_variable(self, name: str, value: Any) -> None:
        """
        Add a variable to the prompt.
        
        Args:
            name (str): Variable name
            value (Any): Variable value
        """
        self.variables[name] = value
        
    def remove_variable(self, name: str) -> None:
        """
        Remove a variable from the prompt.
        
        Args:
            name (str): Variable name
        """
        if name in self.variables:
            del self.variables[name]
            
    def get_variables(self) -> Dict[str, Any]:
        """
        Get all variables.
        
        Returns:
            Dict[str, Any]: Dictionary of variable names to values
        """
        return self.variables.copy()
