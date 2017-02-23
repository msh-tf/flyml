from datasets import generate_user_index_mapping
from datasets import generate_attraction_index_mapping


def get_dim_id_for_serial(**kwargs):
    try:
        try:
            serial=kwargs['serial']
            dim_id_type=kwargs['dim_id_type']
        except (KeyError, UnboundLocalError) as err:
            print(err)

        if dim_id_type=='user':
            row = user_index_mapping.query('serial=='+str(serial)).head(1)
            dim_id = row['user_dim_id'][row.index[0]]
        elif dim_id_type=='attraction':
            row = attraction_index_mapping.query('serial=='+str(serial)).head(1)
            dim_id = row['attraction_id'][row.index[0]]
    except Exception as error:
        print(error)
    return dim_id


# extract recommendations and store in db
def get_attraction_recommendations_by_user(**kwargs):
    try:
        user = kwargs['user']
        n=kwargs['n']
    except KeyError as ke:
        print('Key error: ',ke)
        print('Enter ', ke)

    # get userids purchase history
    users_attraction_history = useritemdf[user].nonzero()[0]
    candidates = []

    # go through purchase history and populate candidate list
    for i in users_attraction_history:
        result = SimilarAttractions.objects.filter(attraction_id=i)
        candidates = list(chain(candidates, result))

    if candidates!=[]:
        deduped_recos = pandas.DataFrame(candidates).drop_duplicates(
            subset=['attraction_id'])
        res = deduped_recos.sort_values('similarity', ascending=False)[:n]
        res = res.to_dict(orient='records')
    else:
        res = []

    return res


# function to take itemid adn return recommended users
def get_user_recommendations_by_attraction(**kwargs):
    try:
        attraction = kwargs['attraction']
    except KeyError as ke:
        print('Key error: ',ke)
        print('Enter ', ke)

    # get userids purchase history
    attractions_user_history = itemuserdf[attraction].nonzero()[0]
    candidates = []

    # go through purchase history and populate candidate list
    for i in attractions_user_history:
        result = SimilarUsers.objects.filter(user_dim_id=i)
        candidates = list(chain(candidates, result))

    if candidates!=[]:
        deduped_recos = pandas.DataFrame(candidates).drop_duplicates(
            subset=['user_dim_id'])
        res = deduped_recos.sort_values('similarity', ascending=False)[:n]
        res = res.to_dict(orient='records')
    else:
        res = []

    return res
