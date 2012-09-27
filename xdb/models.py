from django.db import models

# Create your models here.
class Vector(models.Model):
    vector = models.TextField()
    desc = models.TextField(blank=True)
    root = models.ForeignKey('self',related_name="root_vector", blank=True, null=True)
    source = models.CharField(max_length="200", blank=True)
    family = models.ManyToManyField('VectorFamily', blank=True, null=True)
    def __unicode__(self):
        return "#"+str(self.id)+" - "+self.desc[0:30]+" ( "+self.vector[0:30]+" )"

class Browser(models.Model):
    ua  = models.TextField()
    name = models.CharField(max_length=50)
    valid_ua = models.BooleanField(default=False)
    desc = models.TextField(blank=True)
    build_date = models.DateField(blank=True, null=True)
    test_date = models.DateField(auto_now=True)
    contributor = models.CharField(default="Anonymous",max_length="200")
    family = models.ManyToManyField('BrowserFamily', blank=True, null=True)
    plugins = models.ManyToManyField('BrowserPlugin', blank=True, null=True)
    source  = models.CharField(max_length="200", default="unknown")
    def __unicode__(self):
        return "#"+str(self.id)+" - "+self.name

class Encoding(models.Model):
    name=models.CharField(max_length=32)
    py_encoding=models.CharField(max_length=32)
    web_encoding=models.CharField(max_length=32)
    def __unicode__(self):
        return self.name

class WebContext(models.Model):
    name = models.CharField(max_length=32)
    desc = models.TextField(blank=True)
    # The source is the html / xml / svg code surrounding the xss vector
    # including DTD, doctype, and other declarations
    # ultimately a webcontext can be something passing the vector throug a
    # security filter etc... drifting from the original test model
    # ex: <html>
    # <meta http-equiv="refresh" content="0.1;url=/test/next"/>
    #  %(xss)s
    # </html>
    source = models.TextField(default="%(xss)s")
    mimetype = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Test(models.Model):
    vector = models.ForeignKey('Vector')
    browser = models.ForeignKey('Browser')
    context = models.ForeignKey('WebContext')
    encoding = models.ForeignKey('Encoding')
    result = models.CharField(default="N/A",max_length="4")
    class Meta:
        unique_together = ("vector", "browser", "context","encoding")

    def __unicode__(self):
        return self.result

class Suite(models.Model):
    name=models.CharField(max_length=32)
    desc = models.TextField(blank=True)
    vectors= models.ManyToManyField('Vector')
    contexts= models.ManyToManyField('WebContext')
    encodings= models.ManyToManyField('Encoding')
    def __unicode__(self):
        return self.name

class BrowserFamily(models.Model):
    name=models.CharField(max_length=32)
    desc = models.TextField(blank=True)
    browsers = models.ManyToManyField('Browser', blank=True, null=True)
    def __unicode__(self):
        return self.name

class VectorFamily(models.Model):
    name=models.CharField(max_length=32)
    desc = models.TextField(blank=True)
    vectors = models.ManyToManyField('Vector', blank=True, null=True)
    def __unicode__(self):
        return self.name

class BrowserPlugin(models.Model):
    name=models.CharField(max_length=32)
    def __unicode__(self):
        return self.name

