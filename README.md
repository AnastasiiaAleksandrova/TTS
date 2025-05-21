# React + TypeScript + Vite Frontend & Python Story Generation Backend

This project combines a React + TypeScript + Vite frontend with a Python (Flask) backend for story generation.

### Frontend Setup & Running

1. Navigate to the project root (`TTS`).
2. Install frontend dependencies: `npm install` (or `yarn` or `pnpm`)
3. Run the frontend development server: `npm run dev` (or `yarn dev` or `pnpm dev`)

## Backend (Python Story Generation API)

The Python backend uses Flask to provide an API for generating stories using AWS Bedrock (Anthropic Claude) and synthesizing speech with Amazon Polly, including speech marks for subtitles.

### Backend Setup

1. **Virtual Environment:** Ensure you have a Python virtual environment set up and activated.

    ```bash
    python -m venv venv
    source .venv/bin/activate
    ```

2. **Install Dependencies:** From the project root (`TTS`), install the Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **AWS Credentials:** Set up your AWS credentials. Ensure your AWS identity has permissions for `bedrock:InvokeModel` (for the chosen Claude model) and `polly:SynthesizeSpeech`.
    This can be done via `aws configure` or by setting environment variables:

    ```bash
    export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
    export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN" # If using temporary credentials
    export AWS_DEFAULT_REGION="us-west-2" # Or your preferred region
    ```

4. **Claude Model ID (Optional):** The backend defaults to using Claude 3 Sonnet via Bedrock (`anthropic.claude-3-sonnet-20240229-v1:0`). You can specify a different Claude model ID available in your Bedrock region by setting the `CLAUDE_MODEL_ID` environment variable:

    ```bash
    export CLAUDE_MODEL_ID="anthropic.claude-3-haiku-20240307-v1:0" # Example for Haiku
    ```

### Running the Backend

1. Navigate to the backend directory:

    ```bash
    cd TTS/backend
    ```

2. Run the Flask application (ensure your virtual environment is active):

    ```bash
    python app.py
    ```

    The backend API will typically be available at `http://127.0.0.1:5001`.

## Application Flow

- The React frontend will make API calls to the Python backend (e.g., to `/api/generate_story`).
- The backend generates a story as SSML using AWS Bedrock (Claude).
- This SSML is then sent to Amazon Polly to synthesize speech and generate speech marks.
- The backend returns the audio (as base64 data for now) and speech marks to the frontend.
- The frontend plays the audio and displays the story text synchronized using the speech marks.
