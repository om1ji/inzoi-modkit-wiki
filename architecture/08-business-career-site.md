# Career / Site / Business

Работа, места и права доступа — отдельная, тесно переплетённая подсистема.

`Career` → `Organizations[]` → `RankList[]` → `Shift[]` с полем `bRequiresCareerSeat` — подтверждает,
что у рангов сотрудников есть привязка к рабочему месту. Права доступа к местам (двери, зоны)
выражаются через enum `EB1DoorPermissionGroup`:

`All` · `Nobody` · `Family` · `Me` · `Company` · `BusinessOwner` · `BusinessOwnerOrEmployee` ·
`CareerMember` · `CareerOperating`

`Site`/`SiteAction`/`SiteEvent` таблицы плюс `DA_SiteConfig`/`DA_SiteEditCondition` управляют
локациями (двери, почтовые ящики, видимость UI редактирования сайта по типу/подтипу/конкретному
ID).

Полный разбор этой подсистемы (в контексте механики "владения" объектом) — в
{doc}`../case-studies/change-pc-role`.
