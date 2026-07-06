# Interaction-конвейер

Как игра решает «что можно сделать с этим предметом» — самая многослойная система в ModKit.

```
InteractionBag (пункт меню) → Interaction (обёртка + фильтр цели) → Action (анимации + скрипты)
```

Условия (`Condition_*` таблицы) — универсальный движок: каждая строка — список
`AndConditionsList`/`OrConditionsList`, а внутри — `{BaseObject, Command, CompareType, S1, S2, F1,
F2}`. `Command` — это словарь встроенных проверок (не таблица, а фиксированный набор нативных
функций):

| Command | BaseObject | Проверяет |
|---|---|---|
| `HasObjectTag` | Target/Self | есть ли тег у объекта |
| `Buff` / `BuffTag` | Self/Target | активный бафф / тег баффа |
| `HasOwnership` | Target | личная собственность (дом/вещь) |
| `InteractionTargetIsOwner` | Target | я — владелец именно этой цели интеракции |
| `IsSiteScheduleNPC` | Self | NPC по расписанию этой локации |
| `CharacterGroupType` | Self | тип группы персонажа (`ShopNpc`, `SiteRoleNpc`…) |
| `Stat` / `EnteredSiteHasTag` / `IsCalendarEventDay` | Self/Target | характеристики, тег текущей локации, календарное событие |

Баффы (`Buff` таблица) — то, где реально хранится изменяемое в рантайме состояние персонажа (и это
то, что уходит в savefile), а не статичные поля объекта. Подробный разбор конкретной цепочки —
в {doc}`../case-studies/change-pc-role`.

## ObjectSelectionSet — недостающее звено

`ObjectTemplate.ObjectSelectionSetId` ведёт в таблицу `ObjectSelectionSet`, где для каждого
`StateGroupId` (обычно `Normal`/`Use`/`Broken`…) явно перечислен список `InteractionBagList` —
именно здесь решается, какие пункты меню вообще доступны у конкретного предмета в конкретном
состоянии. Это то место, откуда стоит начинать поиск, если известен только `book_id`, а нужный
`InteractionBag` неизвестен.

Полный пример разобран в {doc}`../case-studies/toilet-money`.

```{important}
**Плоские vs именные таблицы.** У сложных предметов (Computer, TV) — свои таблицы с суффиксом
(`InteractionBag_Computer`, `Action_Interaction_Computer`…). У простой мебели (унитаз, кровать,
большинство обычных вещей) суффикса нет — интеракции лежат в **плоских** таблицах `InteractionBag`
/ `Interaction` / `Action_Interaction` / `Condition_Interaction` / `Script_Interaction` (без
подчёркивания и суффикса). Если `get_row` не находит строку ни в одной из специализированных
таблиц — проверь плоскую версию первой, не перебирай суффиксы вручную.
```

## Валюта: команда AddCurrency

Начисление/списание денег — это не поле объекта, а нативная команда внутри блока `Scripts` строки
таблицы `Script_Interaction*`:

```text
{
  "BaseObject": "Self",
  "Command": "AddCurrency",
  "S1": "<currency id>",
  "F1": <дельта>
}
```

Знак `F1` задаёт направление — отрицательное списывает (проверено на реальной строке
`RemoveCurrency_Mew_5`, `F1: -5`), положительное начисляет (проверено на нашем собственном примере,
см. {doc}`../case-studies/toilet-money`). Валюты в игре: `Zen, CatShopPoint, Mew, Nyang, Ong,
ResortCoin` — основная игровая валюта `Mew`.

Родственная команда — `AddCurrencyToHouseholdBiz` — кладёт/снимает деньги в кассу **бизнеса
игрока**, а не в личный кошелёк (пример: `Buy_Fireworks`, `Pay_TinCanTent`).

```{warning}
**Не путать с `ConsumeCurrencyId`/`ConsumeCurrencyValue`.** На самой строке `InteractionBag` есть
похожие поля — это *гейт* («хватает ли денег, чтобы начать действие»), а не способ начислить.
Отрицательное значение там ничем не подтверждено и, скорее всего, не работает как «начислить».
Верный способ — только через `Command: "AddCurrency"` в `Script_Interaction`-строке, подключённой
через `FinishScriptIds` у `InteractionBag`.
```
