# Story Generation Logic

import boto3
import json
import random
import os

# Initialize the Bedrock runtime client
# Ensure AWS credentials and region are configured
# (e.g., via environment variables or AWS CLI)
# The region can be specified explicitly or taken from AWS_DEFAULT_REGION
bedrock_runtime = boto3.client(service_name="bedrock-runtime")

STORY_GENRES = ["bedtime story", "horror", "fantasy", "comedy"]

# You might want to adjust this based on availability in your region
# and desired capabilities. For example, Claude 3 Sonnet:
CLAUDE_MODEL_ID = os.environ.get(
    "CLAUDE_MODEL_ID", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)
# Or for older models like Claude 2.1:
# CLAUDE_MODEL_ID = "anthropic.claude-v2:1"


def get_random_genre():
    """Selects a random genre from the predefined list."""
    return random.choice(STORY_GENRES)


def generate_story_from_bedrock(genre):
    """
    Generates a short story as an SSML document using Anthropic Claude on AWS Bedrock.

    Args:
        genre (str): The genre of the story to generate.

    Returns:
        str: The generated story as an SSML string, or None if an error occurs.
    """
    prompt_instructions = (
        "You are a creative storyteller. Write a short, engaging story use role playing to make it more engaging "
        "for the given genre. The story should be suitable for text-to-speech "
        "synthesis using Amazon Polly. Format the entire story as a valid "
        "SSML document. The root element must be <speak>. Use <p> tags for "
        "paragraphs and <s> tags for sentences within paragraphs. This is "
        "important for subtitle synchronization. Enhance the storytelling by "
        "using other SSML tags like <emphasis>, <prosody> (to control rate, "
        'pitch, volume), and <break time="Xms"/> where appropriate to make '
        "the narration more natural and expressive. Ensure all special "
        "characters like '&', '<', '>' are correctly escaped if they appear "
        "in the story text itself (e.g., use '&amp;'). The story should have a "
        "clear beginning, middle, and end, and consist of a few paragraphs."
    )

    prompt = (
        f"\n\nHuman: {prompt_instructions}\n\n"
        f"Please write a {genre} story now, following all the SSML "
        f"formatting instructions above.\n\nAssistant: <speak>"
    )
    # We start the assistant response with <speak> to guide it better.
    # Claude might sometimes forget to add it or close it if not explicitly guided.

    # Claude 3 models use the new messages API format
    if "claude-3" in CLAUDE_MODEL_ID:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,  # Increased for SSML verbosity
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
                # Adding assistant prefill guides Claude 3 to start correctly.
                # The prompt ends "Assistant: <speak>", but this can be more robust.
                # {"role": "assistant",
                #  "content": [{"type": "text", "text": "<speak>"}]}
            ],
        }
    else:  # For older Claude models (e.g., v1, v2, Instant)
        # The prompt already ends with "Assistant: <speak>"
        request_body = {
            "prompt": prompt,
            "max_tokens_to_sample": 2048,  # Increased max_tokens
            "temperature": 0.8,
        }

    try:
        response = bedrock_runtime.invoke_model(
            body=json.dumps(request_body),
            modelId=CLAUDE_MODEL_ID,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        generated_content = ""

        if "claude-3" in CLAUDE_MODEL_ID:
            if (
                response_body.get("content")
                and isinstance(response_body["content"], list)
                and len(response_body["content"]) > 0
            ):
                generated_content = response_body["content"][0].get("text")
            else:
                err = response_body
                print(f"Error: Unexpected Claude 3 response: {err}")
                return None
        else:  # Older models
            generated_content = response_body.get("completion")

        if generated_content:
            ssml_output = generated_content.strip()
            # The prompt guides the model to start with <speak>.
            # We also try to ensure it ends with </speak>.

            if not ssml_output.startswith("<speak>"):
                # This case should be rare due to prompt engineering.
                # If model returns only *inside* of <speak>...</speak>:
                if "<speak>" not in ssml_output and "</speak>" not in ssml_output:
                    ssml_output = "<speak>\n" + ssml_output + "\n</speak>"

            # Ensure the LLM closed the <speak> tag. More robust parsing (e.g. XML)
            # is better for production, but Polly will also validate.
            if not ssml_output.endswith("</speak>"):
                # Attempt to gracefully close it if it seems forgotten.
                # This is a heuristic.
                last_speak_idx = ssml_output.rfind("<speak>")
                if (
                    "<speak>" in ssml_output
                    and "</speak>" not in ssml_output[last_speak_idx:]
                ):
                    ssml_output += "\n</speak>"
                else:
                    # If no <speak> or malformed, let Polly handle it.
                    warn_msg_parts = [
                        "SSML might be malformed (no </speak>):",
                        f"{ssml_output[:120]}...",
                    ]
                    print(f"Warning: {' '.join(warn_msg_parts)}")

            return ssml_output
        else:
            err_resp = response_body
            print(f"Error: Could not extract SSML from Bedrock: {err_resp}")
            return None

    except Exception as e:
        err_msg = str(e)
        print(f"Error invoking Bedrock model {CLAUDE_MODEL_ID}: {err_msg}")
        return None


if __name__ == "__main__":
    selected_genre = get_random_genre()
    print(f"--- Generating SSML story for genre: {selected_genre} ---")
    # Example: Use Haiku by uncommenting and setting the env var
    # os.environ["CLAUDE_MODEL_ID"] = "anthropic.claude-3-haiku-20240307-v1:0"
    generated_ssml_story = generate_story_from_bedrock(selected_genre)
    if generated_ssml_story:
        print("\n--- Generated SSML Story ---")
        print(generated_ssml_story)

        # Basic validation check example (optional, Polly will also validate)
        try:
            import xml.etree.ElementTree as ET

            # Attempt to parse SSML string to check for well-formedness
            ET.fromstring(generated_ssml_story)
            print("\n--- SSML appears well-formed (basic XML check) ---")
        except ET.ParseError as e:
            err_parse = str(e)
            print(f"\n--- Warn: SSML not well-formed XML: {err_parse} ---")
        except ImportError:
            # xml.etree.ElementTree might not be available in some minimal
            # Python environments, though it is standard.
            print("\n--- Skipping XML check (xml.etree not available) ---")

    else:
        print("\n--- Failed to generate SSML story. ---")
