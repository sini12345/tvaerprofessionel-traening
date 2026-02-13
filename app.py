import os
from datetime import datetime

import gradio as gr
import anthropic

from core.feedback_engine import build_feedback
from core.logger import save_session_log
from core.prompt_builder import build_system_prompt, load_markdown
from core.role_cards import ROLE_CARDS, get_role_options
from core.scenarios import SCENARIOS, get_scenario_options
from core.state_engine import SessionState, update_state


MEETING_FORMATS = [
    "Koordineringsmoede med borger",
    "Tvaerfagligt planmoede uden borger",
    "Akut overlevering",
]

LEARNING_GOALS = [
    "Borgerperspektiv i centrum",
    "Rolleafklaring",
    "Faelles mikroplan (72 timer)",
    "Konfliktdaempende samarbejde",
]


def _client() -> anthropic.Anthropic:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError("Mangler ANTHROPIC_API_KEY i miljoe/HF Secrets.")
    return anthropic.Anthropic(api_key=key)


def _to_messages(turns: list[dict]) -> list[dict]:
    out = []
    for t in turns:
        out.append({"role": t["role"], "content": t["content"]})
    return out


def update_role2_visibility(meeting_format: str):
    visible = meeting_format == "Tvaerfagligt planmoede uden borger"
    return gr.Dropdown(visible=visible), gr.Checkbox(visible=not visible)


def scenario_brief(scenario_name: str) -> str:
    s = SCENARIOS.get(scenario_name, {})
    return (
        f"### Scenarie-brief\n"
        f"- **Kontekst:** {s.get('context','')}\n"
        f"- **Fokus:** {s.get('focus','')}\n"
        f"- **Risiko for samarbejdsbrud:** {s.get('risk','')}"
    )


def start_session(meeting_format: str, scenario_name: str, role_1: str, role_2: str, include_citizen: bool, goal: str, difficulty: int):
    state = SessionState(difficulty=difficulty)
    scenario = SCENARIOS[scenario_name]
    state.citizen_trust = scenario["initial"]["citizen_trust"]
    state.team_coordination = scenario["initial"]["team_coordination"]
    state.role_clarity = scenario["initial"]["role_clarity"]
    state.conflict_level = scenario["initial"]["conflict_level"]
    state.plan_concreteness = scenario["initial"]["plan_concreteness"]

    session = {
        "id": datetime.utcnow().strftime("%Y%m%d_%H%M%S"),
        "meeting_format": meeting_format,
        "scenario": scenario_name,
        "role_1": role_1,
        "role_2": role_2 if meeting_format == "Tvaerfagligt planmoede uden borger" else "Ingen",
        "include_citizen": include_citizen,
        "goal": goal,
        "difficulty": difficulty,
        "turns": [],
        "state_history": [state.to_dict()],
        "started_at": datetime.utcnow().isoformat(),
    }

    status = f"Session startet | Format: {meeting_format} | Scenarie: {scenario_name}"
    return session, [], status, state.to_panel_text(), scenario_brief(scenario_name)


def chat_turn(user_text: str, session: dict, chat_history: list):
    if not session:
        return "Start en session foerst.", session, chat_history, "Session ikke startet.", ""
    if not user_text.strip():
        return "", session, chat_history, "Tom besked ignoreret.", ""

    state = SessionState.from_dict(session["state_history"][-1])

    role_1_text = load_markdown(f"professionals/{session['role_1']}.md")
    role_2_text = ""
    if session.get("role_2") and session["role_2"] != "Ingen":
        role_2_text = load_markdown(f"professionals/{session['role_2']}.md")

    system_prompt = build_system_prompt(
        meeting_format=session["meeting_format"],
        scenario=SCENARIOS[session["scenario"]],
        learning_goal=session["goal"],
        role_1=role_1_text,
        role_2=role_2_text,
        include_citizen=session["include_citizen"],
        state=state,
    )

    session["turns"].append({"role": "user", "content": user_text})

    try:
        client = _client()
        resp = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=600,
            system=system_prompt,
            messages=_to_messages(session["turns"]),
        )
        ai_text = "".join([b.text for b in resp.content if b.type == "text"])

        session["turns"].append({"role": "assistant", "content": ai_text})
        updated = update_state(state, user_text, session["goal"])
        session["state_history"].append(updated.to_dict())

        chat_history = chat_history + [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": ai_text},
        ]
        return "", session, chat_history, f"Ture: {len(session['turns']) // 2}", updated.to_panel_text()
    except Exception as e:
        return "", session, chat_history, f"API-fejl: {e}", state.to_panel_text()


def end_session(session: dict):
    if not session:
        return "Ingen aktiv session.", "", ""

    session["ended_at"] = datetime.utcnow().isoformat()
    path = save_session_log(session)
    feedback = build_feedback(session["goal"], session["state_history"], session["turns"])
    return feedback, f"Log gemt: {path}", ""


def build_ui():
    with gr.Blocks(title="Tvaerprofessionel Samtaletraening v1") as demo:
        gr.Markdown("# Tvaerprofessionel Samtaletraening v1")
        gr.Markdown("Studerende spiller social-/specialpaedagog. AI simulerer andre professionelle roller.")

        with gr.Row():
            meeting_format = gr.Dropdown(
                choices=MEETING_FORMATS,
                value=MEETING_FORMATS[0],
                label="Moedeformat",
                info="Vae lg om borger er med, eller om det er fagligt planmoede.",
            )
            scenario = gr.Dropdown(
                choices=get_scenario_options(),
                value=get_scenario_options()[0],
                label="Scenarie",
            )
            goal = gr.Dropdown(
                choices=LEARNING_GOALS,
                value=LEARNING_GOALS[0],
                label="Laeringsmaal",
            )
            difficulty = gr.Slider(1, 3, value=2, step=1, label="Svaerhedsgrad")

        with gr.Row():
            role_1 = gr.Dropdown(choices=get_role_options(), value=get_role_options()[0], label="AI-rolle 1")
            role_2 = gr.Dropdown(choices=get_role_options(), value=get_role_options()[1], label="AI-rolle 2", visible=False)
            include_citizen = gr.Checkbox(value=True, label="Borger med i moede", visible=True)

        brief = gr.Markdown(value=scenario_brief(get_scenario_options()[0]))
        start_btn = gr.Button("Start session")

        chat = gr.Chatbot(type="messages", height=420, label="Samtale")
        user_input = gr.Textbox(label="Din besked", placeholder="Skriv dit naeste indlaeg...")

        with gr.Row():
            send_btn = gr.Button("Send")
            end_btn = gr.Button("Afslut + feedback")

        status = gr.Textbox(label="Status", interactive=False)
        panel = gr.Textbox(label="Samarbejds-tilstand", lines=6, interactive=False)
        feedback = gr.Textbox(label="Debrief", lines=10, interactive=False)

        session_state = gr.State(value={})

        meeting_format.change(fn=update_role2_visibility, inputs=[meeting_format], outputs=[role_2, include_citizen])
        scenario.change(fn=scenario_brief, inputs=[scenario], outputs=[brief])

        start_btn.click(
            fn=start_session,
            inputs=[meeting_format, scenario, role_1, role_2, include_citizen, goal, difficulty],
            outputs=[session_state, chat, status, panel, brief],
        )

        send_btn.click(
            fn=chat_turn,
            inputs=[user_input, session_state, chat],
            outputs=[user_input, session_state, chat, status, panel],
        )
        user_input.submit(
            fn=chat_turn,
            inputs=[user_input, session_state, chat],
            outputs=[user_input, session_state, chat, status, panel],
        )

        end_btn.click(fn=end_session, inputs=[session_state], outputs=[feedback, status, user_input])

    return demo


if __name__ == "__main__":
    app = build_ui()
    app.launch(server_name="0.0.0.0", server_port=7860)
