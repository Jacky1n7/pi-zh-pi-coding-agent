# Pi 系统命令汉化版

以下是 Pi（@earendil-works/pi-coding-agent）交互模式下可用的所有命令的中文释义。

## 交互模式命令表

| 命令 | 英文描述 | 中文释义 |
|------|----------|----------|
| `/login`, `/logout` | Manage provider credentials | 管理提供商凭据（登录/登出模型提供商） |
| `/llama` | Download, load, and unload llama.cpp router models | 下载、加载和卸载 llama.cpp 路由器模型 |
| `/model` | Switch models | 切换模型 |
| `/scoped-models` | Enable/disable models for Ctrl+P cycling | 启用/禁用 Ctrl+P 循环使用的模型 |
| `/settings` | Thinking level, theme, message delivery, transport | 设置思考级别、主题、消息交付方式、传输方式 |
| `/resume` | Pick from previous sessions | 从之前的会话中选择/恢复 |
| `/new` | Start a new session | 开始一个新会话 |
| `/name <name>` | Set session display name | 设置会话显示名称 |
| `/session` | Show session info (file, ID, messages, tokens, cost) | 显示会话信息（文件路径、ID、消息、令牌消耗、成本） |
| `/tree` | Jump to any point in the session and continue from there | 跳转到会话中的任意点并继续执行 |
| `/trust` | Save project trust decision for future sessions (restart required) | 保存项目信任决策以供未来会话使用（需要重启 Pi 才能生效） |
| `/fork` | Create a new session from a previous user message | 从之前的用户消息创建一个新会话 |
| `/clone` | Duplicate the current active branch into a new session | 将当前活动分支复制到一个新会话 |
| `/compact [prompt]` | Manually compact context, optional custom instructions | 手动压缩上下文（可选自定义压缩说明） |
| `/copy` | Copy last assistant message to clipboard | 复制最后一个助手消息到剪贴板 |
| `/export [file]` | Export session to HTML or JSONL file | 将会话导出为 HTML 或 JSONL 文件 |
| `/import <file>` | Import and resume a session from a JSONL file | 从 JSONL 文件导入并恢复会话 |
| `/share` | Upload as private GitHub gist with shareable HTML link | 上传为私有的 GitHub Gist 并生成可分享的 HTML 链接 |
| `/reload` | Reload keybindings, extensions, skills, prompts, themes, and context files | 重新加载按键绑定、扩展、技能、提示模板、主题和上下文文件 |
| `/hotkeys` | Show all keyboard shortcuts | 显示所有键盘快捷键 |
| `/changelog` | Display version history | 显示版本历史 |
| `/quit` | Quit pi | 退出 Pi |

---

**使用方法**：
在 Pi 的编辑器中输入 `/` 即可触发命令列表。

如果你需要我把 **CLI Reference**（启动参数和选项）也汉化，或者把这个表格保存为单独的 Markdown 文件，告诉我一声就好！