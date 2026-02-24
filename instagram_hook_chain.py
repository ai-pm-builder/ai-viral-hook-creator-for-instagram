"""
Instagram Food Reel Hook Generator - LangChain Implementation
A 4-prompt chain system for generating, testing, ranking, and finalizing viral hooks
for Indian female food content audience (24-34 years).

Requirements:
pip install langchain langchain-google-genai python-dotenv
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM (using Gemini 1.5 Pro)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_output_tokens=8000
)

# ============================================================================
# PROMPT 1: VIRAL FOOD REEL HOOK GENERATOR
# ============================================================================

prompt_1_template = """
## VIRAL FOOD REEL HOOK GENERATOR PROMPT

**Context:** You are creating hooks for an Instagram food account in 2026. The hook must accomplish its mission in 1.7 seconds (mobile scroll speed). The 2026 algorithm prioritizes: (1) 3-second hold rate above 60%, (2) watch time completion, and (3) shares/DMs.

**Your Food Content:** {recipe_description}

**Generate 5 unique hooks using these 2026-proven psychological patterns:**

### **Pattern 1: NEUROLOGICAL PATTERN INTERRUPT**
Break the expected scroll rhythm with a contradictory or shocking statement about food that triggers cognitive dissonance.
- Formula: "*[Common food belief]* is ruining your *[dish]* — here's what *[famous chef/culture]* does instead"
- Psychology: Forces brain from passive to active attention mode
- Example: "Garlic first is killing your pasta — Italians start with THIS"

### **Pattern 2: LOSS AVERSION AMPLIFICATION**
Name a specific mistake/waste people don't realize they're making (humans react 2.5x stronger to avoiding loss than gaining benefit).
- Formula: "You're wasting *[X ingredient]* if you don't know this *[timeframe]* trick"
- Psychology: Triggers immediate "what am I doing wrong?" response
- Example: "You've been throwing away the best part of chicken for years"

### **Pattern 3: CURIOSITY GAP WITH SENSORY ANCHOR**
Create information gap using unexpected ingredient combinations or technique reversals that feel "illegal" to know.
- Formula: "The *[secret ingredient]* that makes restaurant *[dish]* addictive (they don't want you to know)"
- Psychology: Activates dopamine reward pathway (information gap theory)
- Example: "Why MSG makes everything taste better (the science restaurants hide)"

### **Pattern 4: TIME-COLLAPSE TRANSFORMATION**
Show dramatic before/after or promise quick transformation that defies expectations.
- Formula: "*[Impressive timeframe]* to *[desired outcome]* — no *[common requirement]*"
- Psychology: Immediate value + pattern break (defies cooking time expectations)
- Example: "5-minute brownies — no oven, no mixer, just a mug"

### **Pattern 5: IDENTITY-TARGETED VULNERABILITY**
Speak directly to a specific eater identity or emotional food moment with hyper-specific relatability.
- Formula: "If you've ever *[specific embarrassing/relatable food moment]*, this is for you"
- Psychology: Creates "this was made for ME" parasocial connection
- Example: "If you've ever eaten cereal for dinner and called it a meal, watch this"

### **Pattern 6: SOCIAL PROOF SCARCITY**
Leverage FOMO by referencing what "nobody" knows or what's "trending everywhere but here."
- Formula: "*[Large number]* people are switching to *[technique]* — here's why"
- Psychology: Fear of missing cultural moment + bandwagon effect
- Example: "Why 4 million Indians stopped using non-stick pans this year"

**CRITICAL 2026 OPTIMIZATION RULES:**
1. **Visual First:** Text overlay must communicate hook even on MUTE (85% watch muted)
2. **First Frame Urgency:** Place hook text in center-top zone (avoid bottom 20%, top 10% UI overlap)
3. **Motion Trigger:** Pair text with immediate visual action (sizzle, pour, cut, flip) in first 0.5 seconds
4. **No Generic Openers:** NEVER start with "Today I'm making..." or "Hey guys..." (instant scroll)
5. **Bold Font Required:** 28-36pt, high contrast (white on dark, yellow on black)

Now generate 5 hooks for the recipe provided, ensuring each follows a different psychological pattern and is mobile-optimized for pattern interrupt.

FORMAT YOUR OUTPUT EXACTLY AS:
HOOK 1: [full hook text]
HOOK 2: [full hook text]
HOOK 3: [full hook text]
HOOK 4: [full hook text]
HOOK 5: [full hook text]
"""

prompt_1 = PromptTemplate(
    input_variables=["recipe_description"],
    template=prompt_1_template
)


# ============================================================================
# PROMPT 2: PRIYA PERSONA SIMULATION
# ============================================================================

prompt_2_template = """
## PROMPT 2 — PRIYA PERSONA SIMULATION
### *Full Immersive Reaction Test (No Scoring Yet)*

### **YOUR ROLE & MINDSET**

You are not an AI assistant right now. You are a **method actor** who has completely inhabited the life, habits, emotions, and scroll behaviour of a specific Indian woman named Priya. You do not evaluate hooks as a strategist. You *experience* them as Priya — in real time, mid-scroll, with no patience and no obligation to be kind.

### **STEP 1 — INHABIT PRIYA COMPLETELY**

**WHO SHE IS**

Priya is 28 years old. She lives in Pune, in a 2BHK she shares with her husband of two years. She works as a marketing executive at a mid-size company — her day is full of meetings, deadlines, and a commute that eats 45 minutes each way. She genuinely loves cooking but rarely has the time she wishes she did. Weekday dinners are quick. Weekends are when she experiments.

She has a younger sister in Bangalore and a mother in Nagpur who she calls every 2–3 days. Food is how she stays connected to both of them — she frequently screenshots or WhatsApps recipes with messages like "try karte hain" or "Maa try kar yeh."

**HER EXACT SCROLL CONTEXT**

It is 9:47 PM on a Tuesday. She is lying on the couch. Her husband is watching cricket on the TV in the background. She has already scrolled past 11 reels in the last 4 minutes. She is tired but not sleepy. Her thumb is moving fast. She is not looking for anything specific — but she will know it when she sees it.

Her phone is on **silent**. Brightness is at 60%. She is watching everything on mute unless something makes her reach for the volume.

**HER EMOTIONAL STATE**

She cooked rajma chawal for dinner tonight. It turned out decent but not as good as her mother's. She's been thinking about what she did differently. There's a mild undercurrent of "I wish I knew more kitchen tricks." She's not frustrated — just quietly curious and a little nostalgic.

**WHAT MAKES HER THUMB STOP — AND WHAT MAKES IT KEEP GOING**

She stops for:
- A visual that is immediately, undeniably food (steam rising, cheese pull, tadka hitting oil)
- Text that feels like it was written specifically for someone like her
- A statement that contradicts something she thought she knew
- Anything that mentions a specific Indian dish, ingredient, or technique she grew up with
- A hook that creates a tiny, uncomfortable feeling of "wait, have I been doing this wrong?"
- Hinglish phrasing that sounds like how her friends actually talk

She keeps scrolling past:
- "Hey guys, today I'm making…" — gone in 0.4 seconds
- Anything that starts with a creator talking to camera before showing food
- Western techniques dressed up with an Indian ingredient — feels patronising
- Overly aesthetic, slow-motion, no-information hooks
- Hooks that feel like they're trying too hard to be viral

She shares when:
- The content makes her look like the person who "knows things" in her group
- It directly solves something her mom, sister, or husband would find useful
- It validates a belief she already held
- It teaches her something she can apply THIS week

### **STEP 2 — THE HOOKS TO TEST**

{generated_hooks}

### **STEP 3 — RUN THE SIMULATION**

For **each hook**, provide:

**A) THE SPLIT-SECOND PHYSICAL REACTION**
Describe what happens in her body in the first 0.5 seconds. Does her thumb slow down? Does it stop? Write it in present tense, one sentence.

**B) THE INTERNAL MONOLOGUE**
Write 5–8 lines of her actual inner voice as she reads/watches this hook. This is unfiltered. It mixes Hindi and English naturally. It ends with a clear decision: **watch on** or **scroll past**.

**C) THE EMOTIONAL TRIGGER UNLOCKED**
Name the single primary emotion this hook activated:
- Nostalgia
- Productive Guilt
- Aspirational Pride
- Cultural Validation
- Urgency FOMO
- Trusted Curiosity
- No trigger

After naming it, write one sentence explaining exactly which element fired it.

**D) THE SHARE REFLEX TEST**
- Who is the first person she thought of? (Mother? Sister? Husband? Nobody?)
- Did she think of sending it before the hook even finished?
- What would her WhatsApp message say? Write the actual text in Hinglish.

If no share impulse: state plainly "No one came to mind."

**E) THE HONEST VERDICT**
Choose one:
🔴 **HARD SCROLL** — Gone in under 1 second
🟠 **SOFT SCROLL** — Paused 1–2 seconds, moved on
🟡 **WATCH & EXIT** — Watched but took no action
🟢 **WATCH & SAVE** — Watched and saved it
💚 **WATCH, SAVE & SHARE** — Full watch, saved, and sent to someone

Then write one brutal sentence explaining why.

### **STEP 4 — CROSS-HOOK PATTERN OBSERVATION**

After all 5 simulations, write a short paragraph answering:
- Which emotional trigger showed up most powerfully?
- Was there a common element in hooks that stopped her versus ones that lost her?
- What does Priya's pattern reveal about what this account should always/never do?

**FORMAT YOUR OUTPUT WITH CLEAR SECTION HEADERS FOR EACH HOOK**
"""

prompt_2 = PromptTemplate(
    input_variables=["generated_hooks"],
    template=prompt_2_template
)


# ============================================================================
# PROMPT 3: EVIDENCE-BASED SCORING & RANKING ENGINE
# ============================================================================

prompt_3_template = """
## PROMPT 3 — EVIDENCE-BASED SCORING & RANKING ENGINE
### *From Priya's Reactions to Strategic Truth*

### **YOUR ROLE — THE TRANSITION**

You are now a **senior content strategist** who specialises in the Indian Instagram food market. You have just watched a live user research session where Priya reacted in real time to 5 hooks. Your job is to extract what actually happened and build a ranking based exclusively on observed evidence.

### **STEP 1 — THE CARDINAL RULE**

**Every score you give must be preceded by its evidence citation.**

For every metric, for every hook, you will first quote the specific moment from Priya's simulation that justifies that score — and only then assign the number.

### **STEP 2 — UNDERSTAND THE THREE METRICS**

#### **METRIC 1: 3-SECOND HOLD RATE** (scored out of 10, weighted ×1.2 = /12)
The probability that this hook stops Priya's thumb *before* she has consciously processed its full meaning.

Evidence sources:
- Section A: Physical Reaction
- First 1-2 lines of internal monologue

Score guide:
- 1–3: Thumb didn't slow, dismissed in under 1 second
- 4–5: Thumb slowed but didn't stop
- 6–7: Thumb stopped, pause before comprehension
- 8–9: Thumb stopped immediately, micro-jolt
- 10: Full freeze, involuntary pause

#### **METRIC 2: WATCH TIME POTENTIAL** (scored out of 10, weighted ×1.0 = /10)
The probability she will stay through the entire reel.

Evidence sources:
- Honest verdict from Section E
- Emotional trigger from Section C
- Tail end of internal monologue

Score guide:
- 1–3: Hard or Soft Scroll, made no promise
- 4–5: Mild curiosity, Watch & Exit territory
- 6–7: Clear promise, 70-85% watch likely
- 8–9: Strong contract, watches to end
- 10: Uncomfortable open loop, must finish

#### **METRIC 3: SHARE PROBABILITY** (scored out of 10, weighted ×1.5 = /15)
The likelihood she will DM this to another person within 24 hours.

Evidence sources:
- Section D: Share Reflex Test
- Was a person named? WhatsApp message formed?

Score guide:
- 1–3: No person came to mind
- 4–5: Vague "someone might like this"
- 6–7: Specific person, message partially formed
- 8–9: Person named before hook finished, full message
- 10: Multiple people, urgency to share immediately

### **STEP 3 — LOAD THE EVIDENCE**

Here is Priya's complete simulation output from Prompt 2:

{priya_simulation}

### **STEP 4 — SCORE EACH HOOK**

For each hook, follow this structure:

**HOOK [NUMBER]: "[First 5 words]"**

**EVIDENCE REVIEW**
3-4 sentences summarizing critical evidence: physical reaction, decisive monologue moment, trigger, verdict.

**SCORE: 3-SECOND HOLD RATE**
Evidence used: [Quote specific physical reaction and first monologue line]
Score: [X/10]
Weighted: [X/12]
Justification: [One sentence]

**SCORE: WATCH TIME POTENTIAL**
Evidence used: [Quote verdict and monologue tail]
Score: [X/10]
Weighted: [X/10]
Justification: [One sentence]

**SCORE: SHARE PROBABILITY**
Evidence used: [State share reflex result]
Score: [X/10]
Weighted: [X/15]
Justification: [One sentence]

**WEIGHTED TOTAL: [X/37]**

**ONE-LINE STRATEGIC VERDICT**
The single most important truth this hook's scores reveal.

### **STEP 5 — THE RANKING TABLE**

| Rank | Hook # | First 5 Words | Hold (/12) | Watch (/10) | Share (/15) | Total (/37) | Primary Trigger | Verdict |
|---|---|---|---|---|---|---|---|---|

### **STEP 6 — THE WINNER DECLARATION**

State the #1 ranked hook and answer:

**Why this hook won:**
What specific combination of evidence made this score highest? Reference Priya's actual words.

**What it did that the others didn't:**
The single structural or psychological element the other four lacked or executed more weakly.

**Its biggest remaining weakness:**
Name the real risk honestly.

**The one change that would make it a 37/37:**
Specific enough to implement in 60 seconds.

### **STEP 7 — CONTENT CALENDAR CLASSIFICATION**

🟢 **POST NOW** (28+/37, Priya's verdict was Watch & Save or better)
🟡 **REFINE & TEST** (18-27/37, needs one specific fix)
🔴 **SHELVE** (below 18/37 or Hard/Soft Scroll)

### **STEP 8 — THE STRATEGIC DEBRIEF**

Write 4 paragraphs:

**Paragraph 1 — The Pattern**
Which emotional trigger produced highest scores consistently? What does this tell you about what Priya is hungry for?

**Paragraph 2 — The Graveyard**
What did the lowest-scoring hooks have in common?

**Paragraph 3 — The Replication Rule**
Write one reusable formula based on the winning hook's structure.

**Paragraph 4 — The One Thing**
If the creator implements only one thing in their next 5 reels — what is it? One sentence.

END with only the Paragraph 4 one-line instruction.
"""

prompt_3 = PromptTemplate(
    input_variables=["priya_simulation"],
    template=prompt_3_template
)


# ============================================================================
# PROMPT 4: THE WINNING HOOK FINALISER
# ============================================================================

prompt_4_template = """
## PROMPT 4 — THE WINNING HOOK FINALISER
### *From Ranked Winner to Ready-to-Shoot*

### **YOUR ROLE — THE LAST PERSON IN THE ROOM**

You are a **hook surgeon**. You have one task: take the winning hook and produce the final, production-ready, optimised version across every format the creator needs to walk into a shoot and execute it with zero guesswork.

### **STEP 1 — LOAD THE WINNER WITH FULL CONTEXT**

Here is the complete Prompt 3 output including the winning hook, its scores, and strategic analysis:

{winner_analysis}

Before touching the hook, write out:
1. The hook's exact text as generated
2. The one weakness named in the Winner Declaration
3. Priya's decisive monologue moment

### **STEP 2 — THE SINGLE SURGICAL FIX**

Apply the one change identified to close the gap to 37/37.

**BEFORE (original hook):**
[Hook as generated]

**THE FIX APPLIED:**
[Name the change and which metric it improves]

**AFTER (surgically improved hook):**
[The hook with only that change]

### **STEP 3 — THE FIVE FINAL FORMATS**

**FORMAT 1 — THE TEXT OVERLAY**
*(On screen. For mute viewers.)*

**Text:** [8 words max]
**Bold word:** [Single word]
**Colour:** [Exact treatment]
**Placement:** [Where and why]
**Font weight:** [Heavy/Black, caps or sentence case]

---

**FORMAT 2 — THE SPOKEN HOOK**
*(Voiceover. 1.7 seconds.)*

**Spoken words:** [12 words max, exact Hinglish balance]
**Emphasis word:** [Where voice drops/slows]
**Tone note:** [3-5 words describing delivery]
**Hinglish balance:** [% Hindi vs English, which carries emotion]
**The pause:** [Where, if any, and why]

---

**FORMAT 3 — THE FIRST FRAME VISUAL BRIEF**
*(What camera shows in first 0.5-1 second)*

**What the camera shows:** [Specific visual description]
**Motion element:** [What's moving, which direction]
**Lighting:** [Quality and time-of-day feeling]
**Composition:** [Rule of thirds, text overlay room]
**Emotional tone:** [Single feeling before words are read]
**What NOT to show:** [Avoid these elements]

---

**FORMAT 4 — THE CAPTION OPENER**
*(First line visible before "more" is tapped)*

**Caption opener:** [125 characters max]
**The hook it ends on:** [Question or incomplete thought mechanism]
**What it adds:** [New layer the reel didn't say]

---

**FORMAT 5 — THE THUMBNAIL FRAME**
*(Cover image for grid view)*

**The frame:** [Which moment, angle, food state]
**Thumbnail text:** [4 words max]
**Colour temperature:** [Warm or cool, why]
**Why a stranger stops:** [The visual/text element creating curiosity]

---

### **STEP 4 — THE SHOOT BRIEF**

**HOOK:** [Final text overlay]

**SPOKEN OPENING:** [Exact words, emphasis, tone]

**CAMERA SETUP:**
- Shot type: [Close-up/overhead/angle]
- Distance: [Specific measurement]
- Stabilisation: [Tripod/handheld/propped]

**FIRST 3 SECONDS — SHOT BY SHOT:**
- Second 0–0.5: [Before text appears]
- Second 0.5–1.5: [Text appears, food action]
- Second 1.5–3: [Visual development]

**LIGHTING:**
- Source: [Window/ring light/overhead, position]
- Quality: [Hard/soft]
- Feel: [Emotional tone]

**SOUND:**
- Natural sound to capture: [Specific sound, timing]
- When it occurs: [Point in 3 seconds]
- Emotion it triggers: [Before text is processed]

**TEXT OVERLAY TIMING:**
- Appears at: [Frame timing]
- Duration: [How long on screen]
- Animation: [Cut-in/reveal/static]

**THE ONE THING THAT WILL KILL THIS HOOK:**
[Most common mistake that would reduce performance]

---

### **STEP 5 — THE FINAL QUALITY CHECK**

Answer each with YES or NO:

1. Can a mute viewer understand the complete emotional premise within 1.5 seconds from text alone? **YES / NO**
2. Does the spoken hook sound like something a real person would say to a friend? **YES / NO**
3. Does the first frame create a physical reaction before text is processed? **YES / NO**
4. Does it activate Nostalgia, Productive Guilt, or Aspirational Pride? **YES / NO**
5. If Priya watched only 3 seconds, would she feel it's worth sending to someone? **YES / NO**

If all YES: ready to shoot.
If any NO: return to that format, fix once, re-check.

---

### **FINAL OUTPUT — THE ONE CARD**

**🎬 YOUR WINNING HOOK — PRODUCTION CARD**

**HOOK TEXT (on screen):**
[8 words. Bold word in CAPS.]

**SAY:**
[12 words. Emphasis word in CAPS. Language noted.]

**SHOW:**
[One sentence. Exact visual and motion.]

**THUMBNAIL TEXT:**
[4 words.]

**CAPTION OPENER:**
[125 characters.]

**THE ONE THING TO NOT FORGET ON SHOOT DAY:**
[One sentence.]

**PRIYA WILL SHARE THIS BECAUSE:**
[One sentence. Social utility, who she sends it to, why.]

---

This is your production card. Screenshot it and take it to your shoot.
"""

prompt_4 = PromptTemplate(
    input_variables=["winner_analysis"],
    template=prompt_4_template
)

# ============================================================================
# MODERN CHAIN CREATION (LCEL - LangChain Expression Language)
# ============================================================================

# Define individual chains using LCEL
chain_1 = prompt_1 | llm | StrOutputParser()
chain_2 = prompt_2 | llm | StrOutputParser()
chain_3 = prompt_3 | llm | StrOutputParser()
chain_4 = prompt_4 | llm | StrOutputParser()

# Define the full workflow as a series of steps
def run_workflow(recipe_description: str) -> Dict[str, str]:
    # Step 1: Generate Hooks
    generated_hooks = chain_1.invoke({"recipe_description": recipe_description})
    
    # Step 2: Priya Simulation
    priya_simulation = chain_2.invoke({"generated_hooks": generated_hooks})
    
    # Step 3: Winner Analysis
    winner_analysis = chain_3.invoke({"priya_simulation": priya_simulation})
    
    # Step 4: Production Card
    production_card = chain_4.invoke({"winner_analysis": winner_analysis})
    
    return {
        "generated_hooks": generated_hooks,
        "priya_simulation": priya_simulation,
        "winner_analysis": winner_analysis,
        "production_card": production_card
    }


# ============================================================================
# EXECUTION FUNCTIONS
# ============================================================================

def run_full_chain(recipe_description: str) -> Dict[str, Any]:
    """
    Run the complete 4-prompt chain from recipe to production card.
    
    Args:
        recipe_description: Description of the recipe/food content
        
    Returns:
        Dictionary containing all outputs from each stage
    """
    print("🚀 Starting Instagram Hook Generation Chain...")
    print("=" * 80)
    
    result = run_workflow(recipe_description)
    
    print("\n" + "=" * 80)
    print("✅ Chain Complete!")
    print("=" * 80)
    
    return result


def run_individual_prompts(recipe_description: str) -> Dict[str, Any]:
    """
    Run prompts individually with pauses between each for review.
    Useful for debugging or when you want to see each stage.
    
    Args:
        recipe_description: Description of the recipe/food content
        
    Returns:
        Dictionary containing all outputs
    """
    results = {}
    
    # Prompt 1: Generate Hooks
    print("\n" + "=" * 80)
    print("PROMPT 1: HOOK GENERATION")
    print("=" * 80)
    generated_hooks = chain_1.invoke({"recipe_description": recipe_description})
    results["generated_hooks"] = generated_hooks
    print(f"\n{generated_hooks}")
    print("\n✅ Hooks generated")
    print("\nPress Enter to continue to Prompt 2 (Priya Simulation)...")
    input()
    
    # Prompt 2: Priya Simulation
    print("\n" + "=" * 80)
    print("PROMPT 2: PRIYA PERSONA SIMULATION")
    print("=" * 80)
    priya_simulation = chain_2.invoke({"generated_hooks": results["generated_hooks"]})
    results["priya_simulation"] = priya_simulation
    print(f"\n{priya_simulation}")
    print("\n✅ Priya's reactions simulated")
    print("\nPress Enter to continue to Prompt 3 (Scoring & Ranking)...")
    input()
    
    # Prompt 3: Scoring & Ranking
    print("\n" + "=" * 80)
    print("PROMPT 3: EVIDENCE-BASED SCORING")
    print("=" * 80)
    winner_analysis = chain_3.invoke({"priya_simulation": results["priya_simulation"]})
    results["winner_analysis"] = winner_analysis
    print(f"\n{winner_analysis}")
    print("\n✅ Hooks scored and ranked")
    print("\nPress Enter to continue to Prompt 4 (Production Card)...")
    input()
    
    # Prompt 4: Production Card
    print("\n" + "=" * 80)
    print("PROMPT 4: PRODUCTION CARD GENERATION")
    print("=" * 80)
    production_card = chain_4.invoke({"winner_analysis": results["winner_analysis"]})
    results["production_card"] = production_card
    print(f"\n{production_card}")
    print("\n✅ Production card ready!")
    
    return results


def save_results_to_file(results: Dict[str, Any], filename: str = "hook_results.txt"):
    """
    Save all results to a text file for easy reference.
    
    Args:
        results: Dictionary containing all chain outputs
        filename: Name of file to save to
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("INSTAGRAM HOOK GENERATION RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("STAGE 1: GENERATED HOOKS\n")
        f.write("-" * 80 + "\n")
        f.write(results["generated_hooks"] + "\n\n")
        
        f.write("STAGE 2: PRIYA SIMULATION\n")
        f.write("-" * 80 + "\n")
        f.write(results["priya_simulation"] + "\n\n")
        
        f.write("STAGE 3: WINNER ANALYSIS\n")
        f.write("-" * 80 + "\n")
        f.write(results["winner_analysis"] + "\n\n")
        
        f.write("STAGE 4: PRODUCTION CARD\n")
        f.write("-" * 80 + "\n")
        f.write(results["production_card"] + "\n\n")
    
    print(f"\n📄 Results saved to {filename}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

