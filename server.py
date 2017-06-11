from sanic import Sanic
from sanic.response import json
from annoy import AnnoyIndex
import random
from blaze import data, by, join, merge
from odo import odo
f = 300


# Load sqlite here
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

app = Sanic()

tables = data('sqlite:///../../db.db')
coin_table = tables['coins']

# Compress the information
coin_tables_comp = by(coin_table.name, sentences=coin_table.sentences)

# Prepare to use annoy
ctl = len(coin_tables_comp)
item_arr_set = []
item_names = [i[0] for i in coin_tables_comp]

# Initialize and fill annoy
t = AnnoyIndex(f)  # Length of item vector that will be indexed
for i in range(ctl):
    v = [random.gauss(0, 1) for z in range(f)]
    t.add_item(i, v)
    item_arr_set.append((item_names[i], i))

t.build(10) # 10 trees
t.save('../../test.ann')


annoy_index_table = data(item_arr_set, fields=['name', 'annoyindex'])

# Initialize sqlalchemy
engine = create_engine('sqlite:///../../db.db')
meta = MetaData()
meta.reflect(bind=engine)
annoy_table = meta.tables['annoy']


def list_number_to_text(list_num):
    list_text = []
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in list_num:
        list_text.append(session.query(annoy_table).filter(annoy_table.c.annoyindex == i).first()[0])
    return list_text

# PERFECT!!!! Now let's create a function to grab nearest node by name
def get_nn_by_name(name):
    Session = sessionmaker(bind=engine)
    session = Session()
    # This command should be used to
    name_string = "%{0}%".format(name)
#     print(name_string)
    result = session.query(annoy_table).filter(annoy_table.c.name.like(name_string)).first()
    u = AnnoyIndex(f)
    u.load('../../test.ann') # super fast, will just mmap the file
    list_of_near = u.get_nns_by_item(result[1], 4) # will find the 5 nearest neighbors
    # remove current node
    list_of_near.remove(result[1])
    return list_of_near


@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route('/getRecommendation')
async def recomm(request):
    rargs = request.raw_args
    coins = list_number_to_text(get_nn_by_name(rargs['coin']))
    # coins = get_nn_by_name(rargs['coin'])
    return json({"recommendations": coins})


@app.route("/domath")
async def DoMath(request):
    rargs = request.raw_args
    return json({"result": ['return', 'two possible cryptos'], "query_string": rargs, "message": 'Would {0} between {1} and {2}'.format(rargs['operator'], rargs['coin1'], rargs['coin2'])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

