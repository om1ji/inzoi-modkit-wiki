# Как это всё устроено

Один мод (проект) — это набор «воркспейсов» разных типов поверх общих игровых данных.

```
Project (plugin) → Workspace (book_class) → правки: Object/Table/DataAsset/Blueprint/UI
  → Save → Package → CurseForge
```

Под капотом почти всё, что видно и редактируется, — это строки в общих игровых Data Tables и
Data Assets (см. {doc}`../case-studies/data-hierarchy`). Workspace — это просто «окно
редактирования» поверх них: он решает, какую книгу (`book`) ты Override-ишь или Duplicate-ишь, и
какой набор инструментов тебе доступен.

```{note}
**Сквозное правило.** Почти для всех write-инструментов ModKit важен порядок: сначала структурные
изменения (add/remove component, add/remove workspace), затем `compile_bp`, и только потом —
изменения свойств (`set_mesh`, `set_transform`, `assign_material`, `set_component_prop`).
Компиляция может сбросить значения свойств, если сделать её позже.
```
