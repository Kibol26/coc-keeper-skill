#!/usr/bin/env python3
"""
COC 7e 理智（SAN）检定工具（房规 3）
================================

触发：玩家目睹超自然事件、暴力、死亡等。
每个事件标"X/Y"两个数：
- 投骰 <= 当前 SAN：扣 X
- 投骰 > 当前 SAN：扣 Y（Y 可以是固定数字或骰子表达式，如 "1d6" 或 "2d6+1"）
- 大失败（96-100）：直接扣 Y

疯狂触发：
- 单次损失 >= 5：实时疯狂（1D10 回合）
- 累计损失 >= 当前 SAN / 5：实时疯狂
- 实时疯狂中需 INT 检定决定是否进入失控
"""

import argparse
import random
import re
import sys


def roll_d100() -> int:
    return random.randint(1, 100)


def roll_d10() -> int:
    return random.randint(1, 10)


def roll_dice_expr(expr) -> int:
    """
    投一个骰子表达式。
    接受 int（直接返回）或 str（解析 "1d6", "2d6+1", "1d3-1" 等）。
    """
    if isinstance(expr, int):
        return expr
    if isinstance(expr, str):
        s = expr.replace(" ", "").lower()
        if re.fullmatch(r"\d+", s):
            return int(s)
        # 解析 XdY[+Z[-W]]
        m = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", s)
        if not m:
            raise ValueError(f"无法解析骰子表达式: {expr!r}")
        count = int(m.group(1)) if m.group(1) else 1
        sides = int(m.group(2))
        mod = int(m.group(3)) if m.group(3) else 0
        total = sum(random.randint(1, sides) for _ in range(count)) + mod
        return max(0, total)
    raise TypeError(f"loss 必须是 int 或 str, 实际 {type(expr)}")


def san_check(current_san: int, loss_min, loss_max, label: str = "") -> dict:
    """
    进行一次 SAN check。

    Args:
        current_san: 当前 SAN
        loss_min: 损失下限，可以是 int 或骰子表达式 str
        loss_max: 损失上限，可以是 int 或骰子表达式 str
        label: 事件标签

    Returns:
        dict with roll, loss, new_san, is_crit_fail, old_san, label, loss_min_raw, loss_max_raw
    """
    roll = roll_d100()
    is_crit_fail = roll >= 96  # 房规 3 大失败 96-100

    if is_crit_fail:
        loss = roll_dice_expr(loss_max)
    elif roll <= current_san:
        loss = roll_dice_expr(loss_min)
    else:
        loss = roll_dice_expr(loss_max)

    new_san = max(0, current_san - loss)

    return {
        "roll": roll,
        "loss": loss,
        "new_san": new_san,
        "is_crit_fail": is_crit_fail,
        "old_san": current_san,
        "label": label,
    }


def check_madness_trigger(loss: int, current_san_before: int, new_san: int) -> dict:
    """检查是否触发疯狂发作。"""
    if loss >= 5:
        return {
            "triggered": True,
            "reason": f"单次损失 {loss} >= 5",
            "type": "bout",
        }
    if current_san_before > 0 and loss >= current_san_before / 5:
        return {
            "triggered": True,
            "reason": f"单次损失 {loss} >= 当前 SAN 的 1/5 ({current_san_before / 5:.1f})",
            "type": "bout",
        }
    if new_san == 0:
        return {
            "triggered": True,
            "reason": "SAN 归 0",
            "type": "indefinite",
        }
    return {"triggered": False, "reason": "", "type": None}


def _loss_arg(s: str):
    """
    CLI 参数解析：先尝试 int，失败则当字符串骰子表达式。
    """
    try:
        return int(s)
    except ValueError:
        return s


def main():
    p = argparse.ArgumentParser(
        description="COC 7e SAN check 工具（房规 3）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s 60 0 1d6 --label "看到尸体"          # 0 成功 / 1D6 失败
  %(prog)s 35 0 1 --label "看到书上的符号"       # 全是固定数字
  %(prog)s 50 1d3 2d6+1 --label "看到邪神"      # 骰子表达式
        """,
    )
    p.add_argument("current_san", type=int, help="当前 SAN 值")
    p.add_argument("loss_min", type=_loss_arg, help="损失下限（投 <= SAN 时扣，可为 0/1/1d3 等）")
    p.add_argument("loss_max", type=_loss_arg, help="损失上限（投 > SAN 或大失败时扣，可为 1d6/2d6+1 等）")
    p.add_argument("--label", type=str, default="", help="事件标签")

    args = p.parse_args()

    result = san_check(args.current_san, args.loss_min, args.loss_max, args.label)
    madness = check_madness_trigger(
        result["loss"], result["old_san"], result["new_san"]
    )

    label_str = f"【{args.label}】" if args.label else "【SAN check】"
    crit_str = "大失败！" if result["is_crit_fail"] else ""
    print(
        f"{label_str}d100={result['roll']} "
        f"SAN {result['old_san']} -> {result['new_san']} (扣 {result['loss']}) {crit_str}"
    )

    if madness["triggered"]:
        print(
            f"⚠️  触发疯狂: {madness['reason']} ({madness['type']})"
        )
        print(f"   → 跑 `python3 mad_draw.py` 抽疯狂表")

    sys.exit(0)


if __name__ == "__main__":
    main()
