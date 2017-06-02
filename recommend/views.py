from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from compute.collaborative_filtering import \
    get_attraction_recommendations_by_user
from compute.collaborative_filtering import \
    get_user_recommendations_by_attraction
from models import User, SimilarUsers
from models import Attraction, SimilarAttractions
from django.core import serializers
from django.shortcuts import render
from itertools import chain
import json


def index(request):
    context = {'data': "Hello, world. This is the ticketfly machine learning server"}
    return render(request, 'recommend/index.html', context)


def get_user_info(request, userid):
    simuids = [s['similar_user_id'] for s in list(
        SimilarUsers.objects.filter(user_id=userid).values('similar_user_id'))]
    simusersdictlist = [list(User.objects.filter(user_id=s).values(
        'first', 'last', 'email')) for s in simuids]
    simusers=[]
    for u in simusersdictlist:
        f = u[0]['first']
        l = u[0]['last']
        e = u[0]['email']
        simusers.append(f+" "+l+" ("+e+")")

    history, recs = get_attraction_recommendations_by_user(
        user=int(userid), n=10
    )
    recattrs = [a['similar_attraction_id'] for a in recs]
    recattdictlist = [list(Attraction.objects.filter(
            attraction_id=s).values('attraction_name')) for s in recattrs]
    recattnames = [str(s[0]['attraction_name']) for s in recattdictlist]

    seenattrdictlist = [list(Attraction.objects.filter(
            attraction_id=s).values('attraction_name')) for s in history]
    seen_attrs = [str(s[0]['attraction_name']) for s in seenattrdictlist]

    context = {
        'data': {
            'user': userid,
            'similar_users': simusers,
            'recommended_attractions': recattnames,
            'seen_attractions': seen_attrs
        }
    }
    return render(request, 'recommend/user_info_lists.html', context)


def make_attraction_info_json_response(attrid, simattrs, recusers):
    res = {
        'attraction': attrid,
        'similar_attractions': simattrs,
        'recommended_users': recusers
    }
    return res


def get_attraction_info(request, attrid):
    simattrs = list(
        SimilarAttractions.objects.filter(attraction_id=attrid).values()[:10])
    recusers = get_user_recommendations_by_attraction(
        attraction=int(attrid), n=10)
    return JsonResponse(
        make_attraction_info_json_response(attrid, simattrs, recusers),
        safe=False
    )
