import os
from dotenv import load_dotenv

from Tools.tools import get_profile_url
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
def lookup(name:str) ->str:
    llm=ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",)
    template="""Given the full name {name_of_person}, find their LinkedIn profile page URL. 
    Search specifically for 'site:linkedin.com/in/ {name_of_person}' to find their LinkedIn profile.
    Your answer should contain ONLY the LinkedIn URL starting with https://www.linkedin.com/in/"""

    prompt_template=PromptTemplate(template=template,input_variables=["name_of_person"])

    tools_for_agent =[
        Tool(name="Crawl Google 4 linkedin profile page",
             func=get_profile_url,
             description="useful for when you need Linkedin profile Page URL"
             )
                    ]
    react_prompt=hub.pull("hwchase17/react")
    agent=  create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor=AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True)
    result=agent_executor.invoke(input={"input":prompt_template.format_prompt(name_of_person=name)})
    linkedin_profile_url=result["output"]
    return linkedin_profile_url
if __name__ == '__main__':
    print(lookup(name="Eden Marco"))
