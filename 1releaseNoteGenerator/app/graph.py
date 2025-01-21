from langgraph.graph import START, END, StateGraph
from langgraph.graph import MessagesState
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
import logging

_ = load_dotenv(find_dotenv())
# llm = ChatGroq(model="Gemma2-9b-It")
llm = ChatGroq(model="llama-3.1-70b-versatile")


class State(MessagesState):
    summary: str
    report: str
    logger: logging.Logger


def reportGeneration(state: State):
    logger=state['logger']
    logger.debug(f"Summarizer Input State: {state}")
    report_generation_instructions = """
    As a seasoned Technical Writer, your task is to craft a comprehensive Markdown release note report that effectively communicates the key updates and changes in the latest product release. 
    Your goal is to ensure that the report is informative, well-structured, and tailored to the needs of your target audience.
    Here is the format you will use to organize and present the release note information:
    ---
    Title (## header)
    Summary (### header)
    Stories (### header)
    ---
    
    In title section always put Release Notes
    Use this {summary} for summary section.
    Place this {data} in stories section and display it as table which has two columns User Story and Description.
    
    Only add above sections and add no extra data
    You should adhere to these instruction and don't add any thing on your own.
    """
    system_prompt = report_generation_instructions.format(
        data=state['messages'], summary=state['summary'])
    system_message = SystemMessage(content=system_prompt)

    response = llm.invoke([system_message])
    return {'report': response.content}


def summarize(state: State):
    logger=state['logger']
    logger.debug(f"Summarizer Input State: {state}")
    prompt="""
    Summarize the content and display in number list.
    If content say "Remove not needed data from pod and k3s formula" Then display it like:
    1. Remove unnecessary data: Cleanup of unnecessary data from a pod and k3s formula.
    Where part before colon, is summary of part after colon
    """
    system_message = SystemMessage(content=prompt)
    content = state['messages']+[system_message]
    response = llm.invoke(content)
    logger.debug(f"Summarizer Output: {response}")
    return {'summary': response.content}


def graph_builder(logger: logging.Logger):
    logger.info("Building Graph")
    reporterNode = "r"
    summarizationNode = "s"
    builder = StateGraph(State)
    builder.add_node(reporterNode, reportGeneration)
    builder.add_node(summarizationNode, summarize)
    builder.add_edge(START, summarizationNode)
    builder.add_edge(summarizationNode, reporterNode)
    builder.add_edge(reporterNode, END)
    logger.info("Graph Built")
    return builder.compile()

# g=graph_builder(logging.getLogger())
# data="""
# [FTTH-88640] Remove not needed data from pod and k3s formula

# [FTTH-82655]: SCA version change

# [FTTH-71070] Covering unit test cases for lcm handlerengine and rancher

# [FTTH-88821] Exposing probes config in Values.yaml

# [FTTH-88414] Negname normalization in cleanup
# """
# o=g.invoke({"messages": data})
# print(o['report'])
