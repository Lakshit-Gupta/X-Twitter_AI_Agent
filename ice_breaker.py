from typing import Tuple
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
from agents.twitter_lookup_agents import lookup as twitter_lookup_agent
from output_parsers import person_intel_parser, PersonIntel
from third_party.twitter import scrape_user_tweets, get_profile_image_url


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    # 1) Lookup Twitter username and fetch real tweets
    tweets = []
    try:
        twitter_username = twitter_lookup_agent(name=name)
        print(f"Found Twitter username: {twitter_username}")
        if twitter_username:
            tweets = scrape_user_tweets(username=twitter_username, num_tweets=5) or []
            if not tweets:
                print(f"Warning: No tweets found for @{twitter_username}")
        else:
            print("Warning: Twitter lookup returned empty username")
    except Exception as e:
        print(f"Error with Twitter lookup or scrape: {e}")
        tweets = []

    # 2) Build summary using available data (Twitter only; LinkedIn disabled)
    summary_template = """
         Given the following recent Twitter posts {twitter_information} about a person,
         create the following:
         1. a short professional summary
         2. two interesting facts about them
         3. a topic that may interest them
         4. two creative ice breakers to open a conversation with them
         If Twitter information is sparse or empty, use reasonable generalities based on typical professional backgrounds and clearly indicate uncertainty.
        \n{format_instructions}
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | person_intel_parser

    # Provide safe fallback for the LLM input
    twitter_info_for_llm = tweets if tweets else []

    result = chain.invoke({
        "twitter_information": twitter_info_for_llm,
    })

    # Get a profile picture from Twitter when possible
    profile_pic_url = None
    try:
        profile_pic_url = get_profile_image_url(twitter_username) if 'twitter_username' in locals() else None
    except Exception:
        profile_pic_url = None

    return result, profile_pic_url


if __name__ == "__main__":
    print("Hello LangChain!")
    result = ice_break(name="Harrison Chase")
    print(result)