# CHANGELOG & README templates

## CHANGELOG.md skeleton

```markdown
# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

## [1.2.0] - 2026-09-10

### 摘要
新增导出功能，用户可把数据存成 CSV，方便在 Excel 里继续分析。

### Added
- `src/export/csv.js` — 新增 CSV 导出函数 → 支持一键下载当前表格数据

### Changed
- `src/ui/toolbar.jsx` — 工具栏增加「导出」按钮并绑定快捷键 Ctrl+E → 减少操作步骤

### Fixed
- `src/utils/date.js` — 修正时区导致的日期偏移 → 昨日数据不再显示为今日
```

## Entry rules

Good bullet (must have path + what + why):

- `docs/api.md` — 补充鉴权章节与错误码表 → 新人接入时少踩 401/403

Bad bullets (never use):

- fix bugs
- 更新代码
- `src/app.js` modified
- some improvements

Group mapping:

| Section | Use for |
|---------|---------|
| Added | new files/capabilities |
| Changed | behavior or interface changes |
| Fixed | bug fixes |
| Removed | deletions (optional section) |

## README version block

Insert after the H1 title (or replace an existing matching block):

```markdown
<!-- github-sync:begin -->
**Version:** 1.2.0  
**Last sync:** 2026-09-10
<!-- github-sync:end -->
```

Marker comments must stay intact so the next sync can update in place.

## Plain-language 摘要 tips

- Write for a busy reader: what they can do now, or what stopped being broken.
- 1–3 sentences, no file paths in 摘要 (paths belong in group bullets).
- Example: 「修复登录后偶发白屏；导出功能可用，支持 CSV。」
