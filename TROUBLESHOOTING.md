# Troubleshooting

跑团时翻车？先看这里。

## 脚本问题

### `ModuleNotFoundError`

**不要 `pip install`。** `scripts/` 下所有 Python 文件**只使用标准库**（`random`, `argparse`, `re`, `sys`, `json`, `pathlib`）。

如果报缺模块，**那是 bug**——请提 issue。

### 检定结果不对

- 检查 `--bonus` / `--penalty` 的符号：奖励骰传 `--bonus 1`，惩罚骰传 `--penalty 1`
- **不要同时给两个**——脚本不做抵消，需要抵消时手动算
- 极难成功阈值 = `skill / 5`（向下取整），且必须 > 5 才算"极难成功"

### SAN check 算错

SAN check 命令格式是 `san_check.py <当前SAN> <损失骰面数> <损失骰粒数>`：

```bash
# 当前 SAN = 60，损失 1d6
python3 scripts/san_check.py 60 1 6 --label "看到尸体"
```

第 3 个参数是**面数**（6 = d6），第 4 个是**粒数**（1 = 掷 1 次）。常见错误：把 1d6 写成 `1 6` 是对的，写成 `6 1` 就反了。

### 战斗脚本不支持的规则

`scripts/combat.py` 只覆盖 7e 基础战斗（攻击 / 反击 / 伤害）。以下**未实现**：
- 掩护 / 闪避 / 斗殴
- 先攻顺序
- 持久伤 / 流血

需要时手动裁决。

## AI 守密人问题

### AI 替玩家决策

**最常见的问题。** 检查 [SKILL.md §2](SKILL.md)「绝对不能做的」。

每次 AI 这样做：
1. 立即指出（"你没权利决定 Eleanor 怎么做"）
2. 让 AI 重写那一段
3. 如果连续 3 次都这样，建议换更强的 LLM 后端

### AI 忘记之前的剧情

LLM 的 context window 有限，跑 30 分钟以上会丢状态。**别只靠 AI 记忆**——每次重大事件后，让 AI 更新 `data/<campaign_id>/session_log.md` 顶部的 4 张表（线索 / NPC / 时间线 / 调查员状态）。

详见 [references/llm-state-loss-patterns.md](references/llm-state-loss-patterns.md)。

### AI 改了房规

如果 AI 出现「按 d100 < skill 算成功」「大成功是 1-5 但需要极难成功也是 1-5」之类的胡言乱语，立即在对话里纠正：「房规 3 是：大成功 01-05 / 大失败 96-100 / 极难成功 ≤ skill/5。**不要改。**」

### AI 写不出 5 个候选项

让它重读 [SKILL.md §3](SKILL.md)。最常见的错误：5 个选项都太"安全"，没有 bizarre/risky/reckless。

## 模组问题

### 模组数据错乱

每个 campaign 的存档都在 `data/<campaign_id>/` 下，**互相独立**。开新团一定要新建 campaign_id：

```bash
ls ~/.hermes/skills/coc-keeper/data/  # 查看所有 campaign
```

不要在旧 campaign 里开新剧情——线索账本会乱。

### 模组需要原始模组书

《山间怪屋》《沙漠驿站》模板只写**剧情梗概 + 关键 NPC + 难度调整**——具体场景描述、原文对白需要 KP（也就是你 + AI）临场发挥。

**不**包含模组原文是设计选择：避免版权问题，也避免 KP 被剧情"剧透"到无法自由裁决。
