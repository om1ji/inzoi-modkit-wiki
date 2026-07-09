# Условия и словарь Command

`Condition_*` — это универсальный движок логики игры. Одна строка условия отвечает на вопрос «правда
или ложь прямо сейчас», и на этот ответ завязано почти всё: показывать ли пункт меню
(`InteractionVisibleConditionIds`), можно ли его кликнуть (`InteractionEnableConditionIds`), сработает
ли ветка в `InteractionSequence`, выполнится ли блок скрипта. Если ты хочешь, чтобы действие
появлялось только «в нужный момент», ты почти всегда пишешь или переиспользуешь `Condition_*`.

Ключевое: **`Command` — это фиксированный, встроенный в движок словарь проверок.** Новую команду
изобрести нельзя (она резолвится нативно в C++), но из существующих команд можно собрать сколь угодно
сложное условие. Ниже — как устроена строка и какие команды реально встречаются в данных.

## Анатомия строки условия

У строки два списка групп — `AndConditionsList` и `OrConditionsList` — а внутри каждой группы массив
`Conditions` из атомарных проверок. Логика читается по трём уровням:

- проверки **внутри одной группы** (`Conditions`) — соединяются через **И** (все должны быть истинны);
- группы **внутри `AndConditionsList`** — тоже через **И** (нужны все группы);
- группы **внутри `OrConditionsList`** — через **ИЛИ** (достаточно любой группы).

Пустой список — «нет ограничения». Итог строки — грубо `(&& все And-группы) && (|| хотя бы одна
Or-группа)`.

### Атомарная проверка

Одна проверка — это всегда набор из семи полей:

| Поле | Смысл |
|---|---|
| `BaseObject` | кого проверяем: `Self` (действующий зой) или `Target` (цель/объект интеракции) |
| `Command` | какая встроенная проверка (словарь ниже) |
| `CompareType` | как сравнивать: `Equal`, `NotEqual`, `Greater`, `Less`… |
| `UseHand` | для «ручных» проверок: `Default` / `Right` / `Left` |
| `S1`, `S2` | строковые аргументы (тег, id баффа, эмоция, пол, стат, роль…) |
| `F1`, `F2` | числовые аргументы (уровень, порог) |

## Словарь Command

Ниже — команды, подтверждённые на реальных строках через MCP. Список не исчерпывающий (словарь
нативный и большой), но покрывает самые ходовые.

### Проверки объекта / цели

| Command | `BaseObject` | Аргументы | Что проверяет | Живой пример |
|---|---|---|---|---|
| `HasObjectTag` | `Target` (или `Self`) | `S1` = тег | есть ли у объекта тег | `IsComputer`: Target имеет `Create_Computer` |
| `HasCarriedObject` | `Self` | `UseHand`, `S1` | держит ли предмет в руке | `HasAnyEmptyHand`: рука не занята (`NotEqual`) |
| `HasOwnership` | `Target` | — | принадлежит ли цель домохозяйству | `Check_MyHousehold_Ownership` |
| `GiftBoxTendency` | `Target` | `S1` = `Positive`/`Negative` | «настроение» подарка | `GiftBoxTendency_Positive` |

### Состояние персонажа

| Command | `BaseObject` | Аргументы | Что проверяет | Живой пример |
|---|---|---|---|---|
| `EmotionLevel` | `Self` | `S1` = эмоция, `F1` = уровень | точный уровень эмоции | `Self_Uneasy_Lv2`: `Uneasy == 2` |
| `Emotion` | `Self` | `S1` = эмоция | активна ли эмоция вообще | `Emotion_Sad_Over_Lv2` |
| `Stat` | `Self` | `S1` = стат, `F1` = порог | сравнение характеристики | `Check_Energy_PrisonBreak`: `Energy > -99` |
| `Buff` | `Self` | `S1` = id баффа | активен ли конкретный бафф | `HasBuff_GoOut_Prison` |
| `BuffTag` | `Self` | `S1` = тег баффа | активен ли бафф с тегом | `Resort_Check_In_Related_Buffs` |
| `Gender` | `Self`/`Target` | `S1` = `Male`/`Female` | пол персонажа | `Check_MF`: Self `Male` И Target `Female` |

### Роль, локация, мир

| Command | `BaseObject` | Аргументы | Что проверяет | Живой пример |
|---|---|---|---|---|
| `IsSiteEventRole` | `Self` | `S1` = роль | роль персонажа в событии локации | `IsPlayingEvent_BirthdayPerson`: `BirthdayPerson` |
| `IsPlayingSiteEvent` | `Self` | `S1` = событие/`None` | идёт ли событие локации | `Check_MyHousehold_Ownership` |
| `IsCurrentSiteHouseholdBiz` | `Self` | — | текущая локация — бизнес домохозяйства | `Check_MyHousehold_Ownership` |
| `EnteredSiteHasTag` | `Target`/`Self` | `S1` = тег локации | тег текущей локации | `Resort_Room` |

```{note}
В {doc}`05-interaction-pipeline` задокументированы ещё несколько команд из этого же словаря, которые
чаще резолвятся нативно: `IsSiteScheduleNPC` (сотрудник этой локации по расписанию),
`CharacterGroupType` (тип группы: `ShopNpc`, `SiteRoleNpc`…), `InteractionTargetIsOwner` (я владелец
именно этой цели), `IsCalendarEventDay` (календарное событие).
```

## Как читаются AND и OR — три реальных примера

**Чистое И (одна группа, две проверки).** `Check_MF` — «Self мужчина И Target женщина»:

```{jsonblock} Condition_Interaction.Check_MF.AndConditionsList (фрагмент строки)
"AndConditionsList": [{ "Conditions": [
  { "BaseObject": "Self",   "Command": "Gender", "CompareType": "Equal", "S1": "Male" },
  { "BaseObject": "Target", "Command": "Gender", "CompareType": "Equal", "S1": "Female" }
]}]
```

**Чистое ИЛИ (несколько групп по одной проверке).** `HasAnyEmptyHand` — свободна хотя бы одна рука:
три группы в `OrConditionsList`, каждая проверяет свою руку (`Default`/`Right`/`Left`) через
`HasCarriedObject` c `NotEqual`. Достаточно, чтобы сработала любая.

**Смешанное.** `Check_MyHousehold_Ownership` — четыре Or-группы: «цель в собственности» ИЛИ «это
номер курорта И у меня бафф заселения» ИЛИ «идёт событие локации (не пожар)» ИЛИ «локация — мой
бизнес». Обрати внимание на вторую группу: внутри неё две проверки, соединённые через И
(`EnteredSiteHasTag` + `BuffTag`), — то есть И и ИЛИ свободно комбинируются на разных уровнях.

## Что это значит для мода

- **Сначала ищи готовое условие.** Прежде чем плодить новое, посмотри `list_table_rows` по
  `Condition_Interaction` — очень часто нужная проверка (пол, эмоция, тег объекта, наличие баффа) уже
  есть под понятным именем, и её достаточно вписать в `…ConditionIds` своего `InteractionBag`.
- **Своё условие — комбинация существующих команд.** Ты не пишешь новый `Command`, а собираешь строку
  из атомарных проверок словаря выше, раскладывая их по And/Or-группам под нужную логику.

```{caution}
`AndConditionsList`/`OrConditionsList` и вложенные `Conditions` — это массивы структур, а их MCP
`set_data` стрингифицирует и ломает (см. {doc}`13-gotchas`). Новые условия создавай **вручную в
редакторе ModKit**. MCP отлично подходит, чтобы найти и прочитать существующие (`get_row`,
`list_table_rows`) — этим и собран весь словарь выше.
```

```{seealso}
- Где условия «навешиваются» на пункт меню — {doc}`05a-interaction-bag` и
  {doc}`02b-object-selection-set`.
- Общая механика interaction-конвейера и команды, резолвящиеся нативно — {doc}`05-interaction-pipeline`.
- Как через бафф хранится «владение объектом» (пример условия на `Buff`) —
  {doc}`../case-studies/change-pc-role`.
```
