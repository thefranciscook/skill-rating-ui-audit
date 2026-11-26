# HEDS completeness check

HEDS (Human Evaluation Datasheet; Shimorina & Belz, 2022, *Proceedings of HumEval*) is a standard form for reporting a human evaluation so that it can be compared with and reproduced by others. The questions below follow its structure. Field numbers in the official form have changed between versions, so this file uses field names, not numbers. If the user needs the exact official numbering, point them to the current form in the HEDS GitHub repository (Shimorina/human-evaluation-datasheet) rather than guessing numbers.

For each field, record one of:
- **documented**: the answer is written down somewhere (cite file/section)
- **inferable**: the answer can be worked out from code or data but isn't written down (cite where, and give the answer you inferred)
- **missing**: neither

A fourth status, **conflict**, is useful when the docs say one thing and the code or data another (e.g. the paper says raters were blind but the UI shows model names; the plan says 9 cultures but the data has 8). List conflicts first: they're decisions the authors have to make before the datasheet can be written honestly.

Present the result as a table. The point is to tell the team what they'll have to write up later and what they can still decide now; several fields (e.g. how a criterion is defined, what raters were told) are much easier to fix before launch than to reconstruct after.

## 1. Resources
- Link to paper / preprint / report describing the evaluation
- Link to evaluation materials: the interface itself, instructions, stimuli, collected data, analysis code
- Contact / responsible people

## 2. What is being evaluated
- The systems or conditions compared (names, versions, settings)
- The task the systems perform (e.g. text-to-image generation), with input and output types
- The input given to the systems (e.g. prompts), and how inputs were created
- Output language(s) or domains

## 3. Sample, evaluators, design

### Sample of outputs
- How many system outputs are evaluated, per condition
- How they were selected (all, random, stratified, filtered — and any filtering criteria such as QA removal)
- Whether a power or sample-size justification exists

### Evaluators
- Number of evaluators, per condition/cell
- Type: experts, domain experts, crowdworkers, researchers on the project, students
- How they were recruited and selected; inclusion criteria
- Whether they were paid, and how much
- Training or calibration given (and whether it was the same for all)
- Expertise relevant to the task (e.g. cultural background for cultural-fit judgments)
- Language proficiency in the UI language
- Whether they knew the hypothesis or the systems, and their relationship to the authors

### Experimental design
- How responses were collected (custom web app, crowdsourcing platform, paper, in person)
- Quality assurance: attention checks, gold items, exclusion criteria, pilot
- What raters saw: the interface (screenshots), instructions verbatim, what was shown alongside each item
- Conditions of the session: remote/supervised, device, time limits, breaks, expected duration
- Assignment of items to raters and of conditions to items (e.g. Latin square), randomization and its unit
- How many times each item was rated, and overlap between raters

## 4. Quality criteria (repeat for each criterion rated)

Write a separate block for each criterion, even when most answers are the same, because HEDS repeats this section per criterion and reviewers compare criteria block by block. A shared table with one column per criterion is fine as a summary, but don't use it in place of the blocks.

### Criterion properties
- Name as used in the paper, and the label shown to raters (they often differ — note both)
- Definition as given to raters, verbatim
- What aspect of the output it addresses: form, content, or both
- Frame of reference: judged on the output alone, relative to the input (e.g. prompt), or relative to an external reference (e.g. reference image)
- Whether it assesses goodness (how good), correctness (right/wrong), or a feature (presence/amount of a property)

### Evaluation mode
- Objective vs subjective
- Absolute (each item on its own) vs relative (compared with other outputs)
- Intrinsic (properties of the output) vs extrinsic (effect on a downstream task or user)

### Response elicitation
- Form: direct quality estimation (rating scale), relative estimation (pairwise, ranking, best-worst), counting, post-editing, qualitative feedback, other
- Instrument type: discrete scale, continuous scale (slider/VAS), other
- Size of the scale (number of points) and list of possible response values, including N/A
- Verbatim question or statement shown to raters
- Verbatim anchor labels and whether numbers were shown
- Whether a response was required

### Results
- How raw responses are aggregated (mean, median, majority, mixed model)
- Statistical tests and what they compare
- Inter-annotator agreement: statistic, on which subset, value
- Intra-annotator agreement, if measured

## 5. Ethics
- Ethics approval (body, reference number) or the reason none was needed
- Personal data collected, and how it's stored and anonymized
- Whether any special-category data is collected (e.g. ethnicity, nationality used as a selection criterion)
- Consent procedure and wording
- Potential harms to evaluators (e.g. exposure to offensive generated content) and mitigation
