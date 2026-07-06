# Save → Package → CurseForge

Финальный конвейер публикации, одинаковый для любого типа мода.

```
save → package → cf_create_mod → cf_update_uplugin → cf_publish
```

`cf_publish` — это «упаковать → зазипить → залить» одним вызовом (альтернатива — руками через
`package` + `cf_upload_mod_file`). Авторизация — email OTP: `cf_send_code` → `cf_verify_code`,
статус — `cf_status`.

```{important}
Если плагин — UI Mod (есть `ui/uimod_apps.json`), категория на CurseForge **всегда** форсируется в
`Overlay UI / General`, любые переданные `class_id`/`category` игнорируются.
```

```{note}
MCP не умеет запускать саму игру — `modkit_start_uimod_preview`/`end_uimod_preview` предполагают,
что игра уже запущена отдельным процессом. Для BUILD/CAZ вообще нет аналога «превью в игре» —
только `open_bp_editor` и 3D-превью внутри самого ModKit. Тестирование после `package` — только
руками, отдельным запуском игры.
```
