---
name: axb-clarify
description: When requirements have omissions, contradictions, ambiguities, or undecided decisions, first organize understandable context, refined questions, and comparable options, then interview the user directly — preventing the AI from filling in requirements through imagination. Can serve as a downstream skill for other skills; the caller specifies the priority questioning dimensions and whether to keep detailed Q&A records. Use when the user invokes /axb-clarify, asks the AI to interview for missing requirements, or when another skill needs to resolve incomplete, ambiguous, or conflicting requirements before proceeding.
disable-model-invocation: true
---

# Clarify

When requirements still have insufficient detail, ambiguous definitions, or multiple reasonable interpretations, first supplement the context needed for the decision, then ask the user questions with clear, comparable options — letting the user make the call rather than the AI filling in the blanks itself.

# SOP

## Phase 1 -- Converge this round's interview gaps

1. READ Read the user requirements, the caller skill's instructions, the current context, and existing artifacts; confirm the topic to clarify this time, the decision boundaries, the specified questioning dimensions, and whether detailed Q&A records are needed.
2. THINK First read `rules/high-impact-gap-inventory-and-question-ordering-criteria.md`, then inventory the omissions, contradictions, ambiguities, and undecided decisions in the requirements as it requires; prioritize converging the 1 to 3 questions with the largest impact as this round's questions, and ensure the entire clarify session accumulates no more than 5 questions.

## Phase 2 -- Produce this round's clarify questions

1. WRITE First read `rules/context-and-option-question-drafting-criteria.md`, `templates/clarify-question-round.md`, and `templates/clarify-question-round.example.md`, then output this round's questions directly in the conversation following the skeleton and examples: each question must first provide a `Context` sufficient to help the user judge, then pose a single clear `Summary Question`, and finally list single-choice or multi-choice `Options` in a Markdown table, marking one recommended option with its reason, and always providing `Others` for the user to add input; the Ask Tool must not be used.
2. WRITE Explicitly ask the user to reply with the option numbers by question number, supplementing in `Others` where necessary; stop before receiving answers, and do not assume answers on your own.

## Phase 3 -- Decide follow-up questions, convergence, or recording based on answers

1. READ Read the user's answers to this round's questions; organize the decisions already made, the still-unresolved gaps, and newly surfaced constraints; judge whether the caller skill has enough to continue.
2. WRITE If the caller skill requires detailed Q&A records, first read `templates/clarify-log.md` and `templates/clarify-log.example.md`, then update this clarify session's Q&A record following the skeleton.
3. THINK If high-impact gaps remain and the cumulative question count has not reached 5, return to Phase 1 to prepare the next round of questions; if the information is sufficient, output the confirmed decisions, the user's additions, and the remaining risks, then hand back to the caller skill to continue the follow-up process.
