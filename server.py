from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/domath")
async def DoMath(request):
    rargs = request.raw_args
    return json({"result": ['return', 'two possible cryptos'], "query_string": rargs, "message": 'Would {0} between {1} and {2}'.format(rargs['operator'], rargs['coin1'], rargs['coin2'])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

