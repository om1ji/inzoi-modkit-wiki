# Проект и Workspace

`modkit_create_project` → один проект может содержать много воркспейсов разных типов.

| book_class | Что редактирует | Особенность |
|---|---|---|
| `BUILD` | Мебель/конструкции | Furniture / Construct группы, blueprint-компоненты |
| `CAZ` | Одежда, волосы, аксессуары | Материалы задаются в самом редакторе, не через `assign_material` |
| `CHARACTER_ANIMATION` | Анимации персонажа | Требует `category`: Interaction/Locomotion/StatLocomotion |
| `SOUND` | Звуковые объекты | — |
| `DA` | Data Asset (глобальный конфиг) | Ответ `add_workspace` сразу включает текущие значения |
| `Language` | Локализация | Не использует книги — только source/target culture; singleton на пару культур |
| `UIMod` | Кастомный UI (HTML/JS/CSS) | **Singleton на проект** — повторный `add_workspace` просто возвращает существующий |
| `Talk` | Диалоги/реплики | Одно поле `build_talk_patch` правит сразу 5 таблиц |
| `Script` | Одиночные скрипт-книги | `mode='Duplicate'` должен «чеканить» новый id — **на практике не заработало**, см. {doc}`13-gotchas` |

Режим `Override` подменяет существующий `book_id` "на лету" — с загруженным модом та же вещь в игре
меняется. `Duplicate` — клонирует под новым ID, оригинал остаётся доступен. Для Duplicate можно
указать, копировать ли исходные ассеты (`copy_assets`).

Жизненный цикл воркспейса:

```
add_workspace (открывается сам)
  → inspect_workspace (что заполнено, % готовности — только для типов с IWorkspaceAutomation;
                        BUILD/SOUND его не поддерживают)
  → validate_workspace (готов ли к паке)
  → refresh_workspace (обновить UI/3D-превью после пачки правок)
  → delete_workspace (необратимо)
```
