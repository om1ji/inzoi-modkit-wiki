# Планы развития

Список того, что стоит добавить/дописать в следующих сессиях.

- [ ] **Туториал: как добавить новое действие на объект** — обобщённый пошаговый гайд (не привязанный
  к конкретному предмету вроде туалета), с шаблоном под любой объект: найти `InteractionBag` через
  `ObjectSelectionSet`, решить точку подключения скрипта, создать `Script_Interaction`-строку,
  подключить. Черновик уже есть в {doc}`case-studies/toilet-money`, but нужно обобщить.
- [ ] **Что такое InteractionBag** — отдельная концептуальная страница-объяснение (сейчас это
  подраздел {doc}`architecture/05-interaction-pipeline` и разбор конкретного примера в
  {doc}`case-studies/toilet-money` — нужно вынести общее объяснение в отдельную, самостоятельную
  страницу).
- [ ] **Как добавлять новые Interaction и Script_Interaction строки** — отдельно от InteractionBag:
  подробнее про сам формат `Interaction`/`Action` (не только `InteractionBag`), про структуру
  `Script_Interaction.Scripts[].Executes[]` и доступный словарь `Command` (сейчас частично покрыто
  в {doc}`architecture/05-interaction-pipeline`, но не как отдельный how-to).

## Известные открытые вопросы (не забыть)

- Баг с пропадающими 3D-моделями при паковке нетронутого BUILD-воркспейса (см.
  {doc}`architecture/13-gotchas` и {doc}`case-studies/toilet-money`) — план проверки есть, ещё не
  выполнен.
- Реальный script ID для `AddBuff`/`RemoveBuff` (механика владения объектом, см.
  {doc}`case-studies/change-pc-role`) — не найден через данные, возможно резолвится нативно.
