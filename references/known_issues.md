# Known Issues

当前版本的已知问题与限制。

> 详细设计讨论和失败模式分析见 [v2_design_notes.md](v2_design_notes.md)。
> LLM 状态丢失的补偿方法见 [llm-state-loss-patterns.md](llm-state-loss-patterns.md)。

---

## 1. LLM 状态丢失（高优先级）

**症状**：跑 30 分钟以上后，AI 忘记：
- 玩家之前说过的话
- NPC 当前的态度
- 调查员的 HP / SAN / 调查进度

**原因**：LLM 的 context window + attention decay 是物理限制，**不是 bug**。

**缓解**：
- 强制维护 `data/<campaign_id>/session_log.md` 顶部的 4 张表
- 每次重大事件后让 AI 主动更新这 4 张表
- 单次 session 控制在 2-3 小时内，超过就存档开新 campaign

详见 [llm-state-loss-patterns.md](llm-state-loss-patterns.md)。

---

## 2. AI 替玩家决策（高优先级）

**症状**：AI 替调查员说「我决定打开门」「我攻击他」。

**原因**：很多 LLM 把"叙事流畅度"看得比"不替玩家决策"更重。

**缓解**：
- 看到立即指出，让 AI 重写
- 在 [SKILL.md §2](../SKILL.md) 有详细红线
- 必要时换更大的 LLM

---

## 3. 建卡繁琐（中优先级）

**症状**：γ 模式（玩家自己掷属性）步骤多，新玩家会迷茫。

**原因**：建卡是 CoC 的传统流程，简化会损失角色多样性。

**缓解**：
- α 模式：让 AI 代掷（牺牲一点"仪式感"，换上手速度）
- 模板卡：[investigator_filled.md](../templates/investigator_filled.md) 提供了一个完整的样例可以照抄

---

## 4. 疯狂表不完整（中优先级）

**症状**：缺少部分 mansion 类的额外疯狂表（永久疯狂、克苏鲁疯狂）。

**原因**：这些表在 CoC 7e 守密人屏后手册里，本 skill 故意不收录（避免版权问题）。

**缓解**：KP 遇到这些疯狂时，查阅原版规则书，或临时在 [madness_tables.md](madness_tables.md) 末尾追加自定义表。

---

## 5. 没有自动存档（中优先级）

**症状**：每次开新团要手动 `mkdir data/<campaign_id>/`。

**缓解**：
- 让 AI 在开团时自动建目录（已经在 SKILL.md 里指定）
- 备份建议：定期 `tar czf backup-$(date +%F).tar.gz data/`

---

## 6. 战斗脚本覆盖不全（低优先级）

**症状**：`scripts/combat.py` 不支持：掩护、闪避、先攻顺序、持久伤。

**原因**：7e 战斗规则比较琐碎，全实现会显著增加 prompt 长度而收益有限。

**缓解**：
- 基础攻击 / 反击 / 伤害骰 / 护甲已实现
- 复杂情况手动裁决
- 欢迎 PR 扩展

---

## 报告新问题

提 GitHub issue 时请附上：
- `~/.hermes/skills/coc-keeper/SKILL.md` 的版本号（v 字段）
- 出问题的 `data/<campaign_id>/session_log.md` 节选
- 完整对话 log（去敏感信息后）
