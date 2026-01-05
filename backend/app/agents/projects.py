"""
Projects module - Manages project metadata and persistence.
"""

import json
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

# Projects database file
PROJECTS_FILE = Path(__file__).parent.parent / "data" / "projects.json"


@dataclass
class Project:
    """Project metadata."""
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str
    status: str  # 'active', 'archived', 'deleted'

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        return cls(**data)


class ProjectManager:
    """Manages project CRUD operations."""

    def __init__(self):
        self.projects: dict[str, Project] = {}
        self._load()

    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    def _load(self):
        """Load projects from disk."""
        self._ensure_data_dir()
        if PROJECTS_FILE.exists():
            try:
                data = json.loads(PROJECTS_FILE.read_text())
                self.projects = {
                    pid: Project.from_dict(pdata)
                    for pid, pdata in data.items()
                }
            except Exception:
                self.projects = {}

    def _save(self):
        """Save projects to disk."""
        self._ensure_data_dir()
        data = {pid: p.to_dict() for pid, p in self.projects.items()}
        PROJECTS_FILE.write_text(json.dumps(data, indent=2))

    def create(self, name: str, description: str = "") -> Project:
        """Create a new project."""
        project_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()

        project = Project(
            id=project_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            status='active'
        )

        self.projects[project_id] = project
        self._save()

        return project

    def get(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.projects.get(project_id)

    def update(self, project_id: str, name: str = None, description: str = None) -> Optional[Project]:
        """Update a project."""
        project = self.projects.get(project_id)
        if not project:
            return None

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description

        project.updated_at = datetime.now().isoformat()
        self._save()

        return project

    def delete(self, project_id: str) -> bool:
        """Delete a project (soft delete)."""
        project = self.projects.get(project_id)
        if not project:
            return False

        project.status = 'deleted'
        project.updated_at = datetime.now().isoformat()
        self._save()

        return True

    def hard_delete(self, project_id: str) -> bool:
        """Permanently delete a project."""
        if project_id in self.projects:
            del self.projects[project_id]
            self._save()
            return True
        return False

    def list_all(self, include_deleted: bool = False) -> list[Project]:
        """List all projects."""
        projects = list(self.projects.values())
        if not include_deleted:
            projects = [p for p in projects if p.status != 'deleted']
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)

    def get_active(self) -> list[Project]:
        """Get only active projects."""
        return [p for p in self.projects.values() if p.status == 'active']


# Global project manager instance
project_manager = ProjectManager()
