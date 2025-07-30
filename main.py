import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
    )
from parse import parse_with_ollama

st.title("Scrapy")
url = st.text_input("Enter a website URL: ")

st.text("If you are not seeing the desired output from a popular website it may be because they are using anti-bot and security mechanisms.")

if st.button("Scrape it!"):
    st.write("Scraping......")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

#If we get the dom content from the website we will initate the prompting area
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    #If the user gives presses button we begin to parse
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            #we will send these chunks to the llm
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)