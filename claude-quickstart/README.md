# Claude API quickstart

A minimal Python script that sends one message to Claude through the Messages API.

## 1. Get an API key

1. Sign in at https://platform.claude.com
2. Add billing credits under **Billing** (the API is pay-as-you-go).
3. Go to **API keys** → **Create key** and copy it (it starts with `sk-ant-`).

Keep the key secret. Don't commit it to git.

## 2. Install

Needs Python 3.10+.

```bash
cd claude-quickstart
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Run

```bash
export ANTHROPIC_API_KEY="sk-ant-..."     # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
python hello_claude.py "Write a haiku about uniforms"
```

Claude's reply prints to the screen, followed by a line showing the model and token usage.

## What the script does

- Calls `client.beta.messages.create` with the `claude-opus-5-5` model.
- Sets `effort` to `medium` (controls how much Claude thinks; raise to `high` for harder tasks, lower to `low` for quick ones).
- Turns on server-side fallbacks: if a safety check declines the request, the API retries it on a fallback model in the same call.
- Prints only the `text` blocks of the reply and handles common errors (bad key, rate limit, network).

## Next steps

- Add a `system="..."` argument to give Claude a role or instructions.
- Keep a `messages` list and append each reply to build a multi-turn chat.
- Docs: https://platform.claude.com/docs
