from .models import *

def sort_categories(auction_query):
    categories = {}
    for auction in auction_query:
        category = auction.category.title()
        if category not in categories:
            categories[category] = {
                "amount": 1,
                "auctions": [auction]
            }
        else:
            categories[category]["amount"] += 1
            categories[category]["auctions"].append(auction)
    return categories
            