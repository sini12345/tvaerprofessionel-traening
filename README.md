---
title: Tvaerprofessionel Traening
emoji: "🧩"
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.48.0"
app_file: app.py
pinned: false
---

# Tvaerprofessionel Samtaletraening

Separat repo for tværprofessionel træning, hvor studerende spiller social-/specialpædagog og AI spiller øvrige professioner.

## Lokal kørsel

```bash
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY="sk-ant-..."
python app.py
```

## v1 scope
- 3 mødeformater
- AI-roller: socialrådgiver, psykiatrisk sygeplejerske, UU-vejleder, misbrugsbehandler
- 3 tværprofessionelle scenarier
- Debrief med pædagog-fokuseret feedback

## Hugging Face setup
- Opret en Gradio Space og link til dette repo.
- Tilføj secret: `ANTHROPIC_API_KEY`.
- Push til `main` udløser redeploy.
