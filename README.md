# RedNote-ArticleWriter-Agent

小红书文案写作 Agent，支持多种文案风格与命令行多轮改稿。

## 文案类型

| 类型 | `--agent` 值 | 说明 |
|------|--------------|------|
| 情感输出 | `emotional` | 共鸣、场景、情绪节奏 |
| 理性分析 | `rational` | 逻辑、对比、清单、可信论证 |

## 环境

1. 复制 `.env` 并配置 `DEEPSEEK_API_KEY`
2. 安装依赖：`pip install -r requirements.txt`

## 使用

```bash
# 交互选择类型 + 多轮改稿
python cli.py

# 直接指定类型
python cli.py --agent emotional
python cli.py --agent rational
```

流程：填写产品信息 → 生成首版 JSON 文案 → 输入修改意见（可多轮）→ 输入 `quit` 或 `q` 退出。

## 项目结构

```
agents/          # Agent 实现与 registry
prompts/         # 各类型 system / human 模板
session/         # 会话与多轮历史
llm/             # 模型工厂
schemas/         # 结构化输出
cli.py           # 命令行入口
```

## 扩展新类型

1. 在 `prompts/` 增加模板
2. 在 `agents/` 实现 `BaseAgent` 子类
3. 在 `agents/registry.py` 注册
