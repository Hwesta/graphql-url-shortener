import graphene
from graphene_django.types import DjangoObjectType

from .models import URLMapping

HOST_DOMAIN = "localhost"


class URLMappingType(DjangoObjectType):
    """Graphene object type for the URLMapping model"""
    class Meta:
        model = URLMapping
        only_fields = ("original_url", "short_url")

    def resolve_short_url(self, info):
        return f"http://{HOST_DOMAIN}/{self.short_url}"


class Query:
    """GraphQL queries for URL shortener"""

    url_by_short_url = graphene.Field(URLMappingType, short_url=graphene.String())

    def resolve_url_by_short_url(parent, info, short_url):
        return URLMapping.objects.get(short_url=short_url)


class URLMappingMutation(graphene.Mutation):
    """Mutation to add a new original URL & generate a short URL"""
    class Arguments:
        original_url = graphene.String(required=True)

    url_mapping = graphene.Field(URLMappingType)

    def mutate(self, info, original_url):
        short_url = URLMapping.generate_short_url()
        url_mapping = URLMapping.objects.create(
            original_url=original_url, short_url=short_url
        )
        return URLMappingMutation(url_mapping=url_mapping)


class Mutation:
    """GraphQL mutations for URL shortener"""
    create_short_url = URLMappingMutation.Field()
