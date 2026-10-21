from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import get_webpage_content, scrape_url
from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

def search_agent():
    return create_agent(
        model=llm,
        tools=[get_webpage_content],
    )

def scrape_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# writer_chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("user", """Write a detailed research report on the topic below.

Topic: {topic}
Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 key findings, each with a detailed explanation)
- Conclusion 
- Sources (list all sources used in the research)
..."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()