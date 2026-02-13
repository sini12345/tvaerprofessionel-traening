SCENARIOS = {
    "Udskrivning til kommune": {
        "name": "Udskrivning til kommune",
        "context": "Ung udskrives fra psykiatrisk forløb og har ustabil hverdag.",
        "focus": "Hvem gør hvad i overgangen de næste 72 timer.",
        "risk": "Uklar ansvarsfordeling og parallelle planer.",
        "initial": {
            "citizen_trust": 42,
            "team_coordination": 28,
            "role_clarity": 24,
            "conflict_level": 54,
            "plan_concreteness": 20,
        },
    },
    "Fravaer og mistrivsel": {
        "name": "Fravær og mistrivsel",
        "context": "Ung med stigende fravær, angsttegn og social tilbagetrækning.",
        "focus": "Fælles indsats uden at overbelaste den unge.",
        "risk": "Faglige mål kolliderer med borgerens aktuelle kapacitet.",
        "initial": {
            "citizen_trust": 48,
            "team_coordination": 30,
            "role_clarity": 32,
            "conflict_level": 46,
            "plan_concreteness": 24,
        },
    },
    "Akut boligusikkerhed": {
        "name": "Akut boligusikkerhed",
        "context": "Ung har mistet overnatningsmulighed og er under højt pres.",
        "focus": "Sikkerhed her-og-nu og kort, realistisk handlingsplan.",
        "risk": "Konflikt om prioritering mellem akut hjælp og langsigtede mål.",
        "initial": {
            "citizen_trust": 35,
            "team_coordination": 26,
            "role_clarity": 30,
            "conflict_level": 62,
            "plan_concreteness": 18,
        },
    },
}


def get_scenario_options() -> list[str]:
    return list(SCENARIOS.keys())
