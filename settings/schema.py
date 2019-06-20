import graphene

import shorturls.schema


class Query(shorturls.schema.Query, graphene.ObjectType):
    """Collects all Queries from across project"""


class Mutation(shorturls.schema.Mutation, graphene.ObjectType):
    """Collects all Mutations from across project"""


schema = graphene.Schema(query=Query, mutation=Mutation)
