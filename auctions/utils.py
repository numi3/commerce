from .models import *

def fix_auctions():
    # Update is_active for expired auctions:
    fix_expired(timezone.now())

    # fix is_active for non-expired auctions:
    fix_non_expired(timezone.now())


def fix_expired(current_time):
    conditions = [
        Auction.objects.filter(is_active=True,end_time__lte=current_time),
        Auction.objects.filter(is_active=True, winner__isnull=False)
    ]
    
    for expired_auction in conditions:
        expired_auction.update(is_active=False)


def fix_non_expired(current_time):
    conditions = [
        Auction.objects.filter(is_active=False, end_time__gt=current_time, winner=None),
        
    ]

    for non_expired_auction in conditions:
        non_expired_auction.update(is_active=True)

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
            