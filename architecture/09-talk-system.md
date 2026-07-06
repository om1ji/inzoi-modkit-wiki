# Talk-система

Единственный воркспейс, где один вызов патчит сразу 5 таблиц.

`modkit_build_talk_patch` из 9 полей на реплику создаёт/патчит строки в `TalkSelection`,
`InteractionBag_Talk(+Feedback)`, `CoopTalk`, `Script_Talk`, `Condition_Interaction_Talk` одним
вызовом — включая генерацию ID, путей иконок, массивов анимаций/озвучки и регистрацию в
StringTable.

```{warning}
Повторный вызов с теми же репликами создаёт дубликаты (ID чеканятся по timestamp-хэшу) — все
реплики нужно класть в один вызов.
```
