Below is a **copy-paste-ready presentation script** for your deck [pr-agent-presentation-260601.v2.pptx](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D\&file=pr-agent-presentation-260601.v2.pptx\&action=edit\&mobileredirect=true\&EntityRepresentationId=cf47f8df-464e-4662-8510-fd303096f900). I wrote it for an audience of **Jenny Cho, the PM Team, and the Singapore team**, with a business-friendly tone but still credible from an engineering perspective.

***

## Opening / Before Slide 1

“Hi everyone, thanks for joining.

Today I’d like to share a proposal for applying an AI Reviewer to our pull request review process.

The main goal is not to replace developers or reviewers. The goal is to reduce repetitive review effort, improve consistency, and help teams move PRs through the review process faster while still keeping human accountability and engineering quality.

This is proposed as a controlled pilot, not a full rollout. We want to validate the impact with real data before making any bigger decision.”

***

## Slide 1 — AI-Assisted PR Review Pilot

“Today’s topic is the **AI-Assisted PR Review Pilot**.

The focus is on reducing delivery bottlenecks while maintaining engineering quality.

In many projects, pull request review is one of the most important quality gates. But it can also become a bottleneck when PR volume increases, when reviewers are busy, or when the same types of feedback are repeated again and again.

So the question we want to answer is: can AI help us review PRs faster, without reducing quality or removing human responsibility?” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

***

## Slide 2 — Why This Matters Now

“This matters now because PR volume is increasing across teams.

As more features, fixes, and client requests come in, developers are creating more pull requests. That means reviewers, especially senior engineers, spend more time reviewing code.

The issue is not only the number of PRs. It is also the repeated nature of many review comments — formatting issues, naming, missing checks, unclear logic, small code quality improvements, or missing summaries.

These are important, but they consume reviewer time.

If review bottlenecks grow, delivery slows down and release predictability becomes harder. For PMs, this impacts planning. For engineering, it creates pressure. For clients, it can affect delivery timelines.

So we need a way to scale review capacity without immediately depending on more headcount. AI-assisted review is now mature enough for us to validate through a controlled pilot.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Optional emphasis for PM/Singapore team:**

“From a project management perspective, this is not just a technical improvement. It is also about improving delivery flow and reducing uncertainty in release planning.”

***

## Slide 3 — Current Bottlenecks

“Currently, there are a few bottlenecks in the PR review process.

From the engineering side, long review cycles can delay releases. Sometimes a PR waits for review, then receives feedback, then goes back to the developer, then waits again. This creates multiple review rounds.

Another issue is that review quality can vary depending on who reviews the PR, how much context they have, and how much time they have available.

Senior engineers also repeat the same feedback across different PRs. This is valuable feedback, but it is not always the best use of senior engineering time.

For junior developers, they may rely heavily on reviewers to catch basic issues. That can slow down both the junior developer and the reviewer.

From the business side, these engineering bottlenecks can create slower time-to-market, higher delivery cost, and less predictable release timelines.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Transition:**

“So instead of waiting until human review to catch every basic issue, we can move some of that first-pass feedback earlier in the process.”

***

## Slide 4 — Solution: AI As The First Reviewer

“The proposed solution is to use AI as the first reviewer before human review.

Before a human reviewer spends time checking the PR, AI can help summarize the changes, flag potential issues, and suggest improvements.

For example, AI can provide a quick summary of what changed in the PR, identify possible missing validations, highlight risky logic, or suggest readability improvements.

This helps the human reviewer start with better context. Instead of spending the first few minutes understanding the PR from zero, the reviewer gets a structured summary and initial findings.

But the important point is: human review remains mandatory for final approval.

AI gives support. It does not approve, merge, or take responsibility for the code.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Optional engineering credibility line:**

“In practice, I see AI as a first-pass reviewer, similar to an assistant that checks common patterns before the senior engineer focuses on architecture, business logic, edge cases, and risk.”

***

## Slide 5 — What AI Will Not Do

“This slide is important because we need to be very clear about the boundaries.

AI will support reviewers, but it will not replace reviewer accountability.

It will not approve or merge code. It will not replace human engineering judgment. It will not make architectural decisions independently.

We also should not enable it for all repositories by default. The first pilot should be limited and controlled.

And we should not use it on sensitive repositories during the initial pilot, especially if there are client-confidential concerns or source code exposure risks.

So this is not a proposal to let AI control our code review process. It is a proposal to use AI carefully as an assistant inside our existing engineering governance.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Suggested phrase for management confidence:**

“The final accountability still stays with our engineers and our existing approval process.”

***

## Slide 6 — GitHub AI Reviewer vs PR-Agent

“There are two possible directions we can consider: GitHub AI Reviewer and PR-Agent.

The trade-off is convenience versus control.

GitHub AI Reviewer is native, easy to start, requires minimal setup, and gives us a standard out-of-the-box review experience.

The limitation is that we may have less control over the review behavior and customization.

PR-Agent, on the other hand, gives us more customization. We can tune review behavior, enforce team-specific standards, and control workflow or deployment better.

But the trade-off is that PR-Agent requires more setup and governance.

So I’m not recommending that we make a final tool decision blindly. The recommended approach is to validate through a pilot.

We can compare how useful the comments are, how much noise is produced, how much setup is required, and whether the tool fits our engineering process.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Optional if asked which one you prefer:**

“My initial preference is to pilot the option that gives us enough control for team standards and governance. But the final decision should be based on pilot data, not assumptions.”

***

## Slide 7 — Expected Impact

“The expected impact of the pilot is based on a few hypotheses.

First, we want to see whether we can reduce PR review time by around 30 to 50 percent.

Second, we want to reduce repeated review interactions. For example, instead of a senior reviewer repeatedly commenting on the same basic issue, AI can catch it earlier.

Third, we want to improve consistency of review feedback. AI can apply the same checklist or prompt standards across PRs, which helps reduce variation.

Fourth, we expect developer productivity to improve because developers receive earlier feedback and reviewers can focus on higher-value review areas.

The capacity opportunity here is also important. If we can recover reviewer time currently spent on repetitive feedback, we can improve throughput without immediately increasing headcount.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**PM-focused line:**

“For PMs, the value is better flow: fewer PRs stuck waiting, fewer review rounds, and more predictable release progress.”

***

## Slide 8 — Business Value

“From a business value perspective, this can support faster releases and client delivery.

If PRs move faster through review, features and fixes can reach testing and release sooner.

It can also help make delivery timelines more predictable. When review time is inconsistent, planning becomes harder. If we can reduce that variation, it helps PMs and stakeholders plan more confidently.

There is also a cost benefit. If senior engineers spend less time on repetitive review comments, the engineering cost per feature can go down.

Another value is onboarding. New developers can receive earlier feedback and learn team standards faster.

And finally, AI can help detect common issues before senior review, so human reviewers can spend more time on deeper concerns like business logic, architecture, performance, security, and maintainability.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Strong closing sentence for this slide:**

“So the business value is not only speed. It is speed with consistency, quality, and better use of engineering capacity.”

***

## Slide 9 — Risk & Governance

“Of course, there are risks, and we should not ignore them.

The first risk is AI hallucination or incorrect suggestions. AI may sometimes make comments that are not accurate or not relevant.

The second risk is source code exposure to external APIs. This is why we must be careful about which repositories are included, especially in the first phase.

The third risk is over-reliance. Developers and reviewers should not blindly trust AI comments.

The fourth risk is noise. If AI produces too many low-value comments, it can slow us down instead of helping.

To mitigate these risks, human approval remains mandatory.

We can start with PR summary-only mode, so AI helps with understanding the PR before we allow it to suggest code improvements.

We should restrict the pilot to selected repositories and avoid sensitive or client-confidential repositories in the first phase.

We should define prompt standards and usage rules, track false positives, collect developer feedback, and consider self-hosted deployment where required.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Senior engineering note:**

“The pilot should measure not only whether AI gives comments, but whether those comments are actually useful, accurate, and accepted by developers.”

***

## Slide 10 — Pilot Plan

“The proposed pilot duration is 4 to 6 weeks.

The scope should be small: around 2 to 3 repositories, ideally from teams with medium PR volume. We do not want to start with too many repositories, because we need enough control to measure quality and risk.

The pilot can be done in phases.

Phase one is PR summary only. AI summarizes what changed, which helps reviewers understand the PR faster.

Phase two enables AI suggestions. At this point, AI can start giving improvement recommendations.

Phase three is prompt tuning. Based on team feedback, we adjust the instructions so the AI comments match our coding standards and review expectations.

For success metrics, we should track median PR review cycle time, number of review rounds per PR, reviewer effort, developer satisfaction, accepted versus rejected AI suggestions, and post-merge defects related to reviewed changes.

This gives us both quantitative and qualitative data before deciding whether to expand.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Optional detail if audience asks “how do we measure?”**

“For example, we can compare review cycle time before and during the pilot, and we can sample AI comments to classify them as useful, neutral, noisy, or incorrect.”

***

## Slide 11 — Decision Ask

“So the decision ask is simple.

I’m proposing that we run a controlled AI Reviewer pilot in selected repositories and measure the impact over 4 to 6 weeks.

The decision needed today is approval to start the pilot.

If approved, the next steps would be to select the repositories, define usage rules, confirm which tool or tools to validate, and agree on the success metrics.

The goal is not to force a full rollout. The goal is to collect real evidence and decide based on results.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

**Suggested confident closing:**

“If the pilot shows clear value, we can then prepare a broader rollout plan. If it does not, we still learn where AI review is useful and where human review remains the better approach.”

***

## Slide 12 — Closing

“Thank you everyone.

To summarize, AI Reviewer is not intended to replace our engineers. It is intended to reduce repetitive review effort, improve consistency, and help PRs move faster through the delivery pipeline.

With a controlled pilot, clear governance, and measurable success criteria, we can validate the value safely before making a larger investment.

I’m happy to hear your feedback, concerns, and suggestions on the pilot scope.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

***

# Shorter Executive Version

If you need a more concise script, use this version:

“Today I’m proposing a controlled pilot for AI-assisted PR review.

The reason this matters is that PR volume is increasing, review cycles are becoming a bottleneck, and senior engineers are spending repeated time on common review feedback. This slows delivery and makes release timelines less predictable. [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

The proposal is to use AI as the first reviewer. AI can summarize PR changes, flag potential issues, and suggest improvements before human review. But human approval remains mandatory. AI will not approve code, merge PRs, replace engineering judgment, or be enabled on sensitive repositories during the initial pilot. [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

We can compare options such as GitHub AI Reviewer and PR-Agent. GitHub AI Reviewer is easier to start, while PR-Agent gives us more control and customization. The right approach is to validate through a pilot instead of making assumptions. [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

The expected impact is to reduce PR review time by 30 to 50 percent, reduce repeated review interactions, improve feedback consistency, and recover reviewer time currently spent on repetitive comments. [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

The pilot should run for 4 to 6 weeks across 2 to 3 selected repositories. We can start with PR summary-only mode, then enable suggestions, then tune prompts based on feedback. Success metrics should include review cycle time, number of review rounds, reviewer effort, developer satisfaction, accepted versus rejected AI suggestions, and post-merge defects. [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

The decision ask is approval to start the pilot. This is not a full rollout. It is a measured experiment to confirm whether AI Reviewer can help us improve delivery speed while maintaining engineering quality.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

***

# Suggested Q\&A Preparation

## If Jenny Cho asks: “How do we know this will not reduce quality?”

You can answer:

“That is why the pilot keeps human approval mandatory. AI only supports the review process. It does not approve, merge, or replace engineering judgment. We will also track accepted versus rejected AI suggestions and post-merge defects, so quality is part of the success measurement, not an assumption.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

## If the PM Team asks: “What is the business benefit?”

You can answer:

“The business benefit is faster and more predictable delivery. If we reduce review bottlenecks and repeated review rounds, PRs can move through the pipeline faster. That helps release planning, reduces engineering cost per feature, and supports more consistent delivery timelines.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

## If the Singapore team asks: “Is source code safe?”

You can answer:

“That is one of the key governance concerns. For the initial pilot, we should avoid sensitive or client-confidential repositories, restrict the pilot to selected repositories, define usage rules, and consider self-hosted deployment where required.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

## If someone asks: “Why not enable it for all repositories?”

You can answer:

“Because we need to validate usefulness, accuracy, noise level, security, and team fit first. A controlled pilot lets us measure impact and risks before expanding.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

## If someone asks: “Which tool should we choose?”

You can answer:

“There is a trade-off. GitHub AI Reviewer is easier and more native, while PR-Agent gives us more control and customization. I suggest we validate through the pilot and decide based on actual review quality, setup effort, governance needs, and developer feedback.” [\[pr-agent-p...-260601.v2 \| PowerPoint\]](https://omgww-my.sharepoint.com/personal/thanhlam_vo_verticurl_com/_layouts/15/Doc.aspx?sourcedoc=%7BA95418DE-3CFD-4019-B81E-163556CA19F1%7D&file=pr-agent-presentation-260601.v2.pptx&action=edit&mobileredirect=true)

***

# Delivery Tips

* Speak slowly on slides 5 and 9 because those slides address risk and governance.
* For PM audience, emphasize **predictability, delivery flow, and cost efficiency**.
* For engineering audience, emphasize **human approval, review quality, false positives, and repository restrictions**.
* Avoid saying “AI will review better than humans.” Say: **“AI helps with the first pass, humans remain accountable.”**
* Your strongest message should be: **controlled pilot, measurable results, safe governance, no replacement of human reviewers**.
