from django.db import migrations
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Category = apps.get_model("trips", "Category")
    for category in Category.objects.all():
        if not category.slug:
            category.slug = slugify(category.name)
            category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_populate_category_slugs'),  
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]
