# Commit Guidelines

## 1) Conventional Commits

For all contributions to this repo, you must use the conventional commits standard defined [here](https://www.conventionalcommits.org/en/v1.0.0/).

This is used to generate automated change logs, allow for tooling to decide semantic versions for all applications,
provide a rich and meaningful commit history along with providing
a base for more advanced tooling to allow for efficient searches for decisions and context related to commits and code.

### Commit types

**The following commit types are supported in the dbt project:**

- `fix:` - Should be used for any bug fixes.
- `build:` - Should be used for functionality related to building an application.
- `deploy:` - Should be used for functionality related to deploying an application.
- `revert:` - Should be used for any commits that revert changes.
- `wip:` - Should be used for commits that contain work in progress.
- `feat:` - Should be used for any new features added, regardless of the size of the feature.
- `chore:` - Should be used for tasks such as releases or patching dependencies.
- `ci:` - Should be used for any work on GitHub Action workflows or scripts used in CI.
- `docs:`- Should be used for adding or modifying documentation.
- `style:` - Should be used for code formatting commits and linting fixes.
- `refactor:` - Should be used for any type of refactoring work that is not a part of a feature or bug fix.
- `perf:` - Should be used for a commit that represents performance improvements.
- `test:` - Should be used for commits that are purely for automated tests.
- `instr:` - Should be used for commits that are for instrumentation purposes. (e.g. logs, trace spans and telemetry configuration)
- `local:` - Should be used for commits that are for local environment infrastructure/tools/scripts that are specific to a service or application (i.e. live under the directory of a service or application).

### Commit scopes

**The following commit scopes are supported:**

This list will evolve as more applications and packages are added to the dbt application.

- `ingestion-app` - This commit scope should be used for a commit that represents work that pertains to the project.
- `ingestion-app` - This commit scope should be used for a commit that represents work that pertains to a specific app category.
- `tests / common` - This commit scope should be used for a commit that represents work that pertain the macros.
- `admin` - This commit scope should be used for a commit that represents work that pertain the docs.
The commit scope can be omitted for changes that cut across these scopes.
However, it's best to check in commits that map to a specific scope where possible.

### Commit footers

**The following custom footers are supported:**

- `JiraIssue: DATA-9` - This footer must be provided when a commit pertains to some work where there is a JIRA issue  
  This helps with tooling that links JIRA issues to commits providing a way to easily get extra context and requirements
  that are related to a commit.
- `ConfluencePage: 1277953` - This footer can be provided when a commit represents some work that actions
                      some documentation in Confluence or is somewhat related to said documentation.
                      The value must be the unique Page ID that you can find in confluence.

### Example commit

#### With commit scope

```bash
git commit -m 'feat(ingestion-spotlight-recurly): add structure

Adds structure that allows easier navigation accross folders
for the different business lines.

JiraIssue: DATA-9
ConfluencePage: 1277953
'
```

#### Without commit scope

```bash
git commit -m 'fix: common folder structure'
```

## 2) You must use the imperative mood for commit headers.

https://cbea.ms/git-commit/#imperative

The imperative mood simply means naming the subject of the commit as if it is a unit of work that can be applied instead of reporting facts about work done.

If applied, this commit will **your subject line here**.

Read the article above to find more examples and tips for using the imperative mood.

## 3) Work on trunk and rebase if you must branch out

You should primarily commit and push your work to the trunk and favour feature flags for managing inclusion of new features.
In some cases you might need to create a separate branch for a particular piece of work, when that work is ready to be integrated you should rebase
instead of merge.
When you are out of sync with the main branch, you should rebase origin/main into your local main instead of merge to avoid polluting the commit history with merge commits.
