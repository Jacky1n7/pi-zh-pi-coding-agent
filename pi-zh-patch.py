# -*- coding: utf-8 -*-
"""Pi 中文汉化综合补丁 (90% 覆盖) - 针对 @earendil-works/pi-coding-agent"""
from pathlib import Path

ROOT = Path(r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist")
TARGETS = [
    (ROOT / "core/slash-commands.js", SLASH := None),
]

def patch(path, reps, label):
    if not path.exists():
        print(f"SKIP (missing): {path}")
        return 0, 0
    text = path.read_text(encoding="utf-8")
    hit = miss = 0
    for old, new in reps:
        if old in text:
            text = text.replace(old, new)
            hit += 1
        else:
            miss += 1
    path.write_text(text, encoding="utf-8")
    print(f"{label}: hit={hit} miss={miss}")
    if miss:
        for old, _ in reps:
            if old not in text and False:
                pass
    return hit, miss

# ============ 1. status-indicator.js ============
patch(ROOT / "modes/interactive/components/status-indicator.js", [
    ("`Retrying (${attempt}/${maxAttempts}) in ${seconds}s... (${keyText(\"app.interrupt\")} to cancel)`",
     "`重试中 (${attempt}/${maxAttempts})，${seconds}s 后重试... (${keyText(\"app.interrupt\")} 取消)`"),
    ("(${keyText(\"app.interrupt\")} to cancel)", "(${keyText(\"app.interrupt\")} 取消)"),
    ("`Compacting context... ${cancelHint}`", "`正在压缩上下文... ${cancelHint}`"),
    ("? \"Context overflow detected, \" : \"\"}Auto-compacting... ${cancelHint}`",
     "? \"检测到上下文溢出，\" : \"\"}正在自动压缩... ${cancelHint}`"),
    ("`Summarizing branch... (${keyText(\"app.interrupt\")} to cancel)`",
     "`正在总结分支... (${keyText(\"app.interrupt\")} 取消)`"),
], "status-indicator")

# ============ 2. footer.js ============
patch(ROOT / "modes/interactive/components/footer.js", [
    ("`${modelName} • thinking off`", "`${modelName} • 思考关闭`"),
    ("`$${usageTotals.cost.toFixed(3)}${usingSubscription ? \" (sub)\" : \"\"}`",
     "`$${usageTotals.cost.toFixed(3)}${usingSubscription ? \" (订阅)\" : \"\"}`"),
    ('const modelName = state.model?.id || "no-model";', 'const modelName = state.model?.id || "无模型";'),
    ('const autoIndicator = this.autoCompactEnabled ? " (auto)" : "";',
     'const autoIndicator = this.autoCompactEnabled ? " (自动)" : "";'),
], "footer")

# ============ 3. bash-execution.js ============
patch(ROOT / "modes/interactive/components/bash-execution.js", [
    ("`Running... (${keyText(\"tui.select.cancel\")} to cancel)`", "`运行中... (${keyText(\"tui.select.cancel\")} 取消)`"),
    ('keyHint("app.tools.expand", "to collapse")', 'keyHint("app.tools.expand", "收起")'),
    ("`... ${hiddenLineCount} more lines (`", "`... 还有 ${hiddenLineCount} 行 (`"),
    ('keyHint("app.tools.expand", "to expand")', 'keyHint("app.tools.expand", "展开")'),
    ('theme.fg("warning", "(cancelled)")', 'theme.fg("warning", "(已取消)")'),
    ("theme.fg(\"error\", `(exit ${this.exitCode})`)", "theme.fg(\"error\", `(退出码 ${this.exitCode})`)"),
    ("`Output truncated. Full output: ${this.fullOutputPath}`", "`输出已截断。完整输出：${this.fullOutputPath}`"),
], "bash-execution")

# ============ 4. login-dialog.js ============
patch(ROOT / "modes/interactive/components/login-dialog.js", [
    ("const title = titleOverride ?? `Login to ${providerName}`;", "const title = titleOverride ?? `登录 ${providerName}`;"),
    ("this.inputRejecter(new Error(\"Login cancelled\"));", "this.inputRejecter(new Error(\"登录已取消\"));"),
    ("this.onComplete(false, \"Login cancelled\");", "this.onComplete(false, \"登录已取消\");"),
    ('const clickHint = process.platform === "darwin" ? "Cmd+click to open" : "Ctrl+click to open";',
     'const clickHint = process.platform === "darwin" ? "Cmd+点击打开" : "Ctrl+点击打开";'),
    ("`Enter code: ${info.userCode}`", "`输入代码：${info.userCode}`"),
    ('new Text(`(${keyHint("tui.select.cancel", "to cancel")})`, 1, 0)',
     'new Text(`(${keyHint("tui.select.cancel", "取消")})`, 1, 0)'),
    ("theme.fg(\"dim\", `e.g., ${placeholder}`)", "theme.fg(\"dim\", `例如：${placeholder}`)"),
    ('keyHint("tui.select.cancel", "to cancel,")', 'keyHint("tui.select.cancel", "取消，")'),
    ('keyHint("tui.select.confirm", "to submit")', 'keyHint("tui.select.confirm", "提交")'),
    ('keyHint("tui.select.cancel", "to close")', 'keyHint("tui.select.cancel", "关闭")'),
], "login-dialog")

# ============ 5. first-time-setup.js ============
patch(ROOT / "modes/interactive/components/first-time-setup.js", [
    ('{ value: "dark", label: "Dark" }', '{ value: "dark", label: "深色" }'),
    ('{ value: "light", label: "Light" }', '{ value: "light", label: "浅色" }'),
    ('{ value: true, label: "Share anonymous usage data" },', '{ value: true, label: "共享匿名使用数据" },'),
    ('{ value: false, label: "Don\'t share" },', '{ value: false, label: "不共享" },'),
    ("`Welcome to ${APP_NAME}, the minimal coding agent.`", "`欢迎使用 ${APP_NAME}，极简编码代理。`"),
    ('"Pick a theme."', '"选择主题。"'),
    ("`Detected system appearance: ${this.options.detectedTheme}`", "`检测到系统外观：${this.options.detectedTheme}`"),
    ('"Opt-in to anonymous usage data sharing?"', '"是否同意共享匿名使用数据？"'),
    ('"Opting in stores a tracking identifier in settings.json and enables anonymous\\nusage analytics. This helps us to better debug, reproduce, and resolve issues\\nand bugs within Pi. You can observe what is shared using /privacy and make\\nchanges anytime in settings.json."',
     '"启用后将在 settings.json 中存储跟踪标识并开启匿名用量分析。\\n这有助于我们更好地调试、复现和解决 Pi 中的问题。\\n你可以通过 /privacy 查看共享的内容，并随时在 settings.json 中修改。"'),
    ('keyHint("tui.select.confirm", this.step === "theme" ? "continue" : "finish")',
     'keyHint("tui.select.confirm", this.step === "theme" ? "继续" : "完成")'),
    ('keyHint("tui.select.cancel", "skip setup")', 'keyHint("tui.select.cancel", "跳过设置")'),
    ('rawKeyHint("↑↓", "navigate")', 'rawKeyHint("↑↓", "导航")'),
], "first-time-setup")

# ============ 6. model-selector.js ============
patch(ROOT / "modes/interactive/components/model-selector.js", [
    ('refreshStatusMessage = "Refreshing model catalogs…";', 'refreshStatusMessage = "正在刷新模型目录…";'),
    ('const hintText = "Only showing models from configured providers. Use /login to add providers.";',
     'const hintText = "仅显示已配置提供商的模型。使用 /login 添加提供商。";'),
    ('this.errorMessage = "Model refresh timed out; showing cached models.";',
     'this.errorMessage = "模型刷新超时；显示缓存的模型。";'),
    ('this.errorMessage = `Could not refresh ${result.errors.keys().next().value}; showing cached models.`;',
     'this.errorMessage = `无法刷新 ${result.errors.keys().next().value}；显示缓存的模型。`;'),
    ('this.errorMessage = `Could not refresh ${result.errors.size} model catalogs; showing cached models.`;',
     'this.errorMessage = `无法刷新 ${result.errors.size} 个模型目录；显示缓存的模型。`;'),
    ('this.refreshStatusMessage = "Model catalogs refreshed.";', 'this.refreshStatusMessage = "模型目录已刷新。";'),
    ('return `${theme.fg("muted", "Scope: ")}${allText}${theme.fg("muted", " | ")}${scopedText}`;',
     'return `${theme.fg("muted", "范围：")}${allText}${theme.fg("muted", " | ")}${scopedText}`;'),
    ('return keyHint("tui.input.tab", "scope") + theme.fg("muted", " (all/scoped)");',
     'return keyHint("tui.input.tab", "范围") + theme.fg("muted", " (全部/限定)");'),
    ('theme.fg("muted", "  No matching models")', 'theme.fg("muted", "  没有匹配的模型")'),
    ('theme.fg("muted", `  Model Name: ${selected.model.name}`)', 'theme.fg("muted", `  模型名称：${selected.model.name}`)'),
], "model-selector")

# ============ 7. session-selector.js ============
patch(ROOT / "modes/interactive/components/session-selector.js", [
    ('const title = this.scope === "current" ? "Resume Session (Current Folder)" : "Resume Session (All)";',
     'const title = this.scope === "current" ? "恢复会话（当前文件夹）" : "恢复会话（全部）";'),
    ('const sortLabel = this.sortMode === "threaded" ? "Threaded" : this.sortMode === "recent" ? "Recent" : "Fuzzy";',
     'const sortLabel = this.sortMode === "threaded" ? "树形" : this.sortMode === "recent" ? "最近" : "模糊";'),
    ('const sortText = theme.fg("muted", "Sort: ") + theme.fg("accent", sortLabel);',
     'const sortText = theme.fg("muted", "排序：") + theme.fg("accent", sortLabel);'),
    ('const nameLabel = this.nameFilter === "all" ? "All" : "Named";',
     'const nameLabel = this.nameFilter === "all" ? "全部" : "已命名";'),
    ('const nameText = theme.fg("muted", "Name: ") + theme.fg("accent", nameLabel);',
     'const nameText = theme.fg("muted", "名称：") + theme.fg("accent", nameLabel);'),
    ('scopeText = `${theme.fg("muted", "○ Current Folder | ")}${theme.fg("accent", `Loading ${progressText}`)}`;',
     'scopeText = `${theme.fg("muted", "○ 当前文件夹 | ")}${theme.fg("accent", `加载中 ${progressText}`)}`;'),
    ('scopeText = `${theme.fg("accent", "◉ Current Folder")}${theme.fg("muted", " | ○ All")}`;',
     'scopeText = `${theme.fg("accent", "◉ 当前文件夹")}${theme.fg("muted", " | ○ 全部")}`;'),
    ('scopeText = `${theme.fg("muted", "○ Current Folder | ")}${theme.fg("accent", "◉ All")}`;',
     'scopeText = `${theme.fg("muted", "○ 当前文件夹 | ")}${theme.fg("accent", "◉ 全部")}`;'),
    ('const confirmHint = `Delete session? ${keyHint("tui.select.confirm", "confirm")} · ${keyHint("tui.select.cancel", "cancel")}`;',
     'const confirmHint = `删除会话？${keyHint("tui.select.confirm", "确认")} · ${keyHint("tui.select.cancel", "取消")}`;'),
    ('const pathState = this.showPath ? "(on)" : "(off)";', 'const pathState = this.showPath ? "(开)" : "(关)";'),
    ('keyHint("tui.input.tab", "scope") + sep + theme.fg("muted", \'re:<pattern> regex · "phrase" exact\')',
     'keyHint("tui.input.tab", "范围") + sep + theme.fg("muted", \'re:<模式> 正则 · "短语" 精确\')'),
    ('keyHint("app.session.toggleSort", "sort")', 'keyHint("app.session.toggleSort", "排序")'),
    ('keyHint("app.session.toggleNamedFilter", "named")', 'keyHint("app.session.toggleNamedFilter", "命名")'),
    ('keyHint("app.session.delete", "delete")', 'keyHint("app.session.delete", "删除")'),
    ('keyHint("app.session.togglePath", `path ${pathState}`)', 'keyHint("app.session.togglePath", `路径 ${pathState}`)'),
    ('keyHint("app.session.rename", "rename")', 'keyHint("app.session.rename", "重命名")'),
    ('this.onError?.("Cannot delete the currently active session");', 'this.onError?.("无法删除当前活动会话");'),
    ('emptyMessage = `  No named sessions found. Press ${toggleKey} to show all.`;',
     'emptyMessage = `  未找到已命名的会话。按 ${toggleKey} 显示全部。`;'),
    ('emptyMessage = `  No named sessions in current folder. Press ${toggleKey} to show all, or Tab to view all.`;',
     'emptyMessage = `  当前文件夹中没有已命名的会话。按 ${toggleKey} 显示全部，或按 Tab 查看全部。`;'),
    ('emptyMessage = "  No sessions found";', 'emptyMessage = "  未找到会话";'),
    ('emptyMessage = "  No sessions in current folder. Press Tab to view all.";',
     'emptyMessage = "  当前文件夹中没有会话。按 Tab 查看全部。";'),
    ('panel.addChild(new Text(theme.bold("Rename Session"), 1, 0));', 'panel.addChild(new Text(theme.bold("重命名会话"), 1, 0));'),
    ('panel.addChild(new Text(theme.fg("muted", `${keyText("tui.select.confirm")} to save · ${keyText("tui.select.cancel")} to cancel`), 1, 0));',
     'panel.addChild(new Text(theme.fg("muted", `${keyText("tui.select.confirm")} 保存 · ${keyText("tui.select.cancel")} 取消`), 1, 0));'),
    ('const msg = result.method === "trash" ? "Session moved to trash" : "Session deleted";',
     'const msg = result.method === "trash" ? "会话已移入回收站" : "会话已删除";'),
    ('this.header.setStatusMessage({ type: "error", message: `Failed to delete: ${errorMessage}` }, 3000);',
     'this.header.setStatusMessage({ type: "error", message: `删除失败：${errorMessage}` }, 3000);'),
    ('const errorMessage = result.error ?? "Unknown error";', 'const errorMessage = result.error ?? "未知错误";'),
    ('this.header.setStatusMessage({ type: "error", message: `Failed to load sessions: ${message}` }, 4000);',
     'this.header.setStatusMessage({ type: "error", message: `加载会话失败：${message}` }, 4000);'),
], "session-selector")

# ============ 8. session-selector-search.js ============
patch(ROOT / "modes/interactive/components/session-selector-search.js", [
    ('"Empty regex"', '"正则表达式为空"'),
], "session-selector-search")

# ============ 9. trust-selector.js ============
patch(ROOT / "modes/interactive/components/trust-selector.js", [
    ('const label = decision.decision ? "trusted" : "untrusted";', 'const label = decision.decision ? "已信任" : "未信任";'),
    ('return `${label} (inherited from ${decision.path})`;', 'return `${label}（继承自 ${decision.path}）`;'),
    ('return "none";', 'return "无";'),
    ('theme.bold("Project trust")', 'theme.bold("项目信任")'),
    ('`Saved decision: ${formatDecision(this.trustOptions[0]?.savedPath, options.savedDecision)}`',
     '`已保存的决策：${formatDecision(this.trustOptions[0]?.savedPath, options.savedDecision)}`'),
    ('`Current session: ${options.projectTrusted ? "trusted" : "untrusted"}`',
     '`当前会话：${options.projectTrusted ? "已信任" : "未信任"}`'),
    ('rawKeyHint("↑↓", "navigate")', 'rawKeyHint("↑↓", "导航")'),
    ('keyHint("tui.select.confirm", "save")', 'keyHint("tui.select.confirm", "保存")'),
    ('keyHint("tui.select.cancel", "cancel")', 'keyHint("tui.select.cancel", "取消")'),
], "trust-selector")

# ============ 10. trust-manager.js ============
patch(ROOT / "core/trust-manager.js", [
    ('{ label: "Trust", trusted: true, updates: [{ path: trustPath, decision: true }], savedPath: trustPath },',
     '{ label: "信任", trusted: true, updates: [{ path: trustPath, decision: true }], savedPath: trustPath },'),
    ('label: `Trust parent folder (${parentPath})`,', 'label: `信任父文件夹 (${parentPath})`,'),
    ('trustOptions.push({ label: "Trust (this session only)", trusted: true, updates: [] });',
     'trustOptions.push({ label: "信任（仅本次会话）", trusted: true, updates: [] });'),
    ('label: "Do not trust",', 'label: "不信任",'),
    ('trustOptions.push({ label: "Do not trust (this session only)", trusted: false, updates: [] });',
     'trustOptions.push({ label: "不信任（仅本次会话）", trusted: false, updates: [] });'),
], "trust-manager")

# ============ 11. user-message-selector.js ============
patch(ROOT / "modes/interactive/components/user-message-selector.js", [
    ('theme.fg("muted", "  No user messages found")', 'theme.fg("muted", "  未找到用户消息")'),
    ('theme.bold("Fork from Message")', 'theme.bold("从消息创建分叉")'),
    ('"Select a user message to copy the active path up to that point into a new session"',
     '"选择一条用户消息，将到该点为止的活动路径复制到新会话中"'),
], "user-message-selector")

# ============ 12. thinking-selector.js ============
patch(ROOT / "modes/interactive/components/thinking-selector.js", [
    ('off: "No reasoning"', 'off: "不进行推理"'),
    ('minimal: "Very brief reasoning (~1k tokens)"', 'minimal: "极简推理（约 1k tokens）"'),
    ('low: "Light reasoning (~2k tokens)"', 'low: "轻度推理（约 2k tokens）"'),
    ('medium: "Moderate reasoning (~8k tokens)"', 'medium: "中等推理（约 8k tokens）"'),
    ('high: "Deep reasoning (~16k tokens)"', 'high: "深度推理（约 16k tokens）"'),
    ('xhigh: "Extra-high reasoning (~32k tokens)"', 'xhigh: "超高推理（约 32k tokens）"'),
    ('max: "Maximum reasoning"', 'max: "最大推理"'),
], "thinking-selector")

# ============ 13. theme-selector.js ============
patch(ROOT / "modes/interactive/components/theme-selector.js", [
    ('description: name === currentTheme ? "(current)" : undefined,', 'description: name === currentTheme ? "（当前）" : undefined,'),
], "theme-selector")

# ============ 14. scoped-models-selector.js ============
patch(ROOT / "modes/interactive/components/scoped-models-selector.js", [
    ('theme.bold("Model Configuration")', 'theme.bold("模型配置")'),
    ('`Session-only. ${keyText("app.models.save")} to save to settings.`', '`仅本次会话。按 ${keyText("app.models.save")} 保存到设置。`'),
    ('theme.fg("muted", "  No matching models")', 'theme.fg("muted", "  没有匹配的模型")'),
    ('? " [unavailable]"', '? " [不可用]"'),
    (': "Model unavailable"`', ': "模型不可用"`'),
    ('`  ${selected.model ? `Model Name: ${selected.model.name}` : "Model unavailable"}`',
     '`  ${selected.model ? `模型名称：${selected.model.name}` : "模型不可用"}`'),
    ('? "all enabled"\n            : `${enabledCount}/${this.allIds.length} enabled${unavailableCount ? ` · ${unavailableCount} unavailable` : ""}`;',
     '? "全部启用"\n            : `${enabledCount}/${this.allIds.length} 已启用${unavailableCount ? ` · ${unavailableCount} 不可用` : ""}`;'),
    ('`${keyText("tui.select.confirm")} toggle`,', '`${keyText("tui.select.confirm")} 切换`,'),
    ('`${keyText("app.models.enableAll")} all`,', '`${keyText("app.models.enableAll")} 全部`,'),
    ('`${keyText("app.models.clearAll")} clear`,', '`${keyText("app.models.clearAll")} 清除`,'),
    ('`${keyText("app.models.toggleProvider")} provider`,', '`${keyText("app.models.toggleProvider")} 提供商`,'),
    ('`${keyText("app.models.reorderUp")}/${keyText("app.models.reorderDown")} reorder`,', '`${keyText("app.models.reorderUp")}/${keyText("app.models.reorderDown")} 排序`,'),
    ('`${keyText("app.models.save")} save`,', '`${keyText("app.models.save")} 保存`,'),
    ('theme.fg("warning", "(unsaved)")', 'theme.fg("warning", "（未保存）")'),
], "scoped-models-selector")

# ============ 15. config-selector.js ============
patch(ROOT / "modes/interactive/components/config-selector.js", [
    ('extensions: "Extensions",', 'extensions: "扩展",'),
    ('skills: "Skills",', 'skills: "技能",'),
    ('prompts: "Prompts",', 'prompts: "提示模板",'),
    ('themes: "Themes",', 'themes: "主题",'),
    ('? `User (${formatBaseDir(metadata.baseDir)})`\n                : `Project (${formatBaseDir(metadata.baseDir)})`;',
     '? `用户（${formatBaseDir(metadata.baseDir)}）`\n                : `项目（${formatBaseDir(metadata.baseDir)}）`;'),
    ('return metadata.scope === "user" ? `User (${formatBaseDir(agentDir)})` : `Project (${CONFIG_DIR_NAME}/)`;',
     'return metadata.scope === "user" ? `用户（${formatBaseDir(agentDir)}）` : `项目（${CONFIG_DIR_NAME}/）`;'),
    ('return metadata.scope === "user" ? "User settings" : "Project settings";',
     'return metadata.scope === "user" ? "用户设置" : "项目设置";'),
    ('theme.bold(this.writeScope === "project" ? "Project Local Resources" : "Global Resources")',
     'theme.bold(this.writeScope === "project" ? "项目本地资源" : "全局资源")'),
    ('keyHint("tui.input.tab", "switch mode")', 'keyHint("tui.input.tab", "切换模式")'),
    ('rawKeyHint("space", "cycle inherit/+/-")', 'rawKeyHint("space", "循环 继承/+/-")'),
    ('rawKeyHint("space", "toggle")', 'rawKeyHint("space", "切换")'),
    ('rawKeyHint("esc", "close")', 'rawKeyHint("esc", "关闭")'),
    ('theme.fg("muted", `${CONFIG_DIR_NAME}/settings.json · inherited global resources are dimmed`)',
     'theme.fg("muted", `${CONFIG_DIR_NAME}/settings.json · 继承的全局资源以暗色显示`)'),
    ('theme.fg("muted", "  No resources found")', 'theme.fg("muted", "  未找到资源")'),
    ('`${entry.group.label}${inherited ? " · inherited global" : ""}`', '`${entry.group.label}${inherited ? " · 继承自全局" : ""}`'),
    ('return theme.fg("muted", "  project load");', 'return theme.fg("muted", "  项目加载");'),
    ('return theme.fg("muted", "  project unload");', 'return theme.fg("muted", "  项目卸载");'),
    ('return this.isInheritedGlobalItem(item) ? theme.fg("dim", "  inherited global") : "";',
     'return this.isInheritedGlobalItem(item) ? theme.fg("dim", "  继承自全局") : "";'),
], "config-selector")

# ============ 16. tree-selector.js ============
patch(ROOT / "modes/interactive/components/tree-selector.js", [
    ('`  ${theme.fg("muted", "Type to search:")} ${theme.fg("accent", query)}`', '`  ${theme.fg("muted", "输入以搜索:")} ${theme.fg("accent", query)}`'),
    ('`  ${theme.fg("muted", "Type to search:")}`', '`  ${theme.fg("muted", "输入以搜索:")}`'),
    ('`${indent}${theme.fg("muted", "Label (empty to remove):")}`', '`${indent}${theme.fg("muted", "标签（留空移除）:")}`'),
    ('truncateToWidth(theme.fg("muted", "  No entries found"), width)', 'truncateToWidth(theme.fg("muted", "  未找到条目"), width)'),
    ('theme.fg("success", "assistant: ") + theme.fg("muted", "(aborted)")', 'theme.fg("success", "assistant: ") + theme.fg("muted", "（已中止）")'),
    ('theme.fg("success", "assistant: ") + theme.fg("muted", "(no content)")', 'theme.fg("success", "assistant: ") + theme.fg("muted", "（无内容）")'),
    ('`[label: ${entry.label ?? "(cleared)"}]`', '`[标签: ${entry.label ?? "（已清除）"}]`'),
    ('theme.italic(theme.fg("dim", "empty"))', 'theme.italic(theme.fg("dim", "空"))'),
    ('labels += " [no-tools]";', 'labels += " [无工具]";'),
    ('labels += " [user]";', 'labels += " [用户]";'),
    ('labels += " [labeled]";', 'labels += " [已标记]";'),
    ('{ keys: ["tui.select.up", "tui.select.down"], label: "move" },', '{ keys: ["tui.select.up", "tui.select.down"], label: "移动" },'),
    ('{ keys: ["tui.editor.cursorLeft", "tui.editor.cursorRight"], label: "page" },', '{ keys: ["tui.editor.cursorLeft", "tui.editor.cursorRight"], label: "翻页" },'),
    ('{ keys: ["app.tree.foldOrUp", "app.tree.unfoldOrDown"], label: "branch" },', '{ keys: ["app.tree.foldOrUp", "app.tree.unfoldOrDown"], label: "分支" },'),
    ('{ keys: ["app.message.copy"], label: "copy" },', '{ keys: ["app.message.copy"], label: "复制" },'),
    ('{ keys: ["app.tree.editLabel"], label: "label" },', '{ keys: ["app.tree.editLabel"], label: "标签" },'),
    ('{ keys: ["app.tree.toggleLabelTimestamp"], label: "label time" },', '{ keys: ["app.tree.toggleLabelTimestamp"], label: "标签时间" },'),
    ('label: "filters",', 'label: "过滤",'),
    ('label: "cycle",', 'label: "循环",'),
], "tree-selector")

# ============ 17. assistant-message.js ============
patch(ROOT / "modes/interactive/components/assistant-message.js", [
    ('hiddenThinkingLabel = "Thinking..."', 'hiddenThinkingLabel = "思考中..."'),
    ('"Error: Model stopped because it reached the maximum output token limit. The response may be incomplete."',
     '"错误：模型已达到最大输出令牌数限制而停止。回复可能不完整。"'),
    ('? message.errorMessage\n                    : "Operation aborted";',
     '? message.errorMessage\n                    : "操作已中止";'),
    ('const errorMsg = message.errorMessage || "Unknown error";', 'const errorMsg = message.errorMessage || "未知错误";'),
    ('`Error: ${errorMsg}`', '`错误：${errorMsg}`'),
    ('"Request was aborted"', '"请求已中止"'),
], "assistant-message")

# ============ 18. compaction/branch summary ============
patch(ROOT / "modes/interactive/components/compaction-summary-message.js", [
    ('`\\x1b[1m[compaction]\\x1b[22m`', '`\\x1b[1m[压缩]\\x1b[22m`'),
    ('`**Compacted from ${tokenStr} tokens**\\n\\n`', '`**已从 ${tokenStr} 个令牌压缩**\\n\\n`'),
    ('" to expand)")', '" 展开)")'),
], "compaction-summary")
patch(ROOT / "modes/interactive/components/branch-summary-message.js", [
    ('`\\x1b[1m[branch]\\x1b[22m`', '`\\x1b[1m[分支]\\x1b[22m`'),
    ('const header = "**Branch Summary**\\n\\n";', 'const header = "**分支摘要**\\n\\n";'),
    ('theme.fg("customMessageText", "Branch summary (")', 'theme.fg("customMessageText", "分支摘要（")'),
    ('theme.fg("customMessageText", " to expand)")', 'theme.fg("customMessageText", " 展开）")'),
], "branch-summary")

# ============ 19. show-images-selector ============
patch(ROOT / "modes/interactive/components/show-images-selector.js", [
    ('{ value: "yes", label: "Yes", description: "Show images inline in terminal" },',
     '{ value: "yes", label: "是", description: "在终端中内联显示图片" },'),
    ('{ value: "no", label: "No", description: "Show text placeholder instead" },',
     '{ value: "no", label: "否", description: "改为显示文本占位符" },'),
], "show-images-selector")

print("=== 全部文件补丁完成 ===")
