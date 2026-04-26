```markdown
# 🛡️ The Al-Kahfi Security Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture](https://img.shields.io/badge/Architecture-Zero_Trust-red.svg)]()
[![Focus](https://img.shields.io/badge/Focus-Anti_Phishing-green.svg)]()

> **A Human-Centric, Zero-Trust Cybersecurity Architecture**  
> Designed to mitigate Social Engineering, Phishing, and Account Takeover (ATO) attacks.

## 🎯 The Purpose

Inspired by the philosophical story of Moses and Khidr—*never judging a situation purely by its external appearance*—this framework does not blindly trust the display name or the static identity of a sender. Instead, it aggressively analyzes the **psychological intent**, **behavioral context**, and **community reputation** behind every digital interaction.

> ⚠️ Modern cyber threats (AI-driven scams, hijacked WhatsApp accounts of trusted family members) bypass traditional firewalls. Al-Kahfi acts as a **"Cognitive Firewall"** — identifying psychological manipulation (Fear, Urgency, Greed) and cross-referencing it with Zero-Trust identity vectors (Impossible Travel, Device Anomalies).

## 🏗️ The 4 Pillars of Defense

The framework operates on a highly decoupled, *brain-agnostic* architecture. Every incoming message passes through four distinct layers sequentially: **The Garden → The Journey → The Cave → The Barrier**.

### 🌿 The Garden — Cognitive & Emotional Filter
Analyzes *WHAT* is being said. It scans the text for emotional manipulation, artificial urgency, and deceit using pluggable analysis engines.

| Engine | Use Case | Privacy |
|:-------|:---------|:--------|
| **Regex** | Offline, fast pattern matching | Full offline |
| **Cloud LLM** (OpenAI, Groq) | Advanced reasoning & nuance detection | Requires API |
| **Local LLM** (Ollama) | On-premise, privacy-first deployment | Full offline |

### 🚶 The Journey — Contextual Zero-Trust Filter
Analyzes *WHO* is sending it and *WHERE* it comes from. It verifies spatial, temporal, and identity metadata to catch anomalies that traditional filters miss.

| Signal | What It Detects |
|:-------|:----------------|
| **New Device** | Login from unrecognized device |
| **Abnormal Time** | Interaction outside usual patterns |
| **Impossible Travel** | IP hopping across geographies in short time |
| **Country Mismatch** | Sender ID country vs. IP geolocation |

*💡 A family member's hijacked WhatsApp account will pass traditional spam filters. The Journey catches the impossible travel signal.*

### ⛰️ The Cave — Community Threat Intelligence
Analyzes the *REPUTATION* of the sender. It acts as a decentralized hive-mind using a localized SQLite database. When one user reports a scammer, that entity is instantly blocked for all users.

| Feature | Detail |
|:--------|:-------|
| **Storage** | Local SQLite (no external dependency) |
| **Scope** | Per-deployment shared blacklist |
| **Speed** | Instant lookup, zero network latency |
| **Privacy** | No data leaves your infrastructure |

### 🛡️ The Barrier — Guardrails & Enforcement
The Supreme Judge. Aggregates scores from The Garden, Journey, and Cave, then determines the final action based on the combined risk profile.

| Final Action | Trigger Condition |
|:-------------|:------------------|
| **ALLOW** | All layers report safe |
| **WARN** | One layer reports elevated risk |
| **BLOCK** | Sender is blacklisted or all layers flag danger |
| **FORCE_OOB_AUTH** | Trusted contact sends manipulative message (ATO) |

> 🔴 **The Mismatch Trigger (ATO Mitigation):** If a "trusted contact" (Safe in Journey) suddenly sends a "highly manipulative message" (High Risk in Garden), The Barrier detects this contradiction and flags a potential Account Takeover. It forces an **Out-of-Band (OOB) Authentication** (e.g., prompting the user to make a voice/video call).

## 🚀 Installation & Quick Start

The Al-Kahfi Framework is built as an installable Python package with a built-in CLI wizard.

**Prerequisites:** Python 3.8+ · Git

**Step 1 — Clone & Install**
```bash
git clone https://github.com/sendok/alkahfi-security-framework.git
cd alkahfi-security-framework
pip install -e .
```

**Step 2 — Configure Environment**
```bash
alkahfi config
```
*Follow the on-screen prompts to select between Regex, Cloud API, or Local LLM. No manual `.env` editing needed.*

**Step 3 — Start the Engine**
```bash
alkahfi start
```

| Resource | URL |
|:---------|:----|
| Server | `http://0.0.0.0:8000` |
| Interactive API Docs | `http://localhost:8000/docs` |

## 💻 API Usage

Send a POST request to `/api/v1/scan` to analyze any message.

**Request**
```json
{
  "message": "URGENT: Your bank account will be suspended in 5 minutes! Click here to verify your identity.",
  "sender_id": "+628111222333",
  "metadata": {
    "is_new_contact": false,
    "is_new_device": true,
    "impossible_travel_detected": true,
    "country_code": "+62"
  }
}
```

**Response**
```json
{
  "action": "FORCE_OOB_AUTH",
  "risk_level": "HIGH",
  "overall_score": 85,
  "system_reason": "Critical Mismatch: Trusted contact using high-risk emotional manipulation. Potential ATO.",
  "user_message": "🛑 WARNING: Your trusted contact is requesting urgent action. Please make a voice or video call to verify their identity before proceeding, as their account may be compromised.",
  "filter_logs": [
    {
      "module_name": "The Garden (CLOUD_API)",
      "is_safe": false,
      "score": 85,
      "details": "LLM Reason: High urgency and fear tactics detected demanding immediate credential verification."
    },
    {
      "module_name": "The Journey (LOCAL_HEURISTIC)",
      "is_safe": true,
      "score": 50,
      "details": "Heuristics: Contextual Anomaly: Impossible travel / IP hop detected (+50)"
    },
    {
      "module_name": "The Cave (LOCAL_DB)",
      "is_safe": true,
      "score": 0,
      "details": "Local DB: Entity not found in community blacklist."
    }
  ]
}
```

## 📁 Project Structure

```
al_kahfi_oss/
├── pyproject.toml         # Package definition
├── README.md              # Documentation
├── .env.example           # Example configuration
│
└── al_kahfi/              # Source Code
    ├── cli.py             # Terminal commands wizard
    ├── main.py            # FastAPI Entry Point
    │
    ├── core/              # Agnostic Orchestrator & Schemas
    │
    └── plugins/           # Independent Skill Modules
        ├── garden/        # 🌿 Cognitive NLP Engine
        ├── journey/       # 🚶 Context & Zero-Trust Engine
        ├── cave/          # ⛰️  Threat Intel DB
        └── barrier/       # 🛡️  Guardrail Enforcement
```

## 🤝 Contributing

Contributions are highly welcome. Areas where we especially need help:

* 🔍 Computer Vision plugins for image manipulation detection
* 🧠 LLM prompt engineering & reasoning improvements
* 🌐 OSINT capability expansion
* 📝 Documentation & localization

> Fork the repository and submit a pull request.

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<p align="center">
  <sub>Built with 🔥 by Dhendik Dwi Prasetyo aka Sendok</sub>
</p>
```