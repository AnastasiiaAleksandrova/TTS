# Amazon Polly Interaction Logic

import boto3
import json
import os

# Initialize the Polly client
# Ensure AWS credentials and region are configured (e.g., via AWS CLI)
polly_client = boto3.client("polly")

# Define a directory to store audio files temporarily
# In a real app, consider a more robust solution for serving audio (e.g., S3).
AUDIO_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "audio")
# Ensure this directory exists (Flask app won't run from this file's dir).
# Abs path or path relative to app.py needed if creating here.
# For now, just define it. API in app.py handles creation.

DEFAULT_VOICE_ID = "Joanna"  # Example: A popular neural voice


def synthesize_speech_with_polly(
    ssml_text, voice_id=DEFAULT_VOICE_ID, output_filename="story_audio.mp3"
):
    """
    Synthesizes speech from SSML text using Amazon Polly.
    Retrieves speech marks for synchronization.

    Args:
        ssml_text (str): The SSML formatted text to synthesize.
        voice_id (str): The Amazon Polly voice ID to use.
        output_filename (str): Name for the output audio file (if saved).

    Returns:
        tuple: (audio_data, speech_marks_list)
                 audio_data: Raw audio bytes or None if error.
                 speech_marks_list: List of speech mark objects or None if error.
                 Returns (None, None) on failure.
    """
    if not ssml_text:
        print("Error: No SSML text provided to Polly.")
        return None, None

    try:
        # Request speech synthesis for MP3 audio
        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat="mp3",
            Text=ssml_text,
            TextType="ssml",
            # SpeechMarkTypes are not returned with MP3, so call separately
        )

        audio_stream = response.get("AudioStream")
        if not audio_stream:
            print("Error: Polly did not return an audio stream.")
            return None, None

        audio_data = audio_stream.read()
        audio_stream.close()

        # Request speech marks (JSON output)
        speech_marks_response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat="json",  # Output format for speech marks
            Text=ssml_text,
            TextType="ssml",
            SpeechMarkTypes=["sentence", "word", "ssml"],
        )

        speech_marks_stream = speech_marks_response.get("AudioStream")
        if not speech_marks_stream:
            print("Error: Polly did not return a speech marks stream.")
            return None, None  # Or return audio_data, None

        speech_marks_raw = speech_marks_stream.read().decode("utf-8")
        speech_marks_stream.close()

        # Speech marks are newline-delimited JSON objects
        speech_marks_list = []
        for line in speech_marks_raw.strip().split("\n"):
            if line.strip():  # Ensure line is not empty
                try:
                    speech_marks_list.append(json.loads(line))
                except json.JSONDecodeError as je:
                    err_line = line
                    print(f"Error decoding JSON: {je} - Line: '{err_line}'")
                    return None, None  # Strict: fail if any mark is bad

        return audio_data, speech_marks_list

    except Exception as e:
        # Consider more specific boto3 exception handling (e.g., ClientError)
        print(f"Error during Polly synthesis or marks retrieval: {e}")
        return None, None


if __name__ == "__main__":
    # Example SSML for testing (ensure it's valid)
    test_ssml = """
    <speak>
        <s>This is the first sentence.</s>
        <s>And this is the second sentence with <emphasis level=\"strong\">emphasis</emphasis>.</s>
        <p><s>A new paragraph starts here.</s></p>
        <s><prosody rate=\"slow\">This sentence is spoken slowly.</prosody></s>
    </speak>
    """
    print(f"--- Synthesizing Test SSML (Voice: {DEFAULT_VOICE_ID}) ---")

    audio_bytes, marks = synthesize_speech_with_polly(test_ssml)

    if audio_bytes and marks:
        audio_len = len(audio_bytes)
        print(f"\n--- Audio ({audio_len} bytes) & speech marks received ---")
        print("\nFirst 5 Speech Marks:")
        for i, mark in enumerate(marks[:5]):
            print(mark)

        # Example of saving the audio file (optional, for testing here)
        temp_audio_file_path = "polly_test_output.mp3"
        try:
            with open(temp_audio_file_path, "wb") as f:
                f.write(audio_bytes)
            abs_path = os.path.abspath(temp_audio_file_path)
            print(f"\n--- Audio saved to: {abs_path}")
            print("You can try playing this file.")
        except IOError as ioe:
            print(f"\n--- Error saving audio file: {ioe} ---")
    else:
        print("\n--- Failed: Polly synthesis or speech marks. ---")

    # Test with potentially invalid SSML (Polly should error)
    invalid_ssml = "<speak>This is not properly closed."
    print("\n--- Testing with invalid SSML ---")
    audio_bytes_invalid, marks_invalid = synthesize_speech_with_polly(invalid_ssml)
    if not audio_bytes_invalid and not marks_invalid:
        print("--- Correctly failed for invalid SSML (expected) ---")
    else:
        print("--- Invalid SSML test NOT failed as expected. ---")
