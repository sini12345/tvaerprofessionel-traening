def build_feedback(goal: str, history: list[dict], turns: list[dict]) -> str:
    start = history[0]
    end = history[-1]
    lines = [f"Læringsmål: {goal}", ""]

    if end["team_coordination"] > start["team_coordination"]:
        lines.append("Styrke: Du forbedrede tværfaglig koordination.")
    else:
        lines.append("Fokuspunkt: Gør roller/ansvar tydeligere undervejs.")

    if end["citizen_trust"] > start["citizen_trust"]:
        lines.append("Styrke: Du holdt borgerperspektivet aktivt.")
    else:
        lines.append("Fokuspunkt: Brug flere borgerrettede spørgsmål.")

    if end["plan_concreteness"] > start["plan_concreteness"]:
        lines.append("Styrke: Samtalen endte med mere konkret plan.")
    else:
        lines.append("Fokuspunkt: Lav en 72-timers mikroplan med ansvar.")

    lines.append("")
    lines.append("Næste øvelse: Opsummer aftaler i 3 punkter med ansvar og tidspunkt.")
    return "\n".join(lines)
