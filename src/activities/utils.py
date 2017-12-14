from activities.models import Category

def handle_activity_category(name):
    category_name = name.lower().title()
    category = Category.objects.filter(name=category_name).first()

    if not category:
        category = Category.objects.create(name=category_name)

    return category