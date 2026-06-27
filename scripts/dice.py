#!/usr/bin/env python3
"""
COC 7e 掷骰工具（房规 3）
=======================

房规 3 规则：
- 大成功：01-05（无视技能值）
- 大失败：96-100（无视技能值）
- 极难成功：<= skill/5 且 > 5
- 困难成功：<= skill/2 且 > skill/5
- 一般成功：<= skill 且 > skill/2
- 失败：> skill 且 < 96

奖励骰/惩罚骰：投 3 个 d10（1 个个位 + 2 个十位），十位取 min/max。
"""

import argparse
import random
import sys


def roll_d10() -> int:
    """投 1 个 d10，返回 0-9（视为十位）"""
    return random.randint(0, 9)


def roll_d100(bonus: int = 0, penalty: int = 0) -> int:
    """
    投 1d100。bonus/penalty 是奖励/惩罚骰的个数。
    返回 1-100 的整数。
    """
    if bonus < 0 or penalty < 0:
        raise ValueError("奖励/惩罚骰个数不能为负")

    ones = roll_d10()  # 个位

    # 至少 1 个十位
    tens_list = [roll_d10()]

    # 奖励骰：十位取 min
    for _ in range(bonus):
        tens_list.append(roll_d10())

    # 惩罚骰：十位取 max
    for _ in range(penalty):
        tens_list.append(roll_d10())

    # 房规 3 简化：bonus - penalty 后的净数量
    # 如果有奖励和惩罚，逻辑上应抵消，但这里按"先取好再取坏"
    # 实际上传统规则是：投 N+M 个十位，取 min(M个), max(N个) 然后再比较
    # 简化实现：把负数用 0 替代
    net_bonus = max(0, bonus - penalty)
    net_penalty = max(0, penalty - bonus)

    if bonus > 0 and penalty > 0:
        # 都有：取 min(bonus 个) 和 max(penalty 个) 两个候选
        # 但简单实现：直接把所有十位扔一起，按规则
        # 严格实现需要分别处理
        # 这里简化：净 bonus = bonus - penalty
        tens = min(tens_list) if net_bonus > 0 else (max(tens_list) if net_penalty > 0 else tens_list[0])
    elif net_bonus > 0:
        tens = min(tens_list)
    elif net_penalty > 0:
        tens = max(tens_list)
    else:
        tens = tens_list[0]

    result = tens * 10 + ones + 1
    if result > 100:
        result = 100
    return result


def judge(skill: int, roll: int) -> str:
    """判定骰出 roll 对技能值 skill 是什么等级"""
    if skill < 0 or skill > 100:
        raise ValueError(f"技能值必须在 0-100，实际 {skill}")

    if roll <= 5:
        return "大成功"
    if roll >= 96:
        return "大失败"
    if roll > skill:
        return "失败"
    if roll <= skill // 5:
        return "极难成功"
    if roll <= skill // 2:
        return "困难成功"
    return "一般成功"


def main():
    p = argparse.ArgumentParser(
        description="COC 7e 房规 3 掷骰工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s 50 --label "侦查"
  %(prog)s 50 --bonus 1 --label "聆听（奖励骰）"
  %(prog)s 50 --penalty 1 --label "侦查（惩罚骰）"
  %(prog)s 75 --label "急救"
        """,
    )
    p.add_argument("skill", type=int, help="技能值（0-100）")
    p.add_argument("--bonus", type=int, default=0, help="奖励骰个数")
    p.add_argument("--penalty", type=int, default=0, help="惩罚骰个数")
    p.add_argument("--label", type=str, default="", help="检定名称（仅显示用）")
    p.add_argument("--no-roll", action="store_true", help="不实际投骰，仅显示规则")

    args = p.parse_args()

    if args.no_roll:
        print(f"=== 房规 3 检定规则（技能值 {args.skill}）===")
        print(f"  大成功：01-05")
        print(f"  大失败：96-100")
        if args.skill > 0:
            print(f"  极难成功：01-{max(5, args.skill // 5)}")
            print(f"  困难成功：{max(5, args.skill // 5) + 1}-{args.skill // 2}")
            print(f"  一般成功：{args.skill // 2 + 1}-{args.skill}")
            print(f"  失败：{args.skill + 1}-95")
        return

    roll = roll_d100(args.bonus, args.penalty)
    level = judge(args.skill, roll)

    label_str = f"【{args.label}】" if args.label else ""
    bonus_str = ""
    if args.bonus > 0:
        bonus_str = f" (奖励骰×{args.bonus})"
    elif args.penalty > 0:
        bonus_str = f" (惩罚骰×{args.penalty})"

    print(f"{label_str}D100={roll}/{args.skill} {level}{bonus_str}")

    sys.exit(0)


if __name__ == "__main__":
    main()
