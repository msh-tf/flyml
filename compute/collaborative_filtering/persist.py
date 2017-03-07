from django.utils import timezone

from datasets import writeable_users
from datasets import writeable_attractions
from datasets import useritemdf
from datasets import itemuserdf

from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import LSHForest

from recommend.models import User, Attraction
from recommend.models import SimilarUsers
from recommend.models import SimilarAttractions


def persist_user_data_to_db():
    for i, u in writeable_users.iterrows():
        try:
            u = User(
                app_id = u['app_id'],
                user_id = u['user_id'],
                email = u['user_email_address'],
                first = u['user_first_name'],
                last = u['user_last_name']
            )
            u.save()
        except Exception as ex:
            print(ex)


def persist_attractions_data_to_db():
    for i, e in writeable_attractions.iterrows():
        try:
            e = Attraction(
                app_id = e['app_id'],
                attraction_id = e['attraction_id'],
                attraction_name = e['attraction_name']
            )
            e.save()
        except Exception as ex:
            print(ex)


def persist_user_similarities_to_db():
    # build LSHForest model for reduced dimension dataset
    svd = TruncatedSVD(n_components=10, n_iter=7)
    red_dim_useritemdf = svd.fit_transform(useritemdf)
    user_item_model = LSHForest()
    user_item_model.fit(red_dim_useritemdf)

    # persist user similarities to db
    K=20        # query for K neighbors
    k=10        # return k neighbors
    for i in range(useritemdf.shape[0]):
        distance, indices = user_item_model.kneighbors(
            red_dim_useritemdf[i].reshape(1, -1), n_neighbors=K
        )
        weights = 1 - distance
        for j in range(k):
            if i != indices[0][j]:
                s = SimilarUsers(
                    user_id=User.objects.filter(
                        app_id=int(i)).values('user_id')[0]['user_id'],
                    similar_user_id=User.objects.filter(
                        app_id=int(indices[0][j])).values('user_id')[0]['user_id'],
                    similarity=weights[0][j],
                    ts=timezone.now()
                )
                s.save()


def persist_attraction_similarities_to_db():
    # build LSHForest model for reduced dimension dataset
    svd = TruncatedSVD(n_components=10, n_iter=7)
    red_dim_itemuserdf = svd.fit_transform(itemuserdf)
    item_user_model = LSHForest()
    item_user_model.fit(red_dim_itemuserdf)

    # persist attractions similarities to db
    K=20        # query for K neighbors
    k=10        # return k neighbors
    for i in range(itemuserdf.shape[0]):
        distance, indices = item_user_model.kneighbors(
            red_dim_itemuserdf[i].reshape(1, -1), n_neighbors=K
        )
        weights = 1 - distance
        for j in range(k):
            if i != indices[0][j]:
                e = SimilarAttractions(
                    attraction_id=Attraction.objects.filter(
                        app_id=int(i)).values('attraction_id')[0]['attraction_id'],
                    similar_attraction_id=Attraction.objects.filter(
                        app_id=int(indices[0][j])).values('attraction_id')[0]['attraction_id'],
                    similarity=weights[0][j],
                    ts=timezone.now()
                )
                e.save()
