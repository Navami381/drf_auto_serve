from django.urls import path
from service_requests.views import SignUpView,ObtainAuthToken,ServiceRequestListCreateView,ServiceRequestRetriveUpdateDeleteView
from service_requests.views import PendingRequestView,TotalServiceRequest,StatusTotalServiceRequest,PriorityServiceRequest

urlpatterns=[
    path("Register/",SignUpView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path("servicerequest/",ServiceRequestListCreateView.as_view()),
    path("servicerequest/<int:pk>/",ServiceRequestRetriveUpdateDeleteView.as_view()),
    path("servicerequest/pending/",PendingRequestView.as_view()),
    path("servicerequest/total/",TotalServiceRequest.as_view()),
    path("servicerequest/status/",StatusTotalServiceRequest.as_view()),
    path("servicerequest/priority/",PriorityServiceRequest.as_view())
]