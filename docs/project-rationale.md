# Project Rationale

Magent exists because AI-assisted reasoning is becoming powerful, but most reasoning attempts disappear inside isolated chat sessions. That wastes compute, human attention, and partial progress.

The project treats difficult mathematical work as shared research state:

- what is known
- what has been tried
- what failed
- what might work
- what depends on what
- what should be checked next

The intended audience includes mathematicians, scientists, programmers with model access, prompt engineers, and AI systems. The repository should be readable by humans and easy for models to continue from.

## Motivation

A motivating pattern is that people increasingly report AI-assisted progress on long-standing problems. Whether any single report is correct is not the point. The important point is that future attempts should be cumulative.

If a model finds one useful step, a human should be able to inspect it. If a human finds a gap, the gap should be preserved. If a path fails, the obstruction should be stored so later attempts do not repeat it.

## Design Constraint

The repository must not become a transcript archive.

Raw model output is usually too verbose, too unreliable, and too hard to review. Magent stores distilled research artifacts: statements, dependencies, derivations, gaps, review notes, failed paths, and next tasks.

## Working Thesis

The useful unit is not a conversation. The useful unit is a checkable research object.

