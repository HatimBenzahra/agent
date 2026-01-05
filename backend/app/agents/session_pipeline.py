"""
Session Pipeline - Complete trace system for agent context.
Tracks ALL events (files, commands, validations, messages) as structured JSON.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os


@dataclass
class PipelineEvent:
    """A single event in the session pipeline."""
    timestamp: str
    type: str  # user_message, plan_generated, terminal_command, file_created, etc.
    data: Dict[str, Any]
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "type": self.type,
            **self.data
        }


class SessionPipeline:
    """
    Tracks ALL events in a session as a structured JSON pipeline.
    The LLM can query this for complete context.
    """
    
    def __init__(self, session_id: str, workspace_path: str):
        self.session_id = session_id
        self.workspace_path = workspace_path
        self.pipeline: List[PipelineEvent] = []
        self.pipeline_file = os.path.join(workspace_path, ".session_pipeline.json")
        self._load_or_create()
    
    def _load_or_create(self):
        """Load existing pipeline or create new one."""
        if os.path.exists(self.pipeline_file):
            try:
                with open(self.pipeline_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct events
                    for event_data in data.get('pipeline', []):
                        timestamp = event_data.pop('timestamp')
                        event_type = event_data.pop('type')
                        self.pipeline.append(PipelineEvent(
                            timestamp=timestamp,
                            type=event_type,
                            data=event_data
                        ))
            except Exception as e:
                print(f"Failed to load pipeline: {e}")
                self.pipeline = []
        else:
            self.pipeline = []
            self._save()
    
    def add_event(self, event_type: str, **data):
        """Add an event to the pipeline."""
        event = PipelineEvent(
            timestamp=datetime.utcnow().isoformat(),
            type=event_type,
            data=data
        )
        self.pipeline.append(event)
        self._save()
    
    def _save(self):
        """Persist pipeline to disk."""
        try:
            data = {
                "session_id": self.session_id,
                "started_at": self.pipeline[0].timestamp if self.pipeline else datetime.utcnow().isoformat(),
                "pipeline": [e.to_dict() for e in self.pipeline],
                "current_state": self._compute_current_state()
            }
            with open(self.pipeline_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save pipeline: {e}")
    
    def _compute_current_state(self) -> Dict[str, Any]:
        """Compute current state from pipeline events."""
        files_created = []
        files_modified = []
        last_plan = None
        
        for event in self.pipeline:
            if event.type == "file_created":
                files_created.append(event.data.get('path'))
            elif event.type == "file_modified":
                files_modified.append(event.data.get('path'))
            elif event.type == "plan_generated":
                last_plan = event.data.get('plan')
        
        return {
            "files_created": files_created,
            "files_modified": files_modified,
            "last_created_file": files_created[-1] if files_created else None,
            "last_modified_file": files_modified[-1] if files_modified else None,
            "active_plan": last_plan
        }
    
    def get_recent_events(self, n: int = 20) -> List[Dict]:
        """Get last N events."""
        return [e.to_dict() for e in self.pipeline[-n:]]
    
    def get_context_summary(self, max_events: int = 10) -> str:
        """Generate a text summary of recent context for LLM."""
        recent = self.get_recent_events(max_events)
        summary_lines = ["RECENT SESSION ACTIVITY:"]
        
        for event in recent:
            if event['type'] == 'file_created':
                summary_lines.append(f"- Created: {event.get('path', 'unknown')}")
            elif event['type'] == 'file_modified':
                summary_lines.append(f"- Modified: {event.get('path', 'unknown')}")
            elif event['type'] == 'terminal_command':
                cmd = event.get('command', 'unknown')
                summary_lines.append(f"- Ran: {cmd[:60]}...")
            elif event['type'] == 'user_message':
                content = event.get('content', '')
                summary_lines.append(f"- User: {content[:50]}...")
            elif event['type'] == 'validation':
                success = event.get('success', False)
                status = "✓" if success else "✗"
                summary_lines.append(f"- {status} Validation: {event.get('feedback', '')[:40]}")
        
        return "\n".join(summary_lines)
    
    def get_files_created(self) -> List[str]:
        """Get all files created in this session."""
        return [
            event.data.get('path')
            for event in self.pipeline
            if event.type == 'file_created' and event.data.get('path')
        ]
    
    def get_last_created_file(self) -> Optional[str]:
        """Get the most recently created file."""
        files = self.get_files_created()
        return files[-1] if files else None
