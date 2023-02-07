from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
def validate_even(value):
    if value < 0.0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

class Registro(models.Model):
    fecha = models.DateField()
    detalle = models.CharField(max_length=200)
    ncomprobante = models.CharField(max_length=200)
    eingresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    eegresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    esaldo = models.FloatField(validators=[validate_even], blank=True, null=True)
    bingresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    begresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    bsaldo = models.FloatField(validators=[validate_even], blank=True, null=True)
    etotalingresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    etotalegresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    btotalingresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    btotalegresos = models.FloatField(validators=[validate_even], blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.detalle