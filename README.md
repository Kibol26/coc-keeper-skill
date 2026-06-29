# coc-keeper

> AI 守密人 (Keeper) skill for [Hermes Agent](https://github.com/hermes-agent) — 让 LLM 主持《克苏鲁的呼唤》第七版（房规 3）单人 / 2-4 人跑团。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CoC 7e](https://img.shields.io/badge/Call%20of%20Cthulhu-7th%20Edition-blueviolet)](references/coc7e_rules.md)
[![House Rule 3](https://img.shields.io/badge/House%20Rule-3-important)](references/coc7e_rules.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](scripts/)
[![Skill Version](https://img.shields.io/badge/version-2.0.0-brightgreen)](SKILL.md)

## ✨ Features

| | |
|---|---|
| 🎲 **真实掷骰** | d100 普通 / 奖励 / 惩罚骰 + 大成功 & 大失败自动判定 |
| 🧠 **SAN Check** | 自动算理智损失 + 触发疯狂发作表 |
| 🃏 **疯狂表** | 实时 / 恐惧症 / 躁狂 / 长期疯狂 — 全部内置 |
| ⚔️ **战斗系统** | 攻击 / 反击 / 伤害骰 / 护甲 — Python 脚本后端 |
| 📓 **线索账本** | 强制 4 表维护（线索 / NPC / 时间线 / 调查员），对抗 LLM 状态丢失 |
| 📜 **完整规则** | 7e 核心机制 + 60+ 技能 + 武器护甲表 + 疯狂表 |
| 🎬 **两个开箱即用模组** | 《山间怪屋》2-3 人 2-3h、《沙漠驿站》2 人 30min |
| 🤖 **AI 守密人** | 4 层 prompt 架构 + 机器可读标签 + 5 选项结尾（"bizarre/risky/reckless"） |

## 🎬 Demo

KP 的每轮输出严格按 4 段格式：

```
[NARRATIVE]
你沿着吱嘎作响的楼梯爬上阁楼，灰尘在手电光柱中翻飞。空气里有一股铁锈味。
走到第三阶时，手电照到了地板上的东西——

一摊干涸的暗红色血迹。拖痕一直延伸到东墙的阴影里。

[MECHANICS]
> SPOT_HIDDEN 50 → 掷 73 — **失败**
> SAN_CHECK 0/1d6 → 掷 45 — **损失 1 点 SAN**（当前 64/99）
> 大成功阈值 01-05, 大失败阈值 96-100

[SUGGESTIONS]
① 蹲下来用手指摸血迹的边缘（侦察）
② 直接朝东墙阴影走去（可能遭遇未知）
③ 退回去叫人帮忙（理智保存）
④ 把门关上假装没看到（逃避）
⑤ 喝一口威士忌定定神（社交失败风险）

[CHRONICLE]
T+02:15 | 调查员进入阁楼 | 未发现秘道 | 新线索 C-001
```

## 📦 Installation

`coc-keeper` 是一个 [Hermes Agent skill](https://hermes-agent.nousresearch.com/docs) — 不是独立的 CLI，把它克隆到 Hermes 的 skills 目录即可：

```bash
# 假设你已安装 Hermes Agent
git clone https://github.com/sablea/coc-keeper-skill.git \
  ~/.hermes/skills/coc-keeper

# 验证安装
ls ~/.hermes/skills/coc-keeper/SKILL.md
```

**要求**：
- Python 3.8+（脚本只使用标准库）
- Hermes Agent（任何 LLM 后端，但建议 ≥ 70B 上下文窗口）

## 🚀 Quick Start

启动一次跑团只需一句话：

> 「用 coc-keeper 开个新团」

Hermes 会：
1. 加载 `SKILL.md`（KP 行为守则）
2. 询问模组（默认《山间怪屋》）和人数
3. 进入建卡流程
4. 创建 `~/.hermes/skills/coc-keeper/data/<campaign_id>/`

**手动掷骰**（你也可以让 AI 用脚本后端，而不是凭感觉）：

```bash
# 普通检定
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --label "侦查"

# 奖励骰 / 惩罚骰
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --bonus 1 --label "聆听"
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --penalty 1 --label "侦查(黑暗)"

# SAN check + 疯狂触发
python3 ~/.hermes/skills/coc-keeper/scripts/san_check.py 60 1 6 --label "看到尸体"

# 抽疯狂
python3 ~/.hermes/skills/coc-keeper/scripts/mad_draw.py --kind bout
python3 ~/.hermes/skills/coc-keeper/scripts/mad_draw.py --kind phobia

# 对抗 / 战斗
python3 ~/.hermes/skills/coc-keeper/scripts/skill_check.py "Alice" 50 "Bob" 30
python3 ~/.hermes/skills/coc-keeper/scripts/combat.py \
  --action attack --attacker "Alice" --att-skill 50 \
  --defender "Goblin" --def-skill 30 --damage "1d6" --target-hp 8
```

## 🛠 Architecture

```
┌─────────────────────────────────────────────────┐
│  Layer 0  SYSTEM (version + house rules)        │  ← 不可变
├─────────────────────────────────────────────────┤
│  Layer 1  RULES (CoC 7e + house rule 3)         │  ← 按需注入
├─────────────────────────────────────────────────┤
│  Layer 2  STATE (clue ledger + investigator)    │  ← 每个 turn 重注入
├─────────────────────────────────────────────────┤
│  Layer 3  OUTPUT FORMAT (4 段 + 5 候选)          │  ← 强制
└─────────────────────────────────────────────────┘
```

设计参考见 [`references/v2_design_notes.md`](references/v2_design_notes.md)。

## 📖 Documentation

- **[SKILL.md](SKILL.md)** — KP 行为守则（必读）
- **[references/coc7e_rules.md](references/coc7e_rules.md)** — 7e 规则速查
- **[references/skill_list.md](references/skill_list.md)** — 60+ 技能列表
- **[references/weapons_armor.md](references/weapons_armor.md)** — 武器与护甲
- **[references/madness_tables.md](references/madness_tables.md)** — 疯狂发作表
- **[references/clue_ledger.md](references/clue_ledger.md)** — 线索账本模板
- **[references/known_issues.md](references/known_issues.md)** — 已知问题
- **[references/v2_design_notes.md](references/v2_design_notes.md)** — 设计参考与变更日志
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — 常见故障排查

## 🧩 Built-in Scenarios

| 模组 | 人数 | 时长 | 模板 |
|---|---|---|---|
| 《山间怪屋》 | 2-3 | 2-3h | [scenario_house_on_the_borderland.md](templates/scenario_house_on_the_borderland.md) |
| 《沙漠驿站》 | 2 | 30min | [scenario_solo_crypt.md](templates/scenario_solo_crypt.md) |

## 🤝 Contributing

PR 欢迎，但请先读 [SKILL.md §0](SKILL.md) 了解固定的房规 3（**不能**改大成功 / 大失败阈值）。

**主要可贡献方向**：
- 新模组（放 `templates/`，参照已有格式）
- 疯狂发作的快速判定（自动投 INT）
- 海豹骰 / 真实骰池集成
- 翻译（目前中文为主）

## 📜 License

[MIT](LICENSE) — 爱用就用，记得保留版权声明。

⚖️ **CoC 7e Fair Use 声明**：本 skill 引用了 Chaosium 官方 CoC 7e 守密人规则书的核心机制作为提示工程素材，**不包含模组原文，不用于商业用途**。详见 [NOTICE](NOTICE)。

## 🙏 Credits

设计参考：
- [austin_amento: Prompt Architecture for a Reliable AI Dungeon Master (dev.to)](https://dev.to/austin_amento_860aebb9f55/prompt-architecture-for-a-reliable-ai-dungeon-master-d99)
- [rpgprompts: Call of Cthulhu Prompt (v1.007)](https://www.rpgprompts.com/post/call-of-cthulhu-chatgpt-prompt)
- [Reddit: Call of Cthulhu, Gamekeeper AI prompt feedback](https://www.reddit.com/r/Solo_Roleplaying/comments/1oviwyw/call_of_cthulhu_gamekeeper_ai_prompt_feedback)
- Chaosium 官方 *Call of Cthulhu* 7th Edition Keeper Rulebook

v1 是闭门造车，v2 才查到上面这些。

---

<sub>⚠️ **守密人警告**：本 skill 固定使用 7 版 + **房规 3**（大成功 01-05 / 大失败 96-100 / 极难成功 ≤ skill/5）。改房规请 fork，不要提 PR。</sub>
