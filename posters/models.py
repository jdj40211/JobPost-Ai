from django.db import models

# Create your models here.


class Job(models.Model):
    job_file = models.FileField(upload_to='job_files')
    job_description = models.TextField(blank=True, null=True)
    template_image = models.FileField(upload_to='template_images', blank=True, null=True)

    def __str__(self):
        return self.job_description