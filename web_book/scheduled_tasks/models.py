from django.db import models


# Create your models here.

class BookCreateModel(models.Model):
    book_name = models.CharField(max_length=255)
    author_id = models.IntegerField()
    # author_id = models.ForeignKey(AuthorModel, on_delete=models.DO_NOTHING, db_column="author_id")
    img = models.CharField(max_length=255)
    type_id = models.IntegerField()
    book_intro = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'book'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])


class BookChapterCreateModel(models.Model):
    book_id = models.IntegerField()
    # book_id = models.ForeignKey(BookModel, on_delete=models.DO_NOTHING, db_column="book_id")
    chapter_name = models.CharField(max_length=2048)
    chapter_content = models.TextField()
    num = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'book_chapter'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

