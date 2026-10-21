from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,Count


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions,authentication



from service_requests.serializers import RegisterSerializer,ServiceRequestSerializers
from service_requests.models import ServiceRequestModel
from service_requests.permissions import IsOwner

# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            instance=User.objects.create_user(**cleaned_data)
            serializer_instance=RegisterSerializer(instance)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class ServiceRequestListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        instance=ServiceRequestModel.objects.filter(owner=request.user)
        serializer_instance=ServiceRequestSerializers(instance,many=True)
        return Response(data=serializer_instance.data)
    
    def get(self,request):

        instance=ServiceRequestModel.objects.filter(owner=request.user)

        service_type=request.query_params.get("service_type")
        priority=request.query_params.get("priority")
        status=request.query_params.get("status")

        if service_type:
            instance=instance.filter(service_type=service_type)
        if priority:
            instance=instance.filter(priority=priority)
        if status:
            instance=instance.filter(status=status)

        search = request.query_params.get('search')

        if search:
                  from django.db.models import Q
                  instance = instance.filter(
                     Q(vehicle_number__icontains=search) |
                     Q(vehicle_model__icontains=search)
                  )

        serializer_instance = ServiceRequestSerializers(instance, many=True)
        return Response(data=serializer_instance.data)            
   

    def post(self,request):
        form_data=request.data
        serializer_instance=ServiceRequestSerializers(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class ServiceRequestRetriveUpdateDeleteView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]
    def get(self,request,pk=None):
        instance=get_object_or_404(ServiceRequestModel,id=pk)
        self.check_object_permissions(request,instance)
        serializer_instance=ServiceRequestSerializers(instance)
        return Response(data=serializer_instance.data)

    def put(self, request, pk=None):
        instance = get_object_or_404(
            ServiceRequestModel, id=pk
        )
        self.check_object_permissions(request, instance)

        serializer_instance = ServiceRequestSerializers(
            instance, data=request.data
        )

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)

        return Response(data=serializer_instance.errors)
    
    def delete(self,request,pk=None):
        instance=get_object_or_404(ServiceRequestModel,id=pk)
        self.check_object_permissions(request,instance)
        instance.delete()
        return Response(data={"message":"deleted"})

class PendingRequestView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]
    def get(self,request):
        instance=ServiceRequestModel.objects.filter(owner=request.user).exclude(status="Delivered")
        serializer_instance=ServiceRequestSerializers(instance,many=True)
        return Response(data=serializer_instance.data)
    
class TotalServiceRequest(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]
    def get(self,requset):
        total=ServiceRequestModel.objects.filter(owner=requset.user).count()
        return Response(data={"total no of request":total})

class StatusTotalServiceRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self, request):
        instance = ServiceRequestModel.objects.filter(owner=request.user)

        data = {}

        for item in instance:
            status = item.status

            if status not in data:
                data[status] = []

            data[status].append(ServiceRequestSerializers(item).data)

        return Response(data=data)

class PriorityServiceRequest(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]
    
    def get(self, request):
        instance=ServiceRequestModel.objects.filter(owner=request.user,priority__in=["High","Critical"])
        serializer_instance=ServiceRequestSerializers(instance,many=True)
        return Response(data=serializer_instance.data)
