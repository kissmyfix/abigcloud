# The cold read

A test of whether this project's own files are good enough for a session that starts with
nothing. A fresh agent reads only the orientation material, answers ten fixed questions,
and the gap between its answers and the answer key is the measurement.

**The finding is always a documentation defect, never an agent failure.** If a cold agent
concludes something wrong, the files taught it wrong. That is the entire point.

Devised by Brandon and Claude on 2026-08-17 and run once. Written down 2026-08-18 so it
can be repeated and compared.

---

## Why it exists

Every session after the first is warm: it inherits a conversation that patched the gaps in
the files without anyone noticing the files had gaps. The cold read is the only way to see
the documentation the way a new session actually sees it.

## The procedure

**1. Update the answer key first.** `answer-key.md` carries a "valid as of `<sha>`" stamp.
Bring it to current truth before spawning anything. This step is not overhead — writing
down what is true now is how you discover what changed and was never documented.

Order matters. A key written *after* reading the report grades the report against itself
and measures nothing.

**2. Brandon confirms the key.** His confirmation is what makes it a baseline rather than
Claude's opinion. Without this step the test compares Claude's documentation against
Claude's expectations.

**3. Run the setup pass.** Read the orientation files with fresh eyes and fix anything
obviously broken before spawning. Doing this in 2026-08-17 caught an unscoped "not
negotiable" in the evidence standard. Cheap defects found here cost nothing to fix.

**4. Spawn the cold agent** with `prompt.md`, verbatim, as a `general-purpose` subagent.
It reads only orientation files and whatever they point to. Read-only: no edits, no
state-changing git.

**5. Compare.** Questions 1 to 9 are the control; they should roughly match the key.
**Question 10 is the test.** What it stumbles on is the signal.

**6. Verify every defect before acting on it.** In the first run the cold agent was wrong
about exactly one item. Grep for each claim. A cold agent is a source like any other and
gets the same treatment: never at face value.

**7. Record the run** in `runs/YYYY-MM-DD.md`, tied to the commit it tested, with each
defect and its disposition.

## Reading the score

| Result | What it means |
|---|---|
| Q1-9 match, Q10 empty | The files are good, or the questions have gone stale. Suspect the second. |
| Q1-9 match, Q10 finds real defects | Working as intended. This is the normal healthy outcome. |
| Q1-9 diverge | Serious. The orientation files are actively teaching the wrong thing. |
| Q10 flags known-and-accepted items | Not a defect. See section 10 of the answer key. |

## When to run it

After any structural change to the repo, after a documentation rewrite, and otherwise
roughly monthly. The first run was 2026-08-17; a cadence was never set, which is itself
the reason this file exists.

## What it does not test

Whether the investigation is correct. It tests whether the project explains itself. Those
are different, and only the second one is measurable this way.
