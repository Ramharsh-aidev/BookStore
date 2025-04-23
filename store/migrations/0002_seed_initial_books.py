# store/migrations/0002_seed_initial_books.py

from django.db import migrations

# --- Define sample book data ---
INITIAL_BOOKS = [
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "description": "Seconds before the Earth is demolished to make way for a galactic freeway, Arthur Dent is plucked off the planet by his friend Ford Prefect, a researcher for the revised edition of The Hitchhiker's Guide to the Galaxy who, for the last fifteen years, has been posing as an out-of-work actor.",
        "price": "12.99",
        "stock": 15
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. A classic novel exploring the themes of love, marriage, class, and social conventions in early 19th-century England.",
        "price": "9.50",
        "stock": 25
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "description": "A dystopian social science fiction novel and cautionary tale. Winston Smith wrestles with oppression in Oceania, a place where the Party scrutinizes human actions with ever-watchful Big Brother.",
        "price": "10.80",
        "stock": 10
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it. Compassionate, dramatic, and deeply moving.",
        "price": "14.00",
        "stock": 18
    },
    {
       "title": "Dune",
       "author": "Frank Herbert",
       "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the 'spice' melange, a drug capable of extending life and enhancing consciousness.",
       "price": "18.50",
       "stock": 8
   },
]

def forwards_func(apps, schema_editor):
    """
    Create initial book data.
    """
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Book = apps.get_model("store", "Book")
    db_alias = schema_editor.connection.alias

    books_to_create = []
    for book_data in INITIAL_BOOKS:
        # Check if a book with the same title and author already exists
        # to make this migration potentially runnable multiple times safely
        if not Book.objects.using(db_alias).filter(title=book_data["title"], author=book_data["author"]).exists():
            books_to_create.append(Book(**book_data))

    if books_to_create:
        Book.objects.using(db_alias).bulk_create(books_to_create)
        print(f"\n  Successfully seeded {len(books_to_create)} initial books.")
    else:
        print("\n  Initial books already seeded or list is empty.")


def backwards_func(apps, schema_editor):
    """
    Removes the initial book data if the migration is reversed.
    NOTE: This is basic; it might delete books added manually if they match.
    A safer approach might involve adding a specific flag to seeded books.
    """
    Book = apps.get_model("store", "Book")
    db_alias = schema_editor.connection.alias

    # Get titles and authors from the initial data to identify records to delete
    titles_to_delete = [book["title"] for book in INITIAL_BOOKS]
    authors_to_delete = [book["author"] for book in INITIAL_BOOKS] # Less precise, but simple

    # Build Q objects for filtering (more precise than just titles or authors)
    from django.db.models import Q
    query = Q()
    for book_data in INITIAL_BOOKS:
        query |= Q(title=book_data["title"], author=book_data["author"])

    deleted_count, _ = Book.objects.using(db_alias).filter(query).delete()

    if deleted_count > 0:
        print(f"\n  Successfully deleted {deleted_count} initial books.")
    else:
        print("\n  No initial books found matching seed data to delete.")


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'), # Ensures Book table exists before running this
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]