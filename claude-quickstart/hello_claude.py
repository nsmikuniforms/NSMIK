"""Send one message to Claude through the Messages API and print the reply.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."   # from platform.claude.com -> API keys
    python hello_claude.py "Your question here"
"""

import sys

import anthropic

MODEL = "claude-opus-5-5"


def main() -> int:
    prompt = " ".join(sys.argv[1:]) or "Hello, Claude! In one sentence, what can you help me with?"

    # Reads ANTHROPIC_API_KEY from the environment. Never hardcode the key.
    client = anthropic.Anthropic()

    try:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            output_config={"effort": "medium"},
            # If a safety check declines the request, retry it on a suitable
            # fallback model inside the same call instead of failing.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError:
        print("Invalid or missing API key. Set ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except anthropic.RateLimitError:
        print("Rate limited. Wait a moment and try again.", file=sys.stderr)
        return 1
    except anthropic.APIStatusError as e:
        print(f"API error {e.status_code}: {e.message}", file=sys.stderr)
        return 1
    except anthropic.APIConnectionError:
        print("Could not reach the API. Check your network.", file=sys.stderr)
        return 1

    if response.stop_reason == "refusal":
        print("Claude declined this request.", file=sys.stderr)
        return 1

    for block in response.content:
        if block.type == "text":
            print(block.text)

    usage = response.usage
    print(
        f"\n[model: {response.model} | input tokens: {usage.input_tokens}"
        f" | output tokens: {usage.output_tokens} | stop: {response.stop_reason}]",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
