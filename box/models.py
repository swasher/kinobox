from django.db import models

# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __unicode__(self):
        return u'{0}'.format(self.genre)

class Person(models.Model):
    name = models.CharField(max_length=150)
    tmdb_id = models.IntegerField()
    #url = 'http://www.themoviedb.org/person/' + id
    photo = models.ImageField(blank=True, null=True, upload_to='persons')
    starred = models.BooleanField(blank=True, default=False)

    def url(self):
        try:
            url=self.photo.url
        except:
            url='/static/nobody.jpg'
        return url

class Movi(models.Model):
    title = models.CharField(max_length=150)
    tmdb_id = models.IntegerField()
    origtitle = models.CharField(max_length=150)
    overview = models.CharField(max_length=1000)
    year = models.IntegerField()
    seen = models.BooleanField(blank=True, default=False)
    stored = models.BooleanField(blank=True, default=False)
    seendate = models.DateField(blank=True)
    adddate = models.DateField(blank=True)
    myrating = models.IntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person, through='Duty')
    countries = models.CharField(max_length=200)
    tagline = models.CharField(max_length=150)
    poster = models.ImageField(blank=True, null=True, upload_to='posters')
    posterbig = models.ImageField(blank=True, null=True, upload_to='posters')

    def __unicode__(self):
        return u'{0}.{1}'.format(self.title, self.year)

    def count_starred(self):
        count=Person.objects.filter(movi__tmdb_id=self.tmdb_id, starred=True).count()
        return count

class Duty(models.Model):
    person = models.ForeignKey(Person)
    movi = models.ForeignKey(Movi)
    department = models.CharField(max_length=40)
    character = models.CharField(max_length=40)
    job = models.CharField(max_length=40)
    order = models.SmallIntegerField()

    #def get_name(self):
    #    return self.person.name
    #def get_url(self):
    #    return self.person.photo
