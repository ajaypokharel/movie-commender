from django.contrib.auth import get_user_model
from django.db import models

from moviecommender.commons.constants import APPLICATION_STATUS, PENDING
from moviecommender.commons.models import UUIDBaseModel

USER = get_user_model()


class MovieFiller(UUIDBaseModel):
    filler = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='movie_filler')
    movies_filled = models.IntegerField(default=0)
    level = models.PositiveIntegerField(default=0)



class MovieFillerApply(UUIDBaseModel):
    applicant = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='apply_filler')
    reason = models.TextField()
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=APPLICATION_STATUS, default=PENDING)
