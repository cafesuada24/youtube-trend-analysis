.PHONY: run

run:
	cd src && uv run python -m streamlit run youtube_trend_analysis/main.py

