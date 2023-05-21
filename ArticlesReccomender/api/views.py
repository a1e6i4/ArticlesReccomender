import os

from articles.models import *
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework import status
from rest_framework.decorators import action
from elsapy.elssearch import ElsSearch
from elsapy.elsclient import ElsClient
import json
from collections import Counter
from ArticlesReccomender.recommender import recommendation_engine


client = ElsClient(os.getenv('SCOPUS_API_KEY'))
client.inst_token = ""


class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=['get'])
    def get_user(self, request):
        id_t = request.query_params.get('id')
        user = User.objects.get(id_t=id_t)
        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        users = User.objects.filter(id_t=int(request.data.get("id")))
        if len(users) == 0:
            user = User(
                username=request.data.get("username"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                password=request.data.get("id"),
                id_t=request.data.get("id")
            )
            user.save()
            return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'user already exists'})


class ArticleViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        return Response(ArticleSerializer(article).data)

    def list(self, request):
        articles = Article.objects.all()
        return Response(ArticleSerializer(articles, many=True).data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get("q", None)
        doc_srch = ElsSearch(f"((TITLE {query}) OR (KEY {query})) AND SUBJAREA(COMP)", 'scopus')
        doc_srch.execute(client, get_all=False)

        for article in doc_srch.results:
            try:
                new_article = Article(
                    doi=article["prism:doi"],
                    title=article["dc:title"],
                    url=article["prism:url"]
                )
                new_article.save()
            except Exception as e:
                print(e)

        return Response(doc_srch.results)

    @action(detail=False, methods=['get'])
    def like(self, request):
        doi = request.query_params.get('doi')
        article = Article.objects.get(doi=doi)

        user_id = request.query_params.get('user_id')
        rating = int(request.query_params.get('rating'))

        user = User.objects.get(id_t=user_id)
        like = Like(article=article,
                    user=user,
                    rating=rating)
        like.save()

        return Response(status=status.HTTP_200_OK, data={})

    @action(detail=False, methods=['get'])
    def recommend(self, request):
        recomendations = recommendation_engine.get_recommendations(request.query_params.get('user_id'))
        return Response(ArticleSerializer(recomendations, many=True).data)
