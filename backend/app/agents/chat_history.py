"""
Chat History module - Manages conversation history persistence per project.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

# Chat history storage directory
CHAT_HISTORY_DIR = Path(__file__).parent.parent / "data" / "chat_history"


class ChatHistoryManager:
    """Manages chat history for projects."""

    def __init__(self):
        self._ensure_history_dir()

    def _ensure_history_dir(self):
        """Ensure chat history directory exists."""
        CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    def _get_history_file(self, project_id: str) -> Path:
        """Get the history file path for a project."""
        return CHAT_HISTORY_DIR / f"{project_id}.json"

    def save(self, project_id: str, messages: List[Dict[str, Any]]) -> bool:
        """
        Save chat history for a project.
        
        Args:
            project_id: Project ID
            messages: List of message dictionaries
            
        Returns:
            True if successful
        """
        try:
            history_file = self._get_history_file(project_id)
            history_file.write_text(json.dumps(messages, indent=2))
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False

    def load(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Load chat history for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of message dictionaries (empty if none exists)
        """
        try:
            history_file = self._get_history_file(project_id)
            if not history_file.exists():
                return []
            
            data = json.loads(history_file.read_text())
            return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []

    def clear(self, project_id: str) -> bool:
        """
        Clear chat history for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            True if successful
        """
        try:
            history_file = self._get_history_file(project_id)
            if history_file.exists():
                history_file.unlink()
            return True
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            return False


# Global chat history manager instance
chat_history_manager = ChatHistoryManager()
