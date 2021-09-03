from django.shortcuts import render
from .models import Customer,PolicyDetails
# Create your views here.
from rest_framework import filters
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .serializers import PolicyDetailsSerializer,CustomerSerializer
import pandas as pd
from rest_framework.views import APIView
import re
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q


class PolicyDetailsView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin):
    queryset = PolicyDetails.objects.all()
    serializer_class = PolicyDetailsSerializer
    model = serializer_class.Meta.model
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        serializer = PolicyDetailsSerializer(instance, data=request.data, partial=True,context={'request': request,'key':kwargs})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)    
        return Response(serializer.data)
   
class PolicyDetailsListView(ListAPIView):
    serializer_class = PolicyDetailsSerializer
    filter_backends = [filters.SearchFilter]
    model = serializer_class.Meta.model
    search_fields = ['policy_id', 'customer__customer_digit']
    paginate_by = 5

    def list(self, request, *args, **kwargs):

        page_number = self.request.GET.get('page_number')
        policy_list = self.model.objects.all().order_by('id')
        qry_set = None
        if self.request.GET.get('search'):
            qry_set = policy_list.filter(Q(policy_id=self.request.GET.get('search')) | Q(customer__customer_digit=self.request.GET.get('search')))
        else:
            qry_set = policy_list

        paginator = Paginator(qry_set, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        try:
            policy_details_data = paginator.page(page_number)
        except PageNotAnInteger:
            policy_details_data = paginator.page(1)
        except EmptyPage:
            policy_details_data = paginator.page(paginator.num_pages)
        
        serializer = PolicyDetailsSerializer(policy_details_data, many=True)
        response_list = serializer.data 

        return Response({'result':response_list,'total_page':paginator.num_pages})

class MonthWisePolicyView(ListAPIView):
    queryset = PolicyDetails.objects.all()
    serializer_class = PolicyDetailsSerializer
    model = serializer_class.Meta.model

    def list(self, request, *args, **kwargs):
        policy_list = self.model.objects.all().order_by('date_of_purchase')
        result= {}
        db_result = policy_list.values('policy_id','date_of_purchase')
        for i in db_result:
            month = str(i.get('date_of_purchase').strftime("%B"))
            if month in result.keys():
                result[month] = result[month] +','+ i.get('policy_id')
            else:
                result[month] = i.get('policy_id')

        final_dict = [{'month':k,'number_of_policy':len(v.split(','))} for k,v in result.items()]
        return Response({'result':final_dict})