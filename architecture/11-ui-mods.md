# UI Mods

Кастомный HTML/JS/CSS оверлей поверх игры — единственный воркспейс-синглтон на проект, но с
множеством «app» внутри.

```
add_workspace(UIMod) → create_uimod_app → write_uimod_file / write_uimod_manifest
  → start_uimod_preview
```

Каждый app — 4 файла (`uimod_manifest.json`, `index.html`, `app.js`, `styles.css`). Манифест задаёт
`triggers` (`always_on`/`keybind`/`command`/`game_mode`/`interaction_menu`…) и
`display.input_policy` (`overlay`/`modal`/`passthrough`). Игровые команды из `app.js` вызываются
через `inzoi.cli.execute(...)` — id команд нельзя изобретать, только из каталога
(`list_uimod_cli_commands`/`get_uimod_cli_command`).

Превью — временное (`start_uimod_preview`/`end_uimod_preview`), монтируется в отдельную
`ModKitPreview` папку, не трогая установленные моды игрока.
