# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [SemVer](https://semver.org/).

## [0.2.0] - 2026-09-10

### 摘要
技能开源上传：建仓可见性改为询问用户；仓库内文档明确禁止提交 Token，并附安装与安全说明。

### Added
- `README.md` — 安装路径、前置条件与安全/隐私章节 → 方便安装且避免误提交密钥
- `CHANGELOG.md` — 双层变更日志 → 便于对照版本阅读改动位置与作用
- `.gitignore` — 忽略常见密钥与本地环境文件 → 降低 Token/私钥误提交风险

### Changed
- `SKILL.md` — 建仓由强制 Private 改为询问 Private/Public（推荐 Private） → 满足不同可见性需求
- `locales/zh-CN.json` / `locales/en-US.json` — 文案改为「可见性可选」 → 插件页描述与行为一致

## [0.1.0] - 2026-09-10

### 摘要
首个可用版本：支持私有建仓（README+MIT）与带一致性门禁的同步推送。

### Added
- `SKILL.md` — 完整 Flow A/B/C 指令 → 建仓、同步、仅推送三类工作流
- `scripts/check_sync_consistency.py` — README/CHANGELOG 版本对齐检查 → 推送前防不一致
- `references/changelog-template.md` — 条目模板与好坏示例 → 保证变更说明可读
- `locales/zh-CN.json` / `locales/en-US.json` — MiMo Desktop 展示元数据 → 插件页可发现
