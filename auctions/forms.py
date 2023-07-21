from django.utils import timezone
from django import forms
from .models import Auction, Bid, Comment, Watchlist
from django.core.validators import MinValueValidator
from decimal import Decimal


class AuctionForm(forms.ModelForm):
    
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "image_url",
            "category",
            "end_time",
            "starting_bid"
        ]
        
        widgets = {
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "starting_bid": forms.NumberInput(attrs={"min": "0", "value": "5.00", "step": 1})
        }
        
        
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 6:
            raise forms.ValidationError("Title must be at least 6 characters long.")
        return title
    
    
    def clean_end_time(self):
        if end_time := self.cleaned_data.get("end_time"):
            current_time = timezone.now()
            time_difference = end_time - current_time
            if time_difference.total_seconds() <= 3600:
                raise forms.ValidationError("The end time must be at least 1 hour from the current time.")
            elif time_difference.days > 180:
                raise forms.ValidationError("The end time cannot be more than 180 days from the current time.")
        return end_time

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        
    def clean_amount(self):
        
        amount = self.cleaned_data.get("amount")        
        try:
            current_auction = Auction.objects.get(id=self.initial.get("auction_id"))
            starting_bid = Decimal(current_auction.starting_bid)
            
            # check if higher than starting bid:
            if amount < starting_bid:
                raise forms.ValidationError("Cannot bid less than the starting bid.")

            # check if higher than current bid if exists.
            if current_auction.current_bid is not None:
                current_bid = Decimal(current_auction.current_bid.amount)
                if amount <= current_bid:
                    raise forms.ValidationError("Cannot bid less than the current bid.")
            return amount
        except Auction.DoesNotExist:
            raise forms.ValidationError("Auction does not exist.")

