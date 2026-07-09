# Планы развития

Список того, что стоит добавить/дописать в следующих сессиях.

- [ ] **Туториал: как добавить новое действие на объект** — обобщённый пошаговый гайд (не привязанный
  к конкретному предмету вроде туалета), с шаблоном под любой объект: найти `InteractionBag` через
  `ObjectSelectionSet`, решить точку подключения скрипта, создать `Script_Interaction`-строку,
  подключить. Частично покрыто интерактивной схемой в {doc}`case-studies/interaction-layers`, но
  отдельной пошаговой страницы-туториала пока нет.
- [x] **Что такое InteractionBag** — вынесено в отдельную страницу {doc}`architecture/05a-interaction-bag`
  (поля по смыслу, контраст простого `Toilet01_Use` и сложного `Computer_Use`).
- [x] **Словарь `Command` и движок условий** — вынесено в {doc}`architecture/05b-conditions`
  (`AndConditionsList`/`OrConditionsList`, реальные команды `HasObjectTag`/`Buff`/`Stat`/`EmotionLevel`…).
- [ ] **Как добавлять новые Interaction и Script_Interaction строки** — отдельно от InteractionBag:
  подробнее про сам формат `Interaction`/`Action` (не только `InteractionBag`) и про структуру
  `Script_Interaction.Scripts[].Executes[]` — как отдельный how-to.

## Известные открытые вопросы (не забыть)

- Баг с пропадающими 3D-моделями при паковке нетронутого BUILD-воркспейса (см.
  {doc}`architecture/13-gotchas` и {doc}`case-studies/toilet-money`) — план проверки есть, ещё не
  выполнен.
- Реальный script ID для `AddBuff`/`RemoveBuff` (механика владения объектом, см.
  {doc}`case-studies/change-pc-role`) — не найден через данные, возможно резолвится нативно.
