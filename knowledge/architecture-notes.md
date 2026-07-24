#### <assumptions>

* use the trainstorm-core architecture separating content from expression
* effective content-expression renders are intended to induce some delta in some audience using some set of tools/content and working within some set of constraints. It's always this: outcome, audience, tool (content, modalities, etc), and constraints. 

  * The "course generation" engine seeks to measure these deltas in a more traditional sense, such as KC and quiz. Expression render is largely fixed once at runtime. 
  * The "responsive engine" takes this to another level, measuring receiver deltas scene to scene and serving moves to drive objective completion. Expression render changes based on Bayesian movement.
* the process proceeds from high temperature to cool to deterministic, but there are loops involved. For instance: learning objectives are outcomes specifically scoped per constraints, audience, etc to meet business outcomes. So the right mode might be an early objective tracing, and deeper analysis of audience, tools, constraints, and a refinement.



#### </assumptions>



#### <general thoughts>



1. At certain check points, there is some "mind" (whether it be Ai, human, both, etc) that's deciding the NATURE of the expression based on the deltas: the business deltas, learning objectives, and all the Bayesian changes that are needed of the receiver to reliably produce the overall delta. The nature of the expression is one place that determines which agent is called. For instance, if the delta between status quo and status novus is especially large, or there are unique and potent emotional inhibitors in the audience, then the nature of expression might be persuasive and the "persuasive agent" gets called to run the "psykido prompts" to more deeply map audience globally, audience in context, inhibitors, motivators, objections, aligners, etc, etc. Whereas if the gap is more technically based, perhaps a different agent gets called with a different prompt string -- a tutor or clarity agent, something.

   1. This will likely also proceed in loops. For example: a certain level of audience analysis is needed to determine the nature of expression, and that decision drives a deeper layer of analysis. (No reason to go all the way and burn the tokens if it's not needed.) 
   2. I run into sequencing questions here. For example: what output is the "persuasive agent" producing and two which agent? I think the analysis of audience/outcome/tool is UPSTREAM of a script (actually, it probably has to be given the content vs expression model here), but I suspect there's another pass later that conforms the OBSERVATIONS of that analysis into actionable language. 

      1. &#x20;I need some help untangling this one, because it gets pretty complex and there are different ways it can go. For example, the agents are generally flowing from a business architecture agent to a designer agent to a developer agent in typical ADDIE fashion. But based on this discussion of expression "nature", (there will be others) there are very likely to be different sub-agents called. What are the outputs for each? 



2\. there are competing structures here that I've developed over time, but they all do tend to converge. There are some structures that focus on instructional design principles first, and there are some (like the manifold) that take the object/expression duality a little deeper. There are basically three current layers flowing like archeological dig. 

In Octoberish 2025, I was thinking about how to simply generate courses. This evolved into a prompt chain (not entirely successful, and not wired) that proceeds from beginning to end, takes an audience analysis detour, and tries to compile a ppt that can be imported into Storyline. This effort was sidelined 1 because only generated courses isn't ambitious enough and also because the primitives weren't there to generate ppt effectively.

The next layer was developed in Azure Studio, which essentially sets down "agents" (although they, too, are basically prompts) that work through ADDI with HITL -- the "Thinker" that works through business outcomes, project analysis, the Designer that starts to build learning objectives, the Developer who scripts, etc and the Generator who compiles the render contract. The "Thinker" piece is HIGHLY effective, but it loses coherence a bit moving through Designer to Generator. Still useful, but still incomplete. So in terms of organizing the total architecture, it's a question



3\. Possible agents: 

&#x09;Strategist: Maybe this is the Content Graph creator, and maybe it needs to broken out into modules or other agents. It usually receives a big messy corpus and does the highest order analysis of the project it can, hopefully culminating in business outcomes that will drive the rest of the loop. SO I think it outputs overall project analysis, business outcomes, affected audience, and other constraints. But I also think this is where we need to draw in some newer thinking from the Manifold. Is THIS where the corpus is reduced down to what's important to the business outcome? Or is that an agent that sits between Strategist and Designer? The strategist gives a thorough dossier on the project itself and surfaces all issues. From that (and perhaps with SME involvement) we can determine all the "units of meaning" to extract from the corpus -- this will form the bedrock of content for all future expressions. That content is then "stringfied" per the Manifold "atom-spec" and the object-model is created. So at some point here the object model is part of the output that gets passed in. What about the rest of the architecture? Where does that go? 

&#x09;Designer: probably needs to be dual-mode, as Design actually proceeds as part of a loop with Development - and using business architecture (Strategist) as a check - IRL with ADDIE) I believe the gate here is the learning objectives: think this agent receives the distilled business outcomes and high level thinking, compares against constraints, tools, audience, and produces Learning Objectives and perhaps suggested deliverables (in the case of a Course Engine ask, which is what we're largely discussing here.) Certainly this should be a conversation with the human prior to locking. 

&#x09;Developer: likely a series of tools, skills, sub-agents, whatever works best. 



#### </general thoughts>



#### <open questions>

#### 

#### 

#### 

#### <workflows>

<workflow 1>

The workflow begins, usually with the user accessing a large corpus of project files from sharepoint or other repo. This is largely unstructured data. 



Ingestion workflow starts. 

&#x09;Py files run first to extract all media, file formats, tables, etc, etc into parseable md. Next py runs to merge the entire corpus. 



User submits corpus to a high temperature, high thinking business analysis strategist who runs a complete analysis of the project, opportunities, threats, likely kpis, likely attack surface for training, roi analysis, political considerations, possible modalities. The analysis is talked through with a HITL and key decisions are made, at which point strategist creates the structured output for the first instructional design agent to take over. There may be additional sub-agents, tools, skills, scripts etc that run prior to the Strategist turning over to the Designer.



Designer (there might be more than one) First instructional designer is focused on the "analysis" and early "design" components of ADDIE. This is still relatively high temperature. 

</workflow 1>

