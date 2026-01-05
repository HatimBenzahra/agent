import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SubAgent:
    def __init__(self, role, topic):
        """
        Initializes a specialized sub-agent.
        Args:
            role (str): The specific role (e.g., "Python Coder", "Content Writer").
            topic (str): The specific topic or context this agent is working on.
        """
        self.role = role
        self.topic = topic
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def run(self, task, context=None):
        """
        Executes a specific task.
        Args:
            task (str): The specific step/task description.
            context (str, optional): The result of previous steps or overall plan context.
        """
        system_prompt = (
            f"You are a specialized expert: {self.role}.\n"
            f"Your current focus is: {self.topic}.\n"
            "Perform the user's task accurately and concisely."
        )

        user_content = f"Task: {task}"
        if context:
            user_content += f"\n\nContext/Previous Results:\n{context}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"SubAgent Error: {e}"
