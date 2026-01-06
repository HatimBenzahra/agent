#!/usr/bin/env python3
import sys
import os

# Ajoute les répertoires au path Python
sys.path.append(os.path.dirname(__file__))

from agent.orchestrator import OrchestratorAgent
from tools.terminal import TerminalTool

def main():
    if len(sys.argv) < 2:
        print("Usage: python local-run.py \"votre tâche ici\"")
        print("Exemple: python local-run.py \"crée un programme C qui calcule des nombres premiers\"")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    agent = OrchestratorAgent()
    
    print(f"🎺 Agent Orchestrateur - Mode Local")
    print(f"📋 Tâche: {task}")
    print("\n" + "="*60)
    
    plan = agent.generate_orchestrated_plan(task)
    print(plan)

if __name__ == "__main__":
    main()