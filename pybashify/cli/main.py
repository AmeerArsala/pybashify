import typer
from pybashify.compilation import compiler


app = typer.Typer()


@app.command()
def _(template_file: str, out: str | None = None,
      compat: bool = False, compat_prefix: str = "PY",
):
    """
    Without compat mode:
        - `declare` refers to a python module
        - the name of the variable is the python module (in the same way you import my.python.module)
        - the value is optional, but if specified as an int, that represents the order in which the scripts appear
        - otherwise, order is inferred by the order in which your declares are. And yes you can mix them but it is not recommended
        - aside from the order of the declares, the positioning of them in the file does not matter as they will be deleted in the compiled version
        - The positioning of your final python script declaration, however, DOES matter.
        - Use `declare BASHIFY_EXECUTE` for where you want to execute the Python code. However, as stated above, POSITIONING MATTERS
        - Note that none of these `declare`s will work if they are on the same line separated with semicolons. might add that feature later if yall want but right now each `declare` requires its own line
        - It should also be scoped globally (meaning that it can't be within an if statement)
    With compat mode:
        - Same as without compat mode except all `declare`s are prefixed with `compat_prefix`. By default, it is "PY", so you'd prefix like so: PY.my.python.module
        - This ALSO applies to the execution directive. By default, it would be: `declare PY.BASHIFY_EXECUTE`
        - This means that `declare` by default is not hijacked

    Another Caveat:
        - For system packages, you MUST do `import a.b.c` and not `from a.b import c`
        - There can only be a single BASHIFY_EXECUTE. If there are multiple, it will default to the last one
    """
    typer.echo("Compiling...")
    
    if compat:
        compiler.compile(template_file, out, compat_prefix=compat_prefix)
    else:
        compiler.compile(template_file, out)

    typer.echo("Done.")


if __name__ == "__main__":
    app()
