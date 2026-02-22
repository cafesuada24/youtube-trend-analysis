import gc

import streamlit as st


def reset_chat() -> None:
    """Reset chat history."""
    st.session_state.messages = None
    gc.collect()

def _start_analysis() -> None:
    ...

def _render_sidebar_content() -> None:
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
        start_date = st.date_input("Start Date")
        st.session_state.start_date = start_date
        st.session_state.start_date = start_date.strftime("%Y-%m-%d")

    with col2:
        end_date = st.date_input("End Date")
        st.session_state.end_date = end_date
        st.session_state.end_date = end_date.strftime("%Y-%m-%d")

    st.divider()
    st.button("Start Analysis 🚀", type="primary", on_click=_start_analysis)

def render_home_page() -> None:
    """Start home page lifecycle."""

    st.markdown("# Youtube Trend Analysis")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'response' not in st.session_state:
        st.session_state.response = None

    if 'crew' not in st.session_state:
        st.session_state.crew = None

    with st.sidebar:
        _render_sidebar_content()

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
