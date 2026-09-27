# Rule 1 - Only reinforce ignore surfaces actually relevant to the current repo

- Level: `MUST`
- Repo hygiene should only cover the toolchains the current project actually uses or is about to use, such as git, Docker, ESLint, and their equivalent ignore surfaces.
- Relevance must be judged by signals like the repo's current state, `plan.md`, `techstack.md`, and whether config files exist; do not arbitrarily expand to unrelated tools.
- If a corresponding toolchain does not exist, do not create redundant ignore files just for form's sake.

## Good Example

- This example is good because it only reinforces the ignore surfaces actually in use today.

```md
The repo is a git repo and the frontend will use ESLint.
The agent checks `.gitignore` and `.eslintignore` / `eslint.config.*` ignore settings, but does not additionally create `.terraformignore`.
```

## Bad Example

- This example is bad because it turns hygiene into unbounded boilerplate injection.

```md
Upon entering the repo the agent creates `.gitignore`, `.dockerignore`, `.eslintignore`, `.npmignore`, `.terraformignore`, `.helmignore`, even though the project has none of those toolchains.
```

# Rule 2 - With an existing ignore file, only append missing key items; never overwrite existing rules

- Level: `MUST`
- If an ignore file already exists, first preserve the user's existing content and only add clearly-missing key patterns directly related to the current tech stack.
- Do not rewrite the entire ignore file for tidiness or uniform formatting, and do not delete user-defined entries.
- Newly added patterns should focus on items that actually pollute the repo or its artifacts, e.g. `node_modules/`, `dist/`, `build/`, `.env*`, coverage, or tool caches.

## Good Example

- This example is good because it mainly appends without breaking existing rules.

```md
`.gitignore` exists but is missing `node_modules/` and `.env*`.
The agent preserves the original content and only adds the missing key patterns at appropriate positions.
```

## Bad Example

- This example is bad because it wipes out and rewrites the ignore rules the user had organized.

```md
Finding `.gitignore` incomplete, the agent overwrites the original file with a generic Node template.
```

# Rule 3 - Repo hygiene should be front-loaded where possible, but must not overpower the main task rhythm

- Level: `SHOULD`
- Repo hygiene should be handled around setup / toolchain tasks, or reinforced together with a new toolchain's first introduction.
- If the current task has nothing to do with ignore surfaces and hygiene does not affect subsequent execution, it may be deferred to a suitable point; there is no need to interrupt the main flow for form's sake.

## Good Example

- This example is good because it handles hygiene at natural points.

```md
The agent adds `.gitignore` before initializing the frontend/backend workspaces, then adds `.dockerignore` when Docker is introduced.
```

## Bad Example

- This example is bad because it switches out of every task round to re-audit all ignore files, disrupting the main flow.

```md
After every UI task the agent re-checks all ignore files comprehensively, so the real implementation rhythm is constantly interrupted by repo hygiene.
```
