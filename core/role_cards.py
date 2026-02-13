ROLE_CARDS = {
    "socialraadgiver": {
        "name": "Socialrådgiver",
        "summary": "Fokus på lovgrundlag, ydelser, handleplan og progression.",
    },
    "psykiatrisk_sygeplejerske": {
        "name": "Psykiatrisk sygeplejerske",
        "summary": "Fokus på symptomer, stabilisering, behandlingsadhærens og sikkerhed.",
    },
    "uu_vejleder": {
        "name": "UU-vejleder",
        "summary": "Fokus på uddannelsesdeltagelse, fremmøde og realistiske forløb.",
    },
    "misbrugsbehandler": {
        "name": "Misbrugsbehandler",
        "summary": "Fokus på tilbagefaldsarbejde, motivation og skadesreduktion.",
    },
}


def get_role_options() -> list[str]:
    return list(ROLE_CARDS.keys())
