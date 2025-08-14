import streamlit as st
from graph import graph

st.markdown(
    """
        <style>
                .stAppHeader {
                    background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
                    visibility: visible;  /* Ensure the header is visible */
                }

               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Prompt Optimizer",
    page_icon=":material/prompt_suggestion:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(":material/prompt_suggestion: :blue[Prompt] :red[Optimizer]")
# st.markdown("""
#     Welcome to the Prompt Optimizer! This tool helps you refine your prompts
#     for better results from large language models.
#     Enter your prompt below and let the magic happen. ✨
# """)
st.markdown("---")

with st.container():
    st.subheader("Input Prompt")
    with st.form('input'):
        data = st.text_area(
            "Enter your prompt here:",
            height=200,
            placeholder="e.g., Write a short story about a time-traveling detective."
        )

        iterations = st.slider(
            label='Number of optimization iterations:',
            min_value=1,
            max_value=10,
            value=2,
            help="More iterations may lead to a more optimized prompt but will take longer."
        )

        submit_button = st.form_submit_button(
            "Optimize Prompt",
            use_container_width=True,
            icon=':material/arrow_circle_right:',
            type='primary'
        )

        if submit_button:
            if not data.strip():
                st.error("Please enter a prompt to optimize.")
            else:
                with st.spinner('Processing... This may take a moment.'):
                    try:
                        resp = graph.invoke({'input_prompt': data.strip(),
                                             'iterations': iterations})
                        st.session_state.resp = resp
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

# --- Output Section ---
st.markdown("---")
output_prompt = st.session_state.get('resp', {}).get('output_prompt')
comments = st.session_state.get('resp', {}).get('comments')

if output_prompt:
    col_output, col_review = st.columns(2)

    with col_output:
        st.subheader("Optimized Prompt")
        st.text_area(
            label="Copy this optimized prompt",
            value=output_prompt,
            height=300,
            key='optimized_prompt_output'
        )

    with col_review:
        st.subheader("Prompt Review")
        st.info(comments or "No review comments available.")