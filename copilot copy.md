
Tone = **short, confident, non-defensive** (very important for Jenny Cho + PMs).

***

# 🎯 1. VALUE / ROI QUESTIONS

***

### ❓ “The 30–50% reduction — what is that based on?”

> It’s based on industry benchmarks and expected reduction in review iterations.
> The pilot will validate this with our own data.

***

### ❓ “How do you measure the 2 hours/day savings?”
> We track PR cycle time and number of review iterations before and after.
> The time saving comes from reducing back-and-forth.

### ❓ “Does this improve quality or just speed?”
> It improves consistency and catches common issues earlier.
> Final quality is still ensured by human review.

***

### ❓ “If a team already has a strong review process, is this still useful?”

> Yes — even strong teams still have repetitive feedback.
> This reduces that and frees up senior engineers for higher-value work.

***

# 🔁 2. FLOW / PROCESS QUESTIONS

***

### ❓ “At what point does AI come in?”

> Right after the PR is opened, before human review.
> It acts as the first reviewer.

***

### ❓ “Does the review loop actually get reduced?”

> Yes — because most obvious issues are caught early.
> We reduce the number of iterations, not remove the loop.

***

### ❓ “Are we just shifting effort back to developers?”

> Slightly — but earlier and faster.
> Overall, the total review cycle time still decreases.

***

# ⚠️ 3. RISK / TRUST QUESTIONS

***

### ❓ “Are we sending code to external LLMs?”

> We can configure both external and self-hosted options.
> For sensitive repositories, we can restrict usage or use self-hosted only.

***

### ❓ “What about hallucinations?”

> That’s expected — which is why human review remains mandatory.
> AI assists, it does not make decisions.

***

### ❓ “What if developers follow incorrect suggestions?”

> AI suggestions are treated like peer feedback, not authoritative decisions.
> Reviewers still validate everything.

***

### ❓ “Could this reduce review quality?”

> No — it shifts focus to higher-value feedback instead of repetitive issues.

***

# 🤖 4. TOOL / COMPARISON QUESTIONS

***

### ❓ “Why not just use GitHub Copilot?”

> Copilot helps during coding.
> This improves the review stage and team-level productivity.

***

### ❓ “Isn’t this what SonarQube or linters already do?”

✅

> Those handle rule-based checks.
> This addresses logic, structure, and context.

***

# 👥 5. TEAM IMPACT QUESTIONS

***

### ❓ “Will developers actually use it?”

✅

> Yes — it integrates directly into the PR workflow, so there’s minimal friction.

***

### ❓ “Will junior developers become dependent on it?”

✅

> It actually helps them learn faster by providing immediate feedback.

***

### ❓ “Does this reduce the need for senior engineers?”

✅

> No — it allows them to focus on higher-impact review instead of repetitive comments.

***

# 🧪 6. PILOT QUESTIONS

***

### ❓ “Why start with 2–3 repositories?”

✅

> It gives us enough diversity while keeping the scope manageable.

***

### ❓ “How do we measure success?”

✅

> PR cycle time, number of review iterations, and developer feedback.

***

### ❓ “What if the results are mixed?”

✅

> We refine the scope or limit usage to the teams where it delivers value.

***

### ❓ “When do we decide to roll out?”

✅

> After the pilot shows consistent improvement across key metrics.

***

# 🌏 7. SCALING QUESTIONS (Singapore teams)

***

### ❓ “Can this work across different tech stacks?”

✅

> Yes — the base setup is reusable across repositories.
> Some prompt tuning may be needed.

***

### ❓ “How much effort to onboard a new team?”

✅

> Low — mainly configuration and initial tuning.

***

### ❓ “Who maintains it?”

✅

> Ideally a central owner for governance, with flexibility at team level.

***

# 💣 8. HIGH-LEVEL / STRATEGIC QUESTIONS

***

### ❓ “Why now?”

✅

> AI is mature enough to provide practical value.
> And PR bottlenecks are becoming a scaling constraint.

***

### ❓ “What happens if we do nothing?”

✅

> Review bottlenecks will continue to limit delivery speed and scalability.

***

### ❓ “Is this worth prioritizing?”

✅

> That’s why we propose a small, measurable pilot before scaling.

***

# ⚠️ 9. CRITICAL QUESTIONS (DO NOT ANSWER WRONG)

***

### ❗ “Is AI replacing human reviewers?”

✅

> No — it improves the first pass and reduces back-and-forth.
> Human review remains the decision point.

***

### ❗ “Can we automate approvals?”

✅

> No — not in scope. Human review is mandatory.

***

### ❗ “Does this guarantee better quality?”

✅

> No — it improves consistency and early issue detection, not guarantee.

***

# 🧠 10. FINAL CHEAT SHEET (REMEMBER THIS)

If you get a tough question, anchor back to:

```
1. AI is the first reviewer
2. It reduces back-and-forth
3. Human review is mandatory
4. This is a controlled pilot
5. We validate with measurable outcomes
```

***

# 🚀 Final tip (very real-world)

When answering Jenny or PMs:

* Keep answers **under 10 seconds**
* Pause after answering
* Let them ask follow-up

👉 That signals confidence much more than long explanations.

***

If you want, I can simulate a **real aggressive Q\&A round (like Jenny pushing hard)** so you can stress-test your answers before the meeting.

PR volume is increasing across teams.
Review bottlenecks are slowing delivery and release predictability.
Senior engineers spend repeated time on common review feedback.
We need to scale review capacity without immediately increasing headcount.
AI-assisted review is now mature enough to validate through a controlled pilot.

Summarize code changes.
Highlight potential bugs, risks, and missing tests.
Suggest improvements based on team standards.
Provide reviewers with faster context..



Pilot hypotheses:

Reduce PR review time by 30–50%.
Reduce repeated review interactions.
Improve consistency of review feedback.
Increase developer productivity by reducing avoidable review delays.

Capacity opportunity:

Recover reviewer time currently spent on repetitive feedback.
Improve throughput without immediately increasing headcount.