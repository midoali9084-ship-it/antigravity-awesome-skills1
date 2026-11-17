---
name: book-compression
description: "Compress books or long nonfiction by deleting redundancy and filler while keeping the author's wording, reasoning, nuance and evidence."
risk: safe
source: community
date_added: "2026-11-17"
---

# Information Elimination & Book Compression Skill

## When to Use

- The user uploads or pastes a book, chapter, PDF, article, or long text and asks to "compress," "condense," "distill," "trim," "cut the fluff," "remove the filler," "give me the signal not the noise," or "shorten without losing anything."
- The user complains that a book is padded, repetitive, or too long, or wants a version they can read faster without losing the argument.
- Do NOT use it for a normal summary, an explanation, study notes, a review, or a rewrite in Claude's own words — this skill deletes, it does not summarize.

## Purpose

Your task is to compress books and book chapters by **eliminating unnecessary material while preserving the author's meaningful intellectual content**.

You are **not a summarizer, ghostwriter, reviewer, explainer, or rewriter**.

You are an **information-preserving editor**.

The objective is:

> **Produce the shortest possible version of the original text that preserves its meaningful information, reasoning, nuance, and intellectual structure.**

Do not optimize primarily for readability, entertainment, elegance, or brevity.

Optimize for:

**Information Preservation × Meaning Preservation × Structural Fidelity**

while minimizing unnecessary text.

---

# 1. Core Philosophy

## Delete. Do Not Rewrite.

Your default operation is **elimination**, not generation.

You should prefer:

- deleting sentences
- deleting paragraphs
- deleting repeated explanations
- deleting decorative storytelling
- deleting rhetorical language
- deleting unnecessary examples
- deleting redundant transitions
- deleting motivational filler

over:

- paraphrasing
- rewriting
- explaining
- expanding
- adding examples
- adding interpretations
- adding conclusions
- introducing outside knowledge

The final result should remain recognizably the **author's original text**, only compressed through careful elimination.

Do not turn the book into "your explanation of the book."

---

# 2. The Optimization Target

Do not ask:

> "What is the best summary of this chapter?"

Ask:

> "What can be removed without causing meaningful information loss?"

Formally:

> **Minimize textual length subject to preserving meaningful intellectual content.**

The goal is not the shortest possible text.

The goal is the **minimum sufficient text** required to preserve the substance of the original.

---

# 3. What Counts as Meaningful Information?

Treat the following as potentially valuable and preserve them when they contribute something unique:

### Core Claims
What the author is actually arguing.

### Definitions
How the author defines important concepts.

### Distinctions
Differences between concepts that affect understanding.

### Reasoning
Why the author believes a claim is true.

### Mechanisms
How or why something happens.

### Causal Relationships
Relationships such as:

- A causes B
- A contributes to B
- A happens because of B
- A only works when C is present

### Conditions
When a claim applies.

### Exceptions
When a claim does not apply.

### Limitations
Where the author's argument becomes weaker or narrower.

### Evidence
Research findings, observations, experiments, data, or other evidence that materially supports the argument.

### Examples
Only when the example adds information that is not already adequately communicated elsewhere.

### Practical Implications
Actions or consequences that materially follow from the author's argument.

### Frameworks
Models, processes, principles, equations, checklists, systems, or structures proposed by the author.

### Relationships Between Ideas
Preserve important connections, dependencies, sequences, and logical progression.

---

# 4. Information Is More Important Than Word Count

Never judge a passage by its length.

A 500-word passage may contain one useful idea.

A 30-word passage may contain a critical qualification.

Therefore:

> **Do not optimize for words removed. Optimize for redundant information removed.**

A passage should be evaluated based on its **information contribution**, not its size.

---

# 5. Repetition

Repetition is one of the primary targets for elimination.

When several passages communicate essentially the same proposition:

1. Identify the underlying proposition.
2. Determine whether any version adds new information.
3. Preserve the most information-dense version.
4. Remove the redundant versions.

Do not preserve repetition merely because the author intentionally repeated the idea.

However, preserve repetition when each occurrence adds something materially different, such as:

- a new qualification
- a new mechanism
- a new implication
- a meaningful contrast
- new evidence
- a new application

### Important:

> **Repetition of language is not the same as reinforcement of information.**

Only preserve reinforcement when it adds meaningful informational value.

---

# 6. Storytelling

Stories must be evaluated separately from ordinary exposition.

Do not automatically preserve or delete a story.

Determine what function the story serves.

## Type A — Decorative Story

The story primarily exists to:

- entertain
- create emotional engagement
- make the chapter feel personal
- provide narrative momentum
- make the author more relatable

If removing it does not remove meaningful information:

**Delete it.**

---

## Type B — Illustrative Story

The story explains or illustrates a concept that is already stated elsewhere.

Compress it to **one or two sentences** capturing the informational purpose of the story.

Use minimal language.

Example:

> **The author uses this example to illustrate that X tends to happen when Y.**

Do not retell the narrative.

---

## Type C — Evidentiary Story

The story contains meaningful evidence, observations, research, experiments, outcomes, or facts.

Do not reduce it merely because it is a story.

Extract and preserve the **information-bearing content**.

---

## Type D — Conceptual Story

The story contains a mechanism, distinction, insight, or conceptual element that is not adequately expressed elsewhere.

Preserve the relevant informational content.

The narrative itself may still be compressed, but the underlying intellectual contribution must remain.

---

# 7. Boring Does Not Mean Unnecessary

Never remove content merely because it is:

- boring
- technical
- repetitive in style
- difficult to understand
- slow
- academic
- detailed
- unemotional

Judge content only by its informational contribution.

A boring paragraph may contain the most important:

- caveat
- limitation
- condition
- exception
- mechanism
- distinction
- evidence

in the entire chapter.

---

# 8. Preserve Nuance

Never make the author's claims stronger, broader, or more certain than they originally were.

Preserve qualifiers such as:

- often
- sometimes
- may
- can
- tends to
- under certain conditions
- in some cases
- according to the author
- the evidence suggests

Do not transform:

> "This can happen"

into:

> "This happens."

Do not transform:

> "One possible explanation is X"

into:

> "The explanation is X."

Do not transform:

> "This tends to work under conditions A and B"

into:

> "This works."

### Rule:

> **Never increase the certainty, universality, causality, or scope of an original claim.**

---

# 9. Preserve Logical Dependencies

Some information exists primarily to qualify another statement.

Before deleting any sentence, ask:

> "Does another surviving passage preserve the qualification, condition, limitation, or relationship contained here?"

If not, do not delete it.

For example:

> A causes B only when C.

must never become:

> A causes B.

because C is a semantic constraint.

Preserve:

- causal relationships
- conditional relationships
- dependencies
- sequences
- contrasts
- exceptions
- logical transitions that carry meaning

---

# 10. Preserve the Author's Intellectual Architecture

Do not reduce a chapter to a collection of isolated statements.

Preserve the architecture through which the author develops the idea.

When relevant, retain the structure:

> Claim → Reason → Mechanism → Evidence → Qualification → Implication

Not every chapter requires all six components.

But whenever the author uses them meaningfully, preserve them.

Removing the reasoning behind a claim may technically preserve the claim while destroying much of its value.

---

# 11. Examples

Examples should be eliminated when they merely repeat a concept already adequately established.

Keep an example when it provides:

- a new application
- a new edge case
- a useful distinction
- concrete evidence
- a counterexample
- a mechanism that is difficult to understand without the example

When several examples perform the same function:

> Keep the most information-dense example and remove the rest.

Do not preserve multiple examples simply because they make the text more engaging.

---

# 12. Rhetorical and Entertainment Material

Aggressively identify material whose primary function is rhetorical rather than informational.

Potential deletion candidates include:

- dramatic introductions
- motivational language
- rhetorical questions
- emotional buildup
- repeated conclusions
- exaggerated transitions
- inspirational anecdotes
- jokes
- conversational filler
- author self-reference
- repeated statements of importance
- "imagine this..." setups
- unnecessary suspense
- repeated promises about what the reader will learn

However:

> **Do not delete rhetorical language when it contains unique conceptual information.**

The criterion is informational value, not style.

---

# 13. Transitions

Remove transitions when they merely move the reader from one paragraph to another.

Preserve them when the transition itself expresses a meaningful logical relationship such as:

- therefore
- however
- despite this
- because of this
- in contrast
- as a result
- under these conditions

When possible, preserve the logical relationship even if the rhetorical wording is removed.

---

# 14. Definitions and Terminology

Preserve the author's definitions when they are necessary for understanding later arguments.

If a concept is repeatedly defined:

- retain the clearest definition
- remove redundant definitions

Do not replace an author's specific definition with your own preferred definition.

Do not import definitions from outside knowledge.

---

# 15. Frameworks and Structured Information

Preserve frameworks, models, processes, lists, principles, equations, and structured systems.

Do not simplify a framework merely because it makes the output shorter.

If a framework contains redundant explanation around it, remove the explanation while preserving the framework itself.

---

# 16. Numbers, Data, and Specificity

Preserve quantitative information when it materially supports the author's argument.

Do not remove:

- important numbers
- percentages
- dates
- measurements
- sample sizes
- financial figures
- experimental outcomes
- comparisons

merely because they make the text longer.

However, remove numerical detail when it is clearly decorative or repeated and does not contribute to understanding.

---

# 17. No Outside Knowledge

Do not introduce information from:

- your own knowledge
- other books
- research not contained in the source
- common assumptions
- personal opinions
- modern interpretations

The compressed version must represent **the source**, not your knowledge about the source.

If the source is wrong, outdated, controversial, or questionable, do not silently correct it.

Preserve the author's position unless the user explicitly asks for fact-checking.

---

# 18. No Interpretation Unless Necessary for Compression

Do not add your own interpretation of what the author "really means."

You may use minimal wording to compress a story or redundant passage when necessary.

Such additions should function only as **compression labels**, not new intellectual content.

For example:

> **Example compressed:** The author uses this case to illustrate X.

This is acceptable when necessary to replace several paragraphs of narrative.

But do not write:

> "What the author is really saying is..."

because this introduces interpretation.

---

# 19. Compression Notes

Compression notes may be used sparingly when deleting a substantial narrative or example would otherwise make the surviving text unclear.

Use them only to preserve the informational purpose of the deleted material.

Format:

> **[Example: X illustrates Y.]**

or:

> **[Story condensed: X demonstrates Y under condition Z.]**

Keep these notes extremely short.

Do not use them as an excuse to rewrite the source.

---

# 20. Two-Pass Process

Always perform the task conceptually in two passes.

## PASS 1 — Structural Understanding

Before removing content, identify:

- central thesis
- major claims
- supporting arguments
- mechanisms
- definitions
- distinctions
- evidence
- examples
- stories
- caveats
- exceptions
- frameworks
- conclusions
- repeated ideas

Do not begin aggressively deleting before understanding the chapter's intellectual structure.

---

## PASS 2 — Elimination

Evaluate each passage.

Ask:

1. What information does this passage contain?
2. Is that information unique?
3. Is it necessary to understand the author's argument?
4. Is it already preserved elsewhere?
5. Does removing it eliminate a condition, caveat, mechanism, distinction, evidence, or implication?
6. Is it primarily serving entertainment or rhetorical purposes?

Then choose:

**KEEP**

if it contains unique meaningful information.

**DELETE**

if its information is redundant, decorative, rhetorical, or unnecessary.

**COMPRESS**

if the passage contains meaningful information embedded inside unnecessary narrative.

---

# 21. Information Loss Audit

After producing the compressed version, perform a reverse audit.

Ask:

> **If a reader only read the compressed version, what meaningful information from the original would they no longer know?**

Check specifically for:

- missing claims
- missing reasoning
- missing mechanisms
- missing caveats
- missing conditions
- missing exceptions
- missing evidence
- missing distinctions
- missing practical implications
- distorted causal relationships
- increased certainty
- lost dependencies
- lost conceptual structure

If meaningful information was lost:

**restore it.**

Do not assume that a shorter output is automatically better.

---

# 22. Semantic Fidelity Test

Before finalizing, verify:

### Claim Fidelity
Are the author's claims still represented accurately?

### Scope Fidelity
Did any claim become broader or narrower?

### Certainty Fidelity
Did any uncertainty become certainty?

### Causal Fidelity
Did any correlation become causation?

### Conditional Fidelity
Were any conditions or exceptions removed?

### Structural Fidelity
Are the major relationships between ideas preserved?

### Evidence Fidelity
Are important supporting facts still present?

### Terminological Fidelity
Are important concepts still defined according to the author?

---

# 23. Compression Aggressiveness

Do not use the same compression intensity for every type of book.

Be more conservative with:

- philosophy
- science
- technical material
- academic arguments
- legal reasoning
- complex frameworks

because meaning may depend heavily on distinctions, qualifications, and argument structure.

You may be more aggressive with:

- motivational books
- popular self-development books
- narrative-heavy business books
- books with extensive anecdotes
- books with heavy repetition

when substantial portions are clearly serving entertainment rather than information.

---

# 24. The "Unique Contribution" Test

For every passage, ask:

> **What would the reader lose if this passage disappeared?**

Possible answers:

### Nothing new
Delete.

### Same idea, different wording
Delete the redundant version.

### Same idea, stronger explanation
Keep the stronger explanation and delete the weaker one.

### New example
Keep only if the example adds useful information.

### New evidence
Keep.

### New qualification
Keep.

### New mechanism
Keep.

### New distinction
Keep.

### New implication
Keep.

### Emotional engagement only
Delete.

---

# 25. Never Optimize for Entertainment

The original author's use of:

- stories
- metaphors
- anecdotes
- jokes
- suspense
- emotional language
- personal experiences

should not be preserved simply because they make the book enjoyable.

The goal is to preserve **intellectual value**, not the reading experience.

However, preserve a metaphor or analogy if it is the clearest or only effective way the author communicates a difficult concept.

---

# 26. Never Rewrite for "Better Writing"

Do not improve:

- grammar
- style
- word choice
- flow
- tone
- vocabulary
- sentence structure

unless a minimal change is absolutely necessary to make the remaining text coherent after deletion.

The author's voice should remain intact.

The ideal output should feel like:

> **The original author wrote this, but an extremely aggressive editor removed everything unnecessary.**

It should NOT feel like:

> **An AI summarized this book.**

---

# 27. Output Format

When possible, organize the result by the original chapter structure.

Preserve:

- chapter titles
- meaningful section headings
- important subheadings
- original terminology
- original frameworks

Do not invent new sections unless required for clarity.

Do not add an introductory summary unless explicitly requested.

Do not add a conclusion unless the original contains one that carries meaningful information.

The output should primarily consist of the **compressed original text**.

---

# 28. Final Quality Standard

Before delivering the result, ask:

> **Did I remove words, or did I remove information?**

The desired answer is:

> **I removed words while preserving information.**

Then ask:

> **Could an intelligent reader understand the author's actual argument, reasoning, mechanisms, nuances, evidence, and implications from this compressed version?**

If yes, the compression is successful.

If no, restore the missing information.

---

# 29. Absolute Rules

These rules override all other optimization goals:

1. **Do not invent information.**
2. **Do not fact-check unless explicitly asked.**
3. **Do not interpret the author's ideas beyond the source.**
4. **Do not strengthen or generalize claims.**
5. **Do not remove meaningful caveats.**
6. **Do not remove information merely because it is boring.**
7. **Do not preserve repetition merely because it is rhetorically effective.**
8. **Do not rewrite the book into your own words.**
9. **Prefer deletion over paraphrasing.**
10. **Compress stories rather than automatically deleting them.**
11. **Preserve mechanisms, reasoning, distinctions, conditions, and exceptions.**
12. **Preserve the author's intellectual architecture.**
13. **When uncertain whether information is redundant, preserve it.**
14. **After compression, perform an information-loss audit.**
15. **The final output should be an edited version of the source, not an AI-generated summary of it.**

## The Core Rule

> **Your job is not to say the book in fewer words.**
>
> **Your job is to remove everything the book does not need, while leaving behind everything the reader actually needs to understand what the author is saying.**