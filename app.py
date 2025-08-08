import streamlit as st

from graph import graph

st.title("Prompt Optimizer")
with st.form('input'):
    data = st.text_area("Enter prompt")
    if st.form_submit_button(use_container_width=True):
        with st.spinner('Processing ..'):
            resp = graph.invoke({'input_prompt': data.strip()})
            st.session_state.resp = resp

output_prompt = st.session_state.get('resp', {}).get('output_prompt')
comments = st.session_state.get('resp', {}).get('comments')
if output_prompt:
    st.header("Output")
    st.text_area(label='Optimized Prompt', value=output_prompt, height='content')
if comments:
    st.header("Prompt Review")
    st.write(comments)