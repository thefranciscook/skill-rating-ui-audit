# skill-rating-ui-audit
Audits custom human-evaluation web apps (HTML/CSS, UI copy, screenshots, and protocol specs) for measurement bias, scale anti-patterns, framing effects, cognitive load issues, and HEDS compliance. Use before launching a user study or annotation task to verify the interface won't contaminate the data.

## Layout

```
rating-ui-audit/
├── SKILL.md                    # workflow, severity model, evidence standard, report template
├── references/
│   ├── anti-patterns.md        # checklist: scale design, framing, leakage, order, load, data integrity, protocol, device
│   ├── layout-and-widgets.md   # widget choice (matrix vs item-by-item, sliders, stars), option layout, stimulus presentation, overdesign
│   └── heds.md                 # Human Evaluation Datasheet fields to fill / mark missing
├── scripts/
│   └── extract_ui_text.py      # dumps UI copy + measurement-relevant code hotspots with file:line
└── evals/                      # test cases (claude plugin eval layout)
```

## Install

Copy `rating-ui-audit/` into `~/.claude/skills/` (personal) or `.claude/skills/` in a project, or package it:

```bash
python -m scripts.package_skill rating-ui-audit   # from the skill-creator directory
```

## Helper script

```bash
python rating-ui-audit/scripts/extract_ui_text.py path/to/app/src --conditions modelA,modelB --out inventory.md
```

`--conditions` takes the names of the systems or conditions being compared and lists every place they appear in the UI source, to look for blinding leaks.
