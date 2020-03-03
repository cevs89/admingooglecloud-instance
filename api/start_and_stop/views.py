from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from service.models import ServiceModels
from django.conf import settings
import os
from pprint import pprint
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery


class ValidateState():

    def __init__(self, project, zone, instance, action=None):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.CREDENTIALS_GOOGLE_CLOUD
        GoogleCredentials.get_application_default()
        self.service = googleapiclient.discovery.build('compute', 'v1')
        self.project = project
        self.zone = zone
        self.instance_get = instance
        self.action = action

    def List(self):
        list_reponse = []
        request = self.service.instances().list(project=self.project, zone=self.zone)
        while request is not None:
            response = request.execute()

            for instance in response['items']:
                list_reponse.append(instance)

            request = self.service.instances().list_next(previous_request=request, previous_response=response)
        return list_reponse

    def Operation(self):
        data = self.List()
        queryset = ServiceModels.objects.filter()

        for i in range(len(data)):
            queryset.filter(
                instance__exact=data[i]['name']
            ).update(status=data[i]['status'])

        instancia_value = self.instance_get

        while instancia_value == self.instance_get:
            if self.action == 'start':
                for value in queryset.filter(status='TERMINATED'):
                    request = self.service.instances().start(
                        project=value.project, zone=value.zone,
                        instance=value.instance)
            else:
                for value in queryset.filter(status='RUNNING'):
                    request = self.service.instances().stop(
                        project=value.project, zone=value.zone,
                        instance=value.instance)

            response = request.execute()
            instancia_value = None
        return response


class OperationServiceViews(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = ServiceModels

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        list_reponse = []

        for value in self.queryset.objects.filter():
            if action == 'start':
                data = ValidateState(
                    value.project, value.zone, value.instance, 'start'
                ).Operation()

            elif action == 'stop':
                data = ValidateState(
                    value.project, value.zone, value.instance, 'stop'
                ).Operation()

            else:
                return Response(
                    {'message': 'Verifique la accion y vuelva a intentarlo'},
                    status=status.HTTP_400_BAD_REQUEST)

            list_reponse.append(data)
        return Response(
            list_reponse,
            status=status.HTTP_200_OK
        )


class ListServiceViews(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = ServiceModels

    def get(self, request, *args, **kwargs):
        list_reponse = []
        for value in self.queryset.objects.all():
            dataList = ValidateState(
                value.project, value.zone, value.instance).List()
            for i in range(len(dataList)):
                array = {
                    'name': dataList[i]['name'],
                    'status': dataList[i]['status']
                }
                list_reponse.append(array)
        return Response(
            list_reponse,
            status=status.HTTP_200_OK
        )
