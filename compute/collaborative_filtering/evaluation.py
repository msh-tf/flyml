import pandas as pd
from itertools import chain
from compute.collaborative_filtering import useritemdf, itemuserdf
from compute.collaborative_filtering import attraction_index_mapping
from recommend.models import User, Attraction, SimilarUsers, SimilarAttractions
from numpy import mean
from operator import itemgetter, attrgetter
import time


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
        # print ('User app id: ', user_app_id)
        attr_app_ids = useritemdf[user_app_id].nonzero()[0]
        cases = len(attr_app_ids)
        users_attraction_history = sorted(
            [
                (Attraction.objects.filter(
                    app_id=a).values('attraction_id')[0]['attraction_id'],
                attraction_index_mapping.query(
                    'app_id=='+str(a))[:1]['attraction_start_datetime'].iloc[0])
                for a in attr_app_ids
            ],
            key=itemgetter(1)
        )
        users_attraction_history = [i[0] for i in users_attraction_history]
        # print 'Users attraction history: ', users_attraction_history
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
                sim_sorted = sorted(
                    candidates, key=lambda k: k['similarity'], reverse=True
                )
                recommended = list(
                    set([r['similar_attraction_id'] for r in sim_sorted])
                )[:K]
                # print 'Recommended: ', recommended
            guessed_right = len(set(actual).intersection(set(recommended)))
            precision.append(float(guessed_right)/len(recommended))
            recall.append(float(guessed_right)/len(actual))
            # print 'Precision: {0}, Recall: {1}'.format(
            #     precision[-1], recall[-1]
            # )
    return mean(precision), mean(recall)


def crossvalidation(num_folds, K):
    precisionatK=[]
    recallatK=[]
    for k in K:
        print 'k={0} neighbors'.format(k)
        precisionfolds=[]
        recallfolds=[]
        for i in range(num_folds):
            start = time.time()
            p, r = offline_metrics_at_K(k)
            print 'Fold number {0} - Precision: {1}, Recall: {2} (Execution time {3}) '.format(
                i, p, r, time.time()-start)
            precisionfolds.append(p)
            recallfolds.append(r)
        precisionatK.append(mean(precisionfolds))
        recallatK.append(mean(recallfolds))
    return precisionatK, recallatK

crossvalidation(3, [5, 10, 15, 20])
