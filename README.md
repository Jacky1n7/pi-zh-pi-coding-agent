# Pi 中文汉化 (Pi Chinese Localization)

将 [Pi (@earendil-works/pi-coding-agent)](https://github.com/earendil-works/pi-coding-agent) 的交互界面与 CLI 帮助中文化,并支持**升级后一键恢复**。

> 界面汉化是对本机安装副本的本地补丁,不改动上游源码、不提交上游仓库。pi 升级后补丁会被覆盖,重跑一次本工具即可恢复中文。

---

## ✨ 功能

汉化覆盖以下用户可见文本(25 个文件、240+ 条替换):

| 区域 | 文件 |
| --- | --- |
| `/` 斜杠命令列表 | `core/slash-commands.js` |
| `/settings` 设置菜单 | `modes/interactive/components/settings-selector.js` |
| 启动横幅 / 快捷键提示 | `modes/interactive/interactive-mode.js` |
| `/hotkeys` 快捷键表 | `modes/interactive/interactive-mode.js` |
| 会话信息 `/session` | `modes/interactive/interactive-mode.js` |
| 状态指示器(重试/压缩中) | `modes/interactive/components/status-indicator.js` |
| 底部状态栏 | `modes/interactive/components/footer.js` |
| bash 执行卡片 | `modes/interactive/components/bash-execution.js` |
| 登录对话框 | `modes/interactive/components/login-dialog.js` |
| 首次启动向导 | `modes/interactive/components/first-time-setup.js` |
| 模型选择器 | `modes/interactive/components/model-selector.js` |
| 会话恢复选择器 | `modes/interactive/components/session-selector.js` |
| 项目信任选择器 | `modes/interactive/components/trust-selector.js` |
| 思考级别选择器 | `modes/interactive/components/thinking-selector.js` |
| 树形结构视图 | `modes/interactive/components/tree-selector.js` |
| 模型配置选择器 | `modes/interactive/components/scoped-models-selector.js` |
| 资源选择器(扩展/技能/主题) | `modes/interactive/components/config-selector.js` |
| 助手消息 / 错误提示 | `modes/interactive/components/assistant-message.js` |
| 压缩摘要 / 分支摘要 | `modes/interactive/components/compaction-summary-message.js`、`branch-summary-message.js` |
| 消息分叉选择器 | `modes/interactive/components/user-message-selector.js` |
| CLI 帮助 `pi --help` | `cli/args.js` |
| llama.cpp 模型管理 | `core/slash-commands.js`、`extensions/llama/index.js` |

---

## 🚀 快速开始

```bash
# 1. 下载项目(或直接下载 pi-zh-apply.py + patches.json)
git clone https://github.com/509992828/pi-zh-pi-coding-agent.git
cd pi-zh-pi-coding-agent

# 2. 运行(自动探测 pi 安装位置)
python pi-zh-apply.py

# 3. 完全退出并重启 pi,界面即变为中文
```

### 指定安装位置

```bash
python pi-zh-apply.py --dist "C:/Users/你的用户名/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist"
```

### 只检查状态(不修改)

```bash
python pi-zh-apply.py --check
```

---

## 🔄 pi 升级后恢复汉化

pi 更新(`npm update -g @earendil-works/pi-coding-agent` 等)会覆盖被汉化的文件,此时:

```bash
cd pi-zh-pi-coding-agent
python pi-zh-apply.py
```

脚本幂等:已汉化的文件自动跳过,只需恢复的文件才会被重新打补丁。

---

## 🛠 如何重新生成补丁(进阶)

补丁数据 `patches.json` 由 `generate-patches.py` 从「英文原版 + 已汉化版本」自动提取生成:

```bash
# 需要: 英文原版 dist(如新版本) 与 已汉化 dist
python generate-patches.py \
  --pristine <英文原版dist目录> \
  --localized <已汉化dist目录> \
  -o patches.json
```

生成时会做「原版 + 补丁 == 汉化版」的完整性校验,确保替换对 100% 可重放。

**对新版 pi**:先在新版本上手动汉化需要的内容(或复用本项目的替换思路),再运行生成器更新 `patches.json`。

---

## 📁 项目结构

```
pi-zh-pi-coding-agent/
├── pi-zh-apply.py         # 主脚本:应用补丁 / 升级后恢复 / 状态检查
├── patches.json           # 240+ 条替换对(自动校验过)
├── generate-patches.py    # 补丁生成器(开发用)
├── pi-commands-cn.md      # 交互命令中文参考表
├── archive/               # 历史补丁脚本(早期版本,仅存档)
└── README.md
```

---

## ⚠️ 注意事项

- 补丁只修改**本机安装副本**,不影响其他机器或上游仓库。
- 上游升级后需重新运行本工具(见上)。
- 新版本若改动了源字符串,部分替换可能失效(`~ 部分未匹配` 提示),重新生成 `patches.json` 即可。
- 本工具未包含任何凭据或密钥。

---

## 📄 License

[MIT](LICENSE)

本项目与 Pi 官方无关,仅为社区本地化工具。
