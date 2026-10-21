import re

from agents import search_agent, scrape_agent, writer_chain, critic_chain

def run_workflow(topic: str):
    state = {}
    # Step 1: Use the search agent to gather research
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent_instance = search_agent()
    search_result = search_agent_instance.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information on the topic: {topic}")]
        })
    state['search_result'] = search_result['messages'][-1].content
    print("\n search result ",state['search_result'])


    # Step 2: Use the scrape agent to gather more research
    print("\n"+" ="*50)
    print("step 2 - scrape agent is working ...")
    print("="*50)
    scrape_agent_instance = scrape_agent()
    scrape_result = scrape_agent_instance.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_result'][:800]}"                    
                )]
            })    
    state['scrape_result'] = scrape_result['messages'][-1].content
    print("\n scrape result ",state['scrape_result'])


    # Step 3: Use the writer chain to generate a research report
    print("\n"+" ="*50)
    print("step 3 - writer chain is working ...")
    print("="*50)
    research_content = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPE RESULTS:\n{state['scrape_result']}"
    )

    state['writer_report'] = writer_chain.invoke({"topic": topic, "research": research_content})

    print("\n writer report ",state['writer_report'])

    # Step 4: Use the critic chain to evaluate the research report
    print("\n"+" ="*50)
    print("step 4 - critic chain is working ...")
    print("="*50)
    state['critic_evaluation'] = critic_chain.invoke({"report": state['writer_report']})
    print("\n critic evaluation ",state['critic_evaluation'])

    return state

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_workflow(topic)