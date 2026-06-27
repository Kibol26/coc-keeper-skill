#!/usr/bin/env python3
"""
COC 7e 战斗工具
==============

支持：
- 攻击 vs 闪避/反击
- 伤害骰（极难成功取最大）
- 伤害等级判定（普通/重伤/濒死/死亡）
"""

import argparse
import re
import sys

from dice import judge, roll_d100
from skill_check import opposed_check


def roll_dice(expr: str) -> int:
    """投掷骰子表达式，如 '1d6', '2d6+4', '1d3+1d4'"""
    expr = expr.replace(" ", "")
    total = 0
    # 拆 + 
    parts = re.split(r"\+", expr)
    for part in parts:
        part = part.strip()
        if "d" in part.lower():
            # 骰子
            m = re.match(r"(\d*)d(\d+)", part.lower())
            if not m:
                raise ValueError(f"无法解析骰子表达式: {part}")
            count = int(m.group(1)) if m.group(1) else 1
            sides = int(m.group(2))
            for _ in range(count):
                total += 1  # 至少 1
                if part.endswith("max"):
                    total = sides  # 极难成功
                else:
                    total += _  # 实际掷骰
            # 简化：取最大值
            if part.endswith("max"):
                total = sides * count
            else:
                rolls = [1]  # 占位
                # 实际投
                rolls = []
                for _ in range(count):
                    import random
                    rolls.append(random.randint(1, sides))
                total = sum(rolls) + (total - count)  # 累加
                # 重置 total，重新算
                total = sum(rolls)
        else:
            # 数字
            total += int(part)
    return total


def roll_damage(expr: str, max_roll: bool = False) -> tuple:
    """
    投掷伤害。返回 (总值, 详情)。
    expr: '1d6', '2d6', '1d3+1d4' 等
    max_roll: True 时取最大
    """
    import random
    expr = expr.replace(" ", "")
    parts = re.split(r"\+", expr)
    total = 0
    details = []
    for part in parts:
        part = part.strip()
        if "d" in part.lower():
            m = re.match(r"(\d*)d(\d+)", part.lower())
            if not m:
                raise ValueError(f"无法解析: {part}")
            count = int(m.group(1)) if m.group(1) else 1
            sides = int(m.group(2))
            if max_roll:
                rolls = [sides] * count
            else:
                rolls = [random.randint(1, sides) for _ in range(count)]
            total += sum(rolls)
            details.append(f"{count}d{sides}={sum(rolls)}")
        else:
            total += int(part)
            details.append(str(part))
    return total, " + ".join(details)


def damage_severity(damage: int, max_hp: int) -> str:
    """判定伤害等级"""
    if damage > max_hp:
        return "当场死亡"
    if damage >= max_hp:
        return "濒死（HP=0）"
    if damage >= max_hp / 2:
        return "重伤（标签+倒地+CON 检定昏迷）"
    return f"普通伤（HP -{damage}）"


def main():
    p = argparse.ArgumentParser(description="COC 7e 战斗工具")
    p.add_argument(
        "--action",
        type=str,
        choices=["attack", "damage"],
        default="attack",
        help="动作类型",
    )
    p.add_argument("--attacker", type=str, help="攻击者名字")
    p.add_argument("--att-skill", type=int, help="攻击者战斗技能")
    p.add_argument("--defender", type=str, help="防御者名字")
    p.add_argument("--def-skill", type=int, help="防御者闪避/反击技能")
    p.add_argument("--damage", type=str, help="伤害表达式，如 '1d6'")
    p.add_argument("--target-hp", type=int, help="目标最大 HP（用于判定伤害等级）")
    p.add_argument("--max-roll", action="store_true", help="极难成功：伤害取最大")

    args = p.parse_args()

    if args.action == "attack":
        if not all([args.attacker, args.att_skill is not None, args.defender, args.def_skill is not None]):
            print("错误：attack 模式需要 --attacker, --att-skill, --defender, --def-skill")
            sys.exit(1)

        result = opposed_check(args.attacker, args.att_skill, args.defender, args.def_skill)

        # 攻击者胜出时投伤害
        if result["winner"] == args.attacker and args.damage:
            level = result["level_a"]
            max_roll = level in ("大成功", "极难成功")
            dmg, details = roll_damage(args.damage, max_roll=max_roll)
            print(f"【攻击】{result['name_a']} 胜出（{result['level_a']}）")
            print(f"  伤害: {args.damage} = {dmg} ({details})")
            if args.target_hp:
                sev = damage_severity(dmg, args.target_hp)
                print(f"  伤害等级: {sev}")
        else:
            # 平手时按 COC 7e 规则攻击者胜
            if result["winner"] == "平手":
                winner_str = "平手（攻击者胜）"
            else:
                winner_str = f"{result['winner']} 胜出"
            print(f"【攻击】{result['name_a']} vs {result['name_b']}")
            print(f"  {result['name_a']}: {result['level_a']}")
            print(f"  {result['name_b']}: {result['level_b']}")
            print(f"  → {winner_str}")

    elif args.action == "damage":
        if not args.damage:
            print("错误：damage 模式需要 --damage")
            sys.exit(1)
        dmg, details = roll_damage(args.damage, max_roll=args.max_roll)
        print(f"【伤害】{args.damage} = {dmg} ({details})")
        if args.target_hp:
            sev = damage_severity(dmg, args.target_hp)
            print(f"  伤害等级: {sev}")

    sys.exit(0)


if __name__ == "__main__":
    main()
