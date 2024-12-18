"""
Database utilities for persistent storage.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import Config

class DatabaseManager:
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        self.discussions_file = self.data_dir / "discussions.json"
        self.memories_file = self.data_dir / "memories.json"
        self._init_storage()
    
    def _init_storage(self) -> None:
        """Initialize storage files if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.discussions_file.exists():
            self._save_json(self.discussions_file, {"discussions": []})
        
        if not self.memories_file.exists():
            self._save_json(self.memories_file, {"memories": []})
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Save data to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def save_discussion(self, discussion_id: str, data: Dict[str, Any]) -> None:
        """Save discussion data."""
        discussions = self._load_json(self.discussions_file)
        
        # Update existing or add new
        found = False
        for i, disc in enumerate(discussions.get("discussions", [])):
            if disc.get("id") == discussion_id:
                discussions["discussions"][i] = {
                    "id": discussion_id,
                    "updated_at": datetime.now(),
                    **data
                }
                found = True
                break
        
        if not found:
            discussions.setdefault("discussions", []).append({
                "id": discussion_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                **data
            })
        
        self._save_json(self.discussions_file, discussions)
    
    def get_discussion(self, discussion_id: str) -> Optional[Dict[str, Any]]:
        """Get discussion data by ID."""
        discussions = self._load_json(self.discussions_file)
        for disc in discussions.get("discussions", []):
            if disc.get("id") == discussion_id:
                return disc
        return None
    
    def list_discussions(self) -> List[Dict[str, Any]]:
        """List all discussions."""
        discussions = self._load_json(self.discussions_file)
        return discussions.get("discussions", [])
    
    def save_memory(self, memory_id: str, data: Dict[str, Any]) -> None:
        """Save memory data."""
        memories = self._load_json(self.memories_file)
        
        # Update existing or add new
        found = False
        for i, mem in enumerate(memories.get("memories", [])):
            if mem.get("id") == memory_id:
                memories["memories"][i] = {
                    "id": memory_id,
                    "updated_at": datetime.now(),
                    **data
                }
                found = True
                break
        
        if not found:
            memories.setdefault("memories", []).append({
                "id": memory_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                **data
            })
        
        self._save_json(self.memories_file, memories)
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get memory data by ID."""
        memories = self._load_json(self.memories_file)
        for mem in memories.get("memories", []):
            if mem.get("id") == memory_id:
                return mem
        return None
    
    def list_memories(self) -> List[Dict[str, Any]]:
        """List all memories."""
        memories = self._load_json(self.memories_file)
        return memories.get("memories", [])
