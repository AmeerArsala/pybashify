# pybashify

Ever wanted to use bash scripts but they look like a bunch of mumbo jumbo?
You may have tried the python versions, but they aren't practical when you actually want to run bash, but it's a pain in the neck to actually write that.

That's where pybashify comes in:
It allows you to write bash scripts using python whilst **compiling** them to bash using a template syntax within a bash script that follows the same conventions as regular bash.

In other words, you get to seamlessly interop bash and python! Offload the more complex portions to python, while letting bash do the simple things.

Think of this like a bash template to full bash script compilation that occurs.

And ALL the bash code you write with the template syntax is not only COMPLETELY VALID bash scripting BY ITSELF (which means now you can test just the bash portion without running the python portion; also gives a good separation of concerns at times) but now you are able to write much cleaner code to host on a curl link!

Oh and another side effect of the fact that templates are 100% valid bash: your editor has syntax highlighting for this!

### Wait, so you're hijacking existing bash features and repurposing them to work for interoperating with Python scripts?

Yes. It's not that bad though, since the features it repurposes are features that nobody uses in bash anyway, such as the `declare` keyword.
And even if it were to matter, you have CLI options to mitigate this.

## Installation

```bash
pip install pybashify
```

### Building from source

```bash
pixi run build
```

## Usage

First, create a bash script. This will serve as your template for the real bash script that you will generate.

Then, in the bash script, at its simplest level, you can do this (I'm putting a few variations):
```bash
declare BASHIFY_EXECUTE="my.python.module"
```

```bash
declare BASHIFY_EXECUTE='my.python.module'
```

```bash
declare BASHIFY_EXECUTE=my.python.module
```

```bash
declare BASHIFY_EXECUTE = "my.python.module"
```

...you get the idea.

Then, you can run:


```bash
bashify template.sh [--out full_script.sh] [--compat] [--compat-prefix="PY"]
```

And NOW, a new shell script should be generated with all the same things your original had, except now the area where BASHIFY_EXECUTE was is now replaced with the execution of said python code. This is VERY useful for having users `curl`.

### But wait, there's more!


The example above is functionally equivalent to:

```bash
declare my.python.module

declare BASHIFY_EXECUTE
```

Now why are there 2 ways to do this? Because you can do this:

```bash
declare my.python.module
declare my.other.python.module

declare BASHIFY_EXECUTE
```

This will execute BOTH modules back-to-back inside `BASHIFY_EXECUTE`. And yes that means order matters. `my.python.module` will be executed first, followed by `my.other.python.module`.

You can have the declarations wherever you want, as long as they follow a specific order. However, the position of `BASHIFY_EXECUTE` DOES matter as that will be where they ultimately aggregate.

### This is cool, but I don't like shell features being hijacked

Well you're in luck!

What you need to do to mitigate this is run:
```bash
bashify my_script.sh --compat
```

and then in your `my_script.sh`, you would do:

```bash
declare PY.BASHIFY_EXECUTE=my.python.module
```

or

```bash
declare PY.my.python.module
declare PY.BASHIFY_EXECUTE
```

Obviously, you can also modify the prefix with the `--compat-prefix` flag.

### Compiled Outputs

You can just have your template be `my_script.template.sh` and if you run it without specifying an output, it will have the compiled version be `my_script.sh`.
If you do not use this notation and still go default without specifying an output script, it will by default do `my_script_template-compiled.sh` if your script input was `my_script_template.sh`.

Alright, I'm done yapping. Have a nice day, remember to stay hydrated, and definitely remember that I use blendOS btw :smiling_imp: :fire: :100:

## Raw Reference

Without compat mode:

- `declare` refers to a python module
- the name of the variable is the python module (in the same way you import my.python.module)
- there should not be a value
- order is inferred by the order in which your declares are. And yes you can mix them but it is not recommended
- aside from the order of the declares, the positioning of them in the file does not matter as they will be deleted in the compiled version
- The positioning of your final python script declaration, however, DOES matter.
- Use `declare BASHIFY_EXECUTE` for where you want to execute the Python code. However, as stated above, POSITIONING MATTERS
- Note that none of these `declare`s will work if they are on the same line separated with semicolons. might add that feature later if yall want but right now each `declare` requires its own line
- It should also be scoped globally (meaning that it can't be within an if statement)
- There can only be a single `BASHIFY_EXECUTE`. If there are multiple, it will default to the last one

With compat mode:

- Same as without compat mode except all `declare`s are prefixed with `compat_prefix`. By default, it is "PY", so you'd prefix like so: PY.my.python.module
- This ALSO applies to the execution directive. By default, it would be: `declare PY.BASHIFY_EXECUTE`
- This means that `declare` by default is not hijacked

Another Caveat:
- For system packages, you MUST do `import a.b.c` and not `from a.b import c`

## Compatibility with Python

3.10+ is required. Some features break when on 3.9


## Development

```bash
pixi install
pixi shell --change-ps1=false -e dev
```

Oh yeah, this project uses [pipelight](https://pipelight.dev) btw because I said so. It is used for pre-commit / push hooks while still being readable and maintainable.
You need to download that and Deno then you are good to go. Don't get scared of the deno stuff, this is just for a few things under the hood for logs in dev not prod. :fire:

### Publishing releases

In order to do this, I have standardized it via running this command:

```bash
scripts/update-version.sh
```
