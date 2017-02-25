from datasets import user_index_mapping
from datasets import attraction_index_mapping


def get_id_for_serial(**kwargs):
    try:
        try:
            serial=kwargs['serial']
            id_type=kwargs['id_type']
        except (KeyError, UnboundLocalError) as err:
            print(err)

        if id_type=='user':
            row = user_index_mapping.query('serial=='+str(serial)).head(1)
            dim_id = row['user_dim_id'][row.index[0]]
        elif id_type=='attraction':
            row = attraction_index_mapping.query('serial=='+str(serial)).head(1)
            dim_id = row['attraction_id'][row.index[0]]
    except Exception as error:
        print(error)
    return dim_id


def get_serial_for_id(**kwargs):
    try:
        try:
            iid=kwargs['id']
            serial_type=kwargs['serial_type']
        except (KeyError, UnboundLocalError) as err:
            print(err)

        if serial_type=='user':
            row = user_index_mapping.query('user_dim_id=='+str(iid)).head(1)
            serial = row['serial'][row.index[0]]
        elif serial_type=='attraction':
            row = attraction_index_mapping.query(
                'attraction_id=='+str(iid)).head(1)
            serial = row['serial'][row.index[0]]
    except Exception as error:
        print(error)
    return serial
