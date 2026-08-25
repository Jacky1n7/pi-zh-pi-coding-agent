# Pi 中文补丁手工维护流程

本文用于 Pi 或其依赖升级后，基于新版英文文件手工维护中文补丁。核心原则是始终保留两份临时工作副本：`pristine`（英文原版）与 `localized`（手工汉化版），然后由生成器提取、回放并验证替换对。

## 1. 确认版本与安装位置

```bash
pi --version
npm root -g

PI_ZH_PACKAGE_ROOT="$(npm root -g)/@earendil-works/pi-coding-agent"
PI_ZH_DIST="$PI_ZH_PACKAGE_ROOT/dist"
node -p "require('$PI_ZH_PACKAGE_ROOT/package.json').version"
node -p "require('$PI_ZH_PACKAGE_ROOT/node_modules/@earendil-works/pi-tui/package.json').version"
```

如果正在维护的安装已经打过汉化补丁，先重新安装对应版本以恢复英文原版，再继续。不要使用已汉化目录作为 `pristine`，否则生成器会遗漏补丁。

## 2. 建立主程序双副本

在仓库外或仓库的 `work/` 中创建临时目录：

```bash
PI_ZH_WORK="work/pi-zh-next"
mkdir -p "$PI_ZH_WORK/pristine" "$PI_ZH_WORK/localized"
cp "$PI_ZH_PACKAGE_ROOT/package.json" "$PI_ZH_WORK/pristine/package.json"
cp "$PI_ZH_PACKAGE_ROOT/package.json" "$PI_ZH_WORK/localized/package.json"
cp -R "$PI_ZH_DIST" "$PI_ZH_WORK/pristine/dist"
cp -R "$PI_ZH_DIST" "$PI_ZH_WORK/localized/dist"
```

只编辑 `localized/dist`，不得编辑 `pristine/dist`。

## 3. 手工翻译主程序

优先检查已有补丁在新版上的匹配情况：

```bash
python3 pi-zh-apply.py --dist "$PI_ZH_WORK/localized/dist" --no-dependencies
```

脚本会先复用仍然匹配的旧翻译，并列出新版中未匹配的项目。随后在 `localized/dist` 中手工处理：

1. 根据未匹配输出定位新版文件。
2. 对照 `patches.json` 中旧版的中文译文。
3. 只翻译用户可见字符串，不改变量名、控制流程、导入或函数调用。
4. 保留命令名、参数名、模型 ID、配置键与代码符号。
5. 动态模板字符串中的 `${...}` 表达式必须原样保留。

常见文件包括：

- `cli/args.js`：`pi --help`
- `core/slash-commands.js`：斜杠命令描述
- `modes/interactive/interactive-mode.js`：启动与会话界面
- `modes/interactive/components/settings-selector.js`：设置项目
- `modes/interactive/components/*.js`：各类选择器与状态提示

## 4. 重新生成主补丁

```bash
python3 generate-patches.py \
  --pristine "$PI_ZH_WORK/pristine/dist" \
  --localized "$PI_ZH_WORK/localized/dist" \
  --output patches.json
```

生成器必须输出：

- `[TODO] 校验失败文件: []`
- 文件数和替换条数符合预期
- `patches.json` 的键统一使用 `/`，不得含 Windows `\` 分隔符

## 5. 维护 pi-tui 依赖汉化

依赖补丁单独保存于 `dependency-patches.json`。先建立双副本：

```bash
PI_ZH_TUI_ROOT="$PI_ZH_PACKAGE_ROOT/node_modules/@earendil-works/pi-tui"
PI_ZH_TUI_WORK="work/pi-tui-next"
mkdir -p "$PI_ZH_TUI_WORK/pristine" "$PI_ZH_TUI_WORK/localized"
cp "$PI_ZH_TUI_ROOT/package.json" "$PI_ZH_TUI_WORK/pristine/package.json"
cp "$PI_ZH_TUI_ROOT/package.json" "$PI_ZH_TUI_WORK/localized/package.json"
cp -R "$PI_ZH_TUI_ROOT/dist" "$PI_ZH_TUI_WORK/pristine/dist"
cp -R "$PI_ZH_TUI_ROOT/dist" "$PI_ZH_TUI_WORK/localized/dist"
```

手工编辑 `localized/dist` 后生成依赖补丁：

```bash
PI_ZH_TUI_VERSION="$(node -p "require('$PI_ZH_TUI_ROOT/package.json').version")"
python3 generate-patches.py \
  --pristine "$PI_ZH_TUI_WORK/pristine/dist" \
  --localized "$PI_ZH_TUI_WORK/localized/dist" \
  --package @earendil-works/pi-tui \
  --version "$PI_ZH_TUI_VERSION" \
  --output dependency-patches.json
```

如果未来需要同时维护多个依赖，生成到临时 JSON 后，将新的包节点合并进现有 `dependency-patches.json`，不要覆盖其他包节点。

## 6. 更新版本标记

同步修改：

- `pi-zh-apply.py` 中的 `PATCHSET_PI_VERSION`
- `README.md` 中的兼容版本、文件数和替换数
- `dependency-patches.json` 中每个依赖的 `version`

## 7. 在全新副本中验证

不要直接拿已用于翻译的 `localized` 副本做最终验证。重新从英文原版复制一份 `verify`：

```bash
PI_ZH_VERIFY="$PI_ZH_WORK/verify"
mkdir -p "$PI_ZH_VERIFY"
cp "$PI_ZH_PACKAGE_ROOT/package.json" "$PI_ZH_VERIFY/package.json"
cp -R "$PI_ZH_DIST" "$PI_ZH_VERIFY/dist"
ln -s "$PI_ZH_PACKAGE_ROOT/node_modules" "$PI_ZH_VERIFY/node_modules"

python3 pi-zh-apply.py --dist "$PI_ZH_VERIFY/dist"
python3 pi-zh-apply.py --dist "$PI_ZH_VERIFY/dist" --check
node "$PI_ZH_VERIFY/dist/bundle/cli.js" --version
node "$PI_ZH_VERIFY/dist/bundle/cli.js" --help
python3 -m unittest discover -s tests -v
```

验收条件：

- 主程序与依赖均为 `0 条待处理, 0 条未匹配`
- `运行入口: 已切换`
- `pi --version` 正常
- `pi --help` 为中文且命令参数未损坏
- 全部单元测试通过
- 对修改过的 JavaScript 文件执行 `node --check` 无语法错误

最后以离线、无会话保存模式启动真实 TUI，检查启动页、`/settings`、模型选择器和会话选择器：

```bash
pi --offline --no-session --no-extensions --no-context-files --approve
```

## 8. 应用与提交

验证通过后再应用到实际安装：

```bash
python3 pi-zh-apply.py
python3 pi-zh-apply.py --check
```

然后提交维护分支：

```bash
git add README.md docs/maintenance.md generate-patches.py \
  pi-zh-apply.py patches.json dependency-patches.json tests/
git commit -m "feat: localize Pi TUI dependency"
git push
```

Pi 更新或重新安装会覆盖本地汉化文件。升级后应重新执行上述版本核对与双副本流程，不能默认旧补丁继续兼容。
