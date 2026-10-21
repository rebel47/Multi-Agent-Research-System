import html
import re
from datetime import datetime

import streamlit as st

from agents import critic_chain, scrape_agent, search_agent, writer_chain


st.set_page_config(
    page_title="ResearchMind",
    page_icon="⌁",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
        :root {
            --background: #f6f7f9;
            --surface: #ffffff;
            --text: #17191c;
            --muted: #6b7280;
            --line: #e5e7eb;
            --accent: #4f46e5;
        }

        .stApp {
            background: var(--background);
            color: var(--text);
        }

        [data-testid="stHeader"], #MainMenu, footer {
            display: none;
        }

        .block-container {
            max-width: 780px;
            padding: 4rem 1.5rem 5rem;
        }

        .brand {
            color: var(--accent);
            font-size: .8rem;
            font-weight: 700;
            letter-spacing: .12em;
            margin-bottom: .9rem;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--text);
            font-size: clamp(2.5rem, 7vw, 4.25rem);
            font-weight: 700;
            letter-spacing: -.055em;
            line-height: 1;
            margin: 0;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.65;
            margin: 1.15rem 0 2.5rem;
            max-width: 620px;
        }

        [data-testid="stForm"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(17, 24, 39, .05);
            padding: 1.25rem;
        }

        [data-testid="stTextInput"] label p {
            color: var(--text);
            font-size: .86rem;
            font-weight: 600;
        }

        [data-testid="stTextInput"] input {
            background: #fafafa;
            border-color: var(--line);
            border-radius: 10px;
            color: var(--text);
        }

        [data-testid="stTextInput"] input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] > button {
            border-radius: 10px;
            min-height: 2.75rem;
            transition: transform .15s ease, box-shadow .15s ease;
        }

        [data-testid="stFormSubmitButton"] > button {
            background: var(--accent);
            border: 1px solid var(--accent);
            color: white;
            font-weight: 600;
        }

        [data-testid="stFormSubmitButton"] > button:hover {
            box-shadow: 0 6px 16px rgba(79, 70, 229, .2);
            transform: translateY(-1px);
        }

        h2 {
            color: var(--text) !important;
            font-size: 1.35rem !important;
            letter-spacing: -.025em !important;
            margin-top: 2.75rem !important;
        }

        [data-testid="stStatusWidget"],
        [data-testid="stExpander"] {
            background: var(--surface);
            border-color: var(--line);
            border-radius: 12px;
        }

        .meta {
            color: var(--muted);
            font-size: .8rem;
            margin: -.5rem 0 1.5rem;
        }

        .footer {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: .78rem;
            margin-top: 3.5rem;
            padding-top: 1.25rem;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background: #0f1115;
                --surface: #171a20;
                --text: #f3f4f6;
                --muted: #9ca3af;
                --line: #2b3038;
                --accent: #818cf8;
            }

            [data-testid="stTextInput"] input {
                background: #111318;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def message_content(response):
    """Return the final text message from a LangChain agent response."""
    messages = response.get("messages", [])
    if not messages:
        raise ValueError("The agent returned no messages.")
    return messages[-1].content


def safe_filename(topic: str) -> str:
    """Create a short, filesystem-friendly report filename."""
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50]
    return f"{slug or 'research-report'}.md"


def run_pipeline(topic: str) -> dict[str, str]:
    """Run each research stage and show concise progress updates."""
    results: dict[str, str] = {}

    with st.status("Research in progress", expanded=True) as status:
        st.write("1 of 4 · Searching reliable sources")
        search_response = search_agent().invoke(
            {
                "messages": [
                    ("user", f"Find recent, reliable, and detailed information about: {topic}")
                ]
            }
        )
        results["search"] = message_content(search_response)

        st.write("2 of 4 · Reading the most relevant source")
        reader_response = scrape_agent().invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on these search results about '{topic}', choose the most "
                        "relevant URL and scrape it for deeper content.\n\n"
                        f"Search results:\n{results['search'][:3000]}",
                    )
                ]
            }
        )
        results["reader"] = message_content(reader_response)

        st.write("3 of 4 · Writing the report")
        research = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SOURCE CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({"topic": topic, "research": research})

        st.write("4 of 4 · Reviewing the final draft")
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        status.update(label="Research complete", state="complete", expanded=False)

    return results


if "results" not in st.session_state:
    st.session_state.results = None
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""


st.markdown(
    """
    <div class="brand">ResearchMind</div>
    <h1 class="hero-title">Research, distilled.</h1>
    <p class="hero-copy">
        Enter a topic and let four focused AI agents search, read, write, and
        review a clear research brief for you.
    </p>
    """,
    unsafe_allow_html=True,
)


with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "What would you like to research?",
        value=st.session_state.research_topic,
        placeholder="e.g. Recent progress in fusion energy",
    )
    submitted = st.form_submit_button("Start research", use_container_width=True)


if submitted:
    clean_topic = topic.strip()
    if not clean_topic:
        st.warning("Enter a topic to begin.")
    else:
        st.session_state.research_topic = clean_topic
        st.session_state.results = None
        try:
            st.session_state.results = run_pipeline(clean_topic)
        except Exception as error:
            st.error("The research pipeline could not finish. Check your API keys and try again.")
            with st.expander("Technical details"):
                st.exception(error)


results = st.session_state.results
if results:
    st.subheader("Research report")
    st.markdown(
        f'<p class="meta">Topic · {html.escape(st.session_state.research_topic)}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(results["writer"])

    st.download_button(
        "Download report",
        data=results["writer"],
        file_name=safe_filename(st.session_state.research_topic),
        mime="text/markdown",
        use_container_width=True,
    )

    with st.expander("Review notes"):
        st.markdown(results["critic"])

    with st.expander("Sources and extracted content"):
        st.markdown("#### Search results")
        st.markdown(results["search"])
        st.divider()
        st.markdown("#### Extracted content")
        st.markdown(results["reader"])


st.markdown(
    f'<div class="footer">Multi-agent research workspace · {datetime.now().year}</div>',
    unsafe_allow_html=True,
)
