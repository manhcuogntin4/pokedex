from pokedex.models.analytics import SearchHistory, AgentQuery,AgentQuerySearch
from flask import request

def add_pokemon_search_history(ip, search):
    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    return history

def add_agent_query(platform, browser, version, language, string):
    agent=AgentQuery.create(platform=platform,browser=browser,version=version,language=language,string=string)
    return agent
def add_agent_query_search(request,search):
    #print(request.user_agent)
    print(request.user_agent.platform, request.user_agent.browser, request.user_agent.version,request.user_agent.string)
    print(request.remote_addr, search)
    platform=request.user_agent.platform
    browser=request.user_agent.browser
    version=request.user_agent.version
    language=request.user_agent.language
    string=request.user_agent.string
    ip=request.remote_addr
    history=add_pokemon_search_history(ip,search)
    agent=add_agent_query(platform=platform,browser=browser,version=version,language=language,string=string)
    new_agent_query_search=AgentQuerySearch.create(agent=agent,search=history)
    return new_agent_query_search

def get_agent_request(platform):
    count=SearchHistory.select(SearchHistory,AgentQuerySearch).join(AgentQuerySearch).where(SearchHistory.id==AgentQuerySearch.search).join(AgentQuery).where(AgentQuery.id==AgentQuerySearch.agent).where(AgentQuery.platform==platform)
    count_agent={}
    count_agent[platform]=len(count)
    return count_agent
