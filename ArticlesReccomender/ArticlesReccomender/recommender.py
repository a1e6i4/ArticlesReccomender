import pandas as pd
from surprise import SVD
from articles.models import *
from surprise import Dataset, Reader


class SVDRecommender:
    def __init__(self):
        self.algo = SVD()
        #self.fit()

    def fit(self):
        likes = Like.objects.all()
        # add likes to dataset
        dataset = pd.DataFrame([(like.user.id, like.article.id, like.rating) for like in likes],
                               columns=['user_id', 'article_id', 'rating'])

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(dataset, reader)
        trainset = data.build_full_trainset()

        self.algo.fit(trainset)

    def predict(self, user_id, article_id):
        return self.algo.predict(user_id, article_id).est

    def get_recommendations(self, user_id, n=5):
        articles = Article.objects.all()
        article_ids = [article.id for article in articles]
        predictions = [self.predict(user_id, article_id) for article_id in article_ids]
        predictions = pd.DataFrame({'article_id': article_ids, 'prediction': predictions})
        predictions = predictions.sort_values('prediction', ascending=False)
        predictions = predictions.iloc[:n]

        result = []
        for index, row in predictions.iterrows():
            article = Article.objects.get(id=row['article_id'])
            result.append(article)
        return result


recommendation_engine = SVDRecommender()


