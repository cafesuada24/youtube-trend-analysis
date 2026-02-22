import gc
import os
import time

import streamlit as st
from crew import YoutubeTrendAnalysisCrew
from dotenv import load_dotenv
from scrappers.brightdata_scrapper import BrightDataScrapper
from scrappers.scrapper import Scrapper
from tqdm import tqdm

load_dotenv()


def reset_chat() -> None:
    """Reset chat history."""
    st.session_state.messages = None
    gc.collect()


def _start_analysis(scrapper: Scrapper) -> None:
    with st.spinner('Scraping videos... This may take a moment.'):
        status_container = st.empty()
        status_container.info('Extracting videos from the channels...')
        channel_snapshot_id = scrapper.scrape_channels(
            st.session_state.youtube_channels,
            10,
            st.session_state.start_date,
            st.session_state.end_date,
            'Latest',
            '',
        )
        if channel_snapshot_id is None:
            status_container.error('Failed to create snapshot')
            return

        status = scrapper.get_progress(channel_snapshot_id['snapshot_id'])
        if status is None:
            status_container.error('Failed to get snapshot snapshot status')
            return

        while status['status'] != 'ready':
            status_container.info(f'Current status: {status["status"]}')
            time.sleep(10)
            status = scrapper.get_progress(channel_snapshot_id['snapshot_id'])
            if status is None:
                status_container.error('Failed to get snapshot snapshot status')
                return

            if status['status'] == 'failed':
                status_container.error(f'Scraping failed: {status}')
                return

        if status['status'] == 'ready':
            status_container.success('Scraping completed successfully!')

            channel_scrapped_output = scrapper.get_output(
                status['snapshot_id'],
                output_format='jsonl',
            )
            if channel_scrapped_output is None:
                status_container.error('Failed to get scrapped output')
                return

            st.markdown('## Youtube Videos Extracted')
            carosel_container = st.container()

            videos_per_rows = 3

            with carosel_container:
                num_videos = len(channel_scrapped_output)
                num_rows = (num_videos + videos_per_rows - 1) // videos_per_rows

                for row in range(num_rows):
                    cols = st.columns(videos_per_rows)

                    for col_idx in range(videos_per_rows):
                        video_idx = row * videos_per_rows + col_idx
                        if video_idx >= num_videos:
                            break
                        cols[col_idx].video(
                            channel_scrapped_output[video_idx]['url'],
                        )

            status_container.info('Processing transcripts...')
            st.session_state.all_files = []

            for i in tqdm(range(len(channel_scrapped_output))):
                curr_output = channel_scrapped_output[i]
                youtube_video_id = curr_output['shortcode']

                os.makedirs('transcripts', exist_ok=True)
                file = 'transcripts/' + youtube_video_id + '.txt'
                st.session_state.all_files.append(file)

                with open(file, 'w') as f:
                    for trans in curr_output['formatted_transcript']:
                        text = trans['text']
                        start_time = trans['start_time']
                        end_time = trans['end_time']
                        f.write(f'({start_time:.2f}-{end_time:.2f}: {text}\n')

                st.session_state.channel_scrapped_output = channel_scrapped_output
                status_container.success(
                    'Scraping complete! Generating trends report...',
                )

        else:
            status_container.error(f'Scraping failed with status: {status}')

    if status['status'] == 'ready':
        status_container = st.empty()
        with st.spinner('The agent is analyzing the videos... This may take a moment.'):
            st.session_state.crew = YoutubeTrendAnalysisCrew().crew()
            st.session_state.response = st.session_state.crew.kickoff(
                inputs={'file_paths': ', '.join(st.session_state.all_files)},
            )


def _render_sidebar_content(scrapper: Scrapper) -> None:
    st.header('Youtube Channels')

    if 'youtube_channels' not in st.session_state:
        st.session_state.youtube_channels = ['']

    def _add_channel_field() -> None:
        st.session_state.youtube_channels.append('')

    for i, channel in enumerate(st.session_state.youtube_channels):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.session_state.youtube_channels[i] = st.text_input(
                'Channel URL',
                value=channel,
                key=f'channel_{i}',
                label_visibility='collapsed',
            )

        with col2:
            if i > 0 and st.button('❌', key=f'remove_{i}'):
                st.session_state.youtube_channels.pop(i)
                st.rerun()

    st.button('Add Channel ➕', on_click=_add_channel_field)

    st.divider()

    st.subheader('Data range')

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input('Start Date')
        st.session_state.start_date = start_date
        st.session_state.start_date = start_date.strftime('%Y-%m-%d')

    with col2:
        end_date = st.date_input('End Date')
        st.session_state.end_date = end_date
        st.session_state.end_date = end_date.strftime('%Y-%m-%d')

    st.divider()
    st.button(
        'Start Analysis 🚀', type='primary', on_click=_start_analysis, args=(scrapper,)
    )


def render_home_page(scrapper: Scrapper) -> None:
    """Start home page lifecycle."""
    st.markdown('# Youtube Trend Analysis')
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'response' not in st.session_state:
        st.session_state.response = None

    if 'crew' not in st.session_state:
        st.session_state.crew = None

    with st.sidebar:
        _render_sidebar_content(scrapper)

    if st.session_state.response:
        with st.spinner('Generating content... This may take a moment.'):
            try:
                result = st.session_state.response
                st.markdown('### Generated Analysis')
                st.markdown(result)

                st.download_button(
                    label='Download content',
                    data=result.raw,
                    file_name='youtube_trend_analysis.md',
                    mime='text/markdown',
                )

            except Exception as e:
                st.error(f'An error occured: {str(e)}')

    st.markdown('---')


if __name__ == '__main__':
    scrapper = BrightDataScrapper(os.environ['BRIGHT_DATA_API_KEY'])
    render_home_page(scrapper)
