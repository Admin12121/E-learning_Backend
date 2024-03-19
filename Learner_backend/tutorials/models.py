from django.db import models


class Courses(models.Model):
    name = models.CharField(max_length=500)
    whatyouwilllearn = models.TextField(max_length=10000,blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price =models.CharField(max_length=10)
    offerPrice = models.CharField(max_length=10)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Syllabus(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True, related_name='syllabi')
    nameof_syllabus1 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.course} - {self.nameof_syllabus1}"

class CourseData(models.Model):
    content = models.ForeignKey(Syllabus, on_delete=models.CASCADE, null=True)
    video_title = models.CharField(max_length=200, blank=True, null =True)
    videourl=models.CharField(max_length=1000, blank=True, null =True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    codeType = models.CharField(max_length=100, null=True, blank=True)
    note1 = models.TextField(max_length=100000, null=True, blank=True)
    code1 = models.TextField(max_length=100000, null=True, blank=True)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    note2 = models.TextField(max_length=100000, null=True, blank=True)
    code2 = models.TextField(max_length=100000, null=True, blank=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    note3 = models.TextField(max_length=100000, null=True, blank=True)
    code3 = models.TextField(max_length=100000, null=True, blank=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    note4 = models.TextField(max_length=100000, null=True, blank=True)
    code4 = models.TextField(max_length=100000, null=True, blank=True)
    image4 = models.ImageField(upload_to='images/', blank=True, null=True)
    note5 = models.TextField(max_length=100000, null=True, blank=True)
    code5 = models.TextField(max_length=100000, null=True, blank=True)
    image5 = models.ImageField(upload_to='images/', blank=True, null=True)

            
    def __str__(self):
        return f"{self.content} - {self.video_title}"