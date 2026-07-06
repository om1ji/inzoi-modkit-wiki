# Карта данных: Books / Data Tables / Data Assets

ModKit хранит игровые данные в трёх независимых системах. Они не вложены друг в друга — это
отдельные хранилища, которые ссылаются друг на друга по строковым ID.

```{raw} html
<iframe src="../_static/interactive/data-hierarchy-map.html"
        style="width:100%;height:820px;border:1px solid var(--color-background-border);border-radius:8px;"
        loading="lazy"></iframe>
<p><a href="../_static/interactive/data-hierarchy-map.html" target="_blank">Открыть схему на весь экран ↗</a></p>
```

## 01 · Books — предметы

Конкретные игровые сущности: мебель, одежда, причёски, анимации. У каждой книги (`book_id`,
например `Computer01`) есть blueprint с компонентами (меши, слоты, эффекты) и рабочая область
(workspace) — **Override** (заменяет ID вживую) или **Duplicate** (клонирует под новым ID).

- `BUILD` → **Furniture** и **Construct**
- `CAZ` → одежда/внешность
- `Hair` · `CHARACTER_ANIMATION` · `Script`

Примеры категорий BUILD (Furniture): `HomeOffice_PC` (5 книг), `Light_Ceiling` (82), `Kitchen_
CookingUtensils` (51), `Sofa` (45); Construct: `Window` (65), `Door` (49).

Примеры категорий CAZ: `Hair` (487 книг), `AttachedAccessory` (264), `Jacket` (266), `Top` (257),
`Bottom` (204), `Shoes` (203).

## 02 · Data Tables — построчные данные

980 таблиц (`DT_*` внутри игры). Каждая — обычная строковая таблица с колонкой `Id`. Мод либо
Override-ит существующую строку, либо добавляет новую (Duplicate) через `set_data` /
`set_data_batch`. Самая крупная группа — `Script_*` (104 таблицы) — игровая логика конкретных
систем (питомцы, отношения, события).

| Префикс | Таблиц | Что это, как правило |
|---|---|---|
| `Script_*` | 104 | Логика систем: `Script_Interaction_Computer`, `Script_Farming`, `Script_Crime`… |
| `Condition_*` | 75 | Условия доступности интеракций/действий |
| `InteractionBag_*` | 57 | Наборы (bag) интеракций |
| `Action_*` | 34 | Атомарные игровые действия |
| `Interaction_*` | 33 | Отдельные интеракции (не bag) |
| `Object_*` | 21 | Свойства игровых объектов/предметов |
| `Garment*` | ~30 | Меши и слоты одежды по типу (Top, Jacket, Shoes…) |
| `Appearance*` | ~25 | Внешность персонажа (CAS): волосы, лицо, макияж |
| `Buff_* / Modifier_*` | 32 | Баффы и модификаторы характеристик |
| `Mission_*` | 13 | Квесты/миссии |

## 03 · Data Assets — глобальные конфиги

153 типа (`DA_*`, UClass вида `B1*DataAsset`). В отличие от таблиц — это **не строки**, а один
объект-синглтон на класс: глобальные настройки целой системы (дистанции интеракций, тайминги
автономии, ID заглушек-реакций). Открываются как воркспейс с `book_class='DA'`.

Группировка по домену (примеры):

- **Персонаж и жизнь**: `DA_Ambition`, `DA_Aging`, `DA_Trait`, `DA_Relationship`, `DA_Career`, `DA_Skill`, `DA_Emotion`, `DA_CharacterAttribute`
- **Город и мир**: `DA_CityEdit`, `DA_CityMove`, `DA_TrafficControl`, `DA_Weather`, `DA_Disaster`, `DA_Population`
- **Объекты и взаимодействие**: `DA_Interaction`, `DA_ActiveInteraction`, `DA_BuildCommon`, `DA_Crafting`, `DA_Inventory`, `DA_Depreciation`
- **UI и система**: `DA_Widget`, `DA_Popup`, `DA_LoadingScreen`, `DA_SaveLoad`, `DA_InputMappingContext`, `DA_Minimap`

## Живой пример: Computer01

Трассировка через все три слоя:

1. **Book**: `Computer01` (категория `HomeOffice_PC`, группа Furniture). Blueprint содержит
   `InteractionSlot`, `InteractionSlot_Cleaning`, `FxSlot_Broken` — слоты, которые в рантайме дергают
   конкретные интеракции.
2. **Data Table**: `Script_Interaction_Computer` (18 строк) + `InteractionBag_Computer`. Строки
   описывают конкретные действия на компьютере и группируют их в bag'и, на которые ссылается ID
   вроде `AutonomyFailedInteractionBagId`.
3. **Data Asset**: `DA_Interaction` — глобальные тайминги и радиусы, ОДИН на всю игру.
   `MaxInteractionRange`, `AutonomyIntervalMin/Max`, `ClickableObjectInteractionRange` — эти значения
   действуют на все объекты игры разом, `Computer01` их не переопределяет, а просто наследует.

## Шпаргалка по инструментам

| Слой | Инструменты |
|---|---|
| Books | `list_categories` · `list_books` · `add_workspace` · `list_components` |
| Data Tables | `list_tables` · `list_table_rows` · `get_row` / `get_row_batch` · `set_data` / `set_data_batch` |
| Data Assets | `list_data_asset_types` · `get_data_asset_schema` · `get_data_asset_values` · `set_data_asset_fields` |
