from csv import DictReader
from django.core.management import BaseCommand
from reviews.models import Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Comment.objects.count() > 2:
            print("user data already loaded...exiting.")
            return
        # Show this before loading the data into the database
        print("Loading user data...")
        # Code to load the data into database
        for row in DictReader(
            open("./static/data/comments.csv", encoding="utf-8")
        ):
            comment = Comment(
                id=row["id"],
                review_id=row["review_id"],
                text=row["text"],
                author_id=row["author"],
                pub_date=row["pub_date"],
            )
            comment.save()
        print("...done")
