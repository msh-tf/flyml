from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from compute.collaborative_filtering import \
    get_attraction_recommendations_by_user
from compute.collaborative_filtering import \
    get_user_recommendations_by_attraction
from models import SimilarUsers
from models import SimilarAttractions


def index(request):
    return HttpResponse(
        "Hello, world. This is the ticketfly machine learning server"
    )


def make_user_info_json_response(userid, simusers, recattrs):
    res = {
        'user': userid,
        'similar_users': simusers,
        'recommended_attractions': recattrs
    }
    return res


def get_user_info(request, userid):
    simusers = list(
        SimilarUsers.objects.filter(user_dim_id=userid).values()[:10])
    recattrs = get_attraction_recommendations_by_user(user=int(userid), n=20)
    return JsonResponse(
        make_user_info_json_response(userid, simusers, recattrs),
        safe=False
    )


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
