"""
Context Manager - Intelligent context retrieval for the agent.
Analyzes user requests to fetch relevant files, history, and system state.
"""

from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass
from openai import OpenAI
from app.agents.sandbox import Sandbox
from app.agents.chat_history import chat_history_manager

@dataclass
class RetrievedContext:
    files: List[Dict[str, str]]  # list of {path: ..., content: ...}
    relevant_history: List[Dict[str, str]]
    summary: str

class AdvancedContextManager:
    """
    Intelligently retrieves context based on user query.
    1. Analyzes query to find referenced files/topics.
    2. Searches workspace for matching files.
    3. Retrieves relevant chat history.
    """

    def __init__(self, client: OpenAI, model: str, sandbox: Sandbox, project_id: str):
        self.client = client
        self.model = model
        self.sandbox = sandbox
        self.project_id = project_id

    async def retrieve_context(self, user_input: str) -> RetrievedContext:
        """
        Analyze input and retrieve necessary context.
        """
        
        # 1. Analyze Intent & targets
        analysis = await self._analyze_requirements(user_input)
        
        # 2. Fetch Files
        files_content = []
        if analysis.get('needs_files'):
            files_content = self._fetch_relevant_files(analysis.get('file_patterns', []))
            
        # 3. Retrieve History (Last N + relevant)
        history = chat_history_manager.load(self.project_id)
        relevant_history = history[-10:] # Simple sliding window for now, can be semantic later
        
        return RetrievedContext(
            files=files_content,
            relevant_history=relevant_history,
            summary=analysis.get('reasoning', '')
        )

    async def _analyze_requirements(self, user_input: str) -> Dict[str, Any]:
        """
        Ask LLM what context is needed for this request.
        """
        prompt = f"""Analyze this user request: "{user_input}"
        
        Return JSON with:
        - needs_files: bool (does it refer to code, pdfs, text files?)
        - file_patterns: list[str] (names or patterns of files to look for, e.g. ["*.pdf", "main.py"])
        - reasoning: str (why)
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except:
            return {"needs_files": True, "file_patterns": ["*"], "reasoning": "Fallback"}

    def _fetch_relevant_files(self, patterns: List[str]) -> List[Dict[str, str]]:
        """
        Find and read files matching patterns.
        """
        all_files = self.sandbox.list_files(".")
        matches = []
        
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
