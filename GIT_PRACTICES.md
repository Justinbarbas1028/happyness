# Git and GitHub Best Practices

To maintain a clean, organized, and understandable Git history, we follow a set of best practices for committing and interacting with GitHub.

## Commit Message Guidelines (Conventional Commits)

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification, which provides a lightweight convention on top of commit messages. This leads to more readable history, and makes it easier to automate certain tasks (e.g., generating changelogs).

### Format:

Each commit message consists of a **header**, a **body** (optional), and a **footer** (optional).

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The header is mandatory and has a special format that includes a `type`, an optional `scope`, and a `subject`.

#### Type:
The `type` is mandatory and must be one of the following:

*   **`feat`**: A new feature
*   **`fix`**: A bug fix
*   **`docs`**: Documentation only changes
*   **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, missing semicolons, etc.)
*   **`refactor`**: A code change that neither fixes a bug nor adds a feature
*   **`perf`**: A code change that improves performance
*   **`test`**: Adding missing tests or correcting existing tests
*   **`build`**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
*   **`ci`**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
*   **`chore`**: Other changes that don't modify src or test files
*   **`revert`**: Reverts a previous commit

#### Scope:
The `scope` is optional and consists of a noun describing the section of the codebase affected by the commit. For example, `auth`, `theme`, `homepage`, `api`, `docs`.

#### Subject:
The `subject` is a very short, concise description of the change:

*   Use the imperative, present tense: "change" not "changed" nor "changes".
*   Don't capitalize the first letter.
*   No period (.) at the end.

### Examples:

*   `feat(authentication): add Google OAuth support`
*   `fix(bug_report): correct issue with form submission on Safari`
*   `docs(README): update installation instructions`
*   `style(css): format header styles`
*   `refactor(user_model): extract validation logic to a helper function`
*   `perf(image_upload): optimize image compression algorithm`
*   `test(theme): add unit tests for dark mode toggle`
*   `chore(deps): update Django to 5.2.1`

## GitHub Workflow

1.  **Branching**: Work on features/fixes in dedicated branches (e.g., `feature/my-new-feature`, `bugfix/issue-123`).
2.  **Pull Requests (PRs)**: Create PRs for merging changes into `main` (or `develop`).
    *   PR titles should follow the Conventional Commit subject format.
    *   Provide a clear description of the changes, including motivations and any relevant screenshots or steps to reproduce.
    *   Link to any related issues.
3.  **Code Reviews**: All PRs should be reviewed by at least one other team member.
4.  **Squash and Merge**: When merging PRs, prefer "Squash and Merge" to keep the `main` branch history clean with meaningful commits. Ensure the squashed commit message follows the Conventional Commit format.
