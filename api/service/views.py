from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.authtoken.views import ObtainAuthToken
from service.validators import RegisterServiceValidator
from service.serializers import RegisterServiceSerializer
from service.models import ServiceModels, MachineService, RegisterPhoto, \
                            PermittedMachine
from service.forms import PostFormService


class ObtainExpiringAuthToken(ObtainAuthToken):
    """
    {
    "username": "name",
    "password": "pass"
    }

    """
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = serializer.initial_data

        try:
            User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'message': 'Username does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                    user=serializer.validated_data['user'])

            if not created:
                token.created = timezone.now()
                token.save()

            return Response({"token": token.key})
        return Response(
            {'message': 'Incorrect username or password, please check'},
            status=status.HTTP_400_BAD_REQUEST)


class RegisterServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = ServiceModels.objects.all()
    serializer_class = RegisterServiceSerializer

    def create(self, request):
        get_validation = RegisterServiceValidator(request.data)

        if get_validation.validate():
            data = get_validation.data
            PostFormService(data).save()
            return Response(
                {'message': 'Create Correct'}, status=status.HTTP_201_CREATED)
        else:
            return Response(get_validation.errors(),
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            id_get = int(pk)
        except Exception as e:
            return Response(
                    {'message': "It is not integer", 'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            queryset = ServiceModels.objects.get(pk=id_get)
        except ServiceModels.DoesNotExist:
            return Response(
                    {'message': 'Service Does not exists, please try again'},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        get_validation = RegisterServiceValidator(request.data)

        if get_validation.validate():
            data = get_validation.data

            try:
                id_get = int(pk)
            except Exception as e:
                return Response(
                        {'message': "It is not integer", 'detail': str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            try:
                queryset = ServiceModels.objects.get(pk=id_get)
            except ServiceModels.DoesNotExist:
                return Response(
                        {'message': 'Service Does not exists, please try again'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            form = PostFormService(data, instance=queryset)
            form.save(commit=False).save()

            return Response(
                {'message': 'Update Correct'}, status=status.HTTP_200_OK)
        else:
            return Response(get_validation.errors(),
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            id_get = int(pk)
        except Exception as e:
            return Response(
                    {'message': "It is not integer", 'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            queryset = ServiceModels.objects.get(pk=id_get)
        except ServiceModels.DoesNotExist:
            return Response(
                    {'message': 'The service you are trying to find does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        queryset.delete()
        return Response(
            {'message': 'Delete Correct'}, status=status.HTTP_200_OK)


class RegisterPhotoView(APIView):
    # template_name = "tamplete.html"

    def post(self, request, *args, **kwargs):
        # data = request.POST para formaular HTML

        data = request.data  # para API
        get_chanel = data['chanel']
        get_task = data['task']
        get_country = data['country']

        query_permitted = PermittedMachine.objects.filter(id_permitted=get_task)
        lista_machine = list(
            map(
                lambda x: {"id_permitted": x[0], "id_machine": x[1]},
                [[a.id_permitted, a.machine_id] for a in query_permitted]
            )
        )

        queryset = RegisterPhoto.objects.filter(task=get_task)
        if queryset.exists():
            if queryset.filter(country=get_country, chanel=get_chanel,
                               task=get_task).exists():

                return Response({"msg": "El registro existe"},
                                status=status.HTTP_200_OK)
            else:
                RegisterPhoto.objects.create(
                    country=get_country, chanel=get_chanel, task=get_task,
                    machine_id=queryset.first().machine_id, id_photo=1,
                    position=1
                )
                return Response({"msg": "Existe y se creo uno nuevo"},
                                status=status.HTTP_200_OK)
        else:
            RegisterPhoto.objects.create(
                country=get_country, chanel=get_chanel, task=get_task,
                machine_id=lista_machine[0]['id_machine'], id_photo=1,
                position=1
            )
            return Response(
                {"msg": "No existia y se creo"},
                status=status.HTTP_200_OK
            )


class PhotoView(APIView):
    def get(self, request, *args, **kwargs):

        list_response_machine = []
        for a in MachineService.objects.filter():
            array = {
                "id_machine": a.pk,
                "name_machine": a.name_machine,
                "id_task_permitted": [i.id_permitted for i in PermittedMachine.objects.filter(machine_id=a.pk)]
            }
            list_response_machine.append(array)

        list_response = []
        for value in RegisterPhoto.objects.all():
            array = {
                "machine": {
                    "id": value.machine_id,
                    "name": value.machine.name_machine
                },
                "id_photo": value.id_photo,
                "position": value.position,
                "country": value.country,
                "chanel": value.chanel,
                "task": value.task
            }
            list_response.append(array)

        return Response(
            list_response_machine,
            status=status.HTTP_200_OK
        )
