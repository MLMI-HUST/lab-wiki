# MLMI Wiki

MLMI 实验笔记知识库，使用 Obsidian 编辑 + Git 协作 + Quartz v4 发布到 GitHub Pages。

## 快速开始

### 编辑笔记

1. `git clone` 本仓库
2. `git checkout -b notes/your-name` 创建个人分支
3. 用 Obsidian 打开 `content/` 目录作为 Vault
4. 编辑笔记，commit + push 到个人分支
5. 发起 PR 到 main，至少 1 人 review 后合并

### 本地预览站点

```bash
npm install
npx quartz build --serve
```

访问 `http://localhost:8080` 预览。

## 目录结构

```
content/          Obsidian Vault（笔记内容）
scripts/          自动化脚本（校验/MOC生成/过期检查）
.github/workflows/ GitHub Actions 工作流
quartz.config.ts  Quartz 站点配置
quartz.layout.ts  Quartz 页面布局
```

## 笔记规范

详见 [笔记仓库管理规范](https://github.com/MLMI-HUST/team-git-sop/blob/dev/references/notes-conventions.md)。
