import re 
from rest_framework import serializers
from .models import Customer,PolicyDetails
from rest_framework.exceptions import ValidationError

class CustomerSerializer(serializers.ModelSerializer):
    
    """
        customer serializer
    """
    customer_income_group = serializers.CharField(source='get_customer_income_group_display')
    customer_gender_status = serializers.CharField(source='get_customer_gender_status_display')
    customer_region = serializers.CharField(source='get_customer_region_display')
    customer_martial_status= serializers.CharField(source='get_customer_martial_status_display')

    class Meta:
        model = Customer
        fields = '__all__'

class PolicyDetailsSerializer(serializers.ModelSerializer):

    """
        policy details serializer
    """

    customer = CustomerSerializer()
    fuel = serializers.CharField(source='get_fuel_display')

    class Meta:
        model = PolicyDetails
        fields = '__all__'

    def validate_customer(self,requested_data,match_with_list):

        return_value = None
        for k_,m_ in match_with_list:
            if requested_data == k_:
                return_value = m_
                break

        return return_value

    def custome_save(self,instance,k,v):
        if v is None:
            ValidationError('Please provide valid data')

        setattr(instance, k, v)
        instance.save()

    def update(self, instance, validated_data):
        
        pattern = re.compile(r'\s+')
        if 'customer' in list(self.context['request'].data.keys())[0]:
            customer_instance = Customer.objects.filter(id=self.context['key']['pk']).first()
        
            if self.context['request'].data.get('customer_income_group'):
                data = self.validate_customer(
                    re.sub(pattern,'',self.context['request'].data.get('customer_income_group')),
                    list((('0-$25k',0),('$25-$70K',1),('>$70K',2)))
                )
                self.custome_save(customer_instance,'customer_income_group',data)
    
            elif self.context['request'].data.get('customer_martial_status'):
                
                data = self.validate_customer(
                    re.sub(pattern,'',self.context['request'].data.get('customer_martial_status')),
                    list((('Single',0),('Married',1),('Other',2)))
                )
                self.custome_save(customer_instance,'customer_martial_status',data)

            elif self.context['request'].data.get('customer_gender_status'):
                
                data = self.validate_customer(
                    re.sub(pattern,'',self.context['request'].data.get('customer_gender_status')),
                    list((('Male',0),('Female',1),('Other',2))))
                self.custome_save(customer_instance,'customer_gender_status',data)

            else:
                for k,v in self.context['request'].data.items():        
                    self.custome_save(customer_instance,k,v)
        else:    
            for k,v in validated_data.items():
                self.custome_save(instance,k,v)

            if validated_data.get('get_fuel_display'):
                data = self.validate_customer(re.sub(pattern,'',validated_data['get_fuel_display']),
                    list((('CNG',0),('Petrol',1),('Diesel',2))))
                self.custome_save(instance,'fuel',data)
        
        return instance