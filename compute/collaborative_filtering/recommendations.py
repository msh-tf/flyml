from datasets import useritemdf
from datasets import itemuserdf
from recommend.models import User
from recommend.models import Attraction
from recommend.models import SimilarUsers
from recommend.models import SimilarAttractions
from itertools import chain
import pandas as pd


# extract recommendations and store in db
def get_attraction_recommendations_by_user(**kwargs):
    try:
        user=kwargs['user']
        n=kwargs['n']
    except KeyError as ke:
        print('Key error: ',ke)
        print('Enter ', ke)

    # get userids purchase history
    user_app_id = User.objects.filter(user_id=user).values('app_id')[0]['app_id']
    attr_app_ids = useritemdf[user_app_id].nonzero()[0]
    users_attraction_history = \
        [Attraction.objects.filter(app_id=a).value('attraction_id')[0]['attraction_id'] for a in attr_app_ids]
    candidates = []

    # go through purchase history and populate candidate list
    for i in users_attraction_history:
        result = SimilarAttractions.objects.filter(attraction_id=i).values()
        candidates = list(chain(candidates, result))

    if candidates!=[]:
        deduped_recos = pd.DataFrame(candidates).drop_duplicates(
            subset=['similar_attraction_id'])
        res = deduped_recos.sort_values('similarity', ascending=False)[:n]
        res = res.to_dict(orient='records')
    else:
        res = []

    return res


# function to take itemid adn return recommended users
def get_user_recommendations_by_attraction(**kwargs):
    try:
        attraction = kwargs['attraction']
        n=kwargs['n']
    except KeyError as ke:
        print('Key error: ',ke)
        print('Enter ', ke)

    # get userids purchase history
    attr_app_id = Attraction.objects.filter(attraction_id=attraction).value('app_id')[0]['app_id']
    user_app_ids = itemuserdf[attr_app_id].nonzero()[0]
    attractions_user_history = \
        [User.objects.filter(app_id=u).values('user_id')[0]['user_id'] for u in user_app_ids]
    candidates = []

    # go through purchase history and populate candidate list
    for i in attractions_user_history:
        result = SimilarUsers.objects.filter(user_id=i).values()
        candidates = list(chain(candidates, result))

    if candidates!=[]:
        deduped_recos = pd.DataFrame(candidates).drop_duplicates(
            subset=['similar_user_id'])
        res = deduped_recos.sort_values('similarity', ascending=False)[:n]
        res = res.to_dict(orient='records')
    else:
        res = []

    return res
