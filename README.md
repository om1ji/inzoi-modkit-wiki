# inZOI ModKit Wiki

Неофициальные заметки по моддингу **inZOI** через **ModKit** — собраны на практике, через живой
MCP-сервер редактора: реальные поля таблиц, реальные значения, реальные баги инструментов.

Не официальная документация Krafton/inZOI Team. Материал собран моддерским сообществом путём
исследования данных, доступных через сам ModKit.

## Сборка локально

```bash
git clone https://github.com/om1ji/inzoi-modkit-wiki.git
cd inzoi-modkit-wiki
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make html
open _build/html/index.html
```

## Структура

- `architecture/` — общая механика ModKit (воркспейсы, books, blueprint, interaction-конвейер,
  data assets/tables, известные проблемы MCP и т.д.)
- `case-studies/` — разборы конкретных примеров: карта данных, механика владения объектом
  (Change PC Role), рабочий how-to (Toilet Money)

## Вклад

PR и issue приветствуются — особенно если нашли более надёжный способ обойти баги MCP, описанные
в `architecture/13-gotchas.md`, или подтвердили/опровергли открытые гипотезы в `case-studies/`.

## Лицензия

[MIT](LICENSE).
