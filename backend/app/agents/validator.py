"""
Validator module - Evaluates sub-agent task completion.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""
    success: bool
    feedback: str
    confidence: float  # 0.0 to 1.0


class TaskValidator:
    """
    Validates if a sub-agent's output matches the expected task objective.
    """
    
    def __init__(self, llm_client, model: str):
        """
        Args:
            llm_client: OpenAI client for validation queries
            model: Model to use for validation
        """
        self.client = llm_client
        self.model = model
    
    async def validate(
        self,
        task_objective: str,
        task_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate if a task was completed successfully.
        
        Args:
            task_objective: What the task was supposed to accomplish
            task_result: The actual result from the sub-agent
            context: Additional context (files created, terminal output, etc.)
            
        Returns:
            ValidationResult with success status and feedback
        """
        
        # Build validation prompt
        validation_prompt = f"""You are a task validator. Your job is to determine if a task was completed successfully.

TASK OBJECTIVE:
{task_objective}

ACTUAL RESULT:
{self._format_result(task_result)}

CONTEXT:
{self._format_context(context)}

Evaluate if the task objective was achieved. Consider:
1. Were the required files created/modified?
2. Did commands execute successfully?
3. Is the output consistent with the objective?
4. Are there any errors or issues?

Respond in this exact format:
SUCCESS: [yes/no]
CONFIDENCE: [0.0-1.0]
FEEDBACK: [brief explanation]
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise task validator. Be concise and objective."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.1  # Low temperature for consistent validation
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_validation_response(content)
            
        except Exception as e:
            return ValidationResult(
                success=False,
                feedback=f"Validation failed: {str(e)}",
                confidence=0.0
            )
    
    def _format_result(self, result: Dict[str, Any]) -> str:
        """Format task result for validation prompt."""
        parts = []
        
        if "tools_used" in result:
            parts.append(f"Tools Used: {', '.join(result['tools_used'])}")
        
        if "output" in result:
            parts.append(f"Output: {result['output']}")
        
        if "error" in result:
            parts.append(f"Error: {result['error']}")
        
        return "\n".join(parts) if parts else "No result data"
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context for validation prompt."""
        parts = []
        
        if "files_created" in context:
            parts.append(f"Files Created: {', '.join(context['files_created'])}")
        
        if "files_modified" in context:
            parts.append(f"Files Modified: {', '.join(context['files_modified'])}")
        
        if "terminal_output" in context:
            parts.append(f"Terminal Output: {context['terminal_output'][:200]}...")
        
        return "\n".join(parts) if parts else "No context data"
    
    def _parse_validation_response(self, content: str) -> ValidationResult:
        """Parse the LLM's validation response."""
        lines = content.strip().split("\n")
        
        success = False
        confidence = 0.5
        feedback = "Unable to parse validation response"
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("SUCCESS:"):
                success_str = line.split(":", 1)[1].strip().lower()
                success = success_str in ["yes", "true", "1"]
            
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                    confidence = max(0.0, min(1.0, confidence))
                except:
                    confidence = 0.5
            
            elif line.startswith("FEEDBACK:"):
                feedback = line.split(":", 1)[1].strip()
        
        return ValidationResult(
            success=success,
            feedback=feedback,
            confidence=confidence
        )
