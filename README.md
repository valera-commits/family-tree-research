# family-tree-research

Скилл для Claude Code: поиск предков по архивам Российской империи, СССР и Украины (метрические книги, ревизские сказки, исповедные ведомости, переселенческие списки, базы репрессированных и участников войн) и интерактивный «веер предков» с хроникой рода в одном HTML-файле.

## Установка

Как плагин:

```
/plugin marketplace add valera-commits/family-tree-research
/plugin install family-tree-research@family-tree-research
```

Или вручную: скопируйте папку `skills/family-tree-research` в `~/.claude/skills/`.

## Веер предков

```
cd skills/family-tree-research
python3 scripts/fan/build.py scripts/fan/example/tree.json demo.html --img scripts/fan/example
```

Откройте `demo.html` в браузере. Формат данных описан в `SKILL.md`. Данные в примере вымышлены.

Экспорт того же дерева в GEDCOM:

```
python3 scripts/gedcom_export.py scripts/fan/example/tree.json demo.ged
```

## Принципы

- факт и гипотеза всегда помечены отдельно;
- оригинал документа важнее индекса;
- письма, запросы и оплаты – только с согласия пользователя;
- никаких обходов капч, логинов и ограничений доступа;
- сведения о живых людях остаются у пользователя.

## Что внутри

- `SKILL.md` – метод: отчёт и реестры дела, статусы доказанности, порядок поиска
- `references/` – где искать, как читать записи, запросы в архивы, доказанность, общение в Telegram-чатах и на форумах, рассказ для детей
- `scripts/fan/` – интерактивный веер предков с хроникой рода
- `scripts/gedcom_export.py` – экспорт дерева в GEDCOM
- `assets/` – шаблоны реестров CSV

## Благодарности

Статусы доказанности, группы независимости и реестры дела основаны на подходе скилла [ex-USSR Kinship Research](https://github.com/DenisSergeevitch/ex-ussr-kinship-research) (Denis Shiryaev, MIT). Для глубокого поиска по всем 15 бывшим республикам СССР рекомендую его – он отлично сочетается с веером из этого репозитория.

## Лицензия

MIT
