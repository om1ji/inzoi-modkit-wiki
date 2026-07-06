# Blueprint и компоненты

У каждой BUILD/CAZ книги есть blueprint с деревом компонентов.

`add_component` · `remove_component` · `set_component_prop` · `set_transform` · `set_mesh` ·
`open_bp_editor` · `compile_bp`

`list_components` показывает реальное дерево. Пример из `Computer01`:

```
MeshRootComponent → SkeletalMeshComponent → StaticMeshComponent → SlotComponent
```

(клавиатура/мышь), плюс `InteractionSlot*` и `FxSlot*`.

`set_component_prop` пишет произвольный key/value в PropertyMetaData — это единственный
«open-ended» способ задать нестандартное свойство компонента без готового tool под него.

```{seealso}
Порядок операций: структурные изменения → `compile_bp` → изменения свойств. См.
{doc}`00-overview`.
```
