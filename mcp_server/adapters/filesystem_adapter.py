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
        # Validate script name to prevent path traversal using Path.resolve()
        if not script_name:
            raise RuntimeError(f"Invalid script name: {script_name}")
        
        script_path = (self.scripts_dir / script_name).resolve()
        scripts_dir_resolved = self.scripts_dir.resolve()
        # Ensure the resolved script_path is within the scripts directory
        try:
            script_path.relative_to(scripts_dir_resolved)
        except ValueError:
            raise RuntimeError(f"Script path traversal detected: {script_name}")
        
        if not script_path.exists():
            raise RuntimeError(f"Script not found: {script_path}")
        
        # Validate and sanitize arguments
        sanitized_args = []
        allowed_arg_prefixes = ['--scope', '--ids', '--include', '--edgeTypes', '--outputFormat', 
                                '--filters', '--version', '--targets', '--ruleset', '--fixMode',
                                '--baseRef', '--headRef', '--threshold', '--scopes', 
                                '--includeDiffSummary', '--root', '--patterns']
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            # Check if it's a flag
            if arg.startswith('--'):
                if arg not in allowed_arg_prefixes:
                    raise RuntimeError(f"Invalid argument flag: {arg}")
                sanitized_args.append(arg)
                i += 1
                
                # Get the value for this flag if it exists
                if i < len(args) and not args[i].startswith('--'):
                    value = args[i]
                    # Whitelist: allow only alphanumeric, dash, underscore, dot, forward slash, and colon
                    if not re.fullmatch(r'^[\w\-/.,:]+$', value):
                        raise RuntimeError(f"Invalid characters in argument value: {value}")
                    sanitized_args.append(value)
                    i += 1
            else:
                # Standalone value (not preceded by a flag)
                # Whitelist: allow only alphanumeric, dash, underscore, dot, forward slash, and colon
                if not re.fullmatch(r'^[\w\-/.,:]+$', arg):
                    raise RuntimeError(f"Invalid characters in argument: {arg}")
                sanitized_args.append(arg)
                i += 1
        
        try:
            # Security note: Arguments are sanitized above through:
            # 1. Script name validation (no path traversal)
            # 2. Argument flag whitelist
            # 3. Shell metacharacter filtering
            # 4. Using list form (not shell=True) prevents shell injection
            # CodeQL may flag this as command injection, but it's mitigated by comprehensive
            # input validation above. All user input is sanitized before reaching subprocess.
            result = subprocess.run(
                ["python3", str(script_path)] + sanitized_args,
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
        
        Expected format of docs/glossary.md:
            - Categories are indicated by Markdown headings (e.g., '## CategoryName').
            - Each glossary term is indicated by a subheading (e.g., '### Term').
            - The definition for a term follows the term line, and may span multiple lines 
              until the next term or category.
            - Blank lines are ignored.
        
        Parsing logic:
            - The method iterates through each line, tracking the current category and term.
            - When a new category or term is encountered, the previous entry is saved.
            - Definitions are accumulated for each term until a new term or category is found.
        
        Behavior when file does not exist:
            - If docs/glossary.md is missing, the method returns an empty list.
        
        Returns:
            List of GlossaryEntry objects, each containing term, definition, and category.
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
