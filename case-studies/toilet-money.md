# Разбор и how-to: Toilet01_Use → +50 Mew

Первый доведённый до конца мод серии: «После использования туалета персонажу начисляется 50 Mew».
Подтверждено в игре — деньги реально начисляются.

## Разбор строки InteractionBag.Toilet01_Use

Полный разбор одной реальной строки `InteractionBag` — все поля одного живого пункта меню
(«Использовать унитаз»), с реальными значениями.

- **Id**: `Toilet01_Use` · книга `Toilet01` · таблица — **плоская** `InteractionBag` (без суффикса)
- **Comment**: `변기01 사용 - Normal 빈도. Toilet15 보상...` — служебный конспект разработчика на
  корейском (частота/награда/постура/ветки)

### Награды

| Поле | Значение | Смысл |
|---|---|---|
| `InteractionRewards` | `Toilet +15` | восстановление мотива «Туалет» |
| `PreferenceRewards.EmotionRewards` | `Uncomfortable 1→2 (+8), Irritated 2→3 (−5)` | шанс словить лёгкий дискомфорт/раздражение |

### Теги, группировка, условия

| Поле | Значение | Смысл |
|---|---|---|
| `InteractionBagTags` | `IR_Freq_Normal, GeneralEffectTag_Check_UseToilet` | частота самостоятельного выбора NPC + тег эффектов |
| `AutonomyGroupTag` | `AGTag_Toilet_Use` | группа для системы автономного поведения NPC |
| `PostureGroupId` | `AllGroup` | поза не ограничена конкретной группой |
| `GroupID` / `InteractionBagCategory` / `TPOTags` / `StrongEmotionFilters` | `None` / `None` / `[]` / `[]` | не используется в этой строке |
| `EnqueueConditionIds` / `VisibleConditionIds` / `EnableConditionIds` | `[]` / `[]` / `[]` | условий доступа нет — доступно почти всегда (сравни с `Computer_Use`, где висят реальные условия) |
| `AgingConditionFlags` | `508` | битовая маска допустимых возрастных групп |
| `ZoiGroupFlags` / `RotationCoopId` / `bAddSameInteractionToGroupMember` / `CompetitionRuleId` | `0` / `None` / `false` / `None` | не групповое и не соревновательное действие |
| `RepeatCount` | `1` | без автоповтора |

### InteractionSequence — три ветки

Ядро логики: что реально происходит, когда персонаж садится/встаёт у унитаза.

| Ветка | Вероятность | Условие | → Interaction | Дальше (NextInteractionBagId) |
|---|---|---|---|---|
| `Breakable_Water` | 0.499 | `None` | `Toilet01_Use` | `Next_WashHand04_AfterUse_Toilet` |
| `Toilet_Phone` | 0.5 | `None` | `Toilet01_Use_Phone` | `Next_WashHand04_AfterUse_Toilet` |
| `Break` | 0.001 | `OnlyResidenceType_Target` | `Toilet01_Use_Broken` | `None` (конец цепочки) |

Обычное использование (~50/50 «просто» или «с телефоном») почти всегда ведёт к мытью рук; шанс
поломки — 0.1%, и только дома.

### Скрипты — точка подключения нового Action

| Поле | Значение | Смысл |
|---|---|---|
| `StartScriptIds` | `Object_Start_Toilet_VeryLow` | условный (сработает только при теге `Toilet_VeryLow` — крайняя нужда) |
| `FinishScriptIds` | `Object_Finish_Toilet_VeryLow` | тоже условный; сюда дописан безусловный `AddCurrency_50` |
| `SelectedScriptId` / `StartHowlingInfos` | `None` / `[]` | не используются |

### Валюта, UI, автономия, флаги — по умолчанию выключено

| Поле | Значение |
|---|---|
| `ConsumeCurrencyId` / `ConsumeCurrencyValue` / `bIgnoreConsumeCurrencyCheck` | `None` / `0` / `false` |
| `DisplayInfo` | `DisplayTextId`/`DisplayCategoryTextId` заданы, иконки — дефолтные (`None`) |
| `bRejectable` / `bUniqueInQueue` / `bForFixedDesk` / `bNonCancelable` | `false` / `false` / `false` / `false` |
| `bGhostAvailable` / `AutonomyCooltimeMin` / `bAlwaysExposeToSLM` / `AutonomySLMCooltimeMin` | `false` / `0` / `false` / `0` |
| `ActionHintTextForSLM` | `"Using the toilet"` (дебаг-хинт для ИИ) |

```{note}
**Вывод из разбора.** У «простого» предмета вроде унитаза почти все продвинутые поля (условия,
валюта, групповое поведение) стоят в нейтральном состоянии — задействованы только награда,
ветвление и пара условных скриптов. Это типичная форма для базовой бытовой мебели; сравни с
`Computer_Use` в {doc}`../architecture/05-interaction-pipeline`, где реально заполнены условия
видимости/доступности.
```

## How-to: свой Action в существующей цепочке

### Куда подключать: две независимые точки, не одна цепочка

Ключевая ошибка, которую легко допустить: думать про `InteractionBag → Interaction →
Script_Interaction` как про одну сквозную цепочку. На самом деле `Script_Interaction` подключается в
двух параллельных, независимых местах:

| Точка подключения | Поле | Когда использовать |
|---|---|---|
| Уровень всей интеракции | `InteractionBag.StartScriptIds` / `FinishScriptIds` | награда/эффект должен сработать один раз — в начале или по завершении всего действия целиком (наш случай) |
| Уровень одного шага | `Action.Actions[].StartScriptIdList` / `FinishScriptIdList` | скрипт привязан к конкретной анимации/шагу внутри цепочки Interaction → Action (пример: `Electricity_Usage_200` у компьютера) |

`Interaction`/`Action` в первом варианте вообще не участвуют — это прямая связь `InteractionBag →
Script_Interaction`.

### Рецепт (воспроизведённый на Toilet01_Use)

**1. Найти нужный InteractionBag**

```
ObjectTemplate.<Item>_Template.ObjectSelectionSetId
  → ObjectSelectionSet.<Id>.SelectionSets[].InteractionBagList
```

Берём нужную по `StateGroupId` (обычно `Use`). Сама строка — ищи сначала в **плоской** таблице
`InteractionBag` (без суффикса).

**2. Создать Script_Interaction-строку — вручную в редакторе**

Таблица: `Script_Interaction` (плоская). Пример (`AddCurrency_50`): один блок `If` без условий →
`Executes`: `{BaseObject: Self, Command: AddCurrency, S1: Mew, F1: 50, Prob: 1}`.

```{caution}
**Не через MCP** — `set_data`/`set_data_batch` стрингифицируют массивы/структуры (см.
{doc}`../architecture/13-gotchas`). Регистр имён полей на практике оказался не критичен.
```

**3. Подключить — тоже вручную в редакторе**

В `InteractionBag.<Id>.FinishScriptIds` дописать новый ID к уже существующим (не заменяя!). Было:
`["Object_Finish_Toilet_VeryLow"]` → стало: `["Object_Finish_Toilet_VeryLow", "AddCurrency_50"]`.

**4. Save → Package → запустить игру вручную**

MCP не умеет запускать саму игру (см. {doc}`../architecture/12-publish`) — только
`modkit_save`/`modkit_package`. Дальше — вручную, отдельным процессом.

### Открытый баг: пропадают модели предметов

После включения мода 3D-модели унитазов переставали отображаться (сама интеракция и начисление
денег при этом работали). Отключение мода возвращало модели — значит, дело в самом моде, а не в
игре.

Рабочая гипотеза: BUILD-воркспейс `Toilet01` (Override) был создан для контекста редактирования, но
ни разу не тронут (`set_mesh`/`assign_material`/`compile_bp` не вызывались) — при паковке нетронутый
Override, возможно, экспортирует blueprint без ссылки на меш. При этом сама валютная логика — правки
общих таблиц (`InteractionBag`, `Script_Interaction`) уровня проекта, а не воркспейса, и
BUILD-воркспейс для них вообще не нужен.

```{admonition} План проверки (следующая сессия)
:class: tip

Удалить BUILD-воркспейс `Toilet01` целиком (`delete_workspace`) — оставив только табличные правки —
пересобрать и проверить: остаются ли деньги начисляться и возвращается ли видимость модели.

Также проверить, не остался ли где-то активным старый проект `Toilet_Money_4098A2A4` параллельно с
новым `Toilet_Money_445DBD3A` — оба Override-ят `Toilet01`, возможен конфликт.
```
