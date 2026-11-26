# Rating UI anti-patterns

Checklist for step 4 of the audit. Each entry: what it looks like, why it biases, how to spot it in code, usual fix. IDs are for cross-referencing in reports; you don't have to use them.

## Contents
- S: Scale design
- F: Framing and anchoring
- L: Condition leakage (blinding)
- O: Order and position
- C: Cognitive load and task design
- D: Data integrity caused by the UI
- P: Protocol, raters, quality control
- A: Device, display, accessibility

---

## S. Scale design

**S1. Stem and anchors don't match.** A statement stem ("This image is sharp") paired with extent anchors ("Not at all ... Completely"), or a question stem ("How sharp is it?") paired with agree/disagree anchors. Raters have to translate between the two and do it differently. Spot it by reading each stem next to its anchors aloud. Fix: make the anchors answer the stem directly. Either a question with construct-specific anchors ("How sharp is the image? Very blurry … Perfectly sharp"), or a statement with agreement anchors (accepting acquiescence bias, see S2).

**S2. Agree/disagree statements.** Agreement scales invite acquiescence (people lean toward "agree"), more so with tired or deferential raters, and positively worded statements push scores up. Fix: item-specific questions with construct-labeled anchors. If agreement format is kept for comparability, at least don't make all statements positive.

**S3. Double-barreled items.** One rating for two or more properties ("clear, sharp, and well-made, without obvious errors"; "accurate and culturally appropriate"). A rater who sees a sharp image with a visible error has no correct answer, and different raters resolve it differently. Spot "and", "or", commas, and "without" in stems. Fix: split into separate items, or define one construct and make the others examples of it.

**S4. Anchor labels that aren't ordered or evenly spaced.** Verbal labels like "Somewhat" vs "Moderately", "Fairly" vs "Quite" have no agreed order, and their perceived distance varies by rater and by language. Fully labeled scales help reliability only if the labels are clearly ordered. Fix: use labels with well-established ordering, label endpoints plus midpoint, or show numbers with labeled endpoints. If raters are non-native speakers of the UI language, test the labels with them or translate them.

**S5. Unipolar vs bipolar confusion.** A unipolar construct (amount of quality, from none to complete) shown with a bipolar layout (negative to positive, a neutral midpoint), or the reverse. The midpoint then means different things to different raters. Fix: decide whether the construct has an opposite, and label the midpoint to fit (e.g. "Moderately" for unipolar; "Neither" for bipolar).

**S6. No way to say "can't judge".** Forcing a rating when the rater lacks the knowledge (unfamiliar culture, missing reference, image didn't load) produces midpoint dumping or guesses that look like real data. Conversely, an N/A that's too easy becomes a way to skip hard items. Fix: offer "can't judge / not applicable", store it as a distinct value (never 0 or null-confused with "not answered"), and report its rate by condition.

**S7. Preselected or default values.** A radio pre-checked, or a slider whose handle starts at the middle or one end. Raters anchor on the start point, and an untouched default is indistinguishable from a deliberate answer. Spot `defaultValue`, `checked`, initial state set to a number, `<input type="range" value=...>`. Fix: no default; for sliders, no visible handle until first click, and log whether the control was touched.

**S8. Inconsistent direction or polarity.** The good end is on the right for one item and on the left for another, or "1 = best" on one screen and "7 = best" on another. Raters on autopilot follow the first one. Fix: one direction everywhere, unless reversal is a deliberate attention check that is analyzed as such.

**S9. Numbers that carry meaning.** Showing −3…+3 vs 1…7 vs 0…6 changes the distribution of answers; numbers can also override verbal anchors. Fix: pick deliberately, keep the same everywhere, and store the value as displayed (see D3).

**S10. The construct changes between places.** The label on the item, the tooltip, the onboarding text, and the paper's definition say different things (e.g. the label says "realistically shows the subject" but the help says "right style and details"). Raters use whichever one they read, so different raters measure different things. Fix: one canonical definition, reused verbatim everywhere; if the label must be short, make it a strict summary of the definition.

**S11. Scale granularity and labeling mismatch.** Many points (9, 11, 100) with endpoint-only labels encourage clustering on a few values; few points (3) lose information. Usually fine to keep 5–7 fully or semi-labeled. Flag only if the granularity doesn't fit the analysis (e.g. treating a 3-point scale as interval).

**S12. Slider without numeric feedback, or with too much.** Sliders take longer, are harder on touch screens, and produce clustering at the start position and at round numbers. Fix: prefer discrete radios unless continuous data is needed; if a slider is used, no default handle (S7) and consistent tick marks.

## F. Framing and anchoring

**F1. Leading or evaluative wording.** Copy that signals what a good answer is ("our new model", "AI-generated images often fail at…", "help us show…"), or that tells raters the hypothesis. Look in instructions, onboarding, consent text, emails to participants, and item copy. Fix: neutral wording; describe the task, not the hypothesis.

**F2. Calibration examples that anchor the scale.** Onboarding examples teach raters what a "2" or "6" looks like. That's useful, but if examples come from one condition (one model), or only show extremes, they shift ratings for that condition or compress the scale. Spot where examples are chosen (scripts, JSON). Fix: draw examples from all conditions or from held-out stimuli, cover the middle of the scale, and don't reuse example items as test items.

**F3. Reference or comparison standard effects.** Showing a reference (real photo, gold answer, source text) changes what's being judged: raters drift toward "similarity to reference" even when told not to. If references exist for some items and not others, the rating means something different across items. Fix: decide whether the construct is "matches reference" or "matches the prompt"; word the item accordingly; log whether a reference was shown and analyze with it as a covariate. If references are missing more often for some conditions (e.g. low-resource cultures), that's a confound (see L/O).

**F4. Showing the generation prompt or other text.** The prompt text primes what to look for and can make the "accuracy" judgment a text-matching task. Usually needed; just make sure it's shown identically for all conditions and the item wording tells raters how to use it.

**F5. Visible previous answers, running scores, or easy revision.** Seeing one's own past ratings or a summary encourages consistency effects; back-navigation lets raters re-anchor earlier items after seeing later ones. Neither is always wrong, but both should be deliberate and logged (store revision history, not just the last value).

**F6. Demand characteristics and identity cues.** Telling raters which team/model is "ours", showing sponsor logos, or recruiting raters who know the hypothesis. Fix: neutral branding in the rating UI; document rater relationship to the project.

## L. Condition leakage (blinding)

Check every channel through which a rater, or their browser, could learn which condition an item belongs to. Each leak is a potential confound.

**L1. Names in visible text or attributes.** Model/system names in titles, alt text, captions, `title=` tooltips, CSS class names, or React keys that render. Spot by grepping for each condition name in the UI source and in the data files the UI reads.

**L1b. Masking that only works in some modes.** A masking function that replaces the condition name in a display string works for single-condition links but silently does nothing in a mixed/interleaved mode (e.g. it replaces `metadata.model`, which is `"mixed"`, so `FLUX_...` folder names pass through). Debug-ish lines like "Stimuli ID: <folder>/<file>" in headers are a common culprit. Check each display string in every survey mode the links can open, not just the one the code was first written for.

**L2. Names in URLs and file names.** Image `src` like `.../flux/img_12.png`, `?model=sdxl` in the survey link, or file names with the model in them. Raters hover, right-click "open image", or read the link they were sent. Fix: opaque IDs for assets and links; the mapping lives server-side or in a separate table.

**L3. Embedded metadata.** PNG text chunks and EXIF can contain the generator, sampler, seed, and even the prompt (Stable Diffusion UIs write `parameters` chunks; some services add C2PA/watermarks). Anyone who downloads or inspects the image can see it, and a few raters will. Spot: check a sample image with `exiftool` or a PNG chunk reader; check whether the code strips metadata. Fix: re-encode and strip metadata for all conditions in the same way.

**L4. Perceptual tells unrelated to the construct.** Different resolutions, aspect ratios, file formats/compression, color profiles, borders, watermarks, or load times by condition. Raters learn them within a few items. Fix: normalize size, format and compression across conditions; preload images so load time doesn't vary; log load failures by condition.

**L5. Order or grouping that reveals condition.** Items blocked by condition (all model A, then all model B) or a URL/session per model. Raters infer the condition and compare blocks. Fix: interleave conditions within a session (see O3).

## O. Order and position

**O1. Fixed question order within an item.** The first dimension rated colors the next (halo / carry-over). With "accuracy, cultural fit, technical quality" always in that order, a striking flaw noticed for one leaks into the others. Fix: either accept it and document, or randomize dimension order per participant (not per item, which is confusing) and log it. Note when ratings across dimensions correlate very highly in pilot data; that's a sign of halo.

**O2. Stimulus position not counterbalanced or not logged.** Left/right or top/bottom placement of the stimulus vs the reference, or of system A vs B in pairwise tasks, biases attention and preference (left/first is often favored). Randomizing it is good; randomizing it without storing the realized position makes the bias impossible to check. Spot `Math.random()` near layout state and check whether the result is saved. Also check that randomization is stable across re-renders and revisits.

**O3. Item order not randomized, or randomization not recorded.** Fatigue and learning make early and late items systematically different. Fix: randomize per participant with a recorded seed and store the trial index with each response. Check that the seed actually differs per participant (not e.g. constant when an ID is missing) and that "deterministic shuffle" uses a real PRNG, not `sort(() => Math.random() - 0.5)` which is biased.

**O3b. Broken PRNG or seed hashing.** Hand-written seeded generators (mulberry32, LCGs, string hashes) are often slightly wrong: a missing unsigned shift or a wrong divisor that limits output to [0, 0.5), a hash that collides for similar IDs. A shuffle built on them is then far from uniform, and the first or last items of each pool are systematically over- or under-selected. Check by sampling the generator and by simulating the selection (see SKILL.md step 3).

**O3c. Condition or domain tied to session position.** Even with per-participant shuffling, a construction like "shuffle within domain, concatenate, shuffle again with a weak generator" can leave one domain or condition mostly at the end of the session, where fatigue is highest. Check the average position of each condition and domain across simulated participants.

**O4. Scale option order.** Options listed left-to-right (or top-to-bottom on mobile) have a primacy pull. Small effect; usually just keep one direction consistent (S8). Flag if desktop and mobile layouts flip direction or orientation.

**O5. Session length and fatigue.** Many items × several dimensions per item without breaks degrades attention in the second half. Estimate total judgments and time from the design. Fix: fewer items or dimensions, a break screen, log per-item time, plan `trial_index` as a covariate.

## C. Cognitive load and task design

**C1. Definitions hidden behind clicks.** If the construct definition lives in a modal or tooltip, most raters will read it once or never, and then rate the short label. Spot help buttons/modals and check what's visible without interaction. Fix: keep a one-line definition visible under each item; put the longer version behind the click.

**C2. Too much per screen.** Several dimensions × large images × a reference × prompt text × instructions. Raters satisfice: they start giving the same value across dimensions (straight-lining). Fix: fewer dimensions, or one dimension per screen, or a clear visual hierarchy. Check whether straight-lining can be detected from stored data.

**C3. Stimulus too small to judge the construct.** Technical quality or fine detail judged on a thumbnail, or images scaled down on phones. Fix: large default view, zoom option, and log whether zoom was used. Make sure zoom/lightbox behaves the same for all conditions.

**C4. Scale far from the stimulus.** Rater must scroll between image and scale, so they rate from memory. Check in screenshots at common viewport sizes.

**C5. Jargon or ambiguous constructs.** Terms like "fidelity", "coherence", "authenticity" mean different things to different raters. If the construct is inherently expert-judgment (e.g. cultural authenticity), the definition needs to say what counts and what doesn't, ideally with examples.

**C6. Required knowledge the rater may lack.** Asking a rater from one culture/domain to judge another, or requiring familiarity with the prompt's subject, without a way to signal uncertainty (S6).

## D. Data integrity caused by the UI

**D1. Advancing with missing answers.** "Next" enabled before every required rating is filled, or partial answers silently allowed. Decide per item whether partial is acceptable; if not, block or warn. Also check: can the rater submit before the stimulus loaded?

**D2. Saves that can be lost or overwrite.** Debounced or async autosave that's cancelled on navigation; retries that create duplicate rows; an upsert key that's too coarse (two different items collapse into one record) or too fine (a revisit creates a second record). Trace the save function and its unique key. Check what happens offline.

**D3. Stored value differs from displayed value.** Off-by-one, reversed scale on storage, normalization or percentage computed at save time (keep raw!), N/A stored as 0 or null (indistinguishable from "not answered"), deselection stored as a value.

**D4. Missing context in the stored record.** Without these, many biases above can't be checked after the fact: participant ID, item/stimulus ID, true condition, displayed position (left/right), trial index, dimension order, whether a reference was shown and which one, timestamp per rating (for time-on-item), revision count, device/viewport, image load success, app version/commit.

**D4b. Items paired across conditions by position.** Counterbalancing designs (Latin square: same prompt, different model per group) need a stable identity for "the same prompt". If each condition's stimuli come from a separately generated file and the code pairs `files[modelA][i]` with `files[modelB][i]`, any difference in file order means different prompts are treated as the same one: the stored prompt ID is wrong, prompts aren't balanced, and a participant can see the same subject twice from two models. Pair by a real ID or by normalized prompt text, and assert alignment at load time.

**D4c. Resume and navigation edge cases.** After a reload, is an item with some but not all ratings treated as done? Does going back, editing, and going forward restore the old value? Does deselecting a choice leave the old value in the database? Does looking up progress by a typed name break on apostrophes, capitalization, or a second device? Test these in the running app if you can.

**D5. Identity and session problems.** Participant IDs typed by hand (typos split one person into two), names used as IDs, the same link usable by two people, or a refresh starting a new session with a new randomization.

**D6. Debug output and leftover dev features.** `console.log` of stimulus metadata (model names, file paths) visible in devtools, admin routes reachable from participant links, test data mixed into the production collection.

## P. Protocol, raters, quality control

**P1. No pilot or attention checks.** Some quality control is expected: gold items with a known answer, repeated items for intra-rater consistency, time-on-item thresholds, or straight-lining detection. Too-obvious checks ("select 3 for this item") mostly measure whether people read, which is still useful. Flag absence, not the specific choice.

**P2. Overlap for agreement.** If inter-rater agreement will be reported, enough items need to be rated by multiple raters. Check the assignment design against the agreement statistic planned.

**P3. Rater count per cell.** Very few raters per culture/condition means rater effects dominate. Not a UI issue, but it determines how much the UI biases matter, so note it in the design summary.

**P4. Instructions and consent.** Instructions should define every construct, say how to use references/prompts, explain N/A, and give the expected time. Consent should say what's recorded. Check that what's recorded (D4) matches what consent says.

**P5. Consent and invitation text describing a different study.** Copy written early often goes stale: wrong number of items, wrong duration, a scale format that's no longer used ("Strongly disagree … Strongly agree"), a promise that the name is optional or the data anonymous. Raters calibrate effort to the stated length, and a false anonymity claim is an ethics problem. Compare every number and promise in consent, invitations, and onboarding with the actual app.

## A. Device, display, accessibility

**A1. Colored scales.** Red-to-green options imply valence and pull toward the green end; they're also unreadable for color-blind raters. Use neutral colors for scale options.

**A2. Mobile layout differs from desktop.** Horizontal scales becoming vertical lists, images shrinking, labels truncating. If raters can use phones, the instrument differs by device; log the device and check the layouts are equivalent, or restrict devices.

**A3. Display conditions for perceptual judgments.** Screen size, brightness, color calibration and zoom level affect image-quality and color judgments. Can't be controlled remotely, but can be logged (viewport, devicePixelRatio) and mentioned in instructions.

**A4. Keyboard and screen-reader access.** Radios without labels, click targets too small, focus not visible. Matters for inclusion and also for accidental mis-clicks (which are noise).
