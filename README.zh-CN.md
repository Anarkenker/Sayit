# sayit

中文 | [English](README.md)

`sayit` 是一个 API-first 的 CLI，用来把短句、冒犯、别扭、不适合直接发出去的话，改写成更得体、更可发送的表达。

它不是聊天机器人，也不是长文写作助手。

## 简介

`sayit` 聚焦在：

- 短输入
- 短输出
- 明确社交意图
- 受控改写
- 基于 API 的生成

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

`sayit explain` 仍然会告诉你：

- 识别到的意图
- 风险点
- 改写策略

真正的改写输出现在只走 API。

## 当前能力

- API-only 改写生成
- 本地意图识别和风险识别，用于受控提示
- 基于规则的 planner
- 支持 `argv`、`stdin`、文件、剪贴板输入
- 支持 `pretty`、`plain`、`json` 输出
- 支持 `explain` 命令
- 支持 OpenAI-compatible provider
- Docker 优先使用方式

## 推荐使用方式：Docker

先构建镜像：

```bash
docker build -t sayit .
```

创建本地 `.env`：

```bash
cp .env.example .env
```

填入你的 provider key：

```bash
OPENAI_API_KEY=your_real_key_here
OPENROUTER_API_KEY=
```

直接输入运行：

```bash
docker run --rm --env-file .env sayit "你这个怎么还没弄完"
```

输出 JSON：

```bash
docker run --rm --env-file .env sayit "这个价格太高了" --json
```

运行 explain：

```bash
docker run --rm --env-file .env sayit explain "你先把钱转我"
```

通过 stdin：

```bash
echo "这个价格太高了" | docker run --rm -i --env-file .env sayit --plain
```

挂载文件输入：

```bash
docker run --rm --env-file .env -v "$PWD:/workspace" -w /workspace sayit draft.txt
```

也可以用 Docker Compose：

```bash
docker compose run --rm sayit "你这个怎么还没弄完"
```

说明：

- Docker 是推荐运行方式
- `--clipboard` 在容器里不太实用
- 如果要用文件输入，记得挂载工作目录

## 备选方式：本地 Python

如果你还是想直接本地跑：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
sayit "你这个怎么还没弄完"
```

如果不安装，也可以：

```bash
PYTHONPATH=src python -m sayit "你这个怎么还没弄完"
```

## API Key 放置方式

不要把真实 API key 写进源码或配置文件。

推荐做法：

1. 把真实 key 放到环境变量
2. 配置文件里只保存环境变量名
3. 提交 `.env.example`，不要提交 `.env`

在宿主机直接运行时，程序会自动加载 `.env`。  
在 Docker 里，优先用 `--env-file .env`。

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

```bash
docker run --rm --env-file .env sayit "你这个怎么还没弄完"
docker run --rm --env-file .env sayit "这个价格太高了" --context bargain
docker run --rm --env-file .env sayit explain "我今天不想去了"
```

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
sayit rules list
```

## 输出格式

### `pretty`

适合人类直接阅读，包含：

- 原文
- 意图
- 风险点
- 改写候选

### `plain`

只输出候选文案。

```bash
sayit "你这个怎么还没弄完" --plain
```

### `json`

适合脚本或其他工具集成。

```bash
sayit "这个价格太高了" --json
```

## 运行模式

### `ai`

- 所有改写候选都通过 provider 生成
- 需要 provider 配置和运行时 key
- 这是推荐使用方式

### `auto`

- 当前会解析为配置好的 provider 路径
- 主要是为了兼容 CLI 和配置

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
  rules/
tests/
Dockerfile
compose.yaml
```

## 开发

运行测试：

```bash
pytest
```

查看规则：

```bash
sayit rules list
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

- 改写生成现在必须依赖可用的 provider
- 中文规则覆盖明显强于英文支持
- `explain` 是本地分析，rewrite 是 provider 驱动
- `--clipboard` 在 Docker 容器里不太适合

## 路线图

- 扩展 6 个核心意图的规则覆盖
- 增加英文规则和测试
- 增加稳定快照测试
- 加强事实保全和“禁止乱编理由”的校验
- 补强 provider 错误处理和集成覆盖

## 开源说明

这个仓库现在已经具备首个公开版本的基础结构：

- 清晰 README
- `.gitignore`
- `.env.example`
- 基础 CI
- Docker 运行方式

## 贡献

贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 变更记录

变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。
