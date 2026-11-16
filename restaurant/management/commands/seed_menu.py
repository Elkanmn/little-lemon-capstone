from decimal import Decimal
from django.core.management.base import BaseCommand
from restaurant.models import MenuItem

DISHES = [
    {"title": "Greek Salad", "description": "Crisp cucumber, tomato, olives and feta.", "price": Decimal("12.50"), "inventory": 30, "category": "Starter"},
    {"title": "Bruschetta", "description": "Toasted bread with tomato, basil and olive oil.", "price": Decimal("8.00"), "inventory": 20, "category": "Starter"},
    {"title": "Lemon Pasta", "description": "Fresh pasta with lemon, parmesan and herbs.", "price": Decimal("16.50"), "inventory": 25, "category": "Main"},
    {"title": "Grilled Fish", "description": "Seasonal fish with roasted vegetables.", "price": Decimal("22.00"), "inventory": 15, "category": "Main"},
    {"title": "Lemon Cake", "description": "House-made citrus sponge cake.", "price": Decimal("7.50"), "inventory": 18, "category": "Dessert"},
]

class Command(BaseCommand):
    help = "Create demo menu items without duplicating existing records."

    def handle(self, *args, **options):
        count = 0
        for data in DISHES:
            _, created = MenuItem.objects.get_or_create(title=data["title"], defaults={k:v for k,v in data.items() if k != "title"})
            count += int(created)
        self.stdout.write(self.style.SUCCESS(f"Added {count} menu items."))
