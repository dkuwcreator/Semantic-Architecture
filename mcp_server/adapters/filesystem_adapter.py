"""Filesystem adapter for accessing local repository data."""
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..models import GlossaryEntry


class FilesystemAdapter:
    """Adapter for reading repository files and executing scripts."""
    
    def __init__(self, repo_root: Optional[str] = None):
        """Initialize the filesystem adapter.
        
        Args:
            repo_root: Root directory of the repository. Defaults to current directory.
        """
        self.repo_root = Path(repo_root or os.getcwd())
        self.scripts_dir = self.repo_root / "scripts"
        self.docs_dir = self.repo_root / "docs"
        self.data_dir = self.repo_root / "data"
    
    def run_script(self, script_name: str, args: List[str]) -> Dict[str, Any]:
        """Run a Python script and return parsed JSON output.
        
        Args:
            script_name: Name of the script file (e.g., 'semantic_graph.py')
            args: List of command-line arguments
            
        Returns:
            Parsed JSON output from the script
            
        Raises:
            RuntimeError: If script execution fails
        """
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            raise RuntimeError(f"Script not found: {script_path}")
        
        try:
            result = subprocess.run(
                ["python3", str(script_path)] + args,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Script execution failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse script output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Script execution timed out")
    
    def read_glossary(self) -> List[GlossaryEntry]:
        """Parse and return glossary entries from docs/glossary.md.
        
        Returns:
            List of glossary entries
        """
        glossary_path = self.docs_dir / "glossary.md"
        if not glossary_path.exists():
            return []
        
        entries = []
        current_category = None
        current_term = None
        current_def_lines = []
        
        with open(glossary_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                
                # Category header (## Core Concepts)
                if line.startswith("## "):
                    # Save previous entry if exists
                    if current_term and current_def_lines:
                        entries.append(GlossaryEntry(
                            term=current_term,
                            definition=" ".join(current_def_lines).strip(),
                            category=current_category
                        ))
                    current_category = line.lstrip("#").strip()
                    current_term = None
                    current_def_lines = []
                
                # Term header (### Semantic Architecture)
                elif line.startswith("### "):
                    # Save previous entry if exists
                    if current_term and current_def_lines:
                        entries.append(GlossaryEntry(
                            term=current_term,
                            definition=" ".join(current_def_lines).strip(),
                            category=current_category
                        ))
                    current_term = line.lstrip("#").strip()
                    current_def_lines = []
                
                # Definition line
                elif current_term and line and not line.startswith("#"):
                    current_def_lines.append(line)
        
        # Save last entry
        if current_term and current_def_lines:
            entries.append(GlossaryEntry(
                term=current_term,
                definition=" ".join(current_def_lines).strip(),
                category=current_category
            ))
        
        return entries
    
    def read_file(self, relative_path: str) -> str:
        """Read a file from the repository.
        
        Args:
            relative_path: Path relative to repository root
            
        Returns:
            File contents as string
        """
        file_path = self.repo_root / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def file_exists(self, relative_path: str) -> bool:
        """Check if a file exists in the repository.
        
        Args:
            relative_path: Path relative to repository root
            
        Returns:
            True if file exists
        """
        return (self.repo_root / relative_path).exists()
