"""Project-authored source used only for static inspection."""


def total(items):
    return sum(item["price"] for item in items)
