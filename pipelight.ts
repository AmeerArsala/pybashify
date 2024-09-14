import type { Pipeline, Config } from "https://deno.land/x/pipelight/mod.ts";

// 1.) Format
// 2.) Lint
// Then Push
// On Push, publish to PyPI
// Let that carry to conda-forge

const formatAndLint: Pipeline = {
  name: "fmt-lint",
  steps: [
    {
      name: "format",
      commands: ["ruff format pybashify"],
    },
    {
      name: "lint",
      commands: ["ruff check pybashify --fix"]
    }
  ],
  triggers: [
    {
      branches: ["main", "dev"],
      actions: ["pre-commit", "pre-push"]
    }
  ]
};

const config: Config = {
  pipelines: [formatAndLint],
};

export default config;
