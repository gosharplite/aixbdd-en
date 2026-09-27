# Rule 1 - By default, only modify the minimal set of existing files

- Level: `MUST`
- If a requirement can be fulfilled by modifying the existing `CONSTITUTION.md`, `shared.md`, or a single `skills/<skill>/<artifact>.md`,
  do not additionally create a second rule file or a side explanatory file.
- Only when the requirement explicitly adds a new skill artifact placement should a new `.md` file be created.
- Do not casually rewrite other skills' rule files just because the topic is similar.

## Good Example

- This example is good because it only touches the one artifact rule file that genuinely needs changing.

````md
Requirement: add a technical reference rule to `tasks.md`
Result: only modify `skills/axb-tasks/tasks.md`
````

## Bad Example

- This example is bad because the requirement affects only one artifact, yet a bunch of new files are created.

````md
Requirement: add a technical reference rule to `tasks.md`
Result:
- Create `shared-tasks.md`
- Create `tasks-reference.md`
- Rewrite `CONSTITUTION.md`
````

# Rule 2 - New rules only contain what is necessary to support this round's requirement

- Level: `MUST`
- Each new rule should only cover the judgment surface this round's requirement truly needs; do not opportunistically expand it into a complete governance charter.
- If an extended dimension has not been requested by the user, keep it as a future increment instead of writing it all in advance.
- Good / Bad Examples should also only demonstrate the core difference of this rule, without extending into other unrequested topics.

## Good Example

- This example is good because it only adds the necessary constraint of "response separation".

````md
## Rule 1 - Success and failure responses must be expressed separately

- Level: `MUST`
- success responses and error responses must be described separately.
````

## Bad Example

- This example is bad because it seizes the opportunity to write authentication, pagination, naming, and version governance all at once.

````md
## Rule 1 - Master API governance list

- response separation
- auth header
- cursor pagination
- versioning policy
- deprecation strategy
````

# Rule 3 - When overriding, prefer local fixes over rewriting the whole file

- Level: `SHOULD`
- If an existing rule file is only locally insufficient, prefer patching, renaming, or rewriting local sections rather than rewriting the whole file.
- Only when the existing file's responsibility boundaries are clearly wrong should a major refactor be considered.

## Good Example

- This example is good because it only adds one new Rule without disturbing existing rules.

````md
The file already has Rule 1
This round only adds Rule 2
````

## Bad Example

- This example is bad because it rewrites the whole existing artifact rule file when there is no need.

````md
The file already has 3 stable rules
This round rewrites everything just to add 1 rule
````
