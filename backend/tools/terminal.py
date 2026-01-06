#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

class TerminalTool:
    def __init__(self):
        self.workspace = "/workspace"
        self.ensure_workspace()
    
    def ensure_workspace(self):
        """Crée le workspace s'il n'existe pas"""
        Path(self.workspace).mkdir(parents=True, exist_ok=True)
        # Change le propriétaire pour éviter les problèmes de permissions
        import pwd
        try:
            uid = pwd.getpwnam('root').pw_uid
            gid = pwd.getpwnam('root').pw_gid
            os.chown(self.workspace, uid, gid)
        except:
            pass
    
    def execute_command(self, command, timeout=30):
        """Exécute une commande dans le workspace"""
        try:
            # Change directory to workspace
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Commande timeout après {timeout} secondes",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Erreur: {str(e)}",
                "return_code": -1
            }
    
    def list_files(self, path="."):
        """Liste les fichiers dans le workspace"""
        full_path = os.path.join(self.workspace, path)
        try:
            result = subprocess.run(
                ["ls", "-la", full_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Erreur: {str(e)}"
            }
    
    def read_file(self, filepath):
        """Lit un fichier dans le workspace"""
        full_path = os.path.join(self.workspace, filepath)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "success": True,
                "content": content
            }
        except Exception as e:
            return {
                "success": False,
                "content": f"Erreur: {str(e)}"
            }
    
    def write_file(self, filepath, content):
        """Écrit un fichier dans le workspace"""
        full_path = os.path.join(self.workspace, filepath)
        try:
            # Crée les répertoires si nécessaire
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "success": True,
                "message": f"Fichier écrit: {full_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur: {str(e)}"
            }