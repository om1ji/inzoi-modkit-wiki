# Books → Object → ObjectTemplate

Три слоя одного и того же физического предмета, каждый со своей ролью.

```
Book id (Computer01) → Object (общие свойства) → ObjectTemplate (сцена/меши/слоты)
  → ObjectSelectionSet (см. интеракции, {doc}`05-interaction-pipeline`)
```

- **`Object`** — вес, цена, теги, категория фильтра, налог (`TaxId`).
- **`ObjectTemplate`** — привязка к Actor blueprint, поведение при намокании, `OwnershipCategory`
  (категория для системы личной собственности вроде `Bed`, а **не** «кто владелец» — это частая
  ловушка: у всех проверенных компьютеров/ноутбуков стоит `None`). Полный разбор всех полей шаблона —
  в {doc}`02a-object-template`.

Найти конкретные книги:

```
modkit_list_categories(book_class) → modkit_list_books(book_class, category)
```

Без категории `list_books` отдаёт всё и жжёт токены — всегда сначала категория.

## Пример: Computer01

```{jsonblock} Object.Computer01 (поля сокращены)
{
  "Id": "Computer01",
  "ObjectTemplateId": "Computer01_Template",
  "FilterCategory": "HomeOffice_PC",
  "ObjectTags": ["Expensive", "Create_Computer", "Computer"],
  "TaxId": "Electricity",
  "Price": 980
}
```

```{jsonblock} ObjectTemplate.Computer01_Template (поля сокращены)
{
  "Id": "Computer01_Template",
  "ObjectSelectionSetId": "Computer01",
  "OwnershipCategory": "None",
  "ObjectTags": ["Computer_Check"],
  "IsWettable": true
}
```
