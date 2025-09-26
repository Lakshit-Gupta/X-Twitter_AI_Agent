from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from dotenv import load_dotenv
from Tools.tools import get_twitter_profile_url
load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """
       Given the name {name_of_person}, find their Twitter (X) profile page and extract their username.
       Search specifically for 'site:twitter.com {name_of_person}' or 'site:x.com {name_of_person}' to find their Twitter profile.
       From the Twitter URL (like https://twitter.com/username or https://x.com/username), extract ONLY the username part.
       The username should be 1-15 characters, containing only letters, numbers, and underscores.
       Your final answer should contain ONLY the username (without @ symbol or URL).
       Example: if you find https://twitter.com/elonmusk, return only: elonmusk"""
    tools_for_agent_twitter = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_twitter_profile_url,
            description="useful for when you need get the Twitter Page URL",
        ),
    ]

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm, tools=tools_for_agent_twitter, prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent_twitter, verbose=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    twitter_username = result["output"]

    return twitter_username