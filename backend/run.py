#!/usr/bin/env python3
"""
Setup script pour lancer l'agent IA
"""

import sys
import os

# Ajoute les répertoires au path Python
sys.path.append(os.path.dirname(__file__))

from agent.orchestrator import OrchestratorAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"votre tâche ici\"")
        print("Exemple: python run.py \"créer une application web de gestion de tâches\"")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    orchestrator = OrchestratorAgent()
    
    print(f"🎺 Agent Orchestrateur - Analyse de tâche")
    print(f"📋 Tâche: {task}")
    print(f"🔧 Modèle orchestrateur: gpt-oss:20b")
    print("\n" + "="*60)
    
    plan = orchestrator.generate_orchestrated_plan(task)
    print(plan)
    print("="*50)

if __name__ == "__main__":
    main()