import re
from typing import List, Tuple, Optional

class MermaidValidator:
    """Validates Mermaid.js syntax for v11.4.1 compatibility"""
    
    # Reserved keywords and patterns that cause issues
    RESERVED_KEYWORDS = {
        'graph', 'flowchart', 'subgraph', 'classDef', 'class', 'click', 
        'linkStyle', 'style', 'fill', 'stroke', 'color'
    }
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, mermaid_code: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate Mermaid code and return (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        if not mermaid_code or not mermaid_code.strip():
            self.errors.append("Empty mermaid code")
            return False, self.errors, self.warnings
        
        lines = mermaid_code.strip().split('\n')
        
        # Basic structure validation
        self._validate_diagram_type(lines)
        
        # Validate each line
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
                
            self._validate_line(line, i)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_diagram_type(self, lines: List[str]) -> None:
        """Validate that the diagram starts with a supported type"""
        valid_starts = [
            'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
            'stateDiagram', 'erDiagram', 'journey', 'gantt', 
            'pie', 'mindmap', 'timeline', 'gitGraph'
        ]
        
        first_line = lines[0].strip() if lines else ""
        if not any(first_line.startswith(start) for start in valid_starts):
            self.errors.append(f"Invalid diagram type. Must start with one of: {', '.join(valid_starts)}")
    
    def _validate_line(self, line: str, line_num: int) -> None:
        """Validate individual line syntax"""
        
        # Check for node definitions with invalid IDs
        node_pattern = r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*[\[\(]'
        if re.match(node_pattern, line):
            self._validate_node_definition(line, line_num)
        
        # Check for edge definitions
        if '-->' in line or '---' in line:
            self._validate_edge_definition(line, line_num)
        
        # Check for subgraph definitions
        if line.strip().startswith('subgraph'):
            self._validate_subgraph_definition(line, line_num)
        
        # Check for click events
        if line.strip().startswith('click'):
            self._validate_click_event(line, line_num)
    
    def _validate_node_definition(self, line: str, line_num: int) -> None:
        """Validate node ID and label syntax"""
        # Extract node ID
        match = re.match(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)', line)
        if match:
            node_id = match.group(2)
            
            # Check for reserved keywords
            if node_id.lower() in self.RESERVED_KEYWORDS:
                self.warnings.append(f"Line {line_num}: Node ID '{node_id}' is a reserved keyword")
            
            # Check for invalid characters in node ID
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', node_id):
                self.errors.append(f"Line {line_num}: Invalid node ID '{node_id}'. Use only alphanumeric characters and underscores")
        
        # Check for unquoted labels with special characters
        label_patterns = [
            r'\[([^"\]]*[^\w\s\]]+[^"\]]*)\]',  # Square brackets
            r'\(([^"\)]*[^\w\s\)]+[^"\)]*)\)',  # Round brackets
            r'\{\{([^"}\}]*[^\w\s}\}]+[^"}\}]*)\}\}',  # Double curly
        ]
        
        for pattern in label_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                if any(char in match for char in '()[]{}|"\'\\/<>'):
                    self.errors.append(f"Line {line_num}: Label '{match}' contains special characters and must be quoted")
    
    def _validate_edge_definition(self, line: str, line_num: int) -> None:
        """Validate edge syntax and labels"""
        # Check for edge labels with spaces around pipes
        if re.search(r'\|\s+"[^"]*"\s+\|', line):
            self.errors.append(f"Line {line_num}: Edge label has spaces around pipes. Use |\"label\"| instead")
        
        # Check for unquoted edge labels with special characters
        edge_label_pattern = r'\|([^"|\s][^|]*[^"|\s])\|'
        matches = re.findall(edge_label_pattern, line)
        for match in matches:
            if any(char in match for char in '()[]{}"\'/\\<>') or ' ' in match:
                self.errors.append(f"Line {line_num}: Edge label '{match}' contains special characters or spaces and must be quoted")
    
    def _validate_subgraph_definition(self, line: str, line_num: int) -> None:
        """Validate subgraph syntax"""
        # Check for class application to subgraph
        if ':::' in line and 'subgraph' in line:
            self.errors.append(f"Line {line_num}: Cannot apply classes directly to subgraph declarations")
    
    def _validate_click_event(self, line: str, line_num: int) -> None:
        """Validate click event syntax"""
        # Basic click event pattern: click NodeID "path"
        click_pattern = r'^(\s*)click\s+([A-Za-z_][A-Za-z0-9_]*)\s+"([^"]*)"'
        if not re.match(click_pattern, line.strip()):
            self.errors.append(f"Line {line_num}: Invalid click event syntax. Use: click NodeID \"path\"")

def fix_common_mermaid_issues(mermaid_code: str) -> str:
    """Automatically fix common Mermaid syntax issues"""
    
    if not mermaid_code:
        return mermaid_code
    
    # Fix spaces around edge label pipes
    mermaid_code = re.sub(r'\|\s+"([^"]*)"\s+\|', r'|"\1"|', mermaid_code)
    
    # Fix unquoted node labels with spaces (basic cases)
    mermaid_code = re.sub(r'\[([^"\]]*\s+[^"\]]*)\]', r'["\1"]', mermaid_code)
    mermaid_code = re.sub(r'\(([^"\)]*\s+[^"\)]*)\)', r'("\1")', mermaid_code)
    
    # Remove classes from subgraph declarations
    mermaid_code = re.sub(r'(subgraph\s+"[^"]*"):::[a-zA-Z_][a-zA-Z0-9_]*', r'\1', mermaid_code)
    
    return mermaid_code
