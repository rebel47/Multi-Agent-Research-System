# Multi-Agent Research System

A lightweight AI research assistant that turns a topic into a structured report. Four focused stages work together to search the web, extract useful content, write a report, and review the final result.

The project includes a minimal Streamlit interface and a command-line workflow.

## How it works

1. **Search agent** — finds recent, relevant sources with Tavily.
2. **Reader agent** — selects a useful result and extracts its page content.
3. **Writer chain** — turns the collected research into a structured report.
4. **Critic chain** — scores the report and suggests improvements.

## Features

- Clean, responsive Streamlit interface
- Multi-agent workflow powered by LangChain
- Web search through the Tavily API
- Webpage extraction with Beautiful Soup
- Structured reports with key findings and sources
- Automated quality review and scoring
- Markdown report downloads
- Light and dark mode support

## Tech stack

- Python
- Streamlit
- LangChain
- OpenAI API
- Tavily Search API
- Beautiful Soup

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/rebel47/Multi-Agent-Research-System.git
cd Multi-Agent-Research-System
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The `.env` file is ignored by Git and should never be committed.

## Usage

Start the web interface:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, enter a research topic, and select **Start research**.

You can also run the workflow in the terminal:

```bash
python3 pipeline.py
```

## Project structure

```text
.
├── app.py           # Streamlit interface
├── agents.py        # Search, reader, writer, and critic definitions
├── tools.py         # Tavily search and webpage scraping tools
├── pipeline.py      # Command-line research workflow
├── requirements.txt # Python dependencies
└── README.md
```

## Notes

- The default language model is `gpt-4o-mini`.
- Research quality depends on the available search results and source pages.
- Some websites may restrict automated extraction or require JavaScript to render their content.
- Always verify important claims and citations before relying on generated reports.

## License

No license has been added yet.
