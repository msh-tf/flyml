import pandas
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.preprocessing import LabelEncoder


user_artists = pandas.read_csv(
    '/Users/manas.hardas/projects/event_recommender/user_artist_dataset_2016.csv'
)

# Generate an index for userids and attractionids (items)
# Userids are not incremented by 1 starting from 0. Therefore we map the userids
# and attractionids to an index starting from 0 and incremented by.

le = LabelEncoder()
le.fit(user_artists['user_user_id'])
user_index = le.transform(user_artists['user_user_id'])

user_index_mapping = pandas.DataFrame({
    'user_id': user_artists['user_user_id'],
    'user_email_address': user_artists['user_email_address'],
    'user_first_name': user_artists['user_first_name'],
    'user_last_name': user_artists['user_last_name'],
    'app_id': user_index
})
user_index_mapping.set_index('app_id')
writeable_users = user_index_mapping.drop_duplicates(subset=['user_id'])

le = LabelEncoder()
le.fit(user_artists['attraction_attraction_id'])
attraction_index = le.transform(user_artists['attraction_attraction_id'])

attraction_index_mapping = pandas.DataFrame({
    'app_id': attraction_index,
    'attraction_id': user_artists['attraction_attraction_id'],
    'attraction_name': user_artists['attraction_attraction_name'],
    'attraction_event_name': user_artists['event_event_name'],
    'attraction_start_datetime': user_artists['event_start_datetime']
})
attraction_index_mapping.set_index('app_id')
writeable_attractions = attraction_index_mapping.drop_duplicates(
    subset=['attraction_id'])


# generate the user-attraction   matrix
mat = coo_matrix((
    np.ones(user_index.shape[0]),       # weights
    (user_index, attraction_index)      # adjacency list
))
useritemdf = mat.toarray()
itemuserdf = useritemdf.transpose()
