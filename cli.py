"""小红书文案 Agent 命令行入口（多轮对话）。"""

import argparse
import json
import sys

from agents.registry import get_agent, list_agents
from session.manager import SessionManager


def print_draft(draft) -> None:
    print("\n" + "=" * 48)
    print(json.dumps(draft.model_dump(), ensure_ascii=False, indent=2))
    print("=" * 48 + "\n")


def choose_agent_interactive() -> str:
    agents = list_agents()
    print("请选择文案类型：")
    for i, (agent_type, display_name) in enumerate(agents, start=1):
        print(f"  {i}. {display_name} ({agent_type})")
    while True:
        choice = input("输入序号：").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                return agents[idx][0]
        print("无效选择，请重新输入。")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="小红书文案多轮写作 Agent")
    parser.add_argument(
        "--agent",
        choices=[t for t, _ in list_agents()],
        help="文案类型：emotional（情感输出）或 rational（理性分析）",
    )
    return parser.parse_args()


def run_chat_loop(manager: SessionManager, session_id: str) -> None:
    print("首版已生成。接下来可输入修改意见（多轮）；输入 quit 或 q 退出。\n")
    while True:
        feedback = input("修改意见> ").strip()
        if not feedback:
            print("请输入修改意见，或输入 quit / q 退出。")
            continue
        if feedback.lower() in {"quit", "q", "exit"}:
            print("已结束本次会话。")
            break
        try:
            draft = manager.revise(session_id, feedback)
            print_draft(draft)
        except Exception as exc:
            print(f"修改失败：{exc}", file=sys.stderr)


def main() -> None:
    args = parse_args()
    agent_type = args.agent or choose_agent_interactive()

    try:
        agent = get_agent(agent_type)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    print(f"\n已选择：{agent.display_name} ({agent.agent_type})\n")
    inputs = agent.prompt_for_inputs()

    manager = SessionManager()
    session = manager.create(agent_type)
    print(f"\n会话 ID：{session.session_id}\n正在生成首版文案，请稍候...\n")

    try:
        draft = manager.generate(session.session_id, inputs)
    except Exception as exc:
        print(f"生成失败：{exc}", file=sys.stderr)
        sys.exit(1)

    print_draft(draft)
    run_chat_loop(manager, session.session_id)


if __name__ == "__main__":
    main()
