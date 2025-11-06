"""Unit tests for FilesystemAdapter.

Tests the filesystem adapter that reads repository data and executes scripts.
"""
import pytest

from mcp_server.adapters import FilesystemAdapter


class TestFilesystemAdapter:
    """Test FilesystemAdapter class."""
    
    def test_initialization_with_default_root(self):
        """Test adapter initialization with default root."""
        adapter = FilesystemAdapter()
        assert adapter.repo_root is not None
        assert adapter.scripts_dir.name == "scripts"
        assert adapter.docs_dir.name == "docs"
        assert adapter.data_dir.name == "data"
    
    def test_initialization_with_custom_root(self, temp_repo_dir):
        """Test adapter initialization with custom root."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        assert adapter.repo_root == temp_repo_dir
        assert adapter.scripts_dir == temp_repo_dir / "scripts"
    
    def test_read_glossary_empty(self, temp_repo_dir):
        """Test reading glossary when file doesn't exist."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        entries = adapter.read_glossary()
        assert entries == []
    
    def test_read_glossary_with_content(self, temp_repo_dir, mock_glossary_file):
        """Test reading glossary with content."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        entries = adapter.read_glossary()
        
        assert len(entries) == 3
        assert entries[0].term == "Semantic Architecture"
        assert entries[0].category == "Core Concepts"
        assert "framework" in entries[0].definition.lower()
        
        assert entries[1].term == "Module"
        assert entries[2].term == "Test-Driven Development"
        assert entries[2].category == "Development Practices"
    
    def test_read_glossary_parsing(self, temp_repo_dir):
        """Test glossary parsing with various formats."""
        glossary_path = temp_repo_dir / "docs" / "glossary.md"
        glossary_content = """# Glossary

## Category One

### Term One
Definition for term one.
Continuation of definition.

### Term Two
Short definition.

## Category Two

### Term Three
Another definition here.
"""
        glossary_path.write_text(glossary_content)
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        entries = adapter.read_glossary()
        
        assert len(entries) == 3
        assert entries[0].term == "Term One"
        assert "Continuation" in entries[0].definition
        assert entries[1].category == "Category One"
        assert entries[2].category == "Category Two"
    
    def test_file_exists_true(self, temp_repo_dir):
        """Test file_exists returns True for existing file."""
        test_file = temp_repo_dir / "test.txt"
        test_file.write_text("test content")
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        assert adapter.file_exists("test.txt") is True
    
    def test_file_exists_false(self, temp_repo_dir):
        """Test file_exists returns False for non-existing file."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        assert adapter.file_exists("nonexistent.txt") is False
    
    def test_read_file_success(self, temp_repo_dir):
        """Test reading an existing file."""
        test_file = temp_repo_dir / "test.txt"
        test_content = "Test file content"
        test_file.write_text(test_content)
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        content = adapter.read_file("test.txt")
        assert content == test_content
    
    def test_read_file_not_found(self, temp_repo_dir):
        """Test reading a non-existent file raises error."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        with pytest.raises(FileNotFoundError):
            adapter.read_file("nonexistent.txt")
    
    def test_run_script_validates_script_name(self, temp_repo_dir):
        """Test that run_script validates script name to prevent path traversal."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        # Test empty script name
        with pytest.raises(RuntimeError, match="Invalid script name"):
            adapter.run_script("", [])
        
        # Test path traversal attempts
        with pytest.raises(RuntimeError, match="path traversal"):
            adapter.run_script("../etc/passwd", [])
        
        with pytest.raises(RuntimeError, match="path traversal"):
            adapter.run_script("../../malicious.py", [])
    
    def test_run_script_validates_arguments(self, temp_repo_dir):
        """Test that run_script validates arguments."""
        # Create a dummy script
        script_path = temp_repo_dir / "scripts" / "test_script.py"
        script_path.write_text('import json; print(json.dumps({"result": "ok"}))')
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        # Test invalid argument flag
        with pytest.raises(RuntimeError, match="Invalid argument flag"):
            adapter.run_script("test_script.py", ["--invalidflag", "value"])
        
        # Test invalid characters in argument value
        with pytest.raises(RuntimeError, match="Invalid characters"):
            adapter.run_script("test_script.py", ["--scope", "value;rm -rf /"])
    
    def test_run_script_nonexistent(self, temp_repo_dir):
        """Test running a non-existent script."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        with pytest.raises(RuntimeError, match="Script not found"):
            adapter.run_script("nonexistent.py", [])
    
    def test_run_script_success(self, temp_repo_dir):
        """Test successfully running a script."""
        # Create a simple script that outputs JSON
        script_path = temp_repo_dir / "scripts" / "success_script.py"
        script_content = '''#!/usr/bin/env python3
import json
import sys

result = {
    "status": "success",
    "args": sys.argv[1:]
}
print(json.dumps(result))
'''
        script_path.write_text(script_content)
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        result = adapter.run_script("success_script.py", ["--scope", "project"])
        
        assert result["status"] == "success"
        assert "--scope" in result["args"]
        assert "project" in result["args"]
    
    def test_run_script_timeout(self, temp_repo_dir):
        """Test script timeout handling."""
        # Create a script that sleeps longer than timeout
        script_path = temp_repo_dir / "scripts" / "slow_script.py"
        script_content = '''#!/usr/bin/env python3
import time
time.sleep(60)
'''
        script_path.write_text(script_content)
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        with pytest.raises(RuntimeError, match="timed out"):
            adapter.run_script("slow_script.py", [])
    
    def test_run_script_json_decode_error(self, temp_repo_dir):
        """Test handling of invalid JSON output."""
        script_path = temp_repo_dir / "scripts" / "bad_json.py"
        script_content = '''#!/usr/bin/env python3
print("This is not JSON")
'''
        script_path.write_text(script_content)
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        with pytest.raises(RuntimeError, match="Failed to parse"):
            adapter.run_script("bad_json.py", [])


class TestFilesystemAdapterSecurity:
    """Security-focused tests for FilesystemAdapter."""
    
    def test_argument_sanitization_allowed_flags(self, temp_repo_dir):
        """Test that only allowed argument flags are accepted."""
        script_path = temp_repo_dir / "scripts" / "test.py"
        script_path.write_text('import json; print(json.dumps({"ok": True}))')
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        # Valid flags should work
        result = adapter.run_script("test.py", ["--scope", "project"])
        assert result["ok"] is True
        
        # Invalid flags should be rejected
        with pytest.raises(RuntimeError, match="Invalid argument flag"):
            adapter.run_script("test.py", ["--malicious", "value"])
    
    def test_argument_sanitization_special_chars(self, temp_repo_dir):
        """Test that special characters in arguments are rejected."""
        script_path = temp_repo_dir / "scripts" / "test.py"
        script_path.write_text('import json; print(json.dumps({"ok": True}))')
        
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        # Test various shell metacharacters
        dangerous_inputs = [
            "value; rm -rf /",
            "value && echo hacked",
            "value | cat /etc/passwd",
            "value > /tmp/hack",
            "value$(whoami)",
            "value`whoami`",
        ]
        
        for dangerous in dangerous_inputs:
            with pytest.raises(RuntimeError, match="Invalid characters"):
                adapter.run_script("test.py", ["--scope", dangerous])
    
    def test_path_traversal_prevention(self, temp_repo_dir):
        """Test that path traversal attempts are blocked."""
        adapter = FilesystemAdapter(repo_root=str(temp_repo_dir))
        
        traversal_attempts = [
            "../../../etc/passwd",
            "..%2F..%2Fetc%2Fpasswd",
            "scripts/../../../etc/passwd",
        ]
        
        for attempt in traversal_attempts:
            with pytest.raises(RuntimeError):
                adapter.run_script(attempt, [])
