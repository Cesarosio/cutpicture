from django.db import models


class Image(models.Model):
    main = models.BinaryField(editable=True)
    A1 = models.BinaryField(editable=True)
    A2 = models.BinaryField(editable=True)
    B1 = models.BinaryField(editable=True)
    B2 = models.BinaryField(editable=True)
    C1 = models.BinaryField(editable=True)
    C2 = models.BinaryField(editable=True)
    D = models.BinaryField(editable=True)
