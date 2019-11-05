from peewee import *

from .database import db


class CommonModel(Model):
    class Meta:
        database = db
        schema = 'analytics'


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()

class AgentQuery(CommonModel):
    id=PrimaryKeyField()
    platform=CharField(null = True)
    browser=CharField(null = True)
    version=CharField(null = True)
    language=CharField(null = True)
    string=CharField(null = True)
class AgentQuerySearch(CommonModel):
    id=PrimaryKeyField()
    agent=ForeignKeyField(AgentQuery)
    search=ForeignKeyField(SearchHistory)

with db:
    SearchHistory.create_table(fail_silently=True)
    AgentQuery.create_table(fail_silently=True)
    AgentQuerySearch.create_table(fail_silently=True)
