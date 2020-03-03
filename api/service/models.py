from django.db import models


class ServiceModels(models.Model):
    service = models.CharField(max_length=125)
    machine = models.CharField(max_length=125)
    project = models.CharField(max_length=125)
    zone = models.CharField(max_length=50)
    instance = models.CharField(max_length=125)
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Service Models"

    def __str__(self):
        return str(self.service) + " -  " + str(self.instance) + " " + str(self.project)


class MachineService(models.Model):
    name_machine = models.CharField(max_length=125)

    class Meta:
        verbose_name_plural = "Machine Service Models"

    def __str__(self):
        return str(self.name_machine)


class PermittedMachine(models.Model):
    machine = models.ForeignKey(
        'MachineService', on_delete=models.CASCADE,
        related_name="machine_permitterd",
    )
    id_permitted = models.IntegerField()

    class Meta:
        verbose_name_plural = "Register Photo Models"

    def __str__(self):
        return str(self.machine.name_machine) + " -  " + str(self.id_permitted)


class RegisterPhoto(models.Model):
    machine = models.ForeignKey(
        'MachineService', on_delete=models.CASCADE,
        related_name="machine_register",
    )
    id_photo = models.IntegerField()
    position = models.IntegerField()
    country = models.CharField(max_length=50)
    chanel = models.IntegerField()
    task = models.IntegerField()

    class Meta:
        verbose_name_plural = "Register Photo Models"

    def __str__(self):
        return str(self.machine.name_machine) + " -  " + str(self.country) + " " + str(self.task)
