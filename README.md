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

## Принципы

- факт и гипотеза всегда помечены отдельно;
- оригинал документа важнее индекса;
- письма, запросы и оплаты – только с согласия пользователя;
- никаких обходов капч, логинов и ограничений доступа;
- сведения о живых людях остаются у пользователя.

## Лицензия

MIT
