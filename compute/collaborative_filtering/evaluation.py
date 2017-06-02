import pandas as pd
from itertools import chain
from compute.collaborative_filtering import useritemdf, itemuserdf
from compute.collaborative_filtering import \
    attraction_index_mapping, user_artists
from recommend.models import User, Attraction, SimilarUsers, SimilarAttractions
from numpy import mean
from operator import itemgetter, attrgetter
from sklearn.model_selection import train_test_split
import time


def useritem_offline_metrics_at_K(K):
    user_item_train, user_item_test = train_test_split(
        pd.DataFrame(useritemdf),
        test_size=0.25
    )
    precision=[]
    recall=[]
    accuracy=[]
    diffdate=0
    samedate=0
    for user_app_id in user_item_test.index:
        attr_app_ids = useritemdf[user_app_id].nonzero()[0]
        cases = len(attr_app_ids)
        history = sorted(
            [
                (Attraction.objects.filter(
                    app_id=a).values('attraction_id')[0]['attraction_id'],
                attraction_index_mapping.query(
                    'app_id=='+str(a))[:1]['attraction_start_datetime'].iloc[0])
                for a in attr_app_ids
            ],
            key=itemgetter(1)
        )
        not_same_date_events =  \
            False in [True if i[1]==history[0][1] else False for i in history]
        if (cases>2) and (not_same_date_events):
            diffdate+=1
            history = [i[0] for i in history]
            held=[]
            actual=[]
            candidates=[]
            held=history[:cases/2]
            actual=history[cases/2:]
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
            guessed_right = len(set(actual).intersection(set(recommended)))
            precision.append(float(guessed_right)/len(recommended))
            recall.append(float(guessed_right)/len(actual))
        else:
            samedate+=1
    print 'Cases with same date: {0}, with diff date: {1}'.format(
        samedate, diffdate
    )
    return mean(precision), mean(recall)


def itemuser_offline_metrics_at_K(K):
    item_train, item_test = train_test_split(
        pd.DataFrame(itemuserdf),
        test_size=0.25
    )
    print 'train.shape={0}, test.shape={1}'.format(item_train.shape, item_test.shape)
    precision=[]
    recall=[]
    diffdate=0
    samedate=0
    for item_app_id in item_test.index[:5]:
        print '\nitem_app_id: ', item_app_id
        usr_app_ids = itemuserdf[item_app_id].nonzero()[0]
        print 'usr_app_ids: ', usr_app_ids
        cases = len(usr_app_ids)
        history=[]
        for u in usr_app_ids:
            uid = User.objects.filter(
                app_id=u).values('user_id')[0]['user_id']
            trans_date = user_artists.query(
                'user_user_id=='+str(uid))[:1]['trans_datetime_of_sale'].iloc[0]
            history.append((uid, trans_date))
        history = sorted(history, key=itemgetter(1))
        not_same_date_users =  \
            False in [True if i[1]==history[0][1] else False for i in history]
        if (cases>2) and (not_same_date_users):
            diffdate+=1
            history = [i[0] for i in history]
            print 'history: ', history
            held=[]
            actual=[]
            candidates=[]
            held=history[:cases/2]
            actual=history[cases/2:]
            for h in held:
                result = SimilarUsers.objects.filter(
                    user_id=h).values('similar_user_id', 'similarity')
                candidates = list(chain(candidates, result))
            if candidates!=[]:
                sim_sorted = sorted(
                    candidates, key=lambda k: k['similarity'], reverse=True
                )
                recommended = list(
                    set([r['similar_user_id'] for r in sim_sorted])
                )[:K]
            print 'recommended: ', recommended
            guessed_right = len(set(actual).intersection(set(recommended)))
            precision.append(float(guessed_right)/len(recommended))
            recall.append(float(guessed_right)/len(actual))
        else:
            samedate+=1
    print 'Cases with same date: {0}, with diff date: {1}'.format(
        samedate, diffdate
    )
    return mean(precision), mean(recall)


def crossvalidation(f, num_folds, K):
    precisionatK=[]
    recallatK=[]
    for k in K:
        print '\nk={0} neighbors'.format(k)
        precisionfolds=[]
        recallfolds=[]
        for i in range(num_folds):
            start = time.time()
            p, r = f(k)
            print 'Fold number {0} - Precision: {1}, Recall: {2} \
                (Execution time {3} mins) '.format(
                i, p, r, (time.time()-start)/float(60)
            )
            precisionfolds.append(p)
            recallfolds.append(r)
        precisionatK.append(mean(precisionfolds))
        recallatK.append(mean(recallfolds))
    return precisionatK, recallatK


crossvalidation(useritem_offline_metrics_at_K, 3, [35])
crossvalidation(itemuser_offline_metrics_at_K, 1, [10])
