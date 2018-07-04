from aiohttp import web
import aiohttp_cors
import json
import threading
import fact_recommandation
import suggest_tags
import suggest_summary
import recommandation_news

############################################# USEFUL FUNCTIONS ##############################
#update instances every 10 min
def run_thread():
    threading.Timer(600.0, run_thread).start()
    
    fact_recommandation.update_data()
    


# other function
async def handle(request):
    function = request.match_info.get('function', "index")
    data = await request.json()
    if function == "getFact":
        response_obj = fact_recommandation.suggest_facts(data['tags'])
    elif function == "getTag":
        response_obj = suggest_tags.give_tags(data['link'])
    elif function == "getSummary":
        response_obj = suggest_summary.summarize_text(data['link'])
    

    elif function == "getTasteClient":
        response_obj = recommandation_news.compute_score(data['clientId'])

    #verifier que les facts/fun facts n'existent pas déjà
    elif function == "verifyFact":
        response_obj = fact_recommandation.verify_facts(data['tags'])
    elif function == "verifyFun":
        response_obj = fact_recommandation.verify_fun(data['tags'])
    

    else:
        response_obj = { 'status' : 'success' }
    return web.Response(text=json.dumps(response_obj))

####################################################################################################

# run
app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# update
resource = cors.add(app.router.add_resource("/{function}"))
cors.add(resource.add_route("POST", handle))

run_thread()
web.run_app(app, port=4040)
