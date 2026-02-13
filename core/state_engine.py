from dataclasses import dataclass


@dataclass
class SessionState:
    citizen_trust: int = 45
    team_coordination: int = 35
    role_clarity: int = 35
    conflict_level: int = 50
    plan_concreteness: int = 25
    difficulty: int = 2

    def clamp(self):
        for k in ["citizen_trust", "team_coordination", "role_clarity", "conflict_level", "plan_concreteness"]:
            v = getattr(self, k)
            setattr(self, k, max(0, min(100, v)))

    def to_dict(self):
        return {
            "citizen_trust": self.citizen_trust,
            "team_coordination": self.team_coordination,
            "role_clarity": self.role_clarity,
            "conflict_level": self.conflict_level,
            "plan_concreteness": self.plan_concreteness,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)

    def to_panel_text(self) -> str:
        return (
            f"Borger-tillid: {self.citizen_trust}\n"
            f"Tværfaglig koordination: {self.team_coordination}\n"
            f"Rolleklarhed: {self.role_clarity}\n"
            f"Konfliktniveau: {self.conflict_level}\n"
            f"Plan-konkrethed: {self.plan_concreteness}"
        )


def update_state(s: SessionState, user_text: str, learning_goal: str) -> SessionState:
    n = SessionState.from_dict(s.to_dict())
    t = user_text.lower()

    if any(x in t for x in ["hvem gør hvad", "ansvar", "rolle", "afklare"]):
        n.role_clarity += 5
        n.team_coordination += 3

    if any(x in t for x in ["hvad er vigtigt for dig", "hvordan oplever du", "giver mening"]):
        n.citizen_trust += 4

    if any(x in t for x in ["du skal", "bare", "det er ikke mit", "det må de andre"]):
        n.conflict_level += 5
        n.team_coordination -= 4

    if any(x in t for x in ["næste skridt", "inden 72 timer", "aftaler vi", "konkret"]):
        n.plan_concreteness += 6

    if learning_goal == "Konfliktdaempende samarbejde":
        n.conflict_level -= 1

    n.conflict_level += max(0, n.difficulty - 2)
    n.clamp()
    return n
