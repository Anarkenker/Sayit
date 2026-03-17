# sayit

中文 | [English](README.md)

`sayit` 是一个 Python CLI，用来把短句、冒犯、别扭、不适合直接发出去的话，改写成更得体、更可发送的表达。

它不是聊天机器人，也不是长文写作助手。

## 简介

项目边界很明确：

- 短输入
- 短输出
- 明确社交意图
- 受控改写，不做自由生成

典型输入：

- `你这个怎么还没弄完`
- `这个价格太高了`
- `我今天不想去了`
- `你先把钱转我`
- `我这边要延期`

典型输出：

- `polite`
- `direct`
- `firm`
- `soft`

`sayit explain` 会额外告诉你：

- 识别到的意图
- 风险点
- 改写策略

## 当前能力

- 中文优先的本地改写引擎
- 意图识别与风险识别
- 基于规则的 planner
- 基于 YAML 的模板系统
- 支持 `argv`、`stdin`、文件、剪贴板输入
- 支持 `pretty`、`plain`、`json` 输出
- 支持 `explain` 命令
- 预留 OpenAI-compatible provider 接口
- 支持 `local`、`ai`、`hybrid` 模式

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

也可以直接用 `pipx` 安装本地仓库：

```bash
pipx install .
```

安装后即可直接运行：

```bash
sayit "你这个怎么还没弄完"
```

如果还没安装包，也可以这样运行：

```bash
PYTHONPATH=src python -m sayit "你这个怎么还没弄完"
```

## API Key 放置方式

不要把真实 API key 写进源码或配置文件。

推荐做法：

1. 把真实 key 放到环境变量
2. 配置文件里只保存环境变量名
3. 提交 `.env.example`，不要提交 `.env`

### 本地开发

先创建 `.env`：

```bash
cp .env.example .env
```

然后填入你要用的 key：

```bash
OPENAI_API_KEY=your_real_key_here
OPENROUTER_API_KEY=
```

程序会在运行时自动加载 `.env`。

### 生产或 CI

推荐直接使用系统或平台环境变量：

```bash
export OPENAI_API_KEY="your_real_key_here"
```

### 配置文件位置

用户配置文件位于：

```text
~/.config/sayit/config.toml
```

配置文件应该保存这种内容，而不是保存 secret 本身：

```toml
[providers.openai]
base_url = "https://api.openai.com/v1"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"
```

## 快速开始

### 本地模式，无需 API

```bash
sayit "你这个怎么还没弄完"
sayit "我今天不想去了" --tone soft
sayit explain "这个价格太高了"
```

### AI 或 Hybrid 模式

```bash
sayit "这个价格太高了" --mode ai
sayit "你这个怎么还没弄完" --mode hybrid
```

默认行为：

- 没有可用 provider 时，走 `local`
- 有可用 provider 时，默认走 `hybrid`

## 用法

### 直接输入

```bash
sayit "你这个怎么还没弄完"
```

### 剪贴板

```bash
sayit --clipboard
```

### 文件输入

```bash
sayit draft.txt
```

### 标准输入

```bash
pbpaste | sayit
cat raw.txt | sayit --plain
```

### Explain 模式

```bash
sayit explain "你先把钱转我"
```

### 常用参数

```bash
sayit "这个价格太高了" --context bargain
sayit "今天给我答复" --tone firm
sayit "我今天来不了" --context social --tone soft
sayit "这个事情要延期" --audience client
sayit "这个事情要延期" --mode ai
sayit "这个价格太高了" --json
```

## 命令

```bash
sayit "..."
sayit explain "..."
sayit config init
sayit config show
sayit providers list
sayit providers test
sayit templates list
```

## 输出格式

### `pretty`

适合人类直接阅读，包含：

- 原文
- 意图
- 风险点
- 改写候选

### `plain`

只输出候选文案，适合复制或管道传递。

```bash
sayit "你这个怎么还没弄完" --plain
```

### `json`

适合脚本或其他工具集成。

```bash
sayit "这个价格太高了" --json
```

## 运行模式

### `local`

- 不需要 API
- 快、稳定、可预测
- 由本地规则和模板驱动

### `ai`

- 全部候选生成交给 provider
- 更适合复杂或细腻语气
- 需要 provider 配置和运行时 key

### `hybrid`

- 本地先做 detector 和 planner
- provider 负责受控生成
- provider 出问题时可以回落到本地

## 项目结构

```text
src/sayit/
  cli.py
  main.py
  app/
  domain/
  engines/
  infra/
  input/
  output/
  templates/
tests/
```

## 开发

运行测试：

```bash
pytest
```

列出模板：

```bash
sayit templates list
```

查看 provider 状态：

```bash
sayit providers list
sayit providers test
```

初始化用户配置：

```bash
sayit config init
```

## 已知限制

- 中文模板明显强于英文支持。
- AI 模式已经接上接口，但还需要更多真实场景验证。
- 本地引擎故意保守，只覆盖高频短场景。
- 没有 GUI、聊天记录导入或自动发送。

## 路线图

- 扩展 6 个核心意图的规则和模板
- 增加英文模板和测试
- 增加稳定的快照测试
- 加强事实保全和“禁止乱编理由”的校验
- 补强 provider 错误处理和集成覆盖
- 发布到 PyPI，支持 `pipx install sayit`

## 开源说明

这个仓库已经具备首个公开版本的基础结构：

- 清晰 README
- `.gitignore`
- `.env.example`
- 基础 CI
- 本地 MVP

公开前还要记得把仓库占位符替换掉：

- `pyproject.toml`
- `.github/ISSUE_TEMPLATE/config.yml`

## 贡献

贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 变更记录

变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。

## 设计原则

- 受控生成优先于自由生成
- 默认不乱编事实
- 先解决高频小场景
- 解释能力和文案质量同样重要
