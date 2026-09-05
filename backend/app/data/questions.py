from __future__ import annotations

from typing import Any
from uuid import uuid5, NAMESPACE_URL

STREAM_BASE = {
    "science": {"science": 4.0, "commerce": 1.5, "arts": 0.75},
    "commerce": {"science": 1.5, "commerce": 4.0, "arts": 0.9},
    "arts": {"science": 0.8, "commerce": 1.5, "arts": 4.0},
    "balanced": {"science": 2.2, "commerce": 2.2, "arts": 2.2},
}

INTEREST_STREAMS = {
    "Technology": {"science": 0.78, "commerce": 0.17, "arts": 0.05},
    "Business": {"science": 0.10, "commerce": 0.78, "arts": 0.12},
    "Design": {"science": 0.05, "commerce": 0.12, "arts": 0.83},
    "Finance": {"science": 0.06, "commerce": 0.88, "arts": 0.06},
    "Science": {"science": 0.90, "commerce": 0.05, "arts": 0.05},
    "Law": {"science": 0.10, "commerce": 0.18, "arts": 0.72},
    "Healthcare": {"science": 0.88, "commerce": 0.05, "arts": 0.07},
    "Media": {"science": 0.05, "commerce": 0.12, "arts": 0.83},
    "Psychology": {"science": 0.14, "commerce": 0.16, "arts": 0.70},
    "Entrepreneurship": {"science": 0.12, "commerce": 0.78, "arts": 0.10},
}

ARCHETYPES = [
    ("analysis", {"science": 6.0, "commerce": 0.8, "arts": 0.4}),
    ("decision", {"science": 0.8, "commerce": 6.0, "arts": 0.6}),
    ("people_creative", {"science": 0.4, "commerce": 0.8, "arts": 6.0}),
    ("balanced", {"science": 2.2, "commerce": 2.2, "arts": 2.2}),
]

TEMPLATES: dict[str, list[tuple[str, list[str]]]] = {
    "Technology": [
        ("A school app suddenly becomes slow for many students. What would you do first?", ["Look for a measurable bottleneck and isolate it", "Check which part affects the most users and prioritize it", "Ask students what feels frustrating and redesign the experience", "Compare the main symptoms before choosing a direction"]),
        ("You are given a messy set of student timetable data. What sounds most satisfying?", ["Find patterns and inconsistencies in the data", "Choose rules that make scheduling efficient", "Think about how students should see the timetable", "Break the problem into smaller manageable parts"]),
        ("A website feature is confusing students. How would you investigate?", ["Inspect where the interaction breaks down", "Compare the feature's impact with other priorities", "Observe what students expect the interface to do", "Gather a few perspectives before deciding"]),
        ("You need to explain a complex technical idea to a younger student. What approach feels natural?", ["Use a logical sequence of examples", "Connect it to a practical outcome", "Use a simple visual or analogy", "Ask what they already understand and build from there"]),
        ("Two solutions can fix the same technical problem. How do you choose?", ["Compare evidence, reliability and trade-offs", "Choose the option with the best value for the effort", "Consider which solution will feel clearer to users", "List the pros and cons before committing"]),
        ("A dataset contains several unusual values. What catches your attention first?", ["Whether the values follow a meaningful pattern", "Whether they could affect an important decision", "Whether they represent a real user or real-world case", "Whether more context is needed before interpreting them"]),
        ("A digital product has a feature that few people use. What would you investigate?", ["Usage patterns and possible technical friction", "Whether the feature creates enough value to keep", "Whether people understand the feature", "Different explanations for the low usage"]),
        ("You have one afternoon to improve an online form. What sounds most interesting?", ["Reduce logical errors and unnecessary steps", "Prioritize the changes with the biggest practical impact", "Make the form easier and more intuitive to use", "Test several small improvements and compare them"]),
        ("When a technical project fails, what response feels most useful?", ["Trace the cause systematically", "Decide what should be fixed first", "Talk through the experience of the people affected", "Review assumptions and try again"]),
        ("A teacher asks you to automate a repetitive task. What excites you most?", ["Design the logic that makes it repeatable", "Estimate the time saved and the best trade-off", "Make the result simple for teachers to use", "Map the steps before choosing a solution"]),
        ("You see two charts telling slightly different stories. What do you do?", ["Check the data and definitions behind each chart", "Ask which conclusion would matter more", "Think about how the chart could influence readers", "Look for missing context before judging either"]),
        ("A group project has too many possible technical ideas. How do you help?", ["Break the ideas into technical requirements", "Rank them by impact and effort", "Consider which idea people will actually enjoy using", "Create a simple comparison framework"]),
        ("You are learning a new digital tool. What keeps you engaged?", ["Understanding how its parts work", "Seeing how it can solve a useful problem", "Making something visible or interactive", "Trying a few approaches and refining them"]),
        ("A system gives unexpected results. What is your instinct?", ["Reproduce the issue and inspect the logic", "Check whether the result changes an important outcome", "Look at the experience around the result", "Collect more evidence before drawing a conclusion"]),
        ("At the end of a technology project, what would feel most rewarding?", ["Knowing the system works reliably", "Knowing it created measurable value", "Seeing people enjoy using it", "Knowing you learned how to improve the next version"]),
    ],
    "Business": [
        ("A school event has a limited budget. What would you do first?", ["Analyze likely costs and constraints", "Allocate money to the activities with the strongest return", "Think about what will make the event appealing to students", "Compare several possible plans before choosing"]),
        ("A small store's sales are falling. What interests you most?", ["Find patterns in sales data", "Identify the most important business decision to change", "Understand what customers are experiencing", "Gather evidence from several sources"]),
        ("You have to choose between two suppliers. How do you approach it?", ["Compare quality and performance data", "Compare price, reliability and value", "Consider how the supplier affects the customer experience", "Create a clear list of trade-offs"]),
        ("A product is popular with students but expensive to make. What would you explore?", ["Break down the cost drivers", "Test pricing and margin options", "Understand which parts customers value most", "Compare different ways to deliver the same value"]),
        ("Your team has three good business ideas. How do you narrow them down?", ["Examine the evidence behind each", "Rank market impact and feasibility", "Think about which idea solves a real person's problem", "Use a common framework to compare them"]),
        ("A customer gives an unexpected complaint. What is most useful?", ["Look for patterns in similar complaints", "Decide whether the complaint signals a business priority", "Understand the customer's experience in detail", "Check the complaint against other evidence"]),
        ("You are planning a school fundraiser. Which part sounds most interesting?", ["Estimate demand and constraints", "Choose the pricing and budget strategy", "Create an appealing experience for participants", "Coordinate the whole plan and improve it"]),
        ("A campaign gets lots of attention but few purchases. What would you investigate?", ["Analyze where people drop off", "Compare acquisition cost and conversion value", "Look at what message resonates with people", "Test several explanations before changing the campaign"]),
        ("Your team disagrees about a business decision. What helps most?", ["Bring the relevant facts", "Clarify the objective and trade-offs", "Understand each person's concerns", "Create options and compare them fairly"]),
        ("A new service could save time but costs more. What matters most?", ["Measure the time saved and the process change", "Compare cost against expected business value", "Consider how people would experience the service", "Evaluate benefits and risks together"]),
        ("You are asked to understand why customers leave. Where do you start?", ["Look for patterns in customer data", "Identify the point with the greatest business impact", "Listen to customers' experiences", "Combine evidence from multiple sources"]),
        ("A startup has very little money. What would you prioritize?", ["Understand the key numbers and constraints", "Spend on the action most likely to create value", "Focus on the customer problem", "Keep the plan flexible and test assumptions"]),
        ("A new product needs a launch plan. What feels most satisfying?", ["Map the information needed to make decisions", "Build the pricing, budget and priority plan", "Shape the message and audience experience", "Coordinate the pieces into one practical plan"]),
        ("A competitor changes its pricing. What do you do?", ["Analyze the market data", "Estimate the business consequences and options", "Consider how customers may perceive the change", "Compare several possible responses"]),
        ("What would make a business project feel successful to you?", ["A well-understood problem and evidence-based decision", "Clear value created for the organization", "Customers genuinely enjoying the outcome", "A plan that improved through testing and learning"]),
    ],
    "Design": [
        ("Students say a school website feels difficult to use. What would you do first?", ["Map where users get stuck", "Prioritize the problems with the largest practical impact", "Observe what users expect each screen to do", "Compare a few possible layouts"]),
        ("You are redesigning a poster for a school event. What matters most?", ["Organize information into a clear hierarchy", "Make the important information stand out", "Create a visual style that feels engaging", "Test different arrangements"]),
        ("An app has too many buttons on one screen. What sounds most interesting?", ["Understand the structure and reduce unnecessary steps", "Prioritize the actions that matter most", "Make the interface feel calmer and more intuitive", "Sketch multiple alternatives"]),
        ("A teacher asks you to improve a form. How do you approach it?", ["Break the form into logical sections", "Reduce effort on the most important tasks", "Make the wording and layout easier to understand", "Try different designs and compare them"]),
        ("A student cannot find an important setting. What would you investigate?", ["Trace the information structure", "Decide which settings should be most accessible", "Think about what the student expects to see", "Explore different navigation patterns"]),
        ("You are shown three logos for the same club. What catches your attention?", ["Whether the design has a coherent structure", "Whether it communicates the club's purpose", "Whether it has a distinct and memorable feel", "How different audiences might read it"]),
        ("A product gets good reviews but people still stop using it. What would you explore?", ["Where the experience breaks down", "Which part creates the biggest loss of value", "How the experience feels over time", "Several possible reasons for the drop-off"]),
        ("You have one hour to improve a mobile screen. What feels satisfying?", ["Simplifying the interaction logic", "Making the primary action obvious", "Improving visual clarity and feel", "Trying two or three versions quickly"]),
        ("A design choice divides your team. What helps you decide?", ["Use evidence from user behavior", "Compare impact and effort", "Consider which option better serves people's needs", "Test the options instead of arguing abstractly"]),
        ("You need to make a complex topic easier to understand. What is your instinct?", ["Organize it into a clear sequence", "Focus attention on the most important information", "Use visuals, examples or storytelling", "Create a few ways to present it and compare"]),
        ("A school noticeboard looks cluttered. What do you change first?", ["Group and structure the information", "Give priority to time-sensitive items", "Improve the visual hierarchy", "Create several layout options"]),
        ("What makes a design project rewarding to you?", ["A clear system behind the final result", "A useful outcome for the people using it", "A strong and memorable visual experience", "Learning through iteration"]),
        ("A user gives you vague feedback: 'It just feels wrong.' What do you do?", ["Turn the experience into specific points to inspect", "Identify which part could affect the main task", "Ask them to describe the feeling and context", "Observe the task and test alternatives"]),
        ("You have competing visual ideas. How do you choose?", ["Check consistency and structure", "Choose the design that best supports the goal", "Choose the one that communicates the intended feeling", "Prototype several versions"]),
        ("A successful design to you is one that...", ["Has a clear and coherent system", "Helps people achieve a useful goal", "Feels intuitive and engaging", "Improves because it was tested and refined"]),
    ],
    "Finance": [
        ("You have ₹5,000 to plan a school trip. What do you do first?", ["Break down the costs and constraints", "Allocate the money to maximize value", "Think about what will make the trip enjoyable", "Compare several budget plans"]),
        ("Two savings options offer different returns and risks. What interests you?", ["Understand the numbers and assumptions", "Compare return against risk and goals", "Consider what the choice means for the person's life", "List the trade-offs clearly"]),
        ("A family's monthly spending suddenly rises. What would you investigate?", ["Find which categories changed", "Identify the largest financial impact", "Understand what new need caused it", "Compare several explanations"]),
        ("A small business is profitable but short on cash. What sounds most interesting?", ["Track the movement of money", "Decide which financial priority matters most", "Understand how customers and suppliers affect the situation", "Map the different causes before acting"]),
        ("You are comparing two college options with different costs. How do you think?", ["Calculate the important cost and outcome variables", "Compare long-term value and affordability", "Consider which option fits the student's life", "Build a side-by-side comparison"]),
        ("An investment falls unexpectedly. What is your first instinct?", ["Look for the factors that changed", "Assess the risk and whether the decision still makes sense", "Consider the investor's situation and time horizon", "Gather more context before reacting"]),
        ("A budget is repeatedly exceeded. What would you explore?", ["Check the underlying spending pattern", "Find the biggest source of variance", "Understand why people spend differently from the plan", "Compare actual spending with several scenarios"]),
        ("You are helping organize a fundraiser. What role sounds most satisfying?", ["Track the numbers and reconcile them", "Choose pricing and allocation decisions", "Create an attractive experience that encourages participation", "Coordinate the full plan"]),
        ("A company wants to buy new equipment. What matters most?", ["Estimate the financial and operational effects", "Compare cost, return and risk", "Consider how it changes people's work", "Review multiple scenarios before deciding"]),
        ("A student wants to save for a laptop. What advice process feels useful?", ["Quantify income, costs and savings", "Choose a target and trade-offs", "Understand which features matter to the student", "Create and compare a few realistic plans"]),
        ("Two companies report similar profits but very different cash. What catches your eye?", ["The underlying financial movements", "The implications for business stability", "How operations might explain the difference", "The need for more context before concluding"]),
        ("A friend asks whether a purchase is affordable. How do you respond?", ["Look at the numbers", "Compare the purchase with goals and priorities", "Understand how important the item is to them", "Discuss the alternatives"]),
        ("A finance project feels successful when...", ["The numbers and assumptions are understood", "The decision creates good value", "The outcome supports the people involved", "The plan improves after reviewing evidence"]),
        ("A financial plan has one uncertain assumption. What do you do?", ["Test the assumption with data", "Estimate how much it could change the outcome", "Consider the real-life context behind it", "Build more than one scenario"]),
        ("You need to choose between two spending priorities. What feels natural?", ["Compare their measurable effects", "Rank them by value and urgency", "Think about who benefits and why", "Create a fair comparison"]),
    ],
    "Science": [
        ("A plant experiment produces an unexpected result. What do you do first?", ["Check the variables and evidence", "Consider which explanation best fits the result", "Think about how the finding affects the living system", "Repeat or compare the observation before concluding"]),
        ("You are given three possible explanations for a phenomenon. What interests you?", ["Test which explanation fits the evidence", "Compare how much each explanation accounts for", "Think about the wider context and consequences", "Look for additional information that could distinguish them"]),
        ("A school lab has inconsistent readings. What would you investigate?", ["Measurement methods and sources of error", "Which error would matter most to the conclusion", "How the experiment setup affects people and surroundings", "Different possible causes before repeating the test"]),
        ("You are studying a local ecosystem. What sounds most engaging?", ["Identify patterns and relationships in the data", "Understand which factor most affects the system", "Observe how organisms interact", "Compare several possible explanations"]),
        ("A health-related claim is shared online. What do you do?", ["Check the quality of the evidence", "Decide whether the evidence is strong enough for the claim", "Consider how the claim could affect people", "Look for multiple credible sources"]),
        ("Two experiments reach different conclusions. How do you respond?", ["Compare methods and variables", "Look for the result that is more robust", "Consider context and practical consequences", "Identify what needs to be repeated or clarified"]),
        ("A scientist has limited time to study a problem. What would you prioritize?", ["Collect the most informative evidence", "Focus on the variable most likely to matter", "Study the part of the system most affected", "Choose a manageable question and test it"]),
        ("You see a pattern in observations. What is your next instinct?", ["Form and test a hypothesis", "Estimate how useful the pattern is", "Ask what it means for the people or environment involved", "Check whether the pattern repeats"]),
        ("A practical science project feels rewarding when...", ["The evidence supports a clear explanation", "The work leads to a useful decision", "It helps understand or improve a real situation", "You learn by testing and revising ideas"]),
        ("A result contradicts your expectation. What is most useful?", ["Inspect assumptions and data", "Assess whether the unexpected result changes the decision", "Consider other explanations and contexts", "Stay open and gather more evidence"]),
        ("A team must choose which experiment to run. How do you help?", ["Compare what each experiment can reveal", "Prioritize the experiment with the most useful outcome", "Consider the real-world relevance", "Compare feasibility and uncertainty"]),
        ("You are reading a graph from an experiment. What catches your eye?", ["Patterns, outliers and relationships", "Which trend changes the conclusion", "What the pattern might mean in context", "Whether the graph supports the stated interpretation"]),
        ("A scientific problem is very broad. What do you do?", ["Break it into measurable questions", "Choose the question with the biggest impact", "Start with the part affecting living systems or people", "Define a small testable question"]),
        ("A good science decision should be based mainly on...", ["Reliable evidence and clear reasoning", "Evidence linked to the actual objective", "Evidence interpreted in human and environmental context", "Evidence that has been checked from multiple angles"]),
        ("What would keep you engaged in a science project?", ["Understanding how and why something works", "Solving a meaningful problem with evidence", "Exploring living systems and real-world effects", "Testing ideas and discovering something unexpected"]),
    ],
    "Law": [
        ("Two students give conflicting accounts of an incident. What do you do first?", ["Separate claims from verifiable facts", "Identify which issue matters most to the decision", "Understand how each person experienced the event", "List the evidence needed before deciding"]),
        ("A school rule is challenged as unfair. What interests you?", ["Examine the wording and underlying logic", "Consider the rule's purpose and consequences", "Understand who is affected and why", "Compare the rule with similar cases"]),
        ("You are given a set of documents about a dispute. Where do you start?", ["Organize the facts and sources", "Identify the issues that could change the outcome", "Consider the people and context behind the documents", "Build a timeline and compare the accounts"]),
        ("A friend wants to make a strong argument. What would you suggest?", ["Define the reasoning clearly", "Focus on the strongest point for the intended outcome", "Explain the argument in a way others can understand", "Consider the counterargument too"]),
        ("Someone makes a claim without evidence. How do you react?", ["Ask what evidence supports it", "Consider whether the claim affects an important decision", "Ask how the claim impacts the people involved", "Look for independent information"]),
        ("Two interpretations of a rule are possible. What do you examine?", ["The exact language and logic", "Which interpretation better serves the rule's purpose", "The practical effect on people", "How similar situations were treated"]),
        ("A team has limited time to prepare an argument. What comes first?", ["Organize the strongest evidence", "Prioritize the issue that could decide the case", "Understand the audience and affected people", "Create a clear argument structure"]),
        ("A witness remembers an event differently months later. What do you do?", ["Compare details with other evidence", "Assess which differences matter to the case", "Understand how memory and context could affect the account", "Avoid a conclusion until more evidence is checked"]),
        ("A legal research task feels rewarding when...", ["The facts and rules fit together logically", "You find the point that changes the outcome", "You help clarify a difficult situation for people", "You discover and compare competing interpretations"]),
        ("You discover evidence that weakens your preferred argument. What is your instinct?", ["Reassess the logic", "Decide how it changes the strength of the case", "Consider the interests of everyone affected", "Include it and revise the argument fairly"]),
        ("A community must choose between two policies. How would you help?", ["Compare the facts and assumptions", "Evaluate trade-offs and likely outcomes", "Consider different groups' experiences", "Compare evidence for both options"]),
        ("A long document contains important details. What feels natural?", ["Structure the information and identify key facts", "Find the points that could change the decision", "Notice the human context and consequences", "Cross-check details across sections"]),
        ("A good argument to you is one that...", ["Is logically supported", "Targets the most important issue", "Can be understood and considered by people", "Anticipates reasonable counterarguments"]),
        ("A dispute cannot be solved from the current evidence. What do you do?", ["Identify exactly what information is missing", "Seek the evidence most likely to resolve the issue", "Understand the perspectives involved", "Compare additional possible sources"]),
        ("What would keep you engaged in a law-related task?", ["Analyzing facts and rules", "Solving a difficult dispute", "Understanding people and social systems", "Building and testing arguments"]),
    ],
    "Healthcare": [
        ("A fictional patient has several symptoms. What would you do first?", ["Organize the symptoms and evidence", "Prioritize the issue that could be most important", "Consider the person's overall situation", "Gather more information before concluding"]),
        ("Two possible explanations fit a case. What interests you?", ["Compare evidence for each", "Focus on the explanation with the greatest practical consequence", "Consider the patient's context and experience", "Identify what additional information would distinguish them"]),
        ("A clinic has limited time for appointments. What should be prioritized?", ["Use clear criteria based on evidence", "Address the cases with the highest urgency", "Consider patient needs and circumstances", "Create a fair and transparent process"]),
        ("A health claim is shared on social media. How do you respond?", ["Check the evidence and study quality", "Assess the possible harm if people act on it", "Think about how it could affect different people", "Compare information from credible sources"]),
        ("A team sees different symptoms in the same case. What is useful?", ["Map the evidence systematically", "Identify which symptom could change the priority", "Understand the person's lived experience", "Combine information before deciding"]),
        ("A patient is confused about instructions. What matters most?", ["Make the steps logically clear", "Focus on the instructions that matter most", "Explain them in a way the patient understands", "Check understanding and revise if needed"]),
        ("A public health project needs a target group. How do you choose?", ["Use relevant data", "Focus on the group with the greatest measurable need", "Consider vulnerability and lived circumstances", "Compare evidence across groups"]),
        ("A treatment plan is not producing the expected outcome. What do you do?", ["Review the evidence and assumptions", "Assess whether the plan needs to change urgently", "Consider adherence, context and patient experience", "Gather more observations before changing direction"]),
        ("A healthcare project feels rewarding when...", ["The evidence leads to a clear understanding", "It improves an important outcome", "It helps people feel supported and understood", "It leads to better decisions after testing"]),
        ("A case contains incomplete information. What is your instinct?", ["Identify the most useful missing evidence", "Prioritize what could change the decision", "Ask about the person's context and concerns", "Gather multiple relevant sources"]),
        ("A hospital process creates long waiting times. What would you investigate?", ["Map where delays happen", "Identify the bottleneck with the largest impact", "Understand how the wait affects patients", "Compare several process changes"]),
        ("Two prevention programs have different costs and benefits. How do you compare them?", ["Examine the available data", "Compare impact against resources", "Consider which communities are best served", "Review assumptions and possible outcomes"]),
        ("A patient asks why a recommendation was made. What do you explain?", ["The reasoning and evidence", "The main benefit and trade-off", "How it connects to the person's situation", "What could change the recommendation"]),
        ("A good healthcare decision should combine...", ["Reliable evidence and clear reasoning", "Priority, benefit and risk", "Human context and communication", "Evidence, uncertainty and review"]),
        ("What would keep you engaged in a healthcare task?", ["Understanding causes and evidence", "Solving an important problem", "Helping people through complex situations", "Learning by observing, testing and revising"]),
    ],
    "Media": [
        ("You need to cover a school event. What do you plan first?", ["Collect the key facts and sequence", "Choose the angle most likely to matter to the audience", "Think about the story people will connect with", "Compare several ways to frame it"]),
        ("A post gets lots of views but little trust. What would you investigate?", ["Check the evidence and structure", "Look at what drives attention versus value", "Consider how the audience experiences the message", "Test different explanations for the trust gap"]),
        ("Two sources report different facts. What do you do?", ["Verify the evidence", "Decide which difference matters to the story", "Understand the context behind each source", "Cross-check both with another source"]),
        ("You have one minute to explain a complex issue. What matters?", ["Create a clear information sequence", "Lead with what the audience most needs", "Use a compelling example or narrative", "Compare a few possible ways to frame it"]),
        ("A video has good information but low completion. What interests you?", ["Analyze where viewers leave", "Identify the point where the story loses value", "Consider how the pacing and tone feel", "Test different explanations and edits"]),
        ("You are designing a school newsletter. What sounds most satisfying?", ["Organizing information clearly", "Prioritizing the most important updates", "Creating an engaging visual and editorial experience", "Trying different structures"]),
        ("A headline is catchy but slightly misleading. What do you do?", ["Check whether the wording accurately reflects the evidence", "Consider the effect on trust and audience goals", "Think about how readers might interpret it", "Find alternatives that are both accurate and engaging"]),
        ("A story involves several opinions. How would you handle it?", ["Separate claims from evidence", "Highlight the disagreement that matters most", "Present each perspective fairly and clearly", "Compare multiple possible structures"]),
        ("A media project feels successful when...", ["The information is accurate and well structured", "It creates meaningful audience impact", "People connect with and remember the story", "It improves through testing and feedback"]),
        ("A source asks to stay anonymous. What matters?", ["Assess credibility and supporting evidence", "Consider why the information matters", "Think about context and potential harm", "Seek corroboration before publishing"]),
        ("Your audience is very different from you. How do you plan?", ["Learn the relevant information about them", "Prioritize what will matter to them", "Understand their perspective and language", "Compare ways of presenting the same idea"]),
        ("An interview goes in an unexpected direction. What do you do?", ["Follow the useful evidence", "Focus on the most important new angle", "Explore the person's story and perspective", "Adapt while keeping the main purpose in mind"]),
        ("A good media explanation should be...", ["Clear and evidence-based", "Focused on what matters to the audience", "Engaging and human", "Open to context and nuance"]),
        ("A story contains one dramatic claim with weak evidence. What do you do?", ["Investigate the evidence first", "Decide whether it belongs in the final story", "Consider how repeating it could affect people", "Look for stronger sources or alternative framing"]),
        ("What keeps you engaged in media work?", ["Finding and organizing information", "Making decisions about audience impact", "Telling stories creatively", "Experimenting with different ways to communicate"]),
    ],
    "Psychology": [
        ("A student behaves differently in two settings. What would you explore?", ["Look for patterns in the observations", "Identify which factor could matter most", "Understand the student's experiences and context", "Compare several possible explanations"]),
        ("A survey gives an unexpected result. What do you do?", ["Check the data and method", "Assess whether the result changes the main conclusion", "Consider how participants may have understood the questions", "Look for other evidence before concluding"]),
        ("Two people react differently to the same situation. What interests you?", ["Identify differences in observable factors", "Consider which factor is most influential", "Explore their perspectives and experiences", "Look for multiple explanations"]),
        ("A friend says everyone in the class dislikes a teacher. How do you respond?", ["Ask what evidence supports the claim", "Consider how much it matters to decision-making", "Ask about different people's experiences", "Avoid generalizing without broader information"]),
        ("You are observing a group activity. What do you pay attention to?", ["Patterns in behavior and interaction", "Which behavior seems to influence outcomes", "How people respond to one another", "Changes across different situations"]),
        ("A study claims one habit causes better grades. What do you examine?", ["Method, data and alternative explanations", "Whether the effect is large enough to matter", "How students' circumstances differ", "Whether other studies support it"]),
        ("A student wants advice about a difficult decision. What is most useful?", ["Clarify the facts and patterns", "Identify the most important trade-offs", "Understand their feelings and perspective", "Explore several interpretations before advising"]),
        ("A group becomes unusually quiet during a discussion. What do you investigate?", ["Look for observable changes and patterns", "Consider what decision or event may have caused it", "Think about how people may be feeling", "Compare with how the group behaved before"]),
        ("A psychology project feels rewarding when...", ["You understand a behavior from evidence", "You identify a factor that matters", "You understand people more deeply", "You improve your explanation through observation"]),
        ("A survey question may influence the answer. What do you do?", ["Inspect the wording and design", "Consider how bias affects the result", "Think about how participants may interpret it", "Test or compare alternative wording"]),
        ("You see a repeated behavior pattern. What is your instinct?", ["Document and test the pattern", "Ask what outcome it may influence", "Explore what the behavior could mean to people", "Seek another context to see whether it repeats"]),
        ("Two explanations both seem plausible. How do you choose?", ["Compare them against evidence", "Prefer the one with stronger explanatory power", "Consider context and individual differences", "Keep both open until more evidence appears"]),
        ("A good psychological explanation should...", ["Fit the evidence", "Help explain meaningful outcomes", "Respect people's experiences and context", "Acknowledge uncertainty and alternatives"]),
        ("A new intervention seems helpful. What do you check?", ["Whether the observed change is supported by data", "Whether the improvement is meaningful", "How people experienced the intervention", "Whether the result repeats in other cases"]),
        ("What keeps you engaged in psychology?", ["Understanding patterns in behavior", "Solving real human problems", "Understanding people and experiences", "Testing ideas about why people behave as they do"]),
    ],
    "Entrepreneurship": [
        ("Students complain about a recurring problem at school. What do you do first?", ["Break down the problem and evidence", "Estimate whether solving it creates value", "Understand people's experiences in depth", "Compare several problem interpretations"]),
        ("You have a small budget to test an idea. What matters most?", ["Design a simple measurable test", "Spend where it is most likely to validate the idea", "Make the test easy and appealing for users", "Run a small experiment before committing"]),
        ("A new product gets mixed feedback. What do you investigate?", ["Look for patterns in the responses", "Identify the feedback that could change the business", "Understand why different people react differently", "Compare several hypotheses"]),
        ("Two startup ideas seem promising. How do you choose?", ["Compare evidence and assumptions", "Compare market value and feasibility", "Consider which problem people care about most", "Test the riskiest assumption"]),
        ("Your team is running out of time. What do you prioritize?", ["Focus on the steps that reduce uncertainty", "Do the work with the highest expected value", "Protect the core user experience", "Simplify the plan and keep learning"]),
        ("A customer describes a problem you had not expected. What is your instinct?", ["Investigate whether the pattern is real", "Assess whether it changes the opportunity", "Listen deeply to the customer's context", "Compare it with the original assumptions"]),
        ("A business idea needs a clear price. What sounds interesting?", ["Understand cost and demand data", "Test pricing against value and alternatives", "Consider how customers perceive the price", "Compare several pricing scenarios"]),
        ("A prototype does not work as expected. What do you do?", ["Find what part of the logic failed", "Decide what failure matters most", "Observe how users respond to it", "Change one assumption and test again"]),
        ("A startup project feels rewarding when...", ["You understand the problem clearly", "You create measurable value", "People genuinely want the solution", "You learn quickly through experiments"]),
        ("A team has too many features planned. How do you help?", ["Map dependencies and complexity", "Prioritize the features with the most value", "Focus on what users actually need", "Test the smallest useful version first"]),
        ("A competitor launches a similar product. What do you do?", ["Study the differences using evidence", "Evaluate the market impact and response options", "Understand how customers perceive both products", "Compare several strategic responses"]),
        ("You need to pitch an idea. What is most satisfying?", ["Build a clear logical case", "Show the value and opportunity", "Tell a story people can connect with", "Anticipate objections and improve the pitch"]),
        ("A new idea sounds exciting but has little evidence. How do you respond?", ["Identify what needs testing", "Estimate the downside before investing", "Ask potential users about the problem", "Run the cheapest useful experiment"]),
        ("A good entrepreneurial decision should combine...", ["Evidence and structured thinking", "Value, constraints and risk", "Customer understanding", "Fast learning and willingness to adapt"]),
        ("What keeps you engaged in entrepreneurship?", ["Understanding difficult problems", "Creating value from limited resources", "Talking to people and solving real needs", "Experimenting and learning quickly"]),
    ],
}


def build_questions() -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    for interest, templates in TEMPLATES.items():
        for index, (prompt, options) in enumerate(templates, start=1):
            archetype_offset = (index - 1) % 4
            option_payload = []
            # Rotate the four response archetypes across the visible option order.
            for j, text in enumerate(options):
                archetype_name, weights = ARCHETYPES[(j + archetype_offset) % 4]
                option_payload.append({"id": f"o{j+1}", "text": text, "scores": weights})
            qid = str(uuid5(NAMESPACE_URL, f"skillsensei:{interest}:{index}"))
            questions.append({
                "id": qid,
                "interest": interest,
                "dimension": ARCHETYPES[archetype_offset][0],
                "question": prompt,
                "options": option_payload,
                "active": True,
            })
    return questions


QUESTIONS = build_questions()
QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS}


def interest_profile(interests: list[str]) -> dict[str, float]:
    result = {"science": 0.0, "commerce": 0.0, "arts": 0.0}
    selected = [INTEREST_STREAMS[i] for i in interests if i in INTEREST_STREAMS]
    if not selected:
        return {k: 1/3 for k in result}
    for profile in selected:
        for stream, value in profile.items():
            result[stream] += value
    total = sum(result.values()) or 1.0
    return {k: v / total for k, v in result.items()}
