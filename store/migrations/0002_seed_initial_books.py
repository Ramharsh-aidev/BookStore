from django.db import migrations
from decimal import Decimal

INITIAL_BOOKS = [
    {
        "title": "Shri Ram Charitmanas",
        "author": " Gita Press Gorakhpur",
        "description": "The Shri Ramcharitmanas, composed by Goswami Tulsidas and published by Gita Press Gorakhpur, is a sacred scripture in Hinduism that narrates the divine life and teachings of Lord Shri Ram. Written in the Awadhi dialect with accompanying Hindi translations, this revered text is divided into seven Kandas: Bal Kand, Ayodhya Kand, Aranya Kand, Kishkindha Kand, Sundar Kand, Lanka Kand, and Uttar Kand, each chronicling significant events from Ram's birth to his return as the king of Ayodhya. Celebrated for its profound teachings on dharma, devotion, and the triumph of good over evil, this edition is cherished for its authenticity, clear commentaries, and high-quality print. A cornerstone of Sanatan Dharma, it continues to guide devotees towards a righteous path. Jai Shri Ram!",
        "price": Decimal("1000.00"),
        "stock": 18
    },
    {
        "title": "The Hindu-Yogi Science of Breath",
        "author": "William Walker Atkinson",
        "description": "The Hindu-Yogi Science of Breath by William Walker Atkinson is a comprehensive guide on the principles of breath control and its implications for physical, mental, and spiritual development, written during the early 20th century. This work delves into the ancient practice of Yoga, specifically focusing on the art and philosophy of breathing, outlining exercises and theories that connect breath with vitality, health, and inner peace. The opening of the book introduces readers to the misconceptions that Western students may have about Yogis and their teachings, emphasizing the vast and intricate Yogi tradition that extends beyond superficial characterizations. Atkinson begins by outlining the significance of breath in relation to life, asserting that proper breathing is crucial for maintaining health and energy. He proceeds to set the stage for the detailed exploration of the Science of Breath, portraying it as a bridge between Eastern and Western philosophies. This introduction aims to clarify the misconceptions surrounding Yoga, encouraging readers to adopt these ancient techniques for their well-being, while appreciating the depth and practicality of Yogi knowledge.",
        "price": Decimal("500.00"),
        "stock": 15
    },
    {
        "title": "Shrimad Bhagwat Geeta Yatharoop (Hindi)",
        "author": "A.C. Bhaktivendanta Swami Prabhupada",
        "description": "The largest-selling edition of the Gita all over the world, Bhagavad-Gita as It Is, is more than a book. For many it has changed their lives altogether. Universally Bhagavad-Gita is renowned and truly claimed as the crown jewel of India?s spiritual wisdom. Spoken by Lord Krishna the Supreme Personality of Godhead to His intimate disciple Arjuna, the Gita?s seven hundred concise verses provides a definitive guide to the science of self realization. Complete wisdom with original sanskrit texts, word to word meaning, translation and purpot by His divine gracre A.C Bhakti Vedanta Swami Srila Prabhupada, Founder acharya of ISKCON",
        "price": Decimal("800.00"),
        "stock": 25
    },
    {
        "title": "Mahagatha: 100 Tales from the Puranas",
        "author": "Satyarth Nayak",
        "description": "The Puranas of Hinduism are a universe of wisdom, embodying a fundamental quest for answers that makes them forever relevant. Now, for the first time, 100 of the greatest mythological tales from these ancient texts have been handpicked and compiled into an epic illustrated edition. Besides popular legends of devas, asuras, sages and kings, Satyarth Nayak has dug up lesser-known stories, like the one where Vishnu is beheaded or where Saraswati curses Lakshmi or where Harishchandra tricks Varuna. Nayak also recounts these 100 tales in a unique chronological format, beginning with Creation in Satya Yuga and ending with the advent of Kali Yuga. Using Puranic markers, he constructs a narrative that travels through the four yugas, offering continuous and organic action. In such a reading, it is revealed that these stories are not isolated events but linked to each other in the grand scheme of things. That every occurrence has a past and a future. A cause and effect. An interconnected cycle of karma and karma-phal. Delving into the minds of gods, demons and humans alike, Mahagatha seeks a deeper understanding of their motivations. The timelessness of their impulses speaks across the aeons to readers of today. Written in lively prose with charming illustrations, these 100 tales will entertain and enlighten, and make you connect the dots of Hindu mythology like never before.",
        "price": Decimal("900.00"),
        "stock": 10
    },
]

def forwards_func(apps, schema_editor):
    """
    Create initial book data.
    """
    Book = apps.get_model("store", "Book")
    db_alias = schema_editor.connection.alias

    books_to_create = []
    print("\n  Checking for initial books to seed...") # Added initial message
    for book_data in INITIAL_BOOKS:
        if not Book.objects.using(db_alias).filter(title=book_data["title"], author=book_data["author"]).exists():
            # Ensure price is Decimal before creating the object instance
            book_data['price'] = Decimal(book_data['price'])
            books_to_create.append(Book(**book_data))
        else:
            print(f"    - Skipping '{book_data['title']}', already exists.") # Info message

    if books_to_create:
        Book.objects.using(db_alias).bulk_create(books_to_create)
        print(f"  Successfully seeded {len(books_to_create)} initial books.")
    else:
        print("  No new initial books to seed.")


def backwards_func(apps, schema_editor):
    """
    Removes the initial book data if the migration is reversed.
    """
    Book = apps.get_model("store", "Book")
    db_alias = schema_editor.connection.alias

    from django.db.models import Q
    query = Q()
    for book_data in INITIAL_BOOKS:
        # Match based on the data defined in THIS migration's INITIAL_BOOKS
        query |= Q(title=book_data["title"], author=book_data["author"])

    # Only delete if the query is not empty (i.e., INITIAL_BOOKS was not empty)
    if query:
        deleted_count, deleted_details = Book.objects.using(db_alias).filter(query).delete()
        if deleted_count > 0:
            print(f"\n  Successfully deleted {deleted_count} initial books matching seed data.")
            # print(f"  Deleted details: {deleted_details}") # Optional: more detailed output
        else:
            print("\n  No initial books found matching seed data to delete.")
    else:
        print("\n  INITIAL_BOOKS list is empty, nothing to delete in reverse operation.")


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'), # Make sure this matches the previous migration for 'store'
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]