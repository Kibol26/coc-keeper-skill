# coc-keeper

《克苏鲁的呼唤》第七版（房规 3）守密人 skill。

> ⚠️ **重要**：本 skill 固定使用 **7 版 + 房规 3**。
> - 大成功：01-05（无视技能值）
> - 大失败：96-100（无视技能值）

## 目录结构

```
coc-keeper/
├── SKILL.md                          # KP 行为守则（必读）
├── references/                       # 规则速查
│   ├── coc7e_rules.md               # 7e 规则速查
│   ├── skill_list.md                # 60+ 技能列表 + 职业
│   ├── weapons_armor.md             # 武器与护甲
│   ├── madness_tables.md            # 疯狂发作表
│   └── clue_ledger.md               # 线索账本模板
├── scripts/                          # 工具脚本
│   ├── dice.py                      # 通用 d100 检定
│   ├── san_check.py                 # SAN check + 疯狂触发
│   ├── mad_draw.py                  # 抽疯狂表
│   ├── skill_check.py               # 对抗检定
│   └── combat.py                    # 战斗 + 伤害
├── templates/                        # 模板
│   ├── investigator.md              # 空调查员卡
│   ├── investigator_filled.md       # 示范卡
│   ├── scenario_house_on_the_borderland.md  # 山间怪屋（2-3 人，2-3h）
│   └── scenario_solo_crypt.md       # 沙漠驿站（2 人，30min）
└── data/                            # 跑团存档
    └── <campaign_id>/
        ├── session_log.md
        └── player_sheets/
```

## 快速使用

### 1. 开新团

> 「用 coc-keeper 开个新团」

AI 会：
1. 加载 SKILL.md
2. 询问模组（默认《山间怪屋》）
3. 询问人数（1-4 人）
4. 进入 γ 模式建卡流程
5. 创建 `data/<campaign_id>/` 目录

### 2. 跑团中的检定

KP 应该**用脚本而不是凭感觉**：

```bash
# 普通检定
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --label "侦查"

# 奖励骰
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --bonus 1 --label "聆听"

# 惩罚骰
python3 ~/.hermes/skills/coc-keeper/scripts/dice.py 50 --penalty 1 --label "侦查（黑暗）"

# SAN check
python3 ~/.hermes/skills/coc-keeper/scripts/san_check.py 60 1 6 --label "看到尸体"

# 抽疯狂
python3 ~/.hermes/skills/coc-keeper/scripts/mad_draw.py --kind bout
python3 ~/.hermes/skills/coc-keeper/scripts/mad_draw.py --kind phobia
python3 ~/.hermes/skills/coc-keeper/scripts/mad_draw.py --kind indefinite

# 对抗检定
python3 ~/.hermes/skills/coc-keeper/scripts/skill_check.py "Alice" 50 "Bob" 30

# 战斗
python3 ~/.hermes/skills/coc-keeper/scripts/combat.py \
  --action attack \
  --attacker "Alice" --att-skill 50 \
  --defender "Goblin" --def-skill 30 \
  --damage "1d6" --target-hp 8
```

### 3. 维护线索账本

每次重大事件后，KP 必须在 `data/<campaign_id>/session_log.md` 顶部维护 4 张表：
- 线索表
- NPC 表
- 时间线
- 调查员状态

详见 `references/clue_ledger.md`。

## 限制与已知问题

1. **依赖 LLM 质量**：本 skill 依赖 Hermes 后端的 LLM 能力。minimax-M3 跑长 TRPG 容易丢状态，需要靠**线索账本**弥补。
2. **建卡繁琐**：γ 模式要求玩家自己掷属性。如果玩家懒，可以让 AI 用 α 模式（AI 掷）。
3. **疯狂表不完整**：mansion 类的额外疯狂表（永久疯狂、克苏鲁疯狂）需要查阅原版规则书。
4. **没有自动存档**：每次开团前手动创建 `data/<campaign_id>/`。

## 故障排查

### 脚本报 `ModuleNotFoundError`
不用 `pip install`，所有脚本只用 Python 标准库（`random`, `argparse`, `re`, `sys`）。

### 检定结果不对
检查 `--bonus` / `--penalty` 的符号。**不要同时给两个**，需要抵消时手动算。

### AI 替玩家决策
这是最常见的问题。检查 SKILL.md §2「绝对不能做的」。**每次 AI 这样做，立即指出并让它重写**。

## 后续扩展（未实现）

- [ ] 海豹骰集成（作为可选后端）
- [ ] 自动存档工具
- [ ] 印斯茅斯阴影完整版模组
- [ ] 疯狂发作的快速判定（自动投 INT 检定）

## 协议

本 skill 适用 COC 7e 的 **Fair Use** 规则。
- 引用了规则书的核心机制
- 不包含模组原文
- 不用于商业用途
