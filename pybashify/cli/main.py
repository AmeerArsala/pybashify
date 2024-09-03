import typer


app = typer.Typer()

@app.command()
def _():
    """Something"""
    print("Hello World")


if __name__ == "__main__":
    app()
