---
name: github-sync
description: 创建 GitHub 仓库（建仓前询问可见性）并完成带变更说明的同步推送。Use when the user says 同步到 GitHub, 建仓库, 推送到 GitHub, 上传到 GitHub, 同步代码, 更新 CHANGELOG, 建私有仓库, 建公开仓库, push to GitHub, or asks to create a repo with README and MIT license and keep files/README/CHANGELOG consistent. Do NOT use for GitLab/Bitbucket, CI setup, or unrelated git questions.
---

# GitHub Sync

一键：按规范创建 GitHub 仓库（可见性由用户选择），或把本地变更同步到 GitHub，并保证文件、README 版本块、CHANGELOG 一致且可读。

## Hard contracts (never skip)

### New repository

| Field | Required value |
|-------|----------------|
| Visibility | **Ask user** — `private` or `public` (default suggestion: private) |
| README | **ON** |
| License | **MIT** |

Use the `question` tool (or a clear one-shot question) before create if visibility was not already stated:

- Options: Private（推荐） / Public
- If the user already said 私有/private → `--private`
- If they already said 公开/public → `--public`
- Never assume Public. Never change an existing repo's visibility silently.

```bash
# after user chose private
gh repo create <owner>/<name> --private --add-readme --license mit
# after user chose public
gh repo create <owner>/<name> --public --add-readme --license mit
```

- Owner default: current `gh` user (expect `yangyf724` unless `gh api user` says otherwise).
- If the repo already exists, do not recreate; switch to Sync flow or ask.

### Every sync must guarantee

1. Local files committed and pushed (no silent partial push of an inconsistent tree).
2. `README.md` version block matches the release version and date.
3. `CHANGELOG.md` has a new entry describing **location + what changed + why it matters**.
4. Tag `vX.Y.Z` pushed when releasing a versioned sync.

## Prerequisites

Check once per session (or on failure):

```bash
gh auth status
git config --global user.name
git config --global user.email
ssh -T git@github.com   # expect "Hi <user>!"
```

- Prefer SSH remotes: `git@github.com:<owner>/<repo>.git`
- If `gh` missing: try `C:\Program Files\GitHub CLI\gh.exe` on Windows; do not invent a binary path.
- If unauthenticated: ask for a **Classic PAT** with full `repo` scope (https://github.com/settings/tokens/new). Fine-grained tokens often cannot create user repos (`HTTP 403` on `POST /user/repos`). Then: `gh auth login --with-token`.
- On 403 while creating a repo: tell the user to use Classic `repo` scope; do not retry blindly.

## Flow A — Create repo (visibility chosen by user)

1. Ask (only if missing): repo **name**; **visibility** (Private recommended / Public); optional local **path**.
2. Create remote with the chosen flag (`--private` or `--public`), always with `--add-readme --license mit`.

```bash
gh repo create <owner>/<name> --private --add-readme --license mit --description "<short desc>"
# or --public
```

3. If starting from an existing local folder:
   - `git init -b main` if needed
   - `git remote add origin git@github.com:<owner>/<name>.git`
   - If remote already has README from `--add-readme`, `git pull --rebase origin main` before first push (or clone fresh and copy files).
4. Ensure `README.md` contains the version block (see references/changelog-template.md). Insert if missing.
5. Ensure `CHANGELOG.md` exists; create with initial `[0.1.0]` or `[1.0.0]` entry.
6. Commit, push `main`, report URL + visibility.

Verify after create:

```bash
gh repo view <owner>/<name> --json visibility,licenseInfo,defaultBranchRef
```

Expect chosen visibility (`PRIVATE` or `PUBLIC`), license MIT, default branch `main`.

## Flow B — Sync existing repo

Run in order. Stop and report if a gate fails.

### B1. Inventory

```bash
git status -sb
git diff --stat
git log --oneline -5
git remote -v
```

If no remote or remote is not GitHub, fix remote (SSH form) before continuing.

### B2. Diff vs last release

```bash
git fetch origin
git describe --tags --abbrev=0 2>$null   # last tag, may be empty
git diff --name-status <last-tag-or-empty-tree>...HEAD
```

Collect changed paths. If working tree dirty, those files are also in scope (include uncommitted).

### B3. SemVer suggestion

Infer next version from changes vs last tag (default `0.1.0` if none):

| Change kind | Bump |
|-------------|------|
| Breaking (API/schema/UX contract, data loss risk) | **major** |
| New feature / new file that adds capability | **minor** |
| Fix, docs, refactor, chore | **patch** |

Present suggestion to the user once:

> 建议版本 `X.Y.Z`（原因：…）。确认或回复新版本号。

If the user already stated the version, use it. If they said “直接同步/不用问”, apply the suggestion and continue.

### B4. README consistency

1. `README.md` must exist and be non-empty.
2. Ensure this block exists (top after title, or replace existing block):

```markdown
<!-- github-sync:begin -->
**Version:** X.Y.Z  
**Last sync:** YYYY-MM-DD
<!-- github-sync:end -->
```

3. Set Version = chosen version, Last sync = today (local date).
4. Do not rewrite unrelated README prose unless the user asked.

### B5. CHANGELOG entry

Read `references/changelog-template.md` before writing.

1. Create `CHANGELOG.md` if missing (Keep a Changelog header + link refs).
2. Insert new section at top (after H1 / intro):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 摘要
1–3 sentences in plain language: what this update does for the user.

### Added
- `path/file` — 改了什么 → 有什么用

### Changed
- `path/file` — 改了什么 → 有什么用

### Fixed
- `path/file` — 改了什么 → 有什么用
```

3. Every technical bullet must have **path**, **what**, **why/impact**.
4. Omit empty sections. Match groups to reality (Added/Changed/Fixed).
5. One entry per release; do not stack multiple same-day versions unless user asked.

### B6. Commit

```bash
git add -A
git status
git commit -m "chore(release): vX.Y.Z

See CHANGELOG.md for details."
```

Split commits only when the user or repo policy requires it; still one release tag.

### B7. Consistency gate (must pass before push)

| Check | Command / rule |
|-------|----------------|
| Clean tree after commit | `git status -porcelain` empty |
| CHANGELOG top version | first `## [X.Y.Z]` equals chosen version |
| README version block | Version equals X.Y.Z; Last sync is today |
| Tag free | `git rev-parse vX.Y.Z` fails (not exists) |

If any check fails, fix locally and re-run. Do not push.

### B8. Push

```bash
git push -u origin HEAD
git tag vX.Y.Z
git push origin vX.Y.Z
```

If rejected non-FF, fetch and rebase; re-run consistency gate if files changed.

### B9. Report to user

Short Chinese summary:

- 仓库 / 分支 / tag
- 版本与同步日期
- 本次改动摘要（来自 CHANGELOG）
- 远程 URL
- 提醒：可见性 + README + MIT（新建时）

## Flow C — Sync-only without release bump

If the user says 仅推送 / 不发版 / no version bump:

- Still commit all intended files (AC2 file consistency).
- Still update README Last sync date; do **not** bump Version unless user asks.
- Do not add a new CHANGELOG version section and do not tag.
- Mention 「未发版，仅推送」 in the reply.

## Error handling

| Symptom | Action |
|---------|--------|
| `gh` not found | Use full path `C:\Program Files\GitHub CLI\gh.exe` on Windows; else ask to install GitHub CLI |
| Auth failed | Re-run `gh auth status`; ask for Classic PAT with `repo` scope |
| Create repo HTTP 403 | Token cannot create repos — switch to Classic `repo` scope |
| `Repository not found` on push | Verify name/owner; private repo + missing key; confirm `gh repo view` |
| Push rejected non-FF | `git pull --rebase origin main`, fix, re-gate, push |
| README/CHANGELOG conflict markers | Stop; show user; do not force push |
| User wants public repo | Explicit confirm required; do not default public |

## Examples

**User:** 帮我把这个文件夹建成 GitHub 仓库并推送  
**You:** Flow A → 询问 Private/Public → README+MIT → README version block → CHANGELOG → push → report

**User:** 建成私有仓库并推送  
**You:** Flow A → `--private` + README+MIT → … → push → report

**User:** 同步到 GitHub  
**You:** Flow B → inventory → suggest SemVer → README+CHANGELOG → gate → push+tag → report

**User:** 只推一下，不用改版本  
**You:** Flow C

## Resources

- `references/changelog-template.md` — full CHANGELOG/README templates and good/bad bullets
- `scripts/check_sync_consistency.py` — optional gate helper (version alignment)
