---
name: rating-ui-audit
description: Audits human-evaluation and annotation web apps (source code, UI copy, screenshots, live URLs, protocol or paper drafts) for measurement bias before data collection. Covers scale and anchor wording, layout and widget choice (matrix grids vs item-by-item, sliders, stars, responsive layouts), overdesign where web-UX habits like visual emphasis, auto-advance, color or gamification hurt measurement, condition leakage (model names, file names, metadata), order and position effects, cognitive load, UI-caused data-integrity bugs, and HEDS reporting completeness. Use whenever someone is launching, designing or redesigning a user study, survey, crowdsourcing task, preference test or rating/labeling interface, even if they only say "review my survey", "is this matrix question OK", "does the rating screen look right", "check the eval app before we send links", "will raters be biased", or "fill in HEDS for this study".
---

# Rating UI Audit

A rating interface is part of the measuring instrument. Wording, scale anchors, layout, defaults, order and what the rater can see all shift responses. Most of those shifts can't be fixed after the data is in. The job here is to find them before launch and to say which ones actually matter for the comparisons the study is going to make.

## What "matters" means

Sort every problem into one of two kinds, because they call for different urgency:

- **Confound**: the bias is correlated with a condition being compared (model A vs B, culture X vs Y, with vs without reference). This changes conclusions. Example: system A's images always load slower, or the model name appears in the image URL raters can hover over.
- **Noise or uniform bias**: it affects every condition the same way. It shrinks effect sizes, harms reliability, or makes absolute scores hard to interpret, but leaves relative comparisons mostly intact. Example: a double-barreled question, unclear midpoint label.

A third lens runs through the whole audit: **an instrument is not a product.** Web-design instincts (compact grids, visual hierarchy, auto-advance, color coding, responsive reflow, delight) are tuned for speed and engagement. A rating screen is tuned for careful, independent judgments made under identical conditions. Anything on the screen that doesn't help the judgment is a possible cue, so a plainer layout is often the fix. `references/layout-and-widgets.md` develops this.

A confound or a data-loss bug is a launch blocker. Uniform bias is usually worth fixing if it's cheap, and worth documenting if it isn't. Saying which kind each finding is is the most useful thing the report does; a flat list of 40 "issues" is not.

## Workflow

### 1. Understand the study design first

Before looking at any UI, find out what's being compared and how the analysis will work. Look for protocol docs, paper drafts, analysis plans, READMEs, devlogs, config files. Write down:

- the constructs being rated and how they're defined
- the conditions/factors compared (models, prompts, cultures, domains, ...)
- the assignment scheme (between/within, Latin square, randomization, seeds)
- raters: who, how many, recruited how, how many items each, session length
- the planned analysis (means, mixed models, pairwise preference, agreement stats)

If none of this is written down, infer it from the code and say that you inferred it. You need it to judge severity.

Also find out whether data has already been collected: look for exports, cohort or participant files, analysis notebooks, incident notes, dated result folders. "Pre-launch" is often really "before the next wave". If earlier waves exist, two things change. Some bugs have already affected collected data, so say which, and how to recover it if possible (e.g. from a change log). And rewording items or changing the design now creates a second instrument, so recommend recording a design/scale version on every response and deciding up front whether waves will be pooled. Watch for collection order: if cultures, sites, or conditions are collected one after another, changing the layout or wording partway through confounds the change with whichever groups come later. The options are then to keep the instrument until collection ends, or change it and recollect everyone.

### 2. Build the instrument inventory

Record exactly what a rater sees, verbatim, with `file:line` for every item. Quote copy exactly; paraphrasing hides the wording problems you're looking for.

For each rating question: construct name, question/statement text, help or tooltip text, scale type (radio, slider, pairwise, ranking, free text), number of points, every anchor label, numeric labels shown, N/A or "can't judge" option, default value, whether it's required, and its position on the screen.

For the flow: consent → instructions → training/calibration examples → items → attention checks → end. Note what else is on the screen with each item (stimulus, reference, prompt text, progress, previous answers).

`scripts/extract_ui_text.py <repo-or-dir>` dumps UI string literals and flags code hotspots (randomization, defaults, sliders, required/disabled logic, storage writes, possible condition names in URLs). Use it to find things quickly, then read the actual source around each hit. Don't report from the script output alone: it has false positives and misses copy built at runtime.

### 3. Trace the data path

For each rating, follow the value from the input element to storage. UI bugs that corrupt data are common and are invisible in the interface:

- Is the stored value the same as the displayed value (off-by-one, 0- vs 1-based, normalized at save time, N/A stored as 0)?
- Is presentation context logged: item order index, left/right position, which reference was shown, timestamps, viewport/device?
- What happens on back-navigation, revisits, refresh, double clicks, network failure? Can a revisit overwrite an earlier answer or create a duplicate?
- Can the rater advance with missing answers or an unloaded stimulus?
- Do randomization seeds actually differ between participants, and is the realized order recorded?
- What is the record's unique key, and can two different items share it? A file name or index that repeats across conditions (the same `image_00001.png` under each model's folder) makes one item's rating overwrite another's.

Client code alone can mislead about what's stored. Backends coerce values (a `null` sent to a numeric column often comes back as `0`), drop unknown fields, or enforce their own uniqueness. If exports, a schema file, or migration files are in the repo, check the claim against them before reporting what's stored, and say which source you used.

**Run the assignment logic; don't just read it.** Counterbalancing and shuffle code is where the worst bugs hide, and they're easy to miss by eye. Port the selection code to a short script (or run it with node) and simulate a few hundred participant IDs, including the real IDs if a cohort file has them. Check:

- each participant gets the intended number of items per condition and domain, with no duplicates of the same underlying prompt/stimulus
- items that are supposed to be "the same prompt across conditions" really are the same (pairing by array position across separately built files breaks silently when the files are in different orders)
- every item is about equally likely to be selected, and each condition/domain is spread evenly across positions in the session (a broken PRNG or a biased shuffle shows up here)
- every planned group or cell actually gets participants under the link-generation process
- the overlap between raters is enough for the agreement statistic the analysis plans

Report the numbers. "92% of simulated CHE participants see a repeated prompt" is much more convincing than "the pairing looks fragile".

### 4. Run the checks

Go through `references/anti-patterns.md`. It is organized by category (scale design, framing and anchoring, condition leakage, order and position, cognitive load, data integrity, protocol, device and accessibility). Each entry says what it looks like, why it biases, how to spot it in code, and the usual fix. Not every entry applies to every study; skip ones that don't and don't pad the report with them.

### 5. Review layout, widgets, and overdesign

Read `references/layout-and-widgets.md` and go through the rating screen with it. Treat this as its own step, not a side effect of reading code. Teams rarely question layout, and it shapes every response. Cover at least:

- **Widget choice**: is a matrix/grid, slider, star row, card, or dropdown the right format for these constructs, or should it be item-by-item? Say which and why.
- **Option layout**: equal spacing and widths, where the anchor labels sit relative to the options, how N/A is separated, orientation.
- **Stimulus presentation**: relative sizes, crop mode, frames, labels and warning badges, persistent context boxes, and whether all of this is identical across conditions.
- **Interaction and chrome**: auto-advance, hover-only content, save toasts, progress, praise, timers, debug text on screen.
- **Device equivalence**: does the layout change between desktop and phone, and does that make it a different instrument?
- **The strip test**: list the elements that could be removed or made plain without losing anything, and sketch the minimum layout the judgment needs.

Measure, don't eyeball. In the rendered page, read element geometry with `getBoundingClientRect()` (option column widths, gap before N/A, y-position of the first and last scale row against the viewport height, image sizes per device) and quote the numbers. Visual impressions of "set apart" or "fits on screen" are often wrong.

If responses already exist, check the layout's effect in the data: the share of items where every dimension got the same value (compare with the rate you'd expect if a rater's dimensions were independent, e.g. by shuffling each rater's values across items), that rate per rater, inter-dimension correlations, answer order and time per item where logged. A grid that produces heavy non-differentiation from a few fast raters is a concrete finding; say also that observational data can't fully separate a layout effect from genuinely correlated constructs.

When the layout question is the user's main concern, give a direct verdict on the format ("keep the grid / replace it with item-by-item blocks") with a concrete alternative layout, not just a list of issues.

### 6. Look at it rendered, if you can

Layout bias often only shows up visually: one image larger than the other, the scale below the fold, labels wrapping on phones, a color gradient on the scale. Take screenshots and look at them yourself as part of step 5. If the app can run locally (check `package.json` / README for the dev command) or a URL is given, take screenshots at a desktop size and a phone size with Playwright and walk one item. Run it from a copy outside the repo, and never point it at the live database: intercept backend and image requests (Playwright `page.route`) and answer them from a small in-memory fake so you can complete items, reload mid-item, go back and forward, and simulate a failed save. Those flows (resume after reload, edit then navigate, offline save) are where data loss shows up. If it can't run at all, say so and note which checks therefore come only from reading code.

### 7. HEDS completeness

Read `references/heds.md` and fill in each HEDS field from what the repo and docs say. Mark each field as *documented* (cite where), *inferable from code* (cite where, flag that it needs to be written down), or *missing*. Missing fields are a reporting gap, not a UI bug, so keep them out of the severity-ranked findings and give them their own section.

### 8. Write the report

Use the template below. Save it where the project keeps docs (check CLAUDE.md, .cursorrules, or similar for conventions such as a devlog folder); otherwise write `rating-ui-audit.md` at the repo root. If the user only asked a narrow question ("is my scale OK?"), answer that question with the relevant findings and skip the sections that don't apply.

## Evidence standard

Every finding needs:

- **Where**: `file:line`, screenshot, or doc section.
- **What**: the exact copy or behavior, quoted.
- **Mechanism**: why it shifts responses, in one or two sentences. Cite the relevant effect (acquiescence, anchoring, halo, primacy, central tendency, ...) only where naming it helps.
- **Impact**: which comparison or analysis it affects, and whether it's a confound or noise.
- **Fix**: concrete. Rewritten copy, the code change, or the logging field to add. When proposing new wording, write it out in full.
- **Confidence**: *verified* (you traced it in code or saw it rendered) or *suspected* (plausible, needs checking). Don't present suspicions as facts.

Some deviations from textbook practice are deliberate and defensible (a forced choice with no N/A because the stimuli were pre-screened, a 7-point scale for comparability with earlier work). If the docs justify a choice, say so and don't count it as a defect. Also list briefly what the interface already does well, so the team knows what not to change.

## Report template

```markdown
# Rating UI audit: <study name>

Date, what was reviewed (commit, files, URL, screenshots), and what could not be checked.

## Verdict
One paragraph: ready to launch / launch after fixing N blockers / needs redesign. Name the blockers.

## Study design as understood
Constructs, conditions compared, assignment, raters, planned analysis. Mark anything inferred.

## Findings
### Blockers (confounds and data-integrity bugs)
#### B1. <short title>
- Where / What / Mechanism / Impact / Fix / Confidence

### Major (noise or uniform bias that weakens conclusions)
#### M1. ...

### Minor
#### m1. ...

## Layout and widgets
Verdict on the response format (e.g. keep the grid / switch to item-by-item), the overdesign list from the strip test, device differences, and a sketch of the recommended minimal layout (ASCII wireframe or a short element list). Layout findings that are confounds or major also go in the ranked findings above; this section gives the overall picture.

## What's already good
Bullets.

## HEDS completeness
Table: field | status (documented / inferable / missing) | source or note.

## Pre-launch checklist
Ordered, checkable list of the fixes and the logging to add, blockers first.

## Outside the UI, but found along the way
Privacy, credentials, consent text that contradicts what is recorded. Brief, but don't drop them.
```

Audits of real repos often turn up things that aren't rating bias but would still stop a study: participant names or emails in publicly served files, database credentials in client code, consent text that promises anonymity while names are stored. Put them in the last section, briefly, with the location. Don't let them crowd out the measurement findings, and don't skip them either.

Keep the findings sections ranked by impact, not by where you found them. Group duplicates (the same label problem on three questions is one finding).
