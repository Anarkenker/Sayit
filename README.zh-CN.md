# sayit

<p align="center">
  <img src="assets/logo-wordmark.svg" width="240" alt="sayit logo">
</p>

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml/badge.svg)](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml)
[![Docker First](https://img.shields.io/badge/Run%20with-Docker-2496ED?logo=docker&logoColor=white)](README.zh-CN.md#quick-start)
[![Status](https://img.shields.io/badge/Status-Alpha-orange)](README.zh-CN.md#项目状态)

中文 | [English](README.md)

`sayit` 是一个专注于**消息措辞优化**的 CLI 小工具。  
它用来把那些**不够顺口、不够得体、太冲、太硬、或不适合直接发出去的短句**，改写成几个**更稳妥、更自然、更可发送**的版本。

它不是聊天机器人，也不是长文写作助手。  
它更像一个专门处理“消息怎么说更合适”的工具：**输入尽量短，输出也尽量短，尽量直接可复制，尽量不编造事实。**

---

## 适合做什么

`sayit` 适合处理这类场景：

- 催进度，但不想显得太冲
- 拒绝、改期、请假、婉拒
- 请求、提醒、跟进、道歉
- 议价、协商、表达不满
- 把“太像命令”的话改得更顺一点
- 把“有点冒犯或别扭”的话改成更适合发送的版本

例如：

- `你这个怎么还没弄完`
- `你先把钱转我`
- `这个价格太高了`
- `我今天不想去了`

---

## 不打算做什么

`sayit` 的目标是改善表达，不是替用户包装不当意图。它不适合用来：

- 生成长文、邮件、文章或完整对话
- 编造事实、替用户虚构理由
- 包装威胁、骚扰、操控、欺骗或规避责任的话术
- 替代用户对事实准确性和发送后果的判断

---

## 特点

- 面向**短句改写**，不是通用写作工具
- 一次生成几个不同语气的候选版本
- 请求发出前会先做一层**本地分析和规划**
- 尽量降低“太冲”“太模糊”“太像命令”这类风险
- 支持 `argv`、`stdin`、文件和剪贴板输入
- 支持 `pretty`、`plain`、`json` 三种输出格式
- 默认通过 Docker 运行，减少本地环境差异

---

## Quick Start

第一次使用时，在项目根目录执行：

```bash
git clone https://github.com/Anarkenker/sayit.git
cd sayit
./setup
# setup 会安装 sayit 命令，并准备 .env
# 打开 .env，把 OPENAI_API_KEY= 后面换成你自己的 key
sayit "你这个怎么还没弄完"
```

如果运行完 `./setup` 之后，当前终端还提示找不到 `sayit`，重新打开一次终端即可；少数情况下，`setup` 也会直接告诉你需要补哪一条 `PATH` 配置。

更多示例：

```bash
sayit "这个价格太高了"
sayit "这个价格太高了" --context bargain
sayit explain "我今天不想去了"
sayit "这个价格太高了" --json
echo "这个价格太高了" | sayit --plain
sayit draft.txt
```

---

## 命令总览

如果你只是想快速查命令，不想在 README 里到处翻，可以直接看这一段。`sayit "..."` 是最常用的入口，等价于显式写 `sayit rewrite "..."`；除此之外，项目还提供分析命令、配置命令、provider 检查命令和规则查看命令。下面这些基本就是日常会用到的完整命令集合：

```bash
# 初始化
./setup

# 最常见用法
sayit "你这个怎么还没弄完"
sayit rewrite "你这个怎么还没弄完"
sayit explain "我今天不想去了"

# 输入来源
sayit draft.txt
sayit --clipboard
echo "这个价格太高了" | sayit
echo "这个价格太高了" | sayit --plain

# 常用改写参数
sayit "这个价格太高了" --context bargain
sayit "今天给我答复" --tone firm
sayit "我今天来不了" --context social --tone soft
sayit "这个事情要延期" --audience client
sayit "你这个怎么还没弄完" --variants 3
sayit "你这个怎么还没弄完" --mode auto
sayit "你这个怎么还没弄完" --mode ai
sayit "你这个怎么还没弄完" --language zh

# 输出格式
sayit "这个价格太高了" --plain
sayit "这个价格太高了" --json
sayit explain "你先把钱转我" --json

# 配置和检查
sayit config init
sayit config show
sayit providers list
sayit providers test
sayit rules list
```

其中最常用的参数包括：`--context`、`--tone`、`--audience`、`--variants`、`--mode`、`--language`、`--plain` 和 `--json`。通常来说，`--context` 用来帮助判断场景，`--tone` 用来控制语气，`--plain` 适合复制粘贴，`--json` 适合脚本调用；`--plain` 和 `--json` 不能同时使用。

---

## 参数说明

如果你看到命令里带了很多参数，但一时不知道它们分别是做什么的，可以直接看这里。`sayit` 的参数并不多，核心上分成三类：控制输入来源、控制改写方向、控制输出形式。

### 输入相关

- `sayit "..."`：直接把命令里的短句当成输入，这是最常见的用法。
- `sayit draft.txt`：把文件内容当成输入。
- `echo "..." | sayit`：前面的命令先输出一段文本，竖线 `|` 再把这段文本直接交给 `sayit`。如果你前一个命令已经产生了文本，这种写法会很方便。
- `--clipboard`：从剪贴板读取输入。如果你当前环境不适合读剪贴板，这个选项就不太好用。

### 改写相关

- `--context`：指定场景，帮助工具更稳定地判断这句话是在做什么。比如 `work`、`social`、`bargain`、`email`、`support`。当一句话比较短、比较模糊时，这个参数很有用。
- `--tone`：指定你想要的语气风格。当前支持 `polite`、`direct`、`firm`、`soft`。如果不指定，工具会按默认顺序给出几种不同风格。
- `--audience`：指定对象，例如 `client`、`boss`、`friend`、`colleague`。它会影响生成时的措辞倾向。
- `--variants`：指定返回几个候选版本，默认是 `3`。
- `--mode`：指定运行模式。当前常用的是 `auto` 和 `ai`。大多数情况下用默认值就够了。
- `--language`：手动指定语言，例如 `zh` 或 `en`。如果不写，工具会自动判断。

### 输出相关

- `--plain`：只输出纯文本候选，不带分析和额外结构，适合复制粘贴。
- `--json`：输出结构化 JSON，适合脚本调用或程序集成。
- `explain`：不是改写，而是分析。它会告诉你这句话更接近什么意图、有哪些风险点、建议采用什么策略。

### 配置和检查命令

- `config init`：生成用户配置文件。
- `config show`：显示当前配置。
- `providers list`：查看当前支持哪些服务，以及哪些 key 已经配好。
- `providers test`：快速检查当前 provider 配置是否可用。
- `rules list`：查看当前内置规则。

通常来说，如果你只是日常使用，最值得记住的就是这几个：

```bash
sayit "..."
sayit explain "..."
sayit "..." --context bargain
sayit "..." --tone polite
sayit "..." --plain
sayit "..." --json
```

---

## 示例

输入：

```bash
sayit "你这个怎么还没弄完"
```

示例输出（实际结果会因上下文和模型而不同）：

```text
- 想跟你确认一下，这部分现在进展到哪一步了？
- 方便同步一下当前状态吗？
- 这件事大概还需要多久能处理完？
```

输入：

```bash
sayit explain "你先把钱转我"
```

示例输出：

```text
意图：请求
风险点：语气偏硬，容易显得像直接命令
策略：保留核心诉求，降低命令感，补足礼貌和缓冲
```

---

## 运行方式

仓库根目录提供了一个初始化脚本 `./setup`。它会尽量把日常使用需要的 Docker 细节包起来，并在第一次运行时把 `sayit` 命令安装到你的终端环境里。对大多数用户来说，正常流程就是先运行一次 `./setup`，之后就直接使用 `sayit`。

`sayit` 主要面向 macOS 和常见 shell 环境；在其他平台上，也仍然可以直接使用 Docker 命令运行。

---

## 环境要求

在默认使用方式下，你需要：

* Docker / Docker Desktop
* 一个可用的模型服务 API key
* 项目根目录中的 `.env`

---

## 配置

### `.env`

第一次使用时，你真正需要改的配置，通常只有项目根目录里的 `.env`。如果这个文件还不存在，先运行一次 `./setup`，它会自动按照仓库中的 `.env.example` 帮你生成出来。`.env` 只应该保留在你自己的机器上，**不要提交到 GitHub**，因为这里面可能会放你自己的 key。

如果你使用的是官方 OpenAI，那么 `.env` 里通常只需要改一行，就是把 `OPENAI_API_KEY=` 后面换成你自己的 key。你不需要再额外填写 URL，也不需要改代码里的其他地方；默认地址已经在项目里配好了。最常见的写法就是下面这样：

```env
OPENAI_API_KEY=your_api_key_here
```

这里有几个细节最好一起注意一下：key 直接写在等号后面就行，不要额外加引号，不要在前后留空格，也不要拆成多行。如果你填好以后不确定自己有没有写对，最简单的办法就是直接回到终端执行一次命令看能不能正常返回结果：

```bash
sayit "你这个怎么还没弄完"
```

如果这是你第一次配置，建议按下面这个顺序做，基本不会出错：先运行 `./setup`，让项目自动生成 `.env` 并安装 `sayit` 命令；然后用文本编辑器打开项目根目录里的 `.env`；把 `OPENAI_API_KEY=` 这一行补完整；保存；最后回到终端执行 `sayit "你这个怎么还没弄完"`。对绝大多数用户来说，这一步做完就已经够了，后面的配置都可以先不看。

### 使用兼容 OpenAI 接口的其他服务

如果你不使用官方 OpenAI，而是使用另一个兼容 OpenAI 接口的服务，那么才需要改更多几项。这种情况下，你需要明确告诉 `sayit`：默认使用自定义 provider、请求发到哪个地址、模型名是什么、key 是什么。`.env` 可以写成下面这样：

```env
SAYIT_PROVIDER_DEFAULT=custom
SAYIT_CUSTOM_BASE_URL=https://your-provider.example.com/v1
SAYIT_CUSTOM_MODEL=your-model-name
SAYIT_CUSTOM_API_KEY=your_api_key_here
```

这几项里最容易混淆的是 `SAYIT_CUSTOM_BASE_URL` 和 `SAYIT_CUSTOM_MODEL`。前者是接口地址，后者是你要调用的模型名；只有当你明确知道自己不走官方 OpenAI、而是走其他兼容服务时，才需要填写它们。默认情况下你不需要理解这些字段，也不需要改 `src` 目录；只有在你确实想切换服务时，才需要处理这部分。

### 用户配置文件

除了 `.env` 以外，项目还支持一个用户配置文件 `~/.config/sayit/config.toml`。不过这不是第一次使用的必需项，它更像是“想把默认行为固定下来时”的高级配置。比如你总是想默认输出中文、默认给出 3 个候选、或者默认使用某种输出格式，这时候才值得用它。

如果你确实需要这个文件，可以运行：

```bash
sayit config init
```

这会生成：

```text
~/.config/sayit/config.toml
```

生成之后，你可以再用下面这条命令查看当前生效的配置：

```bash
sayit config show
```

不过对大多数用户来说，第一次使用并不需要手动创建这个文件；只用 `.env`、`./setup` 和 `sayit` 就够了。换句话说，如果你只是想先把项目跑起来，请优先盯住 `.env`，不要一开始就去改 `config.toml`。

常见修改配置如下

```toml
[defaults]
language = "zh"
mode = "auto"
context = "work"
tone = "polite"
variants = 3
preserve_facts = true

[output]
format = "pretty"
show_notes = true

[provider]
default = "openai"
timeout_seconds = 20
```

---

## 使用说明

### 1) 直接改写一句话

```bash
sayit "你这个怎么还没弄完"
```

这是最常见的用法。
`sayit` 会返回几个更适合发送的候选版本。

### 2) 带上下文改写

```bash
sayit "这个价格太高了" --context bargain
```

上下文会帮助工具更稳定地选择改写方向，比如议价、拒绝、提醒等。

### 3) 查看本地分析

```bash
sayit explain "我今天不想去了"
```

`explain` 会输出这句话的本地分析结果，包括：

* 更接近哪种意图
* 可能的风险点
* 建议采用的改写策略

它适合用来调试规则、检查判断过程，或理解为什么某句话会被这样改写。

### 4) 机器可读输出

```bash
sayit "这个价格太高了" --json
```

适合脚本调用或程序集成。

### 5) 只输出纯文本候选

```bash
echo "这个价格太高了" | sayit --plain
```

适合 shell 管道或快速复制粘贴。

### 6) 从文件读取输入

```bash
sayit draft.txt
```

---

## 输入与输出

### 输入来源

`sayit` 支持多种输入方式：

* 命令行参数（argv）
* 标准输入（stdin）
* 文件
* 剪贴板

### 输出格式

支持三种输出格式：

* `pretty`：默认，适合人直接查看
* `plain`：只保留纯文本候选
* `json`：适合脚本和程序消费

---

## 工作方式

`sayit` 当前通过模型服务生成候选文案。
但在请求发送之前，会先做一层**本地检测和规划**，用于：

* 判断更接近跟进、拒绝、请求、道歉、议价或表达不满
* 识别“太冲”“太模糊”“太像命令”之类的风险点
* 给生成过程提供更受控的方向

本地规则不是最终输出本身，而是为了让候选更稳，不完全依赖自由生成。

---

## 故障排查

### `Cannot connect to the Docker daemon`

通常表示 Docker Desktop 还没有完全启动。
在 macOS 上，`./setup` 和 `sayit` 会尽量帮你拉起它并等待一会儿；如果仍然失败，请手动打开 Docker Desktop 后再试。

### `No available AI provider configured`

通常表示：

* `.env` 没有填写
* key 填错了
* key 当前不可用

请先检查 `.env` 中的配置项是否完整、格式是否正确。

### 网络错误

通常表示当前网络访问不到你正在使用的模型服务。
请检查网络连通性、代理设置，或你所使用服务的可访问性。

---

## 开发

如果你要自己开发或修改代码，最直接的方式是跑测试、检查 provider 状态和查看规则列表。

常用命令：

```bash
pytest
PYTHONPATH=src python -m sayit providers list
PYTHONPATH=src python -m sayit providers test
PYTHONPATH=src python -m sayit rules list
```

仓库目前已经包含：

* 基础测试
* 双语 README
* Dockerfile
* compose 配置
* CI
* 贡献说明
* 许可证

这些内容足以支持公开 alpha 阶段的使用与协作。

---

## 项目状态

`sayit` 当前处于 **alpha** 阶段。
接口、规则、输出细节和配置方式都仍有可能调整。

---

## 贡献

贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

欢迎提交：

* bug 修复
* 规则改进
* 文档优化
* 平台兼容性改进
* 使用场景示例
* provider 相关改进

---

## 变更记录

变更记录见 [CHANGELOG.md](CHANGELOG.md)。

---

## 许可证

许可证见 [LICENSE](LICENSE)。

```
```
