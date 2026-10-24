# Getting Started

Follow the instructions below to download, configure, and run the application locally.

## 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/algoradix/401_AI.git
cd 401_AI
```

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project's root directory:

```bash
touch .env
```

Open the `.env` file and add the following configuration:

```dotenv
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

# Model Configuration
OPENAI_MODELS=gpt-5-mini
ANTHROPIC_MODELS=claude-sonnet-5-5
GEMINI_MODELS=gemini-2.5-flash
GROQ_MODELS=qwen/qwen3.8-27b
```


## 5. Run the Application

Start the application:

```bash
python app.py
```

## 6. Open in Browser

Once the application is running, open your web browser and navigate to:

```text
http://127.0.0.1:5000
```

The application should now be accessible locally.

> **Note:** The URL and port may differ depending on the application's configuration. Check the terminal output for the correct address.

## 7. Stop the Application

Press `Ctrl + C` in the terminal to stop the application.

To deactivate the virtual environment:

```bash
deactivate
```
