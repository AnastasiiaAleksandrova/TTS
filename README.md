# React + TypeScript + Vite Frontend & Python Story Generation Backend

This project combines a React + TypeScript + Vite frontend with a Python (Flask) backend for story generation.

## Frontend (React + TypeScript + Vite)

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### Frontend Setup & Running

1. Navigate to the project root (`/Users/andreifeklistov/smartly/aws-hack/TTS`).
2. Install frontend dependencies: `npm install` (or `yarn` or `pnpm`)
3. Run the frontend development server: `npm run dev` (or `yarn dev` or `pnpm dev`)

### Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```

## Backend (Python Story Generation API)

The Python backend uses Flask to provide an API for generating stories using AWS Bedrock (Anthropic Claude) and synthesizing speech with Amazon Polly, including speech marks for subtitles.

### Backend Setup

1. **Virtual Environment:** Ensure you have a Python virtual environment set up and activated. (The user previously mentioned: `/Users/andreifeklistov/smartly/aws-hack/.hackenv`)

    ```bash
    source /Users/andreifeklistov/smartly/aws-hack/.hackenv/bin/activate
    ```

2. **Install Dependencies:** From the project root (`/Users/andreifeklistov/smartly/aws-hack/TTS`), install the Python dependencies:

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
    cd /Users/andreifeklistov/smartly/aws-hack/TTS/backend
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
