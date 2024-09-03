import numpy as np

from pybashify.compilation.schemas import BashifyDeclaration, BashifyExecution
from pybashify.compilation.inlines import inline_imports, inline_imports_from_source

# sys.stdlib_module_names

def bashify_pysource(pysource: str) -> str:
    return f"cat << EOF | python3 -\n{pysource}\nEOF"

def write_to_out(template_file: str, out: str | None, content: str):
    if out is None:
        # Decide a default name
        dot_index: int = template_file.rindex('.')
        file_name: str = template_file[:dot_index]

        out = file_name + "-compiled.sh"
    
    # Write to file
    with open(out, 'w') as output_file:
        output_file.write(content)


def compile(template_file: str, out: str | None, compat_prefix: str = ""):
    # 0. Get all lines
    template_lines: list[str] = []

    with open(template_file, 'r') as tmplt_sh:
        template_lines = tmplt_sh.readlines()
    
    # 1. Get all `declare` lines in the file
    declare_lines: list[BashifyDeclaration] = []
    execution: BashifyExecution = None
    for (i, line) in enumerate(template_lines):
        # Trim the leading/trailing whitespace
        stripped_line: str = line.strip()
        
        template_lines[i] = stripped_line
        
        if stripped_line.startswith(f"declare {compat_prefix}"):
            declare_lines.append(BashifyDeclaration(line=stripped_line, idx=i))
            if BashifyExecution.is_bashify_execution(line=stripped_line, prefix=compat_prefix):
                execution = BashifyExecution(line=stripped_line, idx=i)
                execution.fill()
    
    # 2. Process the BASHIFY_EXECUTE
    # If it is BASHIFY_EXECUTE="my.python.module" then don't associate it w/ any of the previously made declarations; ignore declarations at that point
    full_source: str = ""
    if execution.pymodule is not None:
        full_source = inline_imports(execution.pymodule)
    else:
        # 3. For each declaration, get the source code
        import_sources: str = ""
        for declaration in declare_lines:
            declaration.fill(prefix=compat_prefix)
            import_sources += f"{declaration.as_import(prefix=compat_prefix)}\n"

        full_source = inline_imports_from_source(import_sources)
    
    # Bashify the source
    bashified_source: str = bashify_pysource(full_source)

    # 4. replace the BASH_EXECUTE line with the source code
    template_lines[execution.idx] = bashified_source
    
    # 5. remove the declare statements
    compiled_bash_lines = np.array(template_lines)
    lines_to_delete: list[int] = [declaration.idx for declaration in declare_lines]
    np.delete(compiled_bash_lines, lines_to_delete)
    
    # 6. make a new version of the file
    compiled_bash_file_str: str = "\n".join(compiled_bash_lines.tolist())
    
    # 7. write it to output
    write_to_out(template_file, out, compiled_bash_file_str)
