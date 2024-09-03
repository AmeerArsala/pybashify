# pybashify

Ever wanted to use bash scripts but they look like a bunch of mumbo jumbo?
You may have tried the python versions, but they aren't practical when you actually want to run bash, but it's a pain in the neck to actually write that.

Here's where pybashify comes in:
It allows you to write bash scripts using python whilst **compiling** them to bash using a template syntax within a bash script that follows the same conventions as regular bash.

In other words, your editor has syntax highlighting for this already!

### Wait, so you're hijacking existing bash features and repurposing them to work with Python scripts?

Yes. It's not that bad though, since the features it repurposes are features that nobody uses in bash anyway, such as the `declare` keyword.
And even if it were to matter, you have CLI options to mitigate this.

## Compatibility with Python

3.10+ is required. Some features break when on 3.9
