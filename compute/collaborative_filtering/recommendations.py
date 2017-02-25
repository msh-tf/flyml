from datasets import useritemdf
from datasets import itemuserdf
from recommend.models import SimilarUsers
from recommend.models import SimilarAttractions
from itertools import chain
import pandas as pd
from util import get_id_for_serial
from util import get_serial_for_id


# extract recommendations and store in db
def get_attraction_recommendations_by_user(**kwargs):
    try:
        user=kwargs['user']
        n=kwargs['n']
    except KeyError as ke:
        print('Key error: ',ke)
        print('Enter ', ke)

    # get userids purchase history
    user_serial = get_serial_for_id(id=user, serial_type='user')
    attr_serials = useritemdf[user_serial].nonzero()[0]
    users_attraction_history = \
        [get_id_for_serial(serial=s, id_type='attraction') for s in attr_serials]
    candidates = []

    # go through purchase history and populate candidate list
    for i in users_attraction_history:
        result = SimilarAttractions.objects.filter(attraction_id=i).values()
        candidates = list(chain(candidates, result))
    print(candidates)
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
    attr_serial = get_serial_for_id(id=attraction, serial_type='attraction')
    user_serials = itemuserdf[attr_serial].nonzero()[0]
    attractions_user_history = \
        [get_id_for_serial(serial=s, id_type='user') for s in user_serials]
    candidates = []

    # go through purchase history and populate candidate list
    for i in attractions_user_history:
        result = SimilarUsers.objects.filter(user_dim_id=i).values()
        candidates = list(chain(candidates, result))

    if candidates!=[]:
        deduped_recos = pd.DataFrame(candidates).drop_duplicates(
            subset=['similar_user_dim_id'])
        res = deduped_recos.sort_values('similarity', ascending=False)[:n]
        res = res.to_dict(orient='records')
    else:
        res = []

    return res
