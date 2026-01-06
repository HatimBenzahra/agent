#!/usr/bin/env python3
import sys
import os

# Ajoute les répertoires au path Python
sys.path.append(os.path.dirname(__file__))

from agent.orchestrator import OrchestratorAgent
from tools.terminal import TerminalTool
import re
import json
import requests

class ContainerAgent:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.terminal = TerminalTool()
        
    def extract_and_execute_commands(self, plan_text):
        """Extrait les commandes du plan et les exécute"""
        lines = plan_text.split('\n')
        execution_log = []
        
        print("\n🚀 EXÉCUTION DES COMMANDES TERMINALES:")
        print("=" * 60)
        
        current_step = ""
        for line in lines:
            line = line.strip()
            
            # Nouvelle étape
            if line.startswith('📍 ÉTAPE'):
                current_step = line
            
            # Commandes terminales
            elif line.startswith('- Commandes terminales :'):
                commands_text = line.replace('- Commandes terminales :', '').strip()
                if commands_text and commands_text != '[liste des commandes exactes à exécuter]':
                    # Extraire les commandes entre crochets ou séparées par des virgules
                    commands = re.findall(r'`([^`]+)`|\"([^\"]+)\"|\'([^\']+)\'', commands_text)
                    commands = [cmd for group in commands for cmd in group if cmd]
                    
                    if not commands:
                        # Tentative de parser manuellement
                        commands = [cmd.strip() for cmd in commands_text.split(',') if cmd.strip()]
                    
                    for cmd in commands:
                        print(f"\n📋 {current_step}")
                        print(f"⚡ Exécution: {cmd}")
                        
                        # Nettoyer et préparer la commande
                        clean_cmd = cmd.strip()
                        if clean_cmd.startswith(('#', '//')):
                            continue  # Skip comments
                        
                        # Exécuter la commande
                        result = self.terminal.execute_command(clean_cmd, timeout=30)
                        
                        print(f"🔄 Résultat: {'✅ Succès' if result['success'] else '❌ Erreur'}")
                        if result['stdout']:
                            print(f"📤 Sortie: {result['stdout'][:200]}{'...' if len(result['stdout']) > 200 else ''}")
                        if result['stderr']:
                            print(f"⚠️  Erreur: {result['stderr'][:200]}{'...' if len(result['stderr']) > 200 else ''}")
                        
                        execution_log.append({
                            'step': current_step,
                            'command': clean_cmd,
                            'result': result
                        })
        
        return execution_log
    
    def execute_agent_task(self, agent_type, task_description):
        """Exécute une tâche spécifique avec un agent spécialisé"""
        agent = self.orchestrator.agents[agent_type]
        
        print(f"\n🤖 Appel à {agent['name']} ({agent['model']})")
        print(f"📝 Tâche: {task_description}")
        
        # Construction du prompt pour l'agent spécialisé
        prompt = f"""En tant que {agent['name'].lower()}, expert en {agent['description'].lower()}, exécute la tâche suivante :

Tâche : {task_description}

Tu as accès au terminal. Génère le code/contenu nécessaire et précise les commandes à exécuter.

Réponds avec :
1. Le code/contenu à créer
2. Les commandes terminales exactes à exécuter

Format :
CODE :
[code ou contenu]

COMMANDES :
[liste des commandes]"""
        
        payload = {
            "model": agent['model'],
            "prompt": prompt
        }
        
        try:
            response = requests.post(self.orchestrator.api_url, json=payload, timeout=60, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if data.get("response"):
                            full_response += data["response"]
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
            
            return self.parse_and_execute_agent_response(full_response)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'appel à {agent['name']}: {e}")
            return None
    
    def parse_and_execute_agent_response(self, response):
        """Parse la réponse de l'agent et exécute les commandes"""
        if not response:
            return None
        
        print(f"🔍 Réponse brute de l'agent:\n{response[:500]}...")
        
        # Extraire le contenu markdown/fichier
        content_patterns = [
            r'```markdown\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'CODE\s*:\s*(.*?)(?=COMMANDES|$)',
        ]
        
        content = ""
        for pattern in content_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                print(f"📝 Contenu généré:\n{content[:300]}{'...' if len(content) > 300 else ''}")
                break
        
        # Détecter le type de fichier et le nom
        filename = "generated_content.txt"
        if "react" in response.lower() or "résumé" in response.lower():
            filename = "react-summary.md"
        elif ".py" in response:
            filename = "script.py"
        elif ".c" in response:
            filename = "program.c"
        
        # Écrire le contenu
        if content:
            write_result = self.terminal.write_file(filename, content)
            if write_result['success']:
                print(f"💾 Fichier créé: {write_result['message']}")
        
        # Extraire les commandes de plusieurs manières
        commands = []
        
        # Pattern 1: Section COMMANDES
        commands_match = re.search(r'COMMANDES\s*:?\s*\n(.*?)(?=\n\n|\Z)', response, re.DOTALL | re.IGNORECASE)
        if commands_match:
            commands_text = commands_match.group(1)
            commands.extend([cmd.strip() for cmd in commands_text.split('\n') if cmd.strip()])
        
        # Pattern 2: Commandes dans des backticks
        backtick_commands = re.findall(r'`([^`]+)`', response)
        commands.extend(backtick_commands)
        
        # Pattern 3: Commandes évidentes pour PDF
        if "pdf" in response.lower() and "pandoc" in response.lower():
            if filename.endswith('.md'):
                commands.append(f"pandoc {filename} -o {filename.replace('.md', '.pdf')}")
        
        # Nettoyer et exécuter les commandes
        for cmd in commands:
            cmd = cmd.strip()
            
            # Ignorer les non-commandes
            if not cmd or cmd.startswith('#') or cmd.startswith('//') or len(cmd) < 3:
                continue
                
            # Nettoyer les artefacts
            cmd = re.sub(r'^[\*\-\+]?\s*', '', cmd)  # Enlever les listes
            cmd = re.sub(r'```[a-z]*\s*$', '', cmd)  # Enlever les fin de code block
            
            if cmd:
                print(f"⚡ Exécution: {cmd}")
                result = self.terminal.execute_command(cmd, timeout=60)
                print(f"🔄 {'✅ Succès' if result['success'] else '❌ Erreur'}")
                if result['stdout']:
                    print(f"📤 {result['stdout'][:200]}{'...' if len(result['stdout']) > 200 else ''}")
                if result['stderr']:
                    print(f"⚠️  {result['stderr'][:200]}{'...' if len(result['stderr']) > 200 else ''}")
        
        return response
    
    def execute_with_terminal(self, task):
        """Exécute une tâche complète avec accès terminal actif"""
        print(f"🎺 Agent Orchestrateur - Mode Terminal Actif")
        print(f"📋 Tâche: {task}")
        print(f"🖥️  Environnement: Container Docker isolé")
        print(f"💾 Workspace: {self.terminal.workspace}")
        print(f"🌐 API Endpoint: {self.orchestrator.api_url}")
        print("\n" + "="*60)
        
        # Étape 1: Générer le plan orchestré
        print("📊 GÉNÉRATION DU PLAN ORCHESTRÉ...")
        plan = self.orchestrator.generate_orchestrated_plan(task)
        print(plan)
        
        # Étape 2: Extraire et exécuter les commandes du plan
        execution_log = self.extract_and_execute_commands(plan)
        
        # Étape 3: Pour chaque étape majeure, appeler l'agent spécialisé
        print("\n🤖 EXÉCUTION PAR AGENTS SPÉCIALISÉS:")
        print("=" * 60)
        
        # Parser les étapes et exécuter avec les agents appropriés
        lines = plan.split('\n')
        current_step_info = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('📍 ÉTAPE'):
                # Sauvegarder l'info de l'étape
                current_step_info = {'title': line}
                
            elif line.startswith('📝 Description :'):
                current_step_info['description'] = line.replace('📝 Description :', '').strip()
                
            elif line.startswith('🤖 Agent assigné :'):
                agent_name = line.replace('🤖 Agent assigné :', '').strip()
                
                # Trouver le type d'agent
                agent_type = None
                for atype, info in self.orchestrator.agents.items():
                    if info['name'] == agent_name:
                        agent_type = atype
                        break
                
                if agent_type and current_step_info.get('description'):
                    # Exécuter la tâche avec l'agent spécialisé
                    self.execute_agent_task(agent_type, current_step_info['description'])
        
        # Étape 4: Afficher le workspace final
        print("\n📁 CONTENU DU WORKSPACE FINAL:")
        print("=" * 60)
        workspace_files = self.terminal.list_files()
        if workspace_files['success']:
            print(workspace_files['output'])
        
        print("\n" + "=" * 60)
        print("✅ TÂCHE TERMINÉE - Agent terminal actif opérationnel !")
        
        return plan, execution_log

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"votre tâche ici\"")
        print("Exemple: python run.py \"crée un programme C qui calcule des nombres premiers\"")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    agent = ContainerAgent()
    
    result = agent.execute_with_terminal(task)

if __name__ == "__main__":
    main()