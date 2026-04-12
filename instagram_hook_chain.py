"""
Instagram Food Reel Hook Generator - LangGraph Implementation
A multi-agent architecture to generate, test via personas, and manage viral hooks.
"""

from typing import Dict, Any, List, TypedDict, Literal
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_output_tokens=8000
)

def load_prompt(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Graph State
class GraphState(TypedDict):
    recipe_description: str
    current_hook: str
    manager_message: str
    iterations: int
    verifier_feedback: List[str]
    is_approved: bool
    final_output: str
    programmatic_checks_passed: bool
    programmatic_feedback: str
    history: List[Dict[str, Any]]

def manual_checks(hook: str) -> tuple[bool, str]:
    """Programmatic rules validator for the generated hook."""
    words = hook.strip().split()
    if len(words) > 10:
        return False, f"Hook is too long ({len(words)} words). Must be strictly under 10 words."
    
    filler_phrases = ["hi i'm", "hey guys", "today we're", "let's make", "today i'm", "welcome back"]
    lower_hook = hook.lower()
    for phrase in filler_phrases:
        if phrase in lower_hook:
            return False, f"Hook contains forbidden filler phrase: '{phrase}'"
            
    return True, "Passed programmatic checks (length <= 10, no filler words)."

def generate_hook_node(state: GraphState) -> GraphState:
    print(f"Agent: Generator - Creating Hook (Iteration {state.get('iterations', 0) + 1})...")
    prompt_str = load_prompt("generator_agent.md")
    
    context = ""
    # Incorporate feedback if this is not the first iteration
    if state.get("iterations", 0) > 0:
        manager_msg = state.get('manager_message', '')
        prog_fdbk = state.get('programmatic_feedback', '')
        context = f"\n\n**PREVIOUS MANAGER REJECTION FEEDBACK:**\n{manager_msg}\n"
        if prog_fdbk:
            context += f"**PROGRAMMATIC FEEDBACK OVERRIDE:** {prog_fdbk}\n"
            
    prompt = PromptTemplate.from_template(prompt_str + "\n\nRecipe: {recipe_description}" + context)
    chain = prompt | llm
    
    new_hook = chain.invoke({"recipe_description": state["recipe_description"]})
    return {"current_hook": new_hook.content.strip(), "iterations": state.get("iterations", 0) + 1}

def verify_personas_node(state: GraphState) -> GraphState:
    print("Agent: Verifier Personas - Simulating Reactions...")
    
    # Run 22yo
    p22 = PromptTemplate.from_template(load_prompt("verifier_persona_22yo.md") + "\n\nRecipe: {recipe_description}\nHook: {hook}")
    ans22 = (p22 | llm).invoke({"recipe_description": state["recipe_description"], "hook": state["current_hook"]})
    
    # Run 28yo
    p28 = PromptTemplate.from_template(load_prompt("verifier_persona_28yo.md") + "\n\nRecipe: {recipe_description}\nHook: {hook}")
    ans28 = (p28 | llm).invoke({"recipe_description": state["recipe_description"], "hook": state["current_hook"]})
    
    # Run 34yo
    p34 = PromptTemplate.from_template(load_prompt("verifier_persona_34yo.md") + "\n\nRecipe: {recipe_description}\nHook: {hook}")
    ans34 = (p34 | llm).invoke({"recipe_description": state["recipe_description"], "hook": state["current_hook"]})
    
    feedbacks = [
        f"**22yo Persona (Neha):** {ans22.content}",
        f"**28yo Persona (Priya):** {ans28.content}",
        f"**34yo Persona (Anjali):** {ans34.content}"
    ]
    return {"verifier_feedback": feedbacks}

def manager_evaluation_node(state: GraphState) -> GraphState:
    print("Agent: Manager - Evaluating Hook...")
    
    hook = state["current_hook"]
    
    # 1. Programmatic Checks
    passed, prog_feedback = manual_checks(hook)
    
    # 2. LLM Checks
    prompt_str = load_prompt("verifier_manager.md")
    
    verifiers_text = "\n".join(state["verifier_feedback"])
    full_prompt = f"""{prompt_str}
    
    RECIPE: {state["recipe_description"]}
    PROPOSED HOOK: {hook}
    
    PROGRAMMATIC CHECKS PASSED: {passed}
    PROGRAMMATIC DETAILS: {prog_feedback}
    
    PERSONA FEEDBACK:
    {verifiers_text}
    """
    
    res = llm.invoke(full_prompt)
    manager_ans = res.content.strip()
    
    is_approved = manager_ans.upper().startswith("APPROVED") and passed
    if passed and not manager_ans.upper().startswith("APPROVED") and not manager_ans.upper().startswith("REJECTED"):
        # LLM output safeguard
        is_approved = True if "APPROVED" in manager_ans.upper() else False

    # History logging for UI
    history_entry = {
        "iteration": state["iterations"],
        "hook": hook,
        "programmatic_feedback": prog_feedback,
        "verifier_feedback": state["verifier_feedback"],
        "manager_decision": manager_ans,
        "is_approved": is_approved
    }
    
    new_history = state.get("history", []) + [history_entry]
    
    return {
        "manager_message": manager_ans,
        "is_approved": is_approved,
        "programmatic_checks_passed": passed,
        "programmatic_feedback": prog_feedback,
        "history": new_history
    }

def finalize_hook_node(state: GraphState) -> GraphState:
    print("Agent: Finalizer - Generating Production Card...")
    prompt_str = load_prompt("finalizer_agent.md")
    prompt = PromptTemplate.from_template(prompt_str + "\n\nAPPROVED HOOK: {hook}\nRECIPE: {recipe}")
    res = (prompt | llm).invoke({"hook": state["current_hook"], "recipe": state["recipe_description"]})
    
    return {"final_output": res.content}

def router(state: GraphState) -> Literal["finalize_hook", "generate_hook"]:
    if state["is_approved"]:
        print("Manager approved the hook!")
        return "finalize_hook"
    if state["iterations"] >= 3:
        print("Reached max iterations (3). Finalizing best possible hook...")
        return "finalize_hook"
    
    print("Manager rejected. Returning to Generator...")
    return "generate_hook"

def run_workflow(recipe_description: str) -> GraphState:
    workflow = StateGraph(GraphState)
    
    workflow.add_node("generate_hook", generate_hook_node)
    workflow.add_node("verify_personas", verify_personas_node)
    workflow.add_node("manager_evaluation", manager_evaluation_node)
    workflow.add_node("finalize_hook", finalize_hook_node)
    
    workflow.set_entry_point("generate_hook")
    
    workflow.add_edge("generate_hook", "verify_personas")
    workflow.add_edge("verify_personas", "manager_evaluation")
    
    workflow.add_conditional_edges(
        "manager_evaluation",
        router
    )
    workflow.add_edge("finalize_hook", END)
    
    app = workflow.compile()
    
    initial_state = {
        "recipe_description": recipe_description,
        "current_hook": "",
        "manager_message": "",
        "iterations": 0,
        "verifier_feedback": [],
        "is_approved": False,
        "programmatic_checks_passed": False,
        "programmatic_feedback": "",
        "history": [],
        "final_output": ""
    }
    
    final_state = app.invoke(initial_state)
    return final_state

def run_full_chain(recipe_description: str) -> Dict[str, Any]:
    """
    Run the LangGraph workflow from recipe to production card.
    
    Returns:
        Dictionary containing state at the end of execution.
    """
    print("\n" + "=" * 80)
    print("Starting LangGraph Multi-Agent Workflow...")
    print("=" * 80 + "\n")
    
    result = run_workflow(recipe_description)
    
    print("\n" + "=" * 80)
    print("Webcast Graph Complete!")
    print("=" * 80)
    
    return result
