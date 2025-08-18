from django.db import migrations
from django.utils.text import slugify

def generate_unique_slug(base, existing):
    base = base or "category"
    slug = base
    i = 2
    while slug in existing:
        slug = f"{base}-{i}"
        i += 1
    existing.add(slug)
    return slug

def populate_category_slugs(apps, schema_editor):
    Category = apps.get_model("trips", "Category")

    # Track existing slugs to avoid duplicates during the run
    existing = set(
        Category.objects.exclude(slug__isnull=True).exclude(slug="").values_list("slug", flat=True)
    )

    for cat in Category.objects.all():
        if not cat.slug:
            base = slugify(cat.name)
            cat.slug = generate_unique_slug(base, existing)
            cat.save(update_fields=["slug"])

class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0002_alter_category_options_category_slug"),
    ]

    operations = [
        migrations.RunPython(populate_category_slugs, migrations.RunPython.noop),
    ]
