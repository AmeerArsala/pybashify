from typing import Optional
from pydantic import BaseModel, Field


class BashifyDeclaration(BaseModel):
    line: str
    idx: int
    
    # Filled later
    module_name: str = ""

    def fill(self, prefix: str = ""):
        line_nospaces: str = self.line.replace(" ", "")
        offset: int = 1 if len(prefix) > 0 else 0  # for the '.' in the prefix
        declaration_len: int = len(f"declare{prefix}") + offset
        
        self.module_name = line_nospaces[declaration_len:]
    
    def as_import(self, prefix: str = "") -> str:
        # +1 for the '.' in the prefix
        offset: int = 1 if len(prefix) > 0 else 0
        unprefixed_module_name: str = self.module_name[len(prefix)+offset:]
        
        if True or '.' not in unprefixed_module_name:
            return f"import {unprefixed_module_name}"
        
        # last_dot_idx: int = unprefixed_module_name.rindex('.')
        # parent: str = unprefixed_module_name[:last_dot_idx]
        # child: str = unprefixed_module_name[last_dot_idx+1:]
        # 
        # ret = f"from {parent} import {child}"
        # return ret

class BashifyExecution(BaseModel):
    line: str
    idx: int
    
    # fill later
    # pymodule overrides associated_declarations if defined
    pymodule: str | None = None

    def fill(self):
        if '=' not in self.line:
            return
        
        # Clean the line by removing quotes
        self.line = self.line.replace('"', '').replace("'", "")
        
        eq_idx: int = self.line.index('=')
        self.pymodule = self.line[eq_idx+1:]

    def is_bashify_execution(line: str, prefix: str = "") -> bool:
        line_nospaces: str = line.replace(" ", "")
        offset: int = 1 if len(prefix) > 0 else 0  # for the '.' in the prefix
        declaration_len: int = len(f"declare{prefix}") + offset
        
        s: str = ""
        if '=' in line_nospaces:
            eq_idx: int = line_nospaces.index('=')
            s = line_nospaces[declaration_len:eq_idx]
        else:
            s = line_nospaces[declaration_len:]
        
        return s == "BASHIFY_EXECUTE"
