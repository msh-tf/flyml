import time
import pandas
from django.utils import timezone
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.preprocessing import LabelEncoder


user_artists = pandas.read_csv(
    '/Users/manas.hardas/projects/event_recommender/user_artist_dataset.csv'
)

# Generate an index for userids and attractionids (items)
# Userids are not incremented by 1 starting from 0. Therefore we map the userids
# and attractionids to an index starting from 0 and incremented by.

def generate_user_index():
    le = LabelEncoder()
    le.fit(user_artists['user_dim_id'])
    user_index = le.transform(user_artists['user_dim_id'])
    return user_index

def generate_user_index_mapping():
    user_index_mapping = pandas.DataFrame({
        'user_dim_id': user_artists['user_dim_id'],
        'user_email_address': user_artists['user_email_address'],
        'serial': user_index
    })
    user_index_mapping.set_index('serial')
    return user_index_mapping

def generate_attraction_index():
    le = LabelEncoder()
    le.fit(user_artists['attraction_attraction_id'])
    attraction_index = le.transform(user_artists['attraction_attraction_id'])
    return attraction_index

def generate_attraction_index_mapping():
    attraction_index_mapping = pandas.DataFrame({
        'serial': attraction_index,
        'attraction_id': user_artists['attraction_attraction_id'],
        'attraction_name': user_artists['attraction_attraction_name']
    })
    attraction_index_mapping.set_index('serial')
    return attraction_index_mapping


# generate the user-attraction   matrix
mat = coo_matrix((
    np.ones(user_index.shape[0]),       # weights
    (generate_user_index(), generate_attraction_index())      # adjacency list
))
df = mat.toarray()
useritemdf = pandas.DataFrame(df)
itemuserdf = pandas.DataFrame(df.transpose())
