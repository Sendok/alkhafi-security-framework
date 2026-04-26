import argparse
import os
import subprocess

def create_env_file():
    print("========================================")
    print("🛡️  AlKahfi Security Framework - Initial Setup 🛡️")
    print("========================================\n")
    
    env_content = []
    
    # --- [Phase 1: The Garden Setup] ---
    print("--- [Phase 1: The Garden (Cognitive Engine)] ---")
    print("Choose your NLP Engine Mode:")
    print("  1. REGEX (Fast, offline, no AI)")
    print("  2. CLOUD_API (OpenAI, Groq, Claude)")
    print("  3. LOCAL_ONPREM (Ollama, LM Studio)")
    
    choice = input("Select mode (1/2/3) [1]: ").strip()
    if choice == "2":
        env_content.append("GARDEN_ENGINE_MODE=CLOUD_API")
        api_key = input("Enter Cloud API Key: ").strip()
        env_content.append(f"GARDEN_CLOUD_API_KEY={api_key}")
        
        base_url = input("Enter API Base URL [https://api.openai.com/v1]: ").strip()
        env_content.append(f"GARDEN_CLOUD_BASE_URL={base_url if base_url else 'https://api.openai.com/v1'}")
        
        model = input("Enter Model Name [gpt-3.5-turbo]: ").strip()
        env_content.append(f"GARDEN_CLOUD_MODEL={model if model else 'gpt-3.5-turbo'}")
        
    elif choice == "3":
        env_content.append("GARDEN_ENGINE_MODE=LOCAL_ONPREM")
        base_url = input("Enter Local Base URL [http://localhost:11434/api]: ").strip()
        env_content.append(f"GARDEN_LOCAL_BASE_URL={base_url if base_url else 'http://localhost:11434/api'}")
        
        model = input("Enter Local Model Name [llama3]: ").strip()
        env_content.append(f"GARDEN_LOCAL_MODEL={model if model else 'llama3'}")
    else:
        env_content.append("GARDEN_ENGINE_MODE=REGEX")
        
    # Menambahkan path untuk the Soul
    env_content.append("GARDEN_SOUL_PATH=soul.md")
        
    # --- [Phase 2: The Journey Setup] ---
    print("\n--- [Phase 2: The Journey (Zero-Trust Context)] ---")
    journey_mode = input("Use Cloud OSINT API for Context? (y/N): ").strip().lower()
    if journey_mode == 'y':
        env_content.append("JOURNEY_ENGINE_MODE=OSINT_API")
        ipinfo_key = input("Enter IPinfo API Key: ").strip()
        env_content.append(f"IPINFO_API_KEY={ipinfo_key}")
        whois_key = input("Enter WhoisXML API Key: ").strip()
        env_content.append(f"WHOIS_API_KEY={whois_key}")
    else:
        env_content.append("JOURNEY_ENGINE_MODE=LOCAL_HEURISTIC")
        
    env_content.append("JOURNEY_THRESHOLD=70")
    env_content.append("JOURNEY_DEFAULT_COUNTRY_CODE=+62")
        
    # --- [Phase 3: The Cave Setup] ---
    print("\n--- [Phase 3: The Cave (Community Threat Intel)] ---")
    cave_mode = input("Use Cloud API for Threat Intel? (y/N): ").strip().lower()
    if cave_mode == 'y':
        env_content.append("CAVE_ENGINE_MODE=CLOUD_API")
        threat_key = input("Enter Threat API Key (e.g., AbuseIPDB): ").strip()
        env_content.append(f"THREAT_API_KEY={threat_key}")
        env_content.append("THREAT_API_URL=https://api.abuseipdb.com/api/v2/check")
    else:
        env_content.append("CAVE_ENGINE_MODE=LOCAL_DB")
        env_content.append("CAVE_LOCAL_DB_PATH=jamaah_threats.db")
        
    env_content.append("CAVE_THRESHOLD=80")

    # 1. Write to .env file
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write("\n".join(env_content) + "\n")
        print("\n✅ Configuration saved successfully to '.env' file!")
    except Exception as e:
        print(f"\n❌ Failed to save configuration: {e}")

    # 2. Auto-Generate soul.md
    soul_content = """# THE GARDEN SOUL
You are 'The Garden', an advanced Cognitive Cybersecurity Agent.
Your primary task is to protect your human user from Social Engineering, Hijacking, and Manipulation.

Analyze the user's message against these triggers:
1. Urgency / Time Pressure
2. Fear / Intimidation
3. Greed / Temptation

Always remember the context of previous conversations provided to you. If a sender suddenly changes their tone to be urgent or demanding, treat it as a high-risk Account Takeover (ATO) indicator.

CRITICAL: Respond ONLY in JSON format.
{
    "manipulation_score": <0-100>,
    "reason": "<Explanation>"
}
"""
    if not os.path.exists("soul.md"):
        try:
            with open("soul.md", "w", encoding="utf-8") as f:
                f.write(soul_content)
            print("✅ Default 'soul.md' created! You can edit this file to customize your AI's personality.")
        except Exception as e:
            print(f"❌ Failed to create soul.md: {e}")
            
    print("💡 You can now start the framework by running: alkahfi start")

def start_server():
    if not os.path.exists(".env"):
        print("⚠️  Warning: No '.env' file found in the current directory.")
        print("💡 Tip: It is recommended to run 'alkahfi config' first to set up your environment.\n")
    
    print("🚀 Starting AlKahfi Security Framework Engine...")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 Documentation available at: http://localhost:8000/docs\n")
    
    try:
        subprocess.run([
            "uvicorn", 
            "al_kahfi.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--env-file", ".env",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Al-Kahfi Engine gracefully...")
    except Exception as e:
        print(f"\n❌ Failed to start the server: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="The AlKahfi Security Framework CLI - Human-Centric Cybersecurity Architecture"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("config", help="Initialize and configure environment variables interactively")
    subparsers.add_parser("start", help="Start the Al-Kahfi API server")
    
    args = parser.parse_args()
    
    if args.command == "config":
        create_env_file()
    elif args.command == "start":
        start_server()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()