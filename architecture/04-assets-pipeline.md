# Меши, текстуры, материалы

Импорт внешних ассетов и создание материалов поверх мастер-материалов игры.

| Инструмент | Что делает |
|---|---|
| `import_mesh` | FBX → Mesh-папка мода; скрипт импорта зависит от типа воркспейса (BUILD: collision, CAZ Garment: скелет SK_Base + LOD, CAZ Hair: Face_Archetype + LOD) |
| `import_texture` | Картинка → Textures/; пресет (Normal/BaseColor/ARM/ColorMask/RGBMask/Stocking/UI) определяет mip/сжатие/sRGB. Непочётные степени двойки авто-ресемплятся |
| `create_material` | Новый MaterialInstanceConstant от мастер-материала (префикс `MI_` — автоматически) |
| `assign_material` | Материал → слот меш-компонента. Только BUILD; для CAZ — через панель редактора |
| `set_material_texture` | Текстурный параметр материала |

## Fab / Asset Capture — импорт готовых 3D-ассетов

Отдельный конвейер под «Fab Add to Project»:

```
begin_asset_capture (снимок состояния до)
  → пользователь добавляет ассет через Fab в редакторе
  → finish_asset_capture (диф новых файлов)
  → analyze_asset_capture (какой из новых файлов — «главный» ассет)
  → finalize_fab_capture_to_workspace (привязать к сокету/полю воркспейса)
    или discard_asset_capture (отмена)
```
