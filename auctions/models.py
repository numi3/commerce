from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Auction(models.Model):
    """
    This class represents an auction listing.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    image_url = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Auction"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    end_time = models.DateTimeField()

    bid_count = models.IntegerField(default=0)
    starting_bid = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    current_bid = models.ForeignKey(
        "Bid",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auction_bids"
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="winner"
    )

    
    def bid_status(self):
        if self.is_active:
            if self.current_bid:
                return f"Current bid: {self.current_bid.amount:,}$ by {self.current_bid.bidder}."
            return f"Starting bid: {self.starting_bid:,}$."
        if self.winner:
            return f"Auction was won by {self.winner} for {self.current_bid.amount:,}$."
        return "Unfortunately, nobody has won the auction :("
    
    
    def short_desc(self):
        data = self.description
        info = (data[:124] + '..') if len(data) > 124 else data
        return info
    
    def __str__(self):
        return f"#{self.id:,} {self.title} - {self.bid_status()}"

class Bid(models.Model):
    auction_id = models.ForeignKey(
        "Auction",
        on_delete=models.CASCADE,
        related_name="auction_bids"
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bids"
    )
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.amount}$"

class Comment(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="auction_comments"
    )
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_comments"
    )
    content = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist_user"
    )
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="watchlist_auction"
    )
    
    class Meta:
        unique_together = (("user", "auction"),)
    
    def __str__(self):
        return f"{self.user} -> {self.auction}"