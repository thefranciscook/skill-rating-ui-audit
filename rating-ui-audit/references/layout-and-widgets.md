# Layout, widgets, and overdesign

Read this for any audit that involves a visible interface, and especially when the user asks about layout, widget choice (matrix/grid, sliders, stars, cards), visual design, or whether the instrument is "overdesigned".

## Contents
1. The core idea: an instrument is not a product
2. How raters read a layout (interpretive heuristics)
3. Widget choice
4. Layout of the response options
5. Stimulus presentation
6. Interaction behavior
7. Chrome, feedback, and motivation
8. Visual styling
9. Device equivalence
10. UX instinct vs measurement: quick table
11. The strip test

---

## 1. The core idea: an instrument is not a product

Product UX is tuned for conversion, speed, delight, and low friction. A rating instrument is tuned for something else: every rater makes a careful, independent judgment, under the same conditions as every other rater, on every item and in every condition. Many good web-design instincts work against that:

- **Lower friction** usually means less deliberation. Some friction is the point.
- **Visual hierarchy** tells people what matters. In an instrument, whatever you emphasize becomes part of the question.
- **Delight and motivation** (animations, praise, progress rewards) change how raters feel about the task partway through, and that can differ between conditions or across the session.
- **Responsive layout** changes the instrument from one device to another.
- **Smart defaults and progressive disclosure** hide or pre-answer things, so some raters see the definition and others don't.

The default stance for an instrument is plain, consistent, symmetric, and identical across items, conditions, and devices. Every visual element on the rating screen either helps the judgment or is a possible cue. When you audit a layout, the question for each element is: "Does this help the rater judge the construct, and does it look the same for every condition?" If it does neither, it's a candidate for removal, however good it looks.

This doesn't mean ugly or hostile. Legibility, a clear task, a calm layout, and reasonable comfort all reduce noise. The line is between design that makes the judgment easier and design that adds signals of its own.

## 2. How raters read a layout

Raters, like survey respondents, read meaning into visual features even when nothing is meant (Tourangeau, Couper & Conrad's interpretive heuristics). Use these to explain why a layout choice shifts answers:

- **Middle means typical**: the visual midpoint of the options is read as the neutral or average answer. If N/A sits at the same spacing as the scale points, the visual midpoint moves and "4" stops looking like the middle.
- **Left and top mean first, or most important.** The first option or the first item gets extra weight.
- **Near means related**: options or items placed close together are read as conceptually close. Unequal spacing reads as unequal intervals.
- **Up means good** (and in many locales, right means more). Vertical scales should put the high end on top or be consistent; don't mix orientations.
- **Like means close**: options that share a color or shape are read as similar. Coloring the endpoints differently reads as a valence scale.

## 3. Widget choice

**Matrix / grid of radio buttons** (rows = items, columns = scale points, labels in the header). Fast to answer and compact, but well documented to produce more straight-lining (the same column for every row), less differentiation between items, higher inter-item correlations, and more speeding than asking item by item. The column labels are far from the lower rows, so raters answer by column position, not by label. For a few items with different constructs (accuracy vs cultural fit vs technical quality), these drawbacks hit exactly what you want to keep separate: a grid makes halo effects look like real correlation.
- Fine when: the items share one construct and one scale (a multi-item index), there are few rows, and labels are repeated or the header stays visible.
- Prefer item-by-item or separate blocks when: the rows measure different constructs, discriminant validity matters, or the analysis compares dimensions.
- If keeping the grid: few rows; repeat anchor labels at least at the endpoints of each row, or keep the header sticky; alternate row shading for tracking; check pilot data for straight-lining (share of items where all rows get the same value) and inter-dimension correlation.

**Item-by-item (one question, full labeled scale)**. Slower, better differentiation. The usual choice when dimensions are distinct. One question per screen is the strongest version, at a cost in time and context-switching.

**Sliders / visual analogue scales**. Look modern; in practice take longer, cause more missing data on touch devices, cluster at the start position and at round numbers, and are hard to set precisely. Use only when you need continuous data and can avoid a default handle position (see anti-patterns S7, S12).

**Stars, thumbs, hearts, emoji faces**. Carry meaning from consumer products: 5 stars is "fine", 3 stars is a complaint, so distributions skew to the top. Emoji faces add emotion and differ across cultures. Avoid for expert judgment; if used, label the points with words.

**Segmented buttons / pill toggles / big tappable cards** instead of radios. Fine if every option is the same size and spacing. They become a problem when the selected one grows, changes color strongly, or when option widths follow label length (unequal widths read as unequal intervals).

**Dropdowns for a scale**. Hide the scale, so raters can't see the whole range or the midpoint, and the first option visible gets chosen more often. Avoid for rating scales.

**Drag-and-drop ranking**. Hard on mobile, tiring with more than about 5 items, and the initial order anchors the result. Randomize the starting order and log it.

**Swipe cards / binary keep–reject**. Very fast, encourages gut reactions and speed. Fine for screening tasks; not for nuanced quality judgments.

**Pairwise side-by-side (A vs B)**. Position bias (left/first often wins), so counterbalance and log the position. Keep both panels identical in size, framing, and labels.

## 4. Layout of the response options

- **Equal spacing and equal widths.** Options should be visually equidistant; in tables, check column widths, not just intent (`w-1/12` columns can still differ when labels wrap). Labels of different lengths must not change option spacing.
- **N/A apart from the scale.** Put "can't judge" visibly separated (a gap, a divider, a different row) so it doesn't read as an extra scale point beyond the endpoint or shift the visual midpoint. A thin border on its own column is usually not enough.
- **Labels where the answer is made.** Anchor labels next to the options, not only in a header several rows up. In grids, the top row gets read with labels and the bottom rows by position.
- **Same orientation everywhere.** Horizontal on one screen and vertical on another, or low-to-high on one and high-to-low on another, invites mistakes.
- **Scale near the stimulus.** If the rater has to scroll between image and scale, they rate from memory. Check this at common laptop heights (e.g. 768 px), not only on a large monitor.
- **Long item text in a narrow column.** Wrapping makes rows different heights and pushes the radios away from the text. Rows of different heights are an easy place to click the wrong row.

## 5. Stimulus presentation

- **Equal treatment across conditions** is the hard rule: same size, frame, crop mode, background, and loading behavior for every condition.
- **Relative size and position encode importance.** A large target image and a small reference say "this one matters". That may be intended; it should be deliberate and the same on every item.
- **Crop mode.** `object-cover` vs `object-contain` (cropped vs letterboxed) changes what's visible. Judging composition or technical quality on a cropped image is a different task.
- **Framing and labels.** Colored frames and headings like "Rate this" are fine if neutral and identical. Labels that evaluate ("AI-generated", "Real photo", "⚠ No reference available") frame the item. A warning icon on items without a reference makes those items look deficient, and if references are missing more often for some cultures or conditions, that becomes a confound.
- **Persistent context boxes.** Big, colorful, repeated context (the target culture in large bold type on every item, the prompt in a highlighted box) keeps those things salient for every question on the screen, including questions where they shouldn't matter (a big culture banner can pull technical-quality ratings toward cultural judgments). Show needed context plainly; emphasize only what every question needs.
- **Zoom.** If the construct needs detail (technical quality), offer a zoom that works the same for all items, and log whether it was used.

## 6. Interaction behavior

- **Auto-advance on selection.** Feels smooth and is popular in survey tools. It removes the moment of review, makes misclicks permanent or invisible, and speeds people up. Don't auto-advance multi-question screens; for single-question screens, let raters confirm.
- **Hover-only labels or definitions.** Desktop-only and seen by some raters but not others. Keep labels visible.
- **Validation timing.** Shouting about missing answers as soon as the screen loads, or after each click, adds pressure. Validate on Next, and point to what's missing.
- **Keyboard shortcuts.** Useful for expert annotators at scale, but make sure they map to the visible scale and can't fire accidentally.
- **Deselect by clicking again.** Unusual for radios; fine if it's consistent and the stored value follows (see anti-patterns D4c).
- **Selected-state styling.** Big color changes or animations on the selected option are fine if the same for every option; a selected state that differs by option (green for high, red for low) adds valence.

## 7. Chrome, feedback, and motivation

- **Save indicators and toasts.** "Saving… Saved ✓" banners flicker near the scale and pull attention after every click. Keep them small and away from the rating area, but keep the error state visible.
- **Progress bars.** Usually helpful for long surveys, but a bar that moves slowly at first (or counts sub-steps) can increase dropout, and per-section bars that reset can mislead. Show plain "item N of M".
- **Praise and gamification.** "Great job!", streaks, confetti, points, and leaderboards change motivation unevenly across the session and signal that some answers are good. No evaluative feedback during rating.
- **Timers and countdowns.** Visible timers create time pressure and change judgments. Log time silently instead.
- **Branding, logos, team names.** Can signal who made a system or what the hypothesis is (see anti-patterns F6).
- **Debug info on screen.** IDs, folder names, model names in small grey text. Raters read them (see anti-patterns L1b).

## 8. Visual styling

- **Color on the scale.** Red→green gradients, or colored endpoints, add valence and pull answers toward the "good" color; they also fail for color-blind raters. Keep scale options neutral.
- **Color as category.** Color-coding regions (purple = generated, blue = reference) is fine if consistent and neutral. Avoid colors with built-in meaning (red/amber = warning) on content the rater is judging.
- **Emphasis inside item text.** Bolding one word ("**clearly** belongs") leads raters toward that criterion. Bolding the construct name only is fine.
- **Icons and emoji in instructions or items.** Add tone. Fine in onboarding for friendliness; keep them off the rating area.
- **Animation and transitions.** Fade-ins are harmless if the same for all items. Animations that only run on some items (slow image loads with spinners) differ by condition if load times do.
- **Typography.** Legible size and contrast matter more than style. Tiny grey labels (e.g. `text-xs text-gray-500` anchors) get skipped.

## 9. Device equivalence

A responsive layout that swaps a grid on desktop for a stacked list on phones is two different instruments. The grid invites column-wise answering and straight-lining; the stacked list labels every option and is answered item by item. If raters can use either, either:
- make the layouts equivalent (item-by-item on both is the simplest), or
- restrict devices, or
- log device/layout per response and test for a layout effect.

Also check what sticky or fixed elements do on phones: a sticky stimulus panel can cover most of the screen and hide the questions below it.

## 10. UX instinct vs measurement: quick table

| UX instinct | Why it's good for products | Why it hurts measurement | Instead |
|---|---|---|---|
| Compact matrix to save space | Less scrolling, faster | Straight-lining, halo between different constructs, labels far from rows | Item-by-item for distinct constructs |
| Auto-advance on click | Fewer clicks | No review, permanent misclicks, speeding | Explicit Next |
| Slider for a modern feel | Looks interactive | Start-position anchoring, imprecision, touch problems | Labeled radios |
| Stars or emoji | Familiar | Consumer-review norms, emotion, skew to top | Worded anchors |
| Color-coded scale | Easy to scan | Adds valence, inaccessible | Neutral options |
| Highlight key context in big colored boxes | Visual hierarchy | Makes that context part of every question | Plain context, same weight |
| Warnings and badges for missing data | Transparency | Frames the item as deficient; confound if uneven | Neutral note, or log it only |
| Progressive disclosure of definitions | Clean screen | Some raters never see them | Short definition always visible |
| Responsive grid → list | Works on phones | Different instrument per device | Same layout everywhere, or log device |
| Praise, streaks, confetti | Engagement | Changes motivation, signals good answers | Neutral progress only |
| Smart defaults | Less effort | Anchoring, untouched default looks like an answer | No default |
| Live "Saved ✓" feedback | Reassurance | Distraction after every click | Small, out of the rating area; error stays visible |

## 11. The strip test

For each element on the rating screen, ask whether the study would lose anything if it were removed, or made plain and the same for every item. List the elements that fail the test as "overdesign" findings (usually minor; major if they differ by condition or pull attention toward one construct). Then describe the minimum layout: what the rater needs on screen to judge each construct, and nothing else. Teams find this more useful than a list of complaints, and it heads off redesigns that add more chrome.
