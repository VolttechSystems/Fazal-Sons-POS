from django.db import models

Gender = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

STATUS = (
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('inactive', 'Inactive'),
)

ONLINE_ACCESS = (
    ('no', 'No'),
    ('yes', 'Yes'),

)


class SystemRole(models.Model):
    sys_role_code = models.CharField(max_length=200, null=True, unique=True)  # SYSR-1
    sys_role_name = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_system_role'

    def __str__(self):
        return self.sys_role_name


class CustomerChannel(models.Model):
    cus_ch_code = models.CharField(max_length=200, null=True, unique=True)  # CCH-1
    customer_channel = models.CharField(max_length=100, null=True, unique=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_customer_channel'

    def __str__(self):
        return self.customer_channel


class CustomerType(models.Model):
    cus_type_code = models.CharField(max_length=200, null=True, unique=True)  # CTP-1
    customer_type = models.CharField(max_length=100, null=True, unique=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_customer_type'

    def __str__(self):
        return self.customer_type


class Customer(models.Model):
    date = models.DateTimeField(max_length=100, null=True)
    cust_code = models.CharField(max_length=200, null=True, unique=True)  # CUST-1
    customer_channel = models.ForeignKey(CustomerChannel, to_field='customer_channel', on_delete=models.CASCADE,
                                         null=True)
    customer_type = models.ForeignKey(CustomerType, to_field='customer_type', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    display_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=20, choices=Gender, default='Male')
    company_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    mobile_no = models.CharField(max_length=100, null=True)
    international_no = models.CharField(max_length=100, null=True)
    landline_no = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    shipping_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    internal_note = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='Customer', null=True)
    online_access = models.CharField(max_length=200, choices=ONLINE_ACCESS, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_customer'

    def __str__(self):
        return self.first_name
