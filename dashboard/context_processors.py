def bar(request):
    if not request.user.is_anonymous():
        return {"bar": 100 * (len(request.user.customer.assets.all()) / request.user.customer.asset_limit)}
    else:
        return {}