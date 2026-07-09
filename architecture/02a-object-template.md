# Что такое ObjectTemplate

`ObjectTemplate` — это средний из трёх слоёв, которыми в игре описан один предмет. Если коротко:
`Object` отвечает на вопрос «что это за вещь вообще» (цена, теги, налог), а `ObjectTemplate` — на
вопрос «как эта вещь существует в 3D-мире и как с ней связаны действия». Это не отдельная сущность,
а обычная строка таблицы `ObjectTemplate`, на которую `Object` ссылается по ID.

```
Object (паспорт предмета)
  → ObjectTemplateId ──► ObjectTemplate (предмет на сцене)
                            → ObjectSelectionSetId ──► ObjectSelectionSet (меню действий)
```

Почему слой вынесен отдельно, а не слит с `Object`: один и тот же «паспорт» может переиспользовать
общий шаблон сцены, а главное — именно через шаблон предмет подключается к системе интеракций. Поле
`ObjectSelectionSetId` — тот самый мост, с которого начинается вся цепочка «что можно сделать с
предметом» (подробный разбор — в {doc}`../case-studies/interaction-layers`).

## Из чего состоит строка

Поля шаблона удобно разбить по смыслу. Значения ниже — реальные, вытащенные из редактора через MCP.

### Идентичность и связи

Три поля, которые делают шаблон частью цепочки:

- **`Asset`** — путь к blueprint-актору предмета (например
  `…/Templates/BP_Toilet01_Template.BP_Toilet01_Template`). Это «физическое тело» предмета: меши,
  слоты, эффекты, коллизии. Всё, что ты редактируешь в blueprint-редакторе, живёт по этому пути.
- **`ObjectSelectionSetId`** — ID строки `ObjectSelectionSet`, где перечислены доступные пункты меню
  по состояниям. Ключевая связь вниз: без неё у предмета не будет ни одного действия.
- **`ObjectTags`** — теги уровня шаблона (например `Toilet_Check`, `Computer_Check`). Их проверяют
  условия интеракций через команду `HasObjectTag` — так игра отличает «это компьютер» от «это
  унитаз», не завязываясь на конкретный ID.

### Поведение на сцене

- **`IsWettable`** — может ли предмет намокать (у сантехники и мебели обычно `true`).
- **`FollowSlotRotation`** / **`bForceChildFollowSlotRotation`** — поворачивается ли предмет (и
  предметы, прикреплённые к нему) вслед за слотом размещения.
- **`PlacementFlags`** — битовые флаги правил размещения в режиме строительства (на полу, на
  столешнице и т.д.).
- **`PlacementGuideTextId`** — ID подсказки в UI строительства (у компьютера —
  `UI_BuildMode_KeyGuideDesc_On_ComputerTable_Text`; у унитаза пусто).
- **`ObjectWeatheringGroupId`** / **`WeatherAutonomyBehavior`** / **`WeatherScripts`** — как предмет
  стареет/пачкается и как NPC реагируют на погоду рядом с ним (`AvoidBadWeather` — избегать плохой
  погоды).
- **`CustomizeType`** — что можно кастомизировать (`MaterialOnly` — только материалы/цвет).

### Переносимость и инвентарь

- **`IsCarriable`** — можно ли взять предмет в руки. У мебели `false`, у гитары — `true`.
- **`CarryHandStyle`** — как предмет держат в руках (`OneHand`, `Invalid` если не переносится).
- **`bDisableTakeOutOfInventory`** / **`bCanInteractInInventory`** — можно ли доставать из инвентаря
  и взаимодействовать прямо в нём.
- **`InventroyInteractionBagId`** — набор интеракций, доступных с предметом в инвентаре (обрати
  внимание: в названии поля опечатка разработчиков — `Inventroy`, а не `Inventory`; писать надо ровно
  как в данных).

### Личная собственность

- **`OwnershipCategory`** — категория предмета для системы личной собственности: у кровати — `Bed`,
  у большинства предметов — `None`.

```{warning}
`OwnershipCategory` — это **не «кто владелец»**, а *к какому классу собственности относится сам
предмет*. Это частая ловушка: у всех проверенных компьютеров и унитазов тут `None`, хотя владеть ими
персонаж может. Реальное «владение» (эксклюзивное право NPC на объект) хранится не здесь, а в баффе
на персонаже — см. {doc}`../case-studies/change-pc-role`.
```

## Сравнение реальных шаблонов

Как одни и те же поля отличаются у четырёх разных предметов:

| Поле | `Toilet01` | `Computer01` | `Bed01` | `Guitar01` |
|---|---|---|---|---|
| `ObjectSelectionSetId` | `Toilet01` | `Computer01` | `Bed01` | — |
| `IsCarriable` | `false` | `false` | `false` | **`true`** |
| `CarryHandStyle` | `Invalid` | `Invalid` | `Invalid` | **`OneHand`** |
| `OwnershipCategory` | `None` | `None` | **`Bed`** | `None` |
| `ObjectTags` | `Toilet_Check` | `Computer_Check` | `Bed_Double`, `Bed` | — |
| `IsWettable` | `true` | `true` | `true` | — |
| `PlacementGuideTextId` | (пусто) | `…On_ComputerTable…` | (пусто) | — |

Видно закономерность: мебель неподвижна (`IsCarriable: false`, `CarryHandStyle: Invalid`), а гитара —
переносимый предмет. `OwnershipCategory` заполнен только там, где предмет реально участвует в системе
собственности как отдельный класс (кровать).

## Как шаблон правят в моде

Чаще всего `ObjectTemplate` **не трогают напрямую** — правят либо `Object` (цена, теги), либо
blueprint по пути `Asset` (меши/материалы через BUILD-воркспейс), либо цепочку интеракций через
`ObjectSelectionSetId`. Но если нужно поменять само поведение (сделать предмет переносимым, сменить
`OwnershipCategory`, поправить тег), это делается как Override строки шаблона.

```{caution}
Скалярные поля (`IsCarriable`, `OwnershipCategory`, `PlacementFlags`, имена-enum) через MCP
`set_data` пишутся надёжно. А вот поля-массивы (`ObjectTags`, `AvailableSocialClusterType`,
`WeatherScripts`) MCP стрингифицирует — их правь вручную в редакторе. Подробнее —
{doc}`13-gotchas`.
```

```{seealso}
- Общая тройка слоёв Book → Object → ObjectTemplate — в {doc}`02-books-objects`.
- Куда ведёт `ObjectSelectionSetId` и как из него разворачивается меню — в
  {doc}`../case-studies/interaction-layers`.
```
