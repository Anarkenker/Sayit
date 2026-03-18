# sayit

<p align="center">
  <img src="assets/logo-wordmark.svg" width="700" alt="sayit logo">
</p>

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml/badge.svg)](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml)
[![Docker First](https://img.shields.io/badge/Run%20with-Docker-2496ED?logo=docker&logoColor=white)](README.zh-CN.md#quick-start)
[![Status](https://img.shields.io/badge/Status-Alpha-orange)](README.zh-CN.md#项目状态)

中文 | [English](README.md)

`sayit` 是一个专注于短消息改写的 CLI 工具，用来把不够顺口、太冲、太硬、或不适合直接发出去的短句，改成更自然、更稳妥、更容易发送的版本。它面向短句，不是长文写作工具，也尽量避免编造事实。

## 适合做什么

- 催进度、提醒、拒绝、改期、道歉
- 议价、表达不满、提出敏感请求
- 把语气太硬、太像命令的话改得更顺一点
- 例如：`你这个怎么还没弄完` `你先把钱转我` `这个价格太高了`

## 不打算做什么

- 写长邮件、长文章或完整对话
- 编造事实或理由
- 包装骚扰、威胁、操控、欺骗或规避责任的话术

## 特点

- 一次生成多个不同语气的候选版本
- 生成前先做本地意图和风险分析
- 支持通过 `sayit tui` 进入终端交互界面
- 支持 `argv`、`stdin`、文件和剪贴板输入
- 支持 `pretty`、`plain`、`json` 输出
- 默认通过 Docker 运行

## Quick Start

```bash
git clone https://github.com/Anarkenker/sayit.git
cd sayit
./setup
# 编辑 .env，填入 OPENAI_API_KEY=...
sayit "你这个怎么还没弄完"
```

如果 `./setup` 后当前终端里还找不到 `sayit`，重新打开一次终端即可；如果还需要手动补 `PATH`，`setup` 会直接打印对应命令。

运行示例：

```bash
sayit "这个价格太高了"
sayit "这个价格太高了" --context bargain
sayit explain "我今天不想去了"
sayit tui
sayit "这个价格太高了" --json
echo "这个价格太高了" | sayit --plain
sayit draft.txt
```

## 命令总览

```bash
# 初始化
./setup

# 帮助
sayit --help
sayit rewrite --help
sayit explain --help
sayit tui --help
sayit config --help
sayit providers --help
sayit rules --help

# 终端界面
sayit tui

# 改写（默认子命令）
sayit [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--variants 1-6] [--mode auto|ai] [--language TEXT] [--clipboard] [--plain|--json]
sayit rewrite [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--variants 1-6] [--mode auto|ai] [--language TEXT] [--clipboard] [--plain|--json]

# 分析
sayit explain [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--mode auto|ai] [--language TEXT] [--clipboard] [--json]

# 配置
sayit config init [--force]
sayit config show

# Provider 检查
sayit providers list
sayit providers test

# 规则查看
sayit rules list [--language TEXT]
```

## 参数说明

- `sayit "..."` 等价于 `sayit rewrite "..."`。
- `sayit tui`：打开交互式终端菜单。
- `TEXT_OR_PATH`：原始文本或文件路径。省略时读取 stdin，`--clipboard` 时读取剪贴板。
- `--context`：`work` `social` `email` `bargain` `support`
- `--tone`：`polite` `direct` `firm` `soft`
- `--audience TEXT`：指定对象。
- `--variants`：`1-6`，默认 `3`，仅 `rewrite`。
- `--mode`：`auto` `ai`，默认 `auto`。
- `--language TEXT`：手动指定语言。
- `--plain`：只输出候选文本，仅 `rewrite`。
- `--json`：输出 JSON。
- `--plain` 和 `--json` 不能同时使用。
- `config init --force`：覆盖已有配置文件。
- `rules list --language TEXT`：指定规则语言，默认 `zh`。
- `providers list`：列出 provider、model、base URL 和环境状态。
- `providers test`：检查当前 provider 配置是否可用。

## 配置

默认使用方式需要：

- Docker / Docker Desktop
- 可用的模型服务 API key
- 项目根目录中的 `.env`

官方 OpenAI：

```env
OPENAI_API_KEY=your_api_key_here
```

兼容 OpenAI 接口的其他服务：

```env
SAYIT_PROVIDER_DEFAULT=custom
SAYIT_CUSTOM_BASE_URL=https://your-provider.example.com/v1
SAYIT_CUSTOM_MODEL=your-model-name
SAYIT_CUSTOM_API_KEY=your_api_key_here
```

用户配置：

```bash
sayit config init
sayit config show
```

用户配置文件路径是 `~/.config/sayit/config.toml`，适合保存默认语言、候选数量、模式或输出格式。`.env` 不应提交到 GitHub。

## 工作方式

- `sayit` 通过模型服务生成候选文案。
- 生成前会先做一层本地检测和规划，用来判断意图、识别风险，并给生成过程提供更稳的方向。

## 故障排查

- `Cannot connect to the Docker daemon`：启动 Docker Desktop 后重试。
- `No available AI provider configured`：检查 `.env` 和 API key。
- 网络错误：检查网络连通性、代理设置或服务可用性。

## 开发

```bash
pytest
PYTHONPATH=src python -m sayit providers list
PYTHONPATH=src python -m sayit providers test
PYTHONPATH=src python -m sayit rules list
```

贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目状态

`sayit` 当前处于 **alpha** 阶段，接口、规则、输出细节和配置方式都仍有可能调整。

## 变更记录

变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

许可证见 [LICENSE](LICENSE)。
