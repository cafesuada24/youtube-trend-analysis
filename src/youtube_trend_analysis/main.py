import os

from crewai import LLM
from dotenv import load_dotenv

from youtube_trend_analysis.pages.home import render_home_page

load_dotenv()



# @st.cache_resource
# def load_llm(
#     model: str = 'gemini/gemini-2.5-flash',
#     api_key: str | None = None,
# ) -> LLM:
#     """Load an LLM."""
#     return LLM(
#         model=model,
#         api_key=api_key or os.getenv('GEMINI_API_KEY'),
#     )



if __name__ == '__main__':
    render_home_page()
