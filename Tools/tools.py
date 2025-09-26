from langchain_community.utilities import SerpAPIWrapper
import os
from dotenv import load_dotenv

load_dotenv()


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__(
            serpapi_api_key=os.getenv("SERPAPI_API_KEY")
        )

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(name: str):
    """Searches for LinkedIn Profile Page."""
    search = CustomSerpAPIWrapper()
    res = search.run(f"site:linkedin.com/in/ {name}")
    return res


def get_twitter_profile_url(name: str):
    """Searches for Twitter Profile Page."""
    search = CustomSerpAPIWrapper()
    res = search.run(f"site:twitter.com {name} OR site:x.com {name}")
    return res
# from langchain.utilities import SerpAPIWrapper
# from langchain_community.tools.tavily_search import TavilySearchResults
#
#
# class CustomSerpAPIWrapper(SerpAPIWrapper):
#     def __init__(self):
#         super(CustomSerpAPIWrapper, self).__init__()
#
#     @staticmethod
#     def _process_response(res: dict) -> str:
#         """Process response from SerpAPI."""
#         if "error" in res.keys():
#             raise ValueError(f"Got error from SerpAPI: {res['error']}")
#         if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
#             toret = res["answer_box"]["answer"]
#         elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
#             toret = res["answer_box"]["snippet"]
#         elif (
#             "answer_box" in res.keys()
#             and "snippet_highlighted_words" in res["answer_box"].keys()
#         ):
#             toret = res["answer_box"]["snippet_highlighted_words"][0]
#         elif (
#             "sports_results" in res.keys()
#             and "game_spotlight" in res["sports_results"].keys()
#         ):
#             toret = res["sports_results"]["game_spotlight"]
#         elif (
#             "knowledge_graph" in res.keys()
#             and "description" in res["knowledge_graph"].keys()
#         ):
#             toret = res["knowledge_graph"]["description"]
#         elif "snippet" in res["organic_results"][0].keys():
#             toret = res["organic_results"][0]["link"]
#
#         else:
#             toret = "No good search result found"
#         return toret
#
#
# def get_profile_url(name: str):
#     """Searches for Linkedin or twitter Profile Page."""
#     search = CustomSerpAPIWrapper()
#     res = search.run(f"{name}")
#     return res
#
#
# # --- Compatibility aliases (added) ---
# # Several agent files expect functions named `url_profile_search_travily`
# # or `get_profile_url_tavily` (typos / naming variants). Provide small
# # wrapper functions that call the canonical `get_profile_url`. This
# # avoids changing multiple agent files and keeps behavior unchanged.
#
# def url_profile_search_travily(name: str):
#     """
#     Compatibility wrapper used by agents.linkedin_lookup_agents and
#     agents.twitter_lookup_agents (keeps original repo naming).
#     """
#
#     return get_profile_url(name)
#
#
# def get_profile_url_tavily(name: str):
#     """
#     Another compatibility wrapper — mirrors a misspelled name found in
#     twitter_lookup_agents (keeps backwards compatibility).
#     """
#     search = TavilySearchResults()
#     get_profile_url = search.run(f"{name}")
#     return get_profile_url