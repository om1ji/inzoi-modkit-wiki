# Data Tables

~980 построчных таблиц. Любая правка мода — либо Override существующей строки, либо добавление
новой.

`list_tables` · `list_table_rows` · `get_row` / `get_row_batch` · `set_data` / `set_data_batch`

`get_row_batch`/`set_data_batch` — всегда предпочтительнее цикла одиночных вызовов (меньше токенов,
один патч вместо серии). Для DLC-контента иногда обязателен параметр `dlc` (например, `E01`) —
редактор сам подсказывает об этом в ошибке, если забыть.

Самые крупные семейства по префиксу (подробно разобраны в {doc}`../case-studies/data-hierarchy`):
`Script_*` (104), `Condition_*` (75), `InteractionBag_*` (57), `Action_*` (34).

```{danger}
Про надёжность `set_data`/`set_data_batch` для массивов и структур — см. {doc}`13-gotchas`.
```
