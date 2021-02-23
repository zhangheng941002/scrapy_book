from django.db import models


# Create your models here.


class BookAllInfoModel(models.Model):
    book_name = models.CharField(max_length=255)
    book_login_url = models.CharField(max_length=255)
    type_name = models.CharField(max_length=255)
    type_url = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_img = models.CharField(max_length=255)
    book_intro = models.TextField()
    chapter_login_url = models.CharField(max_length=255)
    chapter_name = models.CharField(max_length=255)
    chapter_url = models.CharField(max_length=255, blank=True, null=True)
    chapter_content = models.TextField()
    num = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'book_all'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])


class AuthorModel(models.Model):
    author_name = models.CharField(max_length=255)
    author_img = models.CharField(max_length=255)
    author_intro = models.TextField()
    author_info = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'author'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])


class BookTypeModel(models.Model):
    type_name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'book_type'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])


class BookModel(models.Model):

    book_name = models.CharField(max_length=255)
    # author_id = models.IntegerField()
    author_id = models.ForeignKey(AuthorModel, on_delete=models.DO_NOTHING, db_column="author_id")
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


class BookChapterModel(models.Model):
    # book_id = models.IntegerField()
    # account_id = models.ForeignKey(AccountMeta, on_delete=models.DO_NOTHING, db_column="FK_account_id")

    book_id = models.ForeignKey(BookModel, on_delete=models.DO_NOTHING, db_column="book_id")
    chapter_name = models.CharField(max_length=255)
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


class InsertErrorModel(models.Model):
    msg = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    class Meta:
        ordering = ('pk',)
        managed = False
        app_label = 'iqiwx'
        db_table = 'insert_error'

    def __str__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])

    def __repr__(self):
        return ' '.join([str(getattr(self, field.name)) for field in self._meta.fields])
