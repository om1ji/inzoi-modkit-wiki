# Разбор: механика "владения" объектом (Change PC Role)

Исследование для мода-идеи «дать возможность менять, кому принадлежит компьютер в офисе — CEO,
NPC или игроку». Цель была не реализовать мод целиком, а понять, как в принципе устроена механика
владения объектом в игре. Ниже — цепочка находок в порядке их обнаружения.

## Интерактивный граф связей

Кликабельная схема (узлы = реальные строки данных, пунктир = черновик, ещё не записанный в игру):

```{raw} html
<iframe src="../_static/interactive/command-graph.html"
        style="width:100%;height:820px;border:1px solid var(--color-background-border);border-radius:8px;"
        loading="lazy"></iframe>
<p><a href="../_static/interactive/command-graph.html" target="_blank">Открыть граф на весь экран ↗</a></p>
```

## Отправная точка: bRequiresCareerSeat

`Career.Organizations[].RankList[].Shift[].bRequiresCareerSeat` (bool) — у каждого ранга сотрудника
в смене есть флаг «требуется закреплённое рабочее место». У `ITcompany` он `true` на всех рангах —
подтверждает, что механика «привязанного рабочего места» в игре есть и завязана на ранг сотрудника.

## Словарь ролей: EB1DoorPermissionGroup

Найден в `DA_SiteEditCondition`/`DA_SiteConfig` — enum, который игра реально использует для контроля
доступа (пока — к дверям):

```
All, Nobody, Family, Me, Relationship, Company,
BusinessOwner, BusinessOwnerOrEmployee, BusinessOperating,
Male, Female, CareerMember, CareerOperating, Invalid
```

`BusinessOwner`, `CareerMember`, `Company` — ровно та классификация ролей, которая нужна для задачи.

## Тупиковая гипотеза: OwnershipCategory

У `ObjectTemplate.Computer01_Template` есть поле `OwnershipCategory`, но это **не роль владельца** —
это категория предмета для системы личной собственности (у кровати там стоит `"Bed"`, у всех
проверенных компьютеров — `"None"`). Не то, что искали.

## Реальный механизм: бафф + условия

Ключевая находка — эксклюзивное право на объект реализовано через **бафф**, а не через поле объекта:

*Источник: `Condition_Interaction.Has_Exclusive_Npc_Object_Right` · MCP `modkit_get_row`.*

```json
{
  "AndConditionsList": [{
    "Conditions": [{
      "BaseObject": "Self", "Command": "Buff",
      "CompareType": "Equal", "S1": "Exclusive_Npc_Object_Right"
    }]
  }]
}
```

Бафф `Exclusive_Npc_Object_Right`: `Duration: -1` (бессрочный), `HiddenFromUI: true`, тег
`BuffTag_NpcSystem`. Живёт на персонаже, не на объекте — вот где хранится «владение» в savefile.

Сопутствующие условия:

- **`OnlySiteScheduledNPC`** — `Self Command: IsSiteScheduleNPC` — персонаж числится сотрудником этой
  локации.
- **`OnlySiteScheduledNPC_Or_ShopNPC`** — то же ИЛИ `CharacterGroupType == "ShopNpc"`.
- Паттерн `HasJob_<Company>_Rank<N>` — генерируется на лету из `Career.Organizations[].RankList[]`
  (не статичная строка таблицы) — гейтит миссии/действия по конкретному рангу в конкретной компании.

## Полная цепочка (пример: Computer01 в проекте Change_PC_Role)

```
01 · Book         Computer01 (категория HomeOffice_PC, группа Furniture)
                   InteractionSlot / InteractionSlot_Cleaning / FxSlot_Broken

02 · Data Table    Script_Interaction_Computer (18 строк) + DT_InteractionBag
                   конкретные действия на компьютере, сгруппированы в bag'и

03 · Data Asset    DA_Interaction — глобальные тайминги/радиусы, ОДИН на всю игру
                   MaxInteractionRange, AutonomyIntervalMin/Max — Computer01 их наследует, не переопределяет
```

## Черновик Action (не доведён до конца)

Схема, которую предлагалось реализовать (условие + interaction + action + патч бага), по образцу
реальных находок выше:

**1. Condition_Interaction → `PCRole_Change_Enable`**

*Черновик (предложение), не из игровых данных. Целевой путь: `Condition_Interaction.PCRole_Change_Enable`.*

```json
{
  "Id": "PCRole_Change_Enable",
  "AndConditionsList": [{
    "Conditions": [
      {"BaseObject": "Target", "Command": "HasObjectTag", "CompareType": "Equal", "S1": "Create_Computer"},
      {"BaseObject": "Self", "Command": "IsSiteScheduleNPC", "CompareType": "Equal"}
    ]
  }]
}
```

**2. Interaction_Computer → `PCRole_Change`**

*Черновик (предложение), не из игровых данных. Целевой путь: `Interaction_Computer.PCRole_Change`.*

```json
{
  "Id": "PCRole_Change",
  "ConditionId": "PCRole_Change_Enable",
  "EnableSlotTags": ["Computer"],
  "ActionIdList": ["PCRole_Change"],
  "SpaceTargetFilterId": "TargetConnectedChair"
}
```

**3. Action_Interaction_Computer → `PCRole_Change`**

*Черновик (предложение), не из игровых данных. Целевой путь: `Action_Interaction_Computer.PCRole_Change`.*

```json
{
  "Id": "PCRole_Change",
  "Actions": [{
    "BaseObject": "Self", "Command": "PlayLoopAnim", "S1": "UseComputer",
    "FinishScriptIdList": ["??? — не найден реальный AddBuff/RemoveBuff script в данных"]
  }]
}
```

**4. InteractionBag_Computer → `PCRole_Change`**

*Черновик (предложение), не из игровых данных. Целевой путь: `InteractionBag_Computer.PCRole_Change`.*

```json
{
  "Id": "PCRole_Change",
  "InteractionEnableConditionIds": ["PCRole_Change_Enable"],
  "InteractionSequence": [{"InteractionInfos": [{"InteractionId": "PCRole_Change"}]}]
}
```

```{note}
Этот черновик **не был доведён до рабочего состояния** — проект переключился на более простую задачу
(см. {doc}`toilet-money`), которая довела до конца похожую механику (`Script_Interaction` +
`Command: AddCurrency`) на реальном примере. Открытый вопрос из этого исследования — реальный script
ID, который выдаёт/снимает `Buff` (`AddBuff`/`RemoveBuff`) — не найден ни в одной `Script_*` таблице
через `get_row`; вероятно, резолвится нативно (C++/blueprint), а не через DataTable.
```
