#!/usr/bin/env python3
"""
COC 7e 对抗检定
==============

两个角色进行对抗（如说服 vs 意志、斗殴 vs 闪避、侦查 vs 潜行）。
双方各掷 1d100，高技能值的人技能更易成功（投出 <= 技能值）。
比较成功等级（不是数值）。
"""

import argparse
import sys

from dice import judge, roll_d100


def opposed_check(name_a: str, val_a: int, name_b: str, val_b: int) -> dict:
    """
    A 和 B 对抗。
    返回谁胜，胜的等级。
    """
    roll_a = roll_d100()
    roll_b = roll_d100()

    # 用 judge 算等级字符串
    level_a = judge(val_a, roll_a)
    level_b = judge(val_b, roll_b)

    # 比较等级
    # 大成功 > 极难成功 > 困难成功 > 一般成功 > 失败 > 大失败
    rank = {
        "大成功": 5,
        "极难成功": 4,
        "困难成功": 3,
        "一般成功": 2,
        "失败": 1,
        "大失败": 0,
    }

    rank_a = rank[level_a]
    rank_b = rank[level_b]

    if rank_a > rank_b:
        winner = name_a
    elif rank_b > rank_a:
        winner = name_b
    else:
        winner = "平手"

    return {
        "name_a": name_a,
        "roll_a": roll_a,
        "val_a": val_a,
        "level_a": level_a,
        "name_b": name_b,
        "roll_b": roll_b,
        "val_b": val_b,
        "level_b": level_b,
        "winner": winner,
    }


def main():
    p = argparse.ArgumentParser(description="COC 7e 对抗检定")
    p.add_argument("name_a", help="A 的名字")
    p.add_argument("val_a", type=int, help="A 的技能值")
    p.add_argument("name_b", help="B 的名字")
    p.add_argument("val_b", type=int, help="B 的技能值")

    args = p.parse_args()

    result = opposed_check(args.name_a, args.val_a, args.name_b, args.val_b)

    print(f"【对抗】{result['name_a']} vs {result['name_b']}")
    print(f"  {result['name_a']}: D100={result['roll_a']}/{result['val_a']} {result['level_a']}")
    print(f"  {result['name_b']}: D100={result['roll_b']}/{result['val_b']} {result['level_b']}")
    if result["winner"] == "平手":
        print(f"  → 平手（按 COC 7e 规则：攻击者胜 / 双方对峙僵持）")
    else:
        print(f"  → {result['winner']} 胜出")

    return result


if __name__ == "__main__":
    main()
