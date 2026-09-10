# github-sync

MiMo Desktop skill：创建 GitHub 仓库（建仓前询问可见性），并完成带 README / CHANGELOG 一致性的同步推送。

<!-- github-sync:begin -->
**Version:** 0.2.0  
**Last sync:** 2026-09-10
<!-- github-sync:end -->

## 功能

- **建仓**：询问 Private / Public（推荐 Private）；始终添加 README 与 MIT License
- **同步**：差异盘点 → SemVer 建议 → 更新 README 版本块 → 撰写双层 CHANGELOG（摘要 + 路径/改动/作用）→ 一致性门禁 → push + tag
- **校验脚本**：`scripts/check_sync_consistency.py` 对齐 README 与 CHANGELOG 版本

## 安装（MiMo Desktop）

将本仓库内容放到：

```text
~/.claude/skills/github-sync/
```

目录结构：

```text
github-sync/
├── SKILL.md
├── locales/
│   ├── zh-CN.json
│   └── en-US.json
├── references/
│   └── changelog-template.md
└── scripts/
    └── check_sync_consistency.py
```

新对话中即可触发，例如：「同步到 GitHub」「建仓库并推送」。

## 使用前提

1. Git 已配置 `user.name` / `user.email`
2. SSH 已绑定 GitHub（`ssh -T git@github.com`）
3. 已安装 [GitHub CLI](https://cli.github.com/) 并用 **Classic PAT（scope: `repo`）** 登录：

```bash
gh auth login --with-token
```

## 安全 / 隐私

- **禁止**将 PAT、SSH 私钥、`.env` 等密钥提交进本仓库或任何技能目录
- 本仓库不包含任何 Token；认证只保存在本机 `gh` keyring / SSH agent
- 建仓与同步时请确认可见性；默认不会把 Public 仓库自动改成 Private
- 若 Token 曾出现在聊天或脚本中，请到 GitHub 吊销并更换

## 校验脚本示例

```bash
python scripts/check_sync_consistency.py --repo /path/to/project --expect-version 0.2.0
```

## License

MIT
