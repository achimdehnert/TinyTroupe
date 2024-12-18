from typing import Any
from .agent import SemanticMemory as BaseSemanticMemory

class EnhancedSemanticMemory(BaseSemanticMemory):
    """Enhanced version of SemanticMemory with store implementation."""

    def store(self, value: Any) -> None:
        """
        Stores a value in semantic memory. For semantic memory, we store the value as a document
        that can be retrieved later based on relevance.
        
        Args:
            value (Any): The value to store in memory. Should be a dictionary with metadata about the information.
        """
        if isinstance(value, dict):
            # Create a document from the value
            doc_name = f"memory_{len(self.documents)}"
            doc_content = str(value)  # Convert dict to string for storage
            self.documents.append({"name": doc_name, "content": doc_content})
            self.filename_to_document[doc_name] = doc_content
