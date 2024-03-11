from django.db import models
from moviepy.editor import VideoFileClip


class Courses(models.Model):
    name = models.CharField(max_length=500)
    # demo_video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(max_length=5000)
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
    codeType = models.CharField(max_length=100, null=True, blank=True)
    note1 = models.TextField(max_length=100000, null=True, blank=True)
    code1 = models.TextField(max_length=100000, null=True, blank=True)
    note2 = models.TextField(max_length=100000, null=True, blank=True)
    code2 = models.TextField(max_length=100000, null=True, blank=True)
    note3 = models.TextField(max_length=100000, null=True, blank=True)
    code3 = models.TextField(max_length=100000, null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.videourl:
            clip = VideoFileClip(self.videourl)
            duration_in_seconds = clip.duration
            self.duration_minutes = int(duration_in_seconds // 60)
            self.duration_seconds = int(duration_in_seconds % 60)
            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.content} - {self.video_title}"