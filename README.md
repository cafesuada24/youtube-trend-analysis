# YouTube Trend Analysis

YouTube Trend Analysis is an AI-powered platform designed to transform raw video data into actionable intelligence. By leveraging multi-agent orchestration and advanced LLMs, the system automates the process of scraping YouTube transcripts and synthesizing high-level trends, sentiment, and key topics.

## Overview

The application utilizes **CrewAI** to manage a specialized team of AI agents that process YouTube content. It bridges the gap between massive amounts of video data and human-readable insights, making it an ideal tool for content creators, marketers, and researchers.

![Application Dashboard Placeholder]

## Key Features

- **Automated Scraping:** Integrated with BrightData to extract metadata and transcripts from any YouTube channel within specific date ranges.
- **Multi-Agent Analysis:** Features a specialized `Transcript Analyzer` for deep data extraction and a `Response Synthesizer` for high-level summaries.
- **Sentiment & Pattern Recognition:** Identifies emerging trends, recurring keywords, and shifts in speaker sentiment across multiple videos.
- **Streamlit Interface:** A clean, interactive web dashboard for managing analysis parameters and viewing results in real-time.
- **Markdown Reports:** Generates structured, downloadable reports containing granular insights and recommendations.

## Architecture

The system is built on a modular Python architecture:
- **Orchestration:** CrewAI manages the sequential workflow between agents.
- **LLM:** Powered by Google Gemini (`gemini-2.5-flash`) for high-context transcript processing.
- **Data Pipeline:** Custom scrapers handle the transition from YouTube URLs to localized transcript files.

![Workflow Diagram Placeholder]

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- BrightData API Key (for scraping)
- Google Gemini API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/youtube-trend-analysis.git
   cd youtube-trend-analysis
   ```

2. Configure environment variables:
   ```bash
   cp .env-template .env
   # Edit .env with your BrightData and Gemini API keys
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

### Usage

Start the Streamlit application using the provided Makefile:

```bash
make run
```

Once the server is running, navigate to the local URL (typically `http://localhost:8501`), enter your target YouTube channel URLs, and select the desired date range to begin the analysis.

## Development

The project adheres to high-quality code standards using **Ruff** for linting and formatting.

- **Check Linting:** `ruff check .`
- **Apply Formatting:** `ruff format .`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
