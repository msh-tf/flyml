import pandas as pd
from itertools import chain
from compute.collaborative_filtering import useritemdf, itemuserdf
from recommend.models import User, Attraction
from numpy import mean

def offline_metrics_at_K(K):
    from sklearn.model_selection import train_test_split
    user_item_train, user_item_test = train_test_split(
        pd.DataFrame(useritemdf),
        test_size=0.25
    )

    precision=[]
    recall=[]
    accuracy=[]

    for user_app_id in user_item_test.index:
        attr_app_ids = useritemdf[user_app_id].nonzero()[0]
        cases = len(attr_app_ids)
        users_attraction_history = [
            Attraction.objects.filter(
                app_id=a).values('attraction_id')[0]['attraction_id']
            for a in attr_app_ids
        ]

        held=[]
        actual=[]
        candidates=[]
        if cases>2:
            held=users_attraction_history[:cases/2]
            actual=users_attraction_history[cases/2:]

            for h in held:
                result = SimilarAttractions.objects.filter(
                    attraction_id=h).values('similar_attraction_id', 'similarity')
                candidates = list(chain(candidates, result))

            if candidates!=[]:
                topK = sorted(
                    candidates, key=lambda k: k['similarity'], reverse=True)[:K]
                recommended = [r['similar_attraction_id'] for r in topK]

            guessed_right = len(set(actual).intersection(set(recommended)))
            precision.append(float(guessed_right)/len(recommended))
            recall.append(float(guessed_right)/len(actual))

    return mean(precision), mean(recall)


def crossvalidation(num_folds, K):
    precisionatK=[]
    recallatK=[]
    for k in K:
        precisionfolds=[]
        recallfolds=[]
        for i in range(num_folds):
            p, r = offline_metrics_at_K(k)
            precisionfolds.append(p)
            recallfolds.append(r)
        precisionatK.append(mean(precisionfolds))
        recallatK.append(mean(recallfolds))
    return precisionatK, recallatK

crossvalidation(3, [5,10,15,20])
