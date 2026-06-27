# v2 设计参考与变更日志

> 本文档记录 coc-keeper skill 的设计参考来源、v1→v2 变更、已知失败模式。
> v3 写之前先看这个。

---

## 参考来源

### 1. dev.to: Prompt Architecture for a Reliable AI Dungeon Master

- **作者**：austin_amento
- **URL**：https://dev.to/austin_amento_860aebb9f55/prompt-architecture-for-a-reliable-ai-dungeon-master-d99
- **核心观点**：4 层 prompt 架构
  1. System prompt 当"合同"，要版本化
  2. 按需注入规则（不要全塞进去）
  3. Game state 是真相（每个 turn 注入完整状态）
  4. 强制响应结构（4 段、机器可读）

- **学到的关键技巧**：
  - **机器可读标签**（`ITEM_USED: X`）让外部解析器能跟踪状态
  - **"先掷骰再叙事"** 在 prompt 里展示错误模式和正确模式
  - **"Warlock callout"** —— 针对 AI 容易出错的规则做专门 callout
  - **失败模式 cataloguing** —— 每次 AI 违反规则就加一条到 prompt

- **v1 没做这些**：v1 完全没设计机器可读协议、按需注入、错误模式 callout

### 2. rpgprompts: Call of Cthulhu Prompt v1.007

- **URL**：https://www.rpgprompts.com/post/call-of-cthulhu-chatgpt-prompt
- **作者**：Prompt Pup
- **核心观点**：5 个候选项结尾 + 长度限制

- **5 个候选项规则**：
  - 编号 1-5
  - 一个必须 brilliant/ridiculous/dangerous
  - 用 `{}` 包住
  - 显示在每轮结尾

- **长度限制**：
  - 1000-3000 字符（英文）
  - **v2 调整为 800-2000 字（中文）**

- **v1 没做这些**：v1 没要求每轮 5 候选项

### 3. Reddit: Call of Cthulhu, Gamekeeper AI prompt

- **URL**：https://www.reddit.com/r/Solo_Roleplaying/comments/1oviwyw/call_of_cthulhu_gamekeeper_ai_prompt_feedback
- **作者**：Gemini user 的 prompt 设计
- **关键发现**：
  - "End every Keeper turn with 5 possible numbered actions in curly braces"
  - "One must be bizarre, risky, or reckless"
  - "Player actions may be helpful, harmful, or neutral, reflecting location's danger level"

- **v1 没做这些**：v1 没强制 5 候选项，没强调"最后一个必须 bizarre"

### 4. Chaosium 官方 CoC 7e 守秘人规则书

- 来源：coc7e 守秘人规则书（公开摘要）
- **v1 部分引用 + v2 验证**：检定等级、SAN check、疯狂发作、战斗

---

## v1 → v2 主要变更

| 项目 | v1 | v2 |
|---|---|---|
| 总体设计 | 自拍脑袋 | 参考 4 层架构 |
| 机器可读标签 | 无 | [NARRATIVE][MECHANICS][SUGGESTIONS][CHRONICLE] |
| 5 候选项结尾 | 无 | 强制 5 个，最后一个 bizarre/risky/reckless |
| 先掷骰再叙事 | 只说"必须用 dice.py" | 展示错误模式 + 正确模式 |
| 按需注入规则 | 无 | KP_INTERNAL_THINKING 段 + 关键词 → 规则映射 |
| 平衡保护 | 无 | 1920s HP / 怪物比例硬约束 |
| 长度限制 | 无 | 800-2000 字（叙事）+ 200-400 字（候选项）|
| 房规 3 失败 callout | 无 | 4 条具体反例（"我觉得这次大失败是 1/100" 等）|
| System version 协议 | 无 | SYSTEM_VERSION: coc-keeper/v2.0 |
| 调查员状态真相 | 只在 references 里提 | §1.3 明确"状态表是唯一真相"|
| 不替玩家决策 | 散落在各条 | §1.2 集中 + 错误模式示例 |

---

## 已知失败模式（v2 后还要观察）

> 这些是基于 dev.to 的 failure pattern cataloguing 方法，**实际跑出来再补**。

### F-001：AI 在叙事里写"造成 N 点伤害"但前面没 ROLL 标签
- **来源**：dev.to §"Rolls are mandatory before outcomes"
- **解决**：v2 §1.1 明确禁止 + 错误模式示例
- **检测**：每次 turn 后扫一遍 MECHANICS 段
- **重写条件**：MECHANICS 里没 `ROLL: damage`，但 NARRATIVE 里出现 "造成 X 点伤害"

### F-002：AI 替玩家决策
- **来源**：COC KP 共识
- **解决**：v2 §1.2
- **检测**：NARRATIVE 里出现"你应该…"、"也许可以…"、"作为调查员你应该知道…"
- **重写条件**：任意一条出现

### F-003：AI 凭印象给线索
- **来源**：dev.to §"Game state as source of truth"
- **解决**：v2 §1.4
- **检测**：NARRATIVE 里出现"你突然发现 X"、"你意识到 Y" 但前面没 ROLL:侦查
- **重写条件**：任意"突然" / "意识到" + 没 ROLL

### F-004：房规 3 漂移
- **来源**：dev.to §"Warlock callout"
- **解决**：v2 §1.5
- **检测**：dice.py 输出 vs KP 叙事
- **重写条件**：脚本说"失败"，但叙事说"勉强成功"

### F-005：1920s 平衡崩坏
- **来源**：dev.to §"Encounter balance guardrails"
- **解决**：v2 §1.6
- **检测**：怪物 HP vs 调查员平均 HP
- **重写条件**：违反 §1.6 硬约束

### F-006：5 候选项格式错
- **来源**：rpgprompts + Reddit
- **解决**：v2 §2.3
- **检测**：候选项数量、格式、最后一项类型
- **重写条件**：数量不是 5、最后一项不是 bizarre/risky/reckless

### F-007：AI 改房规
- **来源**：玩家可能要求
- **解决**：v2 §0 明确"不换"
- **检测**：玩家说"这次算 1 吧"等
- **回应**：拒绝并重申

---

## v2 验证

### 已验证
- 5 个 Python 脚本：dice.py / san_check.py / mad_draw.py / skill_check.py / combat.py
- 普通检定 / 奖励骰 / 惩罚骰
- SAN check + 疯狂触发
- 对抗检定 + 平手规则
- 战斗 + 伤害等级

### 未验证
- 实际跑一场完整团（30 分钟小品 / 2-3 小时山间怪屋）
- 4 段输出格式是否在 LLM 里能稳定执行
- 5 候选项机制是否真的能引导出 bizarre 选项
- 1920s 平衡约束是否合理

### 下次跑团后补
- 实际跑出来的失败模式（F-008, F-009...）
- 哪些规则放在 §1 还是 §3 效果更好
- 1920s 平衡数字是否要调

---

## v3 方向（待定）

- 集成海豹骰（作为可选后端）
- 自动存档（写完 turn 后自动备份 session_log）
- 多模组框架（玩家选模组后自动加载）
- 失败模式自动 cataloguing（脚本检测 NARRATIVE 中的禁止词）
