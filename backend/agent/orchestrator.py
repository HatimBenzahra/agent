#!/usr/bin/env python3
import requests
import json
import sys
import os
import re

# Ajoute le path pour importer les modèles
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
from models import MODELS, RECOMMENDED_MODELS

class OrchestratorAgent:
    def __init__(self):
        self.api_url = "http://100.68.221.26:11434/api/generate"
        self.orchestrator_model = "gpt-oss:20b"
        
        # Définition des agents spécialisés
        self.agents = {
            "code": {
                "name": "CodeAgent",
                "model": "qwen3-coder:30b",
                "description": "Spécialisé en programmation et développement"
            },
            "vision": {
                "name": "VisionAgent", 
                "model": "qwen3-vl:32b",
                "description": "Spécialisé en analyse d'images et vision"
            },
            "general": {
                "name": "GeneralAgent",
                "model": "gpt-oss:20b", 
                "description": "Agent polyvalent pour tâches générales"
            },
            "lightweight": {
                "name": "FastAgent",
                "model": "mistral:latest",
                "description": "Agent rapide pour tâches simples"
            }
        }
    
    def classify_section(self, section_text):
        """Classifie une section du plan pour choisir l'agent approprié"""
        section_lower = section_text.lower()
        
        # Code/programmation
        code_keywords = ['code', 'programme', 'développer', 'script', 'python', 'javascript', 'api', 'application', 'logiciel', 'coding', 'programming', 'fonction', 'algorithme']
        if any(keyword in section_lower for keyword in code_keywords):
            return "code"
        
        # Vision/images
        vision_keywords = ['image', 'photo', 'vision', 'visuel', 'dessin', 'graphique', 'analyse d\'image', 'traitement d\'image']
        if any(keyword in section_lower for keyword in vision_keywords):
            return "vision"
        
        # Tâches légères
        lightweight_keywords = ['simple', 'rapide', 'court', 'léger', 'basique', 'configuration', 'installation']
        if any(keyword in section_lower for keyword in lightweight_keywords):
            return "lightweight"
        
        # Par défaut : général
        return "general"
    
    def generate_orchestrated_plan(self, task):
        """Génère un plan orchestré avec agents spécialisés"""
        prompt = f"""En tant qu'agent orchestrateur expert avec accès permanent au terminal, analyse la tâche suivante et génère un plan d'action détaillé. 

Tu as accès COMPLET au terminal Linux pour :
- Installer des paquets (apt-get install)
- Créer/éditer/lire des fichiers
- Compiler du code
- Exécuter des commandes
- Faire des recherches web (curl)
- Tester des programmes

Pour chaque étape, précise les commandes terminales à exécuter.

Tâche : {task}

Réponds avec un plan structuré comme ceci :
PLAN GLOBAL : [brève description du plan]

ÉTAPE 1 : [titre de l'étape]
- Description : [description détaillée]
- Commandes terminales : [liste des commandes exactes à exécuter]
- Type de tâche : [code/vision/général/simple]
- Complexité : [faible/moyenne/élevée]

ÉTAPE 2 : [titre de l'étape]
- Description : [description détaillée]
- Commandes terminales : [liste des commandes exactes à exécuter]
- Type de tâche : [code/vision/général/simple]
- Complexité : [faible/moyenne/élevée]

[etc...]"""
        
        payload = {
            "model": self.orchestrator_model,
            "prompt": prompt
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=30, stream=True)
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
            
            # print(f"DEBUG: Réponse brute de l'API: {full_response[:500]}...")
            return self.parse_and_assign_agents(full_response) if full_response else "Erreur: pas de réponse générée"
            
        except requests.exceptions.RequestException as e:
            return f"Erreur de connexion à l'API: {e}"
    
    def parse_and_assign_agents(self, plan_text):
        """Parse le plan et assigne les agents appropriés"""
        # Nettoyer le texte pour enlever les marqueurs markdown
        plan_text = plan_text.replace('**', '').replace('###', '')
        
        # Si le plan ne contient pas le format attendu, créer un plan simple
        if not plan_text or 'ÉTAPE' not in plan_text and 'ETAPE' not in plan_text:
            return self.create_simple_plan(plan_text)
        
        lines = plan_text.split('\n')
        orchestrated_plan = []
        current_step = {}
        
        for line in lines:
            line = line.strip()
            
            # Détection d'une nouvelle étape
            if line.startswith('ÉTAPE') or line.startswith('ETAPE'):
                if current_step:
                    # Assigner un agent à l'étape précédente
                    agent_type = self.classify_section(current_step.get('description', ''))
                    current_step['agent'] = self.agents[agent_type]
                    orchestrated_plan.append(current_step)
                
                # Nouvelle étape
                step_match = re.match(r'(?:ÉTAPE|ETAPE)\s+(\d+)\s*[:\-]\s*(.+)', line)
                if step_match:
                    current_step = {
                        'step_number': int(step_match.group(1)),
                        'title': step_match.group(2),
                        'description': '',
                        'task_type': '',
                        'complexity': ''
                    }
            
            # Description
            elif line.startswith('- Description :') or line.startswith('Description :'):
                current_step['description'] = line.replace('- Description :', '').replace('Description :', '').strip()
            
            # Type de tâche
            elif line.startswith('- Type de tâche :') or line.startswith('Type de tâche :'):
                current_step['task_type'] = line.replace('- Type de tâche :', '').replace('Type de tâche :', '').strip()
            
            # Complexité
            elif line.startswith('- Complexité :') or line.startswith('Complexité :'):
                current_step['complexity'] = line.replace('- Complexité :', '').replace('Complexité :', '').strip()
        
        # Dernière étape
        if current_step:
            agent_type = self.classify_section(current_step.get('description', ''))
            current_step['agent'] = self.agents[agent_type]
            orchestrated_plan.append(current_step)
        
        return self.format_orchestrated_plan(orchestrated_plan)
    
    def create_simple_plan(self, plan_text):
        """Crée un plan orchestré simple à partir du texte brut"""
        # Découper le plan en sections logiques
        sections = []
        lines = plan_text.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                if current_section:
                    sections.append(current_section.strip())
                current_section = line
            else:
                current_section += " " + line
        
        if current_section:
            sections.append(current_section.strip())
        
        # Créer le plan orchestré
        orchestrated_plan = []
        for i, section in enumerate(sections[:5], 1):  # Limiter à 5 sections
            agent_type = self.classify_section(section)
            orchestrated_plan.append({
                'step_number': i,
                'title': f"Section {i}",
                'description': section[:100] + "..." if len(section) > 100 else section,
                'task_type': agent_type,
                'complexity': 'moyenne',
                'agent': self.agents[agent_type]
            })
        
        return self.format_orchestrated_plan(orchestrated_plan)
    
    def format_orchestrated_plan(self, orchestrated_plan):
        """Formate le plan orchestré pour l'affichage"""
        output = "🎺 PLAN ORCHESTRÉ PAR L'AGENT CHEF\n"
        output += "=" * 60 + "\n\n"
        
        for i, step in enumerate(orchestrated_plan, 1):
            agent = step.get('agent', {'name': 'Unknown', 'model': 'unknown', 'description': 'No description'})
            
            # Utiliser i comme step_number si non défini
            step_num = step.get('step_number', i)
            title = step.get('title', f"Étape {step_num}")
            description = step.get('description', 'Pas de description')
            task_type = step.get('task_type', 'général')
            complexity = step.get('complexity', 'moyenne')
            
            output += f"📍 ÉTAPE {step_num} : {title}\n"
            output += f"📝 Description : {description}\n"
            output += f"🏷️  Type : {task_type} | 📊 Complexité : {complexity}\n"
            output += f"🤖 Agent assigné : {agent['name']}\n"
            output += f"🔧 Modèle : {agent['model']}\n"
            output += f"💡 Spécialité : {agent['description']}\n"
            output += "-" * 40 + "\n\n"
        
        return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"votre tâche ici\"")
        print("Exemple: python run.py \"créer une application web avec analyse d'images\"")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    orchestrator = OrchestratorAgent()
    
    print(f"🎺 Agent Orchestrateur - Analyse de tâche")
    print(f"📋 Tâche: {task}")
    print(f"🔧 Modèle orchestrateur: gpt-oss:20b")
    print("\n" + "="*60)
    
    plan = orchestrator.generate_orchestrated_plan(task)
    print(plan)

if __name__ == "__main__":
    main()