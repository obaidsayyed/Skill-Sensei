DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  domain text NOT NULL,
  scenario text NOT NULL,
  option_a text NOT NULL,
  option_p text NOT NULL,
  option_c text NOT NULL,
  option_i text NOT NULL
);
CREATE INDEX idx_questions_domain ON questions(domain);

INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'A production system starts throwing errors at 2am. What''s your instinct?', 'Trace the logs methodically until you find the root cause', 'Restart the service first to stop the bleeding, investigate later', 'Check if any teammates are awake to help troubleshoot together', 'Try a couple of quick fixes and see what sticks');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You''re handed a codebase with zero documentation. How do you feel?', 'Curious — I''d start mapping out how the pieces connect', 'Frustrated but practical — I''d just focus on the part I need to touch', 'I''d look for whoever wrote it and ask them to walk me through it', 'I''d poke around and break small things on purpose to learn how it works');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'Your code passes all tests but still feels "off" to you. What do you do?', 'Re-read the logic line by line until I find the flaw', 'Ship it — if the tests pass, the risk is probably acceptable', 'Ask a teammate to review it with fresh eyes', 'Rewrite it a different way and compare the two approaches');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'A new programming language releases with a lot of hype. Your reaction?', 'Read the technical spec to see if it solves a real problem', 'Wait and see if the industry actually adopts it', 'Check what other developers are saying about their experience with it', 'Build a small toy project with it immediately');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You have to choose between a fast, hacky fix and a slow, correct one.', 'I want to understand exactly why the hacky fix would break later', 'Ship the hacky fix now, schedule the correct one for later', 'Check with the team/users how much the hack would actually hurt them', 'Try the hacky fix first as an experiment, see how far it gets');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'Reading about a massive data breach at a company, what draws your attention?', 'The specific technical vulnerability that was exploited', 'How much it likely cost the company and its users', 'What it must have felt like for affected users to lose their data', 'What other attack methods could have achieved the same result');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You''re asked to automate a task a colleague has done manually for years.', 'Study exactly what steps they take before writing any code', 'Automate the 80% that saves the most time, skip the edge cases', 'Sit with them and understand why they do it the way they do', 'Build a rough version fast and iterate based on what breaks');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'A user reports a bug you can''t reproduce. What''s next?', 'Request logs, screenshots, exact steps — build a reproducible case', 'Check if it''s affecting many users before spending more time', 'Get on a call with the user to see it happen live', 'Try several environments/devices to see if it shows up anywhere');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You''re deciding between two technical architectures for a new project.', 'Compare their theoretical trade-offs on paper first', 'Pick whichever is faster to build and ship this quarter', 'Ask which one the team is more comfortable maintaining long-term', 'Prototype both quickly and see which one feels better to work in');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'What part of building software gives you the most satisfaction?', 'Understanding exactly why something works the way it does', 'Seeing a real problem get solved efficiently', 'Knowing people are actually using and benefiting from it', 'The process of experimenting until something clicks');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'A teammate''s code review comment says your solution is "overengineered."', 'I''d want to understand specifically which part is unnecessary complexity', 'I''d simplify it fast — shipping matters more than being right', 'I''d ask them to pair with me so we land on something we both like', 'I''d try a simpler version and see if it still covers the cases');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You''re given a vague technical requirement with no clear spec.', 'I''d start by listing every assumption I''m making explicit', 'I''d build the smallest thing that could plausibly be right', 'I''d go find the person who requested it and ask clarifying questions', 'I''d build something rough and use it as a conversation starter');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'Your team debates whether to rewrite a fragile legacy system.', 'I''d want data on exactly how often it actually breaks', 'I''d weigh the rewrite cost against how much pain it''s really causing', 'I''d ask whoever maintains it daily how they feel about it', 'I''d propose rewriting one small piece first as a test');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'You discover a security vulnerability in a widely-used open-source tool.', 'I''d want to fully understand the exploit before reporting it', 'I''d report it immediately through the right disclosure channel', 'I''d think about who could be harmed and how urgently to warn them', 'I''d try to reproduce it in a few different contexts first');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('TECHNOLOGY', 'What would make you seriously consider leaving a tech role?', 'Being stuck solving the same shallow problems with no depth', 'The work having no real, visible impact on outcomes', 'A team culture with little collaboration or trust', 'No room to experiment or try new approaches');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'A client says they''ll "know it when they see it" about a design brief.', 'I''d build a structured mood board of concrete visual references', 'I''d design the most commercially safe option first', 'I''d ask them detailed questions about what they''ve reacted to before', 'I''d rapidly sketch a handful of very different directions');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'Two design options test equally well with users, but look very different.', 'I''d check if one aligns better with the brand''s existing system', 'I''d pick whichever is cheaper/faster to implement', 'I''d ask real users which one they''d actually choose and why', 'I''d combine elements of both into a new third option');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'What frustrates you most about a cluttered interface?', 'The lack of a clear visual hierarchy or logic', 'How much time it wastes for the people using it', 'How confusing or overwhelming it must feel to a first-time user', 'That nobody tried simplifying it before adding more');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'You''re redesigning something that already "works fine."', 'I''d study exactly why it works before changing anything', 'I''d only touch the parts causing real friction', 'I''d ask the people who use it daily what actually bothers them', 'I''d try a few bold alternatives just to see what''s possible');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'A design trend is everywhere right now. Your instinct?', 'Understand the underlying principle behind why it works', 'Adopt it only if it fits the current project''s goals', 'Notice how it makes people feel when they encounter it', 'Try it out just to see how it feels to work with');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'You get harsh, blunt feedback on a design you''re proud of.', 'I''d want the specific reasoning behind each critique', 'I''d focus only on the feedback that affects the outcome', 'I''d want to understand the emotional reaction behind the feedback', 'I''d try a few revised versions rather than defend the original');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'What''s most satisfying about finishing a design project?', 'Knowing the system behind it is clean and coherent', 'Knowing it will genuinely help people get something done', 'Seeing someone enjoy or connect with what you made', 'How much you learned by trying different approaches');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'A brand''s visual identity feels inconsistent across platforms.', 'I''d audit every touchpoint against a strict style guide', 'I''d fix the highest-visibility inconsistencies first', 'I''d think about how the inconsistency affects customer trust', 'I''d test a few unifying visual directions before locking one in');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'You have to design something for a culture/context very different from your own.', 'I''d research the visual conventions and symbolism deeply first', 'I''d focus on what''s functionally necessary regardless of culture', 'I''d talk to people from that context before designing anything', 'I''d sketch several drafts and get reactions before refining');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'Given unlimited time on one project, what would you spend it on?', 'Perfecting the underlying visual system and consistency', 'Making sure it solves the actual problem as efficiently as possible', 'Making sure it genuinely delights the people who''ll use it', 'Exploring as many different creative directions as possible');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'A design pattern is technically "best practice" but feels sterile to you.', 'I''d want to understand exactly why it''s considered best practice', 'I''d use it anyway if it performs better', 'I''d think about whether it makes the product feel cold to users', 'I''d try breaking the pattern deliberately and see what happens');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'You''re asked to design for accessibility constraints you''ve never worked with.', 'I''d study the technical accessibility guidelines closely', 'I''d prioritize the constraints with the biggest usability impact', 'I''d try to understand the lived experience behind the constraint', 'I''d prototype a few approaches and test which works best');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'A stakeholder wants to add five more features to a clean interface.', 'I''d map out how each addition affects the existing hierarchy', 'I''d push back on whichever additions add the least value', 'I''d understand why they feel each addition is necessary', 'I''d mock up a version with everything, then start removing');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'What draws you to visual work in the first place?', 'The satisfaction of a well-structured, coherent system', 'Making things that are genuinely more usable', 'Creating something that resonates emotionally with people', 'The open-ended process of creating and experimenting');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('DESIGN', 'You see a beautiful design that''s actually hard to use. Your reaction?', 'Curiosity about how the tradeoff between form and function happened', 'Frustration — usability should have won that trade-off', 'Sympathy for the confused users who''ll encounter it', 'Interest in how you''d redesign it differently yourself');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'A department''s process is inefficient but nobody''s fixed it. Why?', 'I''d map the process end-to-end to find the actual bottleneck', 'I''d estimate the cost of the inefficiency before proposing anything', 'I''d ask the people doing the work what''s actually frustrating them', 'I''d try a small process change and see if it helps');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'Your team disagrees sharply on strategic direction. What helps most?', 'Bringing in hard data to settle the disagreement', 'Clarifying what the actual business goal and deadline are', 'Understanding each person''s underlying concern first', 'Running a small pilot of each direction before committing');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'What part of running or managing a business excites you most?', 'Understanding exactly why certain decisions lead to certain outcomes', 'Making resource allocation decisions that create the most value', 'Building a team and culture people want to be part of', 'Constantly adapting the plan as new information comes in');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'A competitor undercuts your pricing overnight. Your first move?', 'Analyze exactly how they''re able to sustain that price', 'Calculate the real impact on your margins before reacting', 'Consider how customers will perceive the price gap', 'Test a few different responses in a small market segment');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'You inherit a team with low morale and unclear goals.', 'I''d diagnose exactly where the breakdown happened', 'I''d set one clear, achievable near-term goal to build momentum', 'I''d spend real time understanding what people are frustrated about', 'I''d try a few small changes and see what improves morale');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'A key metric is trending down and nobody knows why.', 'I''d dig into the underlying data until I find the cause', 'I''d check if it actually matters to the bottom line right now', 'I''d ask the team closest to that metric what they''ve noticed', 'I''d test a few hypotheses quickly rather than fully investigate one');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'You have to cut costs, and every option has some downside.', 'I''d model the long-term impact of each option carefully', 'I''d cut wherever the least critical value is lost', 'I''d think hard about the human impact of each option', 'I''d trial partial cuts before going all-in on one option');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'What''s most rewarding about closing a difficult negotiation?', 'Having reasoned your way to the strongest possible position', 'Getting the outcome that maximizes actual value', 'Reaching something both sides genuinely feel good about', 'Adapting cleverly as the negotiation twisted and turned');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'A new market opportunity looks promising but risky. Your instinct?', 'Research the market thoroughly before forming an opinion', 'Weigh the potential upside against the realistic downside', 'Understand who the actual customers would be and what they need', 'Test the idea small-scale before committing real resources');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'You''re told to "just make the numbers work" on an unrealistic plan.', 'I''d want to see exactly where the numbers break down', 'I''d push back with a more realistic alternative plan', 'I''d raise concerns about the pressure this puts on the team', 'I''d try a few different approaches to see if any get close');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'A long-time client is unhappy but hasn''t said exactly why.', 'I''d review the account history for what might have changed', 'I''d address whatever''s causing the biggest business risk first', 'I''d have a direct, honest conversation to understand their concern', 'I''d try a few relationship-repair gestures and gauge the response');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'What would frustrate you most in a business role?', 'Decisions made without any real analysis behind them', 'Effort spent on things that don''t move the needle', 'A culture where people don''t feel heard or valued', 'Being locked into one rigid plan with no room to adjust');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'Two departments are fighting over the same limited budget.', 'I''d want clear data on which use creates more value', 'I''d allocate based on which need is more urgent right now', 'I''d get both sides talking to understand the full picture', 'I''d propose a temporary split and revisit after seeing results');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'You''re asked to present a plan you personally have doubts about.', 'I''d want to interrogate the plan''s assumptions before presenting', 'I''d present it but flag the specific risks clearly', 'I''d raise my concerns privately with leadership first', 'I''d suggest testing a scaled-down version before full rollout');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('BUSINESS', 'What would make a business decision feel like the right one to you?', 'It was backed by solid reasoning and evidence', 'It created clear, measurable value', 'It considered the people affected by it', 'It came out of genuinely exploring multiple options first');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'You''re reviewing a company''s financials and something doesn''t add up.', 'I''d trace every line item until I find the discrepancy', 'I''d check if the discrepancy is material enough to matter', 'I''d ask someone in accounting what might explain it', 'I''d compare it against a few similar companies for context');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'A client wants to invest in something you think is too risky.', 'I''d walk them through the numbers behind the risk', 'I''d show them the realistic range of best/worst outcomes', 'I''d try to understand what''s drawing them to that risk', 'I''d suggest a smaller test allocation instead of the full amount');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'What part of finance genuinely interests you?', 'The precision and logic of how numbers reveal the truth', 'Making decisions that create real financial value', 'Helping people make sound decisions about their money', 'Reacting cleverly as markets and conditions shift');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'Markets suddenly become volatile. Your instinct?', 'Analyze exactly what''s driving the volatility', 'Assess how this changes actual portfolio risk', 'Consider how anxious clients might be feeling right now', 'Watch closely and adjust positions as things develop');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'You find a small error in a report that''s already gone out.', 'I''d want to know exactly how the error happened', 'I''d assess whether it''s significant enough to require a correction', 'I''d think about how the error affects whoever relied on it', 'I''d check nearby reports to see if the same error recurs');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'A budget is being blown every month for unclear reasons.', 'I''d track every category of spending line by line', 'I''d focus first on the single biggest overspend', 'I''d ask whoever controls that budget what''s changed for them', 'I''d compare several months to look for a pattern');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'Two investment options offer similar expected returns.', 'I''d compare their risk profiles in detail', 'I''d pick whichever has better liquidity/practicality', 'I''d consider what fits the client''s actual life situation', 'I''d model a few different scenarios before deciding');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'What would be most satisfying about a career in finance?', 'The rigor of getting the numbers exactly right', 'Making decisions with clear, measurable financial impact', 'Genuinely helping someone reach a financial goal', 'Adapting strategy as real-world conditions change');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'A financial model relies on one very uncertain assumption.', 'I''d stress-test the model against different assumption values', 'I''d flag how much the outcome actually depends on that one number', 'I''d want to understand the real-world context behind the assumption', 'I''d build a few versions of the model with different assumptions');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'You''re asked to explain a complex financial concept to a non-expert.', 'I''d walk them through the underlying logic step by step', 'I''d focus on just what matters for their specific decision', 'I''d use an analogy tied to something familiar in their life', 'I''d try a few different explanations and see what clicks');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'A company''s cash flow and profit numbers tell different stories.', 'I''d dig into exactly why they diverge', 'I''d assess which one actually threatens near-term stability', 'I''d think about what this means for employees and stakeholders', 'I''d look at how this compares to similar companies');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'What would you find most frustrating in a finance role?', 'Decisions made ignoring what the numbers actually show', 'Time spent on things with no real financial impact', 'Clients or colleagues not being upfront about real constraints', 'Being locked into one strategy with no room to adapt');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'You have to tell a client their financial goal isn''t realistic.', 'I''d walk them through the numbers that prove it', 'I''d offer a scaled-back but still meaningful alternative goal', 'I''d deliver the news carefully, given how disappointing it''ll be', 'I''d explore a few creative alternative paths with them');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'A regulatory change affects how your firm reports numbers.', 'I''d study the new requirement in detail before acting', 'I''d assess the minimum needed to stay compliant on time', 'I''d think about how this affects clients who rely on our reports', 'I''d test the new reporting approach on a small sample first');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('FINANCE', 'What would make a financial decision feel like the "right" one?', 'It was backed by rigorous, careful analysis', 'It created clear, measurable value with acceptable risk', 'It genuinely served the person or people it was meant to help', 'It held up well after being tested against real scenarios');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'An experiment gives a result you didn''t expect. Your first reaction?', 'Check the data and method carefully before concluding anything', 'Assess whether the surprise actually changes your main conclusion', 'Think about what it might mean for the real-world problem you''re studying', 'Repeat the experiment or try a variation to see if it holds');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'You have limited time and a broad scientific question to explore.', 'I''d narrow it into the smallest testable, precise question', 'I''d focus on whichever sub-question has the most real impact', 'I''d think about which angle most affects people or the environment', 'I''d run several small quick tests before committing to one direction');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'What part of scientific work do you find most satisfying?', 'Understanding exactly why something happens the way it does', 'Producing evidence that leads to a genuinely useful decision', 'Work that improves real outcomes for people or ecosystems', 'The process of testing, failing, and refining ideas');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'Two studies on the same topic reach conflicting conclusions.', 'I''d compare their methods to find what caused the difference', 'I''d figure out which one is more reliable for the decision at hand', 'I''d consider the practical consequences of trusting each', 'I''d look for what further evidence could resolve the conflict');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'You''re asked to explain your research to someone outside your field.', 'I''d walk them logically through the key findings', 'I''d focus only on what matters for their situation', 'I''d relate it to something they already care about', 'I''d try a couple of framings and see what actually lands');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'A long-held theory in your field is being seriously challenged.', 'I''d want to examine the new evidence rigorously myself', 'I''d care mainly about how it changes practical applications', 'I''d think about who''s affected by the theory being wrong', 'I''d be excited to see how the debate plays out over time');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'Your lab has very limited resources for a promising project.', 'I''d design the most information-efficient experiment possible', 'I''d prioritize whichever result would unlock more resources', 'I''d consider whose work depends on this project succeeding', 'I''d run cheap, quick pilot tests before requesting more resources');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'What would frustrate you most in a scientific career?', 'Conclusions drawn without rigorous evidence', 'Research that never translates into anything useful', 'Work disconnected from any real human or environmental impact', 'Being stuck repeating the same method with no room to explore');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'You notice an unusual pattern while reviewing old data.', 'I''d formally test whether the pattern is statistically real', 'I''d assess if the pattern matters enough to pursue further', 'I''d wonder what it might mean for people affected by the topic', 'I''d look for the pattern in other datasets to see if it repeats');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'A colleague''s experimental design has a flaw you''ve noticed.', 'I''d walk through exactly why the flaw would bias the results', 'I''d flag it if it''s serious enough to change the conclusion', 'I''d raise it gently, aware of how much work they''ve put in', 'I''d suggest a modified version of the experiment to test');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'You have to choose a research question to spend years on.', 'I''d choose the one with the most rigorous, answerable core question', 'I''d choose the one most likely to lead to practical impact', 'I''d choose the one that matters most to real people or systems', 'I''d choose the one that leaves room for unexpected discovery');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'Public trust in a scientific finding is being questioned online.', 'I''d want to check the actual quality of evidence behind it', 'I''d think about the real-world harm of the finding being doubted', 'I''d think about how to communicate clearly to worried people', 'I''d look for how the evidence has evolved over time');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'A grant proposal needs one especially strong, focused hypothesis.', 'I''d tighten it until every claim is precisely testable', 'I''d focus it on whatever''s most fundable and impactful', 'I''d frame it around the human or ecological problem it solves', 'I''d draft a few versions and pick the strongest after feedback');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'What draws you to studying the natural or physical world?', 'The logic and structure behind how things work', 'The chance to produce knowledge that solves real problems', 'Understanding how it affects living things and people', 'The open-ended curiosity of discovering the unknown');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SCIENCE', 'An unexpected finding could be a breakthrough or just noise.', 'I''d want more rigorous testing before believing either way', 'I''d assess what''s at stake if I''m wrong either direction', 'I''d think about the impact if the finding turns out to be real', 'I''d stay curious and keep exploring it further either way');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A patient describes vague symptoms that could mean several things.', 'I''d systematically rule out possibilities one by one', 'I''d prioritize checking for the most urgent possibility first', 'I''d spend time understanding their full experience and context', 'I''d order a broad set of tests and see what comes back');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'What part of healthcare work matters most to you?', 'Getting the diagnosis or reasoning precisely right', 'Making the biggest difference with the resources available', 'Genuinely helping someone through a hard moment', 'Continuously learning as medicine and cases evolve');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A treatment isn''t working as expected for a patient.', 'I''d review the evidence behind the treatment choice again', 'I''d weigh whether to switch approaches given time pressure', 'I''d talk to the patient about how they''re experiencing it', 'I''d try an adjusted approach and monitor closely');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'You have very limited time with each patient today.', 'I''d focus on the most clinically important information first', 'I''d triage so the most urgent cases get more time', 'I''d still try to make each patient feel heard, even briefly', 'I''d adapt my approach patient by patient as the day goes');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A patient doesn''t follow the treatment plan you gave them.', 'I''d want to understand exactly why it isn''t being followed', 'I''d adjust the plan to something more realistic for them', 'I''d explore what''s really going on in their life or fears', 'I''d try a different way of explaining or framing the plan');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'Conflicting medical guidelines exist for the same condition.', 'I''d dig into the evidence behind each guideline', 'I''d follow whichever is more practical given constraints', 'I''d consider what matters most to this specific patient', 'I''d stay flexible and adjust based on how the patient responds');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'What would you find hardest about healthcare work?', 'Making decisions without enough solid evidence', 'Constraints that prevent giving patients the best possible care', 'Not having enough time to really connect with patients', 'Rigid protocols that don''t allow for adapting to the individual');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A community shows a sudden rise in a particular health issue.', 'I''d investigate the data to find the likely cause', 'I''d prioritize whichever intervention helps the most people fastest', 'I''d want to understand what''s happening in people''s daily lives', 'I''d try a few different interventions and see what works');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A patient asks you to explain a serious diagnosis simply.', 'I''d walk them logically through what it means and why', 'I''d focus on the information that changes what they need to do', 'I''d think carefully about how to deliver it with real compassion', 'I''d check in and adjust my explanation based on how they react');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'You''re the last line before a potentially risky decision is made.', 'I''d want to review every piece of relevant evidence first', 'I''d weigh the risk of acting versus the risk of delay', 'I''d think hard about what this means for the patient and family', 'I''d consult others and stay open to reconsidering');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A new medical technology could improve outcomes but is unproven.', 'I''d want to see the evidence behind its claims first', 'I''d consider whether the potential benefit justifies the cost', 'I''d think about how it might affect patient trust and comfort', 'I''d be open to trying it cautiously in select cases');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'What would make a case in healthcare feel meaningful to you?', 'Reaching the diagnosis through careful, correct reasoning', 'Achieving the best outcome given real constraints', 'The patient feeling genuinely cared for throughout', 'Learning something that changes how you handle future cases');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'Two patients need the same limited resource urgently.', 'I''d want clear clinical criteria to guide the decision', 'I''d prioritize based on likely outcome and urgency', 'I''d want to understand both situations fully before deciding', 'I''d look for any alternative that avoids the hard trade-off');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'A patient is scared and reluctant to accept a necessary procedure.', 'I''d explain the medical reasoning clearly and thoroughly', 'I''d focus on the most important risk of not proceeding', 'I''d spend real time addressing their fear directly', 'I''d explore what might help them feel more comfortable deciding');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('HEALTHCARE', 'What draws you to healthcare as a field?', 'The intellectual challenge of diagnosis and treatment', 'Making a measurable difference in health outcomes', 'Being there for people during vulnerable moments', 'Constantly learning as knowledge and cases evolve');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'You''re given a case file with two plausible but conflicting narratives.', 'I''d build a timeline and check every fact against evidence', 'I''d focus on whichever narrative most affects the outcome', 'I''d want to understand each party''s perspective deeply', 'I''d look for what additional evidence could resolve the conflict');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'What part of legal work do you think you''d find most engaging?', 'The precision of applying rules and precedent correctly', 'Winning outcomes that matter for your client', 'Helping someone navigate a genuinely difficult situation', 'The strategy and back-and-forth of building an argument');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'A client''s case is legally weak, but they insist on pursuing it.', 'I''d walk them through exactly why the law isn''t on their side', 'I''d assess if there''s still a practical path to a good outcome', 'I''d want to understand what''s driving their insistence', 'I''d explore less obvious legal angles before ruling it out');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'You have to read hundreds of pages of dense documents overnight.', 'I''d systematically extract and organize the key facts', 'I''d skim for whatever''s most likely to matter to the case', 'I''d keep in mind the real people this case affects while reading', 'I''d flag anything unusual to come back to, rather than reading linearly');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'Two interpretations of the same law are both defensible.', 'I''d examine the precise wording and precedent closely', 'I''d argue for whichever interpretation serves the client best', 'I''d consider which interpretation is fairer to those affected', 'I''d look at how courts have leaned in similar recent cases');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'A witness''s story doesn''t quite add up under questioning.', 'I''d methodically cross-check it against other evidence', 'I''d focus on whichever inconsistency matters most to the case', 'I''d consider whether memory or stress explains the gaps', 'I''d keep probing from different angles to see what shifts');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'What would you find most frustrating about legal work?', 'Arguments that ignore the actual facts or law', 'Cases dragging on with no real progress', 'The legal system feeling cold to the people caught in it', 'No room to think creatively about a case''s strategy');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'You uncover evidence that weakens your own client''s position.', 'I''d want to fully understand its implications before acting', 'I''d assess how much it actually changes the likely outcome', 'I''d think about how to handle this honestly with my client', 'I''d explore how the case strategy could adapt around it');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'A new law is ambiguous and hasn''t been tested in court yet.', 'I''d analyze its exact language and legislative intent', 'I''d advise clients based on the most likely interpretation', 'I''d think about who''s most affected by the ambiguity', 'I''d watch closely for early court rulings that clarify it');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'A community feels a law is being applied unfairly to them.', 'I''d examine the legal basis for how it''s being applied', 'I''d assess what a realistic legal challenge could achieve', 'I''d spend time understanding their actual experience', 'I''d explore multiple legal strategies before choosing one');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'You have very little time to prepare a strong argument.', 'I''d organize the strongest evidence in logical order', 'I''d focus only on the point most likely to decide the case', 'I''d think about who the argument needs to resonate with', 'I''d sketch a rough argument and refine it under pressure');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'What would make a legal case feel meaningful to you?', 'Reasoning through it with precision and rigor', 'Achieving a decisive, favorable outcome', 'Genuinely helping the person or people affected', 'The intellectual challenge of building a novel argument');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'A judge''s past rulings suggest they lean a certain way on your issue.', 'I''d study their written opinions closely for reasoning patterns', 'I''d adjust the argument strategy to fit that likely lean', 'I''d think about how to make the human stakes clear to them', 'I''d prepare a few different argument angles just in case');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'You disagree with a law you''re required to apply or argue for.', 'I''d separate my personal view from the legal reasoning required', 'I''d focus on doing the job effectively regardless', 'I''d feel the tension of that and think about it seriously', 'I''d look for legal ways to challenge or reform it later');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('LAW', 'What draws you to law as a field in the first place?', 'The rigor of reasoning through complex rules and facts', 'The high-stakes nature of real outcomes and decisions', 'The chance to advocate for people who need it', 'The strategic, argumentative nature of the work');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'A story you''re covering has two sides giving very different accounts.', 'I''d verify each claim against independent evidence', 'I''d focus on whichever detail most changes the story''s meaning', 'I''d want to understand both sides'' experience of events', 'I''d keep digging for a source that could clarify things further');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'What part of media/content work excites you most?', 'Getting the facts and structure of a story exactly right', 'Creating something that actually reaches and matters to people', 'Telling stories that genuinely move or connect with an audience', 'The creative process of finding a fresh angle');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'Your content isn''t performing as well as expected. Why?', 'I''d analyze the data on where people drop off or disengage', 'I''d focus on the one change most likely to fix performance', 'I''d think about whether it''s actually resonating emotionally', 'I''d test a few different versions or formats');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'You have to cover a story that''s emotionally difficult for those involved.', 'I''d stick closely to verified facts to avoid causing more harm', 'I''d focus on what the public genuinely needs to know', 'I''d handle the people involved with real care and sensitivity', 'I''d think carefully about the best way to tell it');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'A trend everyone''s covering suddenly gets significant backlash.', 'I''d want to understand exactly what triggered the backlash', 'I''d assess whether it''s worth continuing to cover', 'I''d think about who might be hurt by how it''s being portrayed', 'I''d explore a different angle nobody else has covered');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'What would frustrate you most in a media career?', 'Sloppy reporting or an inaccurate account gaining traction', 'Effort spent on content nobody actually engages with', 'Stories told without regard for the people in them', 'Being stuck making the same kind of content repeatedly');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'You have a tight deadline and an unverified but explosive claim.', 'I''d hold the story until it can be properly verified', 'I''d weigh being first against the risk of being wrong', 'I''d think about who could be harmed if it''s wrong', 'I''d look for a fast alternative way to substantiate it');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'Your audience reacts very differently than you expected to a piece.', 'I''d analyze exactly what part triggered the unexpected reaction', 'I''d assess if it''s worth addressing or just move on', 'I''d genuinely want to understand how people are feeling', 'I''d try a follow-up piece that explores the reaction itself');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'You''re asked to make a complex topic accessible to a broad audience.', 'I''d structure it logically, building up from the basics', 'I''d focus only on what the audience actually needs to know', 'I''d find relatable human stories to anchor the topic', 'I''d try a few creative formats and see what lands');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'A source asks to stay anonymous for a sensitive story.', 'I''d verify their claims independently regardless', 'I''d weigh how essential their information is to the story', 'I''d take their safety concerns seriously and respect them', 'I''d look for creative ways to substantiate the story without exposing them');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'Two competing outlets are racing to break the same story first.', 'I''d make sure my facts are airtight before anything else', 'I''d weigh speed against accuracy given the stakes', 'I''d think about what the audience actually needs, not just "first"', 'I''d look for a genuinely different angle instead of racing');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'What would make a piece of content feel meaningful to you?', 'Getting the facts and craft precisely right', 'Actually reaching and impacting a large audience', 'Genuinely connecting with or moving people', 'Trying something creatively different that worked');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'You realize a past piece you made contained an error.', 'I''d want to trace exactly how the error happened', 'I''d assess how much it matters and correct accordingly', 'I''d think about who might have been misled by it', 'I''d use it as a chance to improve your future process');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'A story could be told safely-but-dull, or riskier-but-compelling.', 'I''d want more facts before judging which risk is acceptable', 'I''d weigh the real cost/benefit of taking the riskier route', 'I''d think about the impact on people involved either way', 'I''d look for a creative way to make the safe version compelling');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('MEDIA', 'What draws you to media and storytelling as a field?', 'The craft of structuring information clearly and rigorously', 'The ability to reach and influence a real audience', 'Genuinely connecting with people through stories', 'The endless creative possibility of how to tell something');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A student consistently struggles despite seeming to try hard.', 'I''d try to diagnose exactly where their understanding breaks down', 'I''d focus my limited time on the highest-impact intervention', 'I''d want to understand what''s going on for them beyond academics', 'I''d try a few different teaching approaches with them');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'What part of teaching or education work appeals to you most?', 'Structuring information so it''s genuinely easy to understand', 'Seeing measurable improvement in student outcomes', 'Genuinely connecting with and mentoring students', 'Constantly adapting your approach to what works');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A lesson you planned carefully isn''t landing with the class.', 'I''d analyze exactly where the explanation is losing them', 'I''d adjust to cover the most essential point before time runs out', 'I''d check in with students about what''s confusing them', 'I''d try explaining it a completely different way on the spot');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'You have very limited time to cover an important topic well.', 'I''d focus on the core logical structure students need', 'I''d prioritize what''s most likely to be tested or applied', 'I''d make sure the students who are struggling most keep up', 'I''d try a quick, different format to cover more ground');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'Two students learn the same material at very different paces.', 'I''d want to understand exactly what''s different in how they process it', 'I''d focus attention where it makes the most overall difference', 'I''d think about what each of them individually needs', 'I''d try pairing different methods for each of them');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A curriculum you''re required to teach feels outdated or ineffective.', 'I''d analyze specifically what''s failing about it', 'I''d focus on making the most essential parts still land well', 'I''d think about how it affects students'' real learning experience', 'I''d experiment with supplementing it creatively where I can');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'What would you find most frustrating in an education role?', 'Teaching methods that ignore how learning actually works', 'Effort going into things that don''t improve outcomes', 'Students feeling unseen or unsupported', 'Being stuck teaching the same way with no room to adapt');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A student is clearly capable but disengaged and unmotivated.', 'I''d want to understand exactly what''s causing the disengagement', 'I''d focus on whatever re-engagement effort is most likely to work', 'I''d spend real time one-on-one understanding them as a person', 'I''d try several different ways to spark their interest');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'You design a lesson plan and it needs to work for a very mixed class.', 'I''d structure it with a clear logical progression for all levels', 'I''d focus on making sure most students get the essential point', 'I''d design it around making everyone feel included', 'I''d build in flexible activities that adapt as you go');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'Parents push back on how you''re teaching or grading their child.', 'I''d walk them through the reasoning behind my approach clearly', 'I''d focus the conversation on what actually helps the student improve', 'I''d want to understand their concerns and perspective fully', 'I''d be open to adjusting my approach based on the conversation');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A new teaching technology is being pushed but seems unproven.', 'I''d want evidence it actually improves learning outcomes', 'I''d weigh whether it''s worth the time to adopt', 'I''d think about how it changes the student experience', 'I''d be willing to try it in a small way to see what happens');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'What would make a teaching moment feel meaningful to you?', 'A concept finally clicking because of how clearly it was explained', 'Clear evidence that students actually learned and improved', 'A student feeling genuinely supported and understood', 'Finding a completely new way to reach a struggling student');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'You have to give a student difficult feedback on their work.', 'I''d explain precisely what didn''t meet the standard and why', 'I''d focus feedback on what will most improve their next attempt', 'I''d deliver it in a way that keeps them motivated, not discouraged', 'I''d frame it as one of several ways they could improve');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'A class discussion goes in an unexpected but interesting direction.', 'I''d want to bring it back to the structured learning objective', 'I''d allow it briefly if it still serves the lesson''s goal', 'I''d follow it if students are genuinely engaged and learning', 'I''d let it run and see where the curiosity leads');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('EDUCATION', 'What draws you to education as a field?', 'The satisfaction of explaining things clearly and well', 'Making a measurable difference in outcomes for students', 'Genuinely mentoring and connecting with young people', 'Constantly adapting and learning new ways to teach');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'You''re studying a social pattern that doesn''t fit existing theory.', 'I''d want to test it rigorously before drawing conclusions', 'I''d focus on whether it has any real-world policy relevance', 'I''d want to understand the lived experience behind the pattern', 'I''d explore it from a few different theoretical angles');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'What part of studying society or human behavior interests you most?', 'Understanding the underlying structures and mechanisms', 'Producing insight that can inform real decisions or policy', 'Understanding people''s lived experiences deeply', 'The open-ended nature of exploring how societies work');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'Two studies on the same social issue reach very different conclusions.', 'I''d compare their methodologies to see what caused the difference', 'I''d figure out which is more useful for real-world decisions', 'I''d consider how each portrays the people being studied', 'I''d look for what further research could resolve the disagreement');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'You''re doing fieldwork in a community very different from your own.', 'I''d prepare rigorously to observe and record accurately', 'I''d focus on gathering the most useful information efficiently', 'I''d spend real time building trust and understanding first', 'I''d stay open and let the community shape what you focus on');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'A policy is being proposed based on questionable data.', 'I''d want to scrutinize the data''s quality and methodology', 'I''d assess the practical risk of the policy being wrong', 'I''d think about who would be most affected if it''s flawed', 'I''d look for alternative data sources to check it against');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'What would you find most frustrating in social science work?', 'Conclusions drawn from weak or biased evidence', 'Research that never actually informs real decisions', 'Studying people without genuinely understanding their experience', 'Being locked into one narrow theoretical framework');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'A vulnerable community is skeptical of researchers studying them.', 'I''d want to design the study to be as rigorous and fair as possible', 'I''d focus on what would make the research genuinely useful to them', 'I''d spend real time earning trust before anything else', 'I''d be open to reshaping the research based on their input');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'You notice your own assumptions might be biasing your research.', 'I''d systematically check my methods for that specific bias', 'I''d assess how much it could be skewing the real conclusions', 'I''d reflect on how it might affect the people being studied', 'I''d seek outside perspectives to challenge my assumptions');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'A community is divided on how a shared resource should be managed.', 'I''d analyze the data on actual resource use and needs', 'I''d focus on the allocation that avoids the worst outcomes', 'I''d spend time understanding each group''s perspective', 'I''d explore a few different management models with them');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'Your research findings challenge a popular but flawed belief.', 'I''d want the evidence to be airtight before publishing', 'I''d think about how to present it so it actually changes minds', 'I''d think carefully about who holds that belief and why', 'I''d look for multiple ways to communicate the finding');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'You have limited resources to study a large-scale social issue.', 'I''d design the most rigorous small-scale study possible', 'I''d focus on whichever angle has the clearest practical use', 'I''d prioritize whichever affected group needs attention most', 'I''d run a few small exploratory studies before committing');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'What would make a piece of social research feel meaningful to you?', 'Rigorous, well-supported conclusions', 'Findings that actually inform real policy or decisions', 'Genuinely representing and honoring people''s experiences', 'Discovering something unexpected about how people or society work');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'A well-meaning policy has had unintended negative consequences.', 'I''d want data on exactly what went wrong and why', 'I''d focus on the most urgent fix given real constraints', 'I''d want to understand who''s been harmed and how', 'I''d explore alternative approaches that avoid the same pitfall');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'You''re asked to summarize nuanced research for policymakers.', 'I''d present the findings with careful, honest caveats', 'I''d focus on what''s most decision-relevant for them', 'I''d frame it around the real people the policy would affect', 'I''d offer a few different ways to interpret the findings');
INSERT INTO questions (domain, scenario, option_a, option_p, option_c, option_i)
VALUES ('SOCIAL SCIENCES', 'What draws you to studying people and society as a field?', 'The rigor of uncovering real patterns and mechanisms', 'The potential to inform decisions that actually help people', 'Genuine curiosity about people''s lives and experiences', 'The open-ended, evolving nature of understanding society');