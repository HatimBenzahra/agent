"""
Context Manager - Intelligent context retrieval for the agent.
Analyzes user requests to fetch relevant files, history, and system state.
"""

from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass
from openai import AsyncOpenAI
from app.agents.sandbox import Sandbox
from app.agents.chat_history import chat_history_manager

@dataclass
class RetrievedContext:
    files: List[Dict[str, str]]  # list of {path: ..., content: ...}
    relevant_history: List[Dict[str, str]]
    summary: str
    recent_actions: Dict[str, Any] = None  # NEW: Track recent file operations

class AdvancedContextManager:
    """
    Intelligently retrieves context based on user query.
    1. Analyzes query to find referenced files/topics.
    2. Searches workspace for matching files.
    3. Retrieves relevant chat history.
    """

    def __init__(self, client: AsyncOpenAI, model: str, sandbox: Sandbox, project_id: str):
        self.client = client
        self.model = model
        self.sandbox = sandbox
        self.project_id = project_id

    async def retrieve_context(self, user_input: str, messages: List[Dict] = None, pipeline=None) -> RetrievedContext:
        """
        Analyze input and retrieve necessary context.
        """
        # Load messages if not provided
        if messages is None:
            messages = chat_history_manager.load(self.project_id)
        
        # 1. Extract recent actions from conversation history
        recent_actions = self._extract_recent_actions(messages[-5:])
        
        # 2. Resolve references (e.g., "le" -> most recent file)
        resolved_files = self._resolve_references(user_input, recent_actions)
        
        # 3. Analyze Intent & targets
        analysis = await self._analyze_requirements(user_input, recent_actions)
        
        # 4. Fetch Files (prioritize resolved references)
        files_content = []
        if resolved_files or analysis.get('needs_files'):
            files_content = self._fetch_relevant_files(
                patterns=analysis.get('file_patterns', []),
                priority_files=resolved_files
            )
            
        # 5. Retrieve History (Last N + relevant)
        relevant_history = messages[-10:]
        
        # 6. Get pipeline summary if available
        pipeline_summary = ""
        if pipeline:
            pipeline_summary = pipeline.get_context_summary()
        
        return RetrievedContext(
            files=files_content,
            relevant_history=relevant_history,
            summary=analysis.get('reasoning', '') + "\n\n" + pipeline_summary,
            recent_actions=recent_actions
        )

    async def _analyze_requirements(self, user_input: str, recent_actions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask LLM what context is needed for this request.
        """
        recent_context = ""
        if recent_actions and recent_actions.get('files_created'):
            recent_context = f"\n\nRECENT FILES CREATED: {', '.join(recent_actions['files_created'])}"
        
        prompt = f"""Analyze this user request: "{user_input}"{recent_context}
        
        Return JSON with:
        - needs_files: bool (does it refer to code, pdfs, text files?)
        - file_patterns: list[str] (names or patterns of files to look for, e.g. ["*.pdf", "main.py"])
        - reasoning: str (why)
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except:
            return {"needs_files": True, "file_patterns": ["*"], "reasoning": "Fallback"}

    def _extract_recent_actions(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        Extract files created/modified from recent assistant messages.
        """
        files_created = []
        files_modified = []
        primary_output = None
        
        for msg in reversed(messages):  # Most recent first
            if msg.get('role') == 'assistant':
                metadata = msg.get('metadata', {})
                if metadata:
                    files_created.extend(metadata.get('files_created', []))
                    files_modified.extend(metadata.get('files_modified', []))
                    if not primary_output and metadata.get('primary_output'):
                        primary_output = metadata['primary_output']
        
        return {
            'files_created': files_created,
            'files_modified': files_modified,
            'primary_output': primary_output or (files_created[0] if files_created else None)
        }
    
    def _resolve_references(self, user_input: str, recent_actions: Dict[str, Any]) -> List[str]:
        """
        Resolve pronouns and references to specific files.
        Examples: "améliore le" -> most recent file, "fix it" -> last modified file
        """
        pronouns = ["le", "la", "it", "that", "this", "celui", "celle", "l'", "les"]
        user_lower = user_input.lower()
        
        # Check if user is using a pronoun/reference
        if any(f" {p} " in f" {user_lower} " or user_lower.startswith(f"{p} ") for p in pronouns):
            # Return most recent file (created or modified)
            if recent_actions.get('primary_output'):
                return [recent_actions['primary_output']]
            elif recent_actions.get('files_created'):
                return [recent_actions['files_created'][-1]]  # Most recent
            elif recent_actions.get('files_modified'):
                return [recent_actions['files_modified'][-1]]
        
        return []
    
    def _fetch_relevant_files(self, patterns: List[str], priority_files: List[str] = None) -> List[Dict[str, str]]:
        """
        Find and read files matching patterns. Prioritize specific files if provided.
        """
        all_files = self.sandbox.list_files(".")
        matches = []
        
        # First, fetch priority files (from reference resolution)
        if priority_files:
            for priority_path in priority_files:
                for f in all_files:
                    if f.is_dir:
                        continue
                    if f.path == priority_path or f.name == priority_path:
                        success, content = self.sandbox.read_file(f.path)
                        if success:
                            matches.append({
                                "path": f.path,
                                "content": content[:5000] + ("...[truncated]" if len(content) > 5000 else "")
                            })
                        break
            # If we found priority files, return them
            if matches:
                return matches
        
        # Simple heuristic matching
        # If pattern is "*", get all text files (limit size)
        # If pattern is specific (e.g. "pdf"), filter
        
        for f in all_files:
            if f.is_dir: continue
            
            # Read logic
            is_match = False
            if "*" in patterns:
                is_match = True
            else:
                for p in patterns:
                    if p.replace("*", "") in f.name:
                        is_match = True
                        break
            
            if is_match:
                # Read content (truncate if too large)
                success, content = self.sandbox.read_file(f.path)
                if success:
                    matches.append({
                        "path": f.path,
                        "content": content[:5000] + ("...[truncated]" if len(content) > 5000 else "")
                    })
        
        return matches
