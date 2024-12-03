from django.db import models

# SEASONS_CHOICES = (
#     ('Spring', 'Spring'),
#     ('Summer', 'Summer'),
#     ('Autumn', 'Autumn'),
#     ('Winter', 'Winter'),
# )

STATUS = (
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('inactive', 'Inactive'),
)


# Create your models here.
class Outlet(models.Model):
    outlet_code = models.CharField(max_length=100, null=True, unique=True)
    outlet_name = models.CharField(max_length=100, null=True, unique=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_outlet'

    def __str__(self):
        return self.outlet_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_brand'

    def __str__(self):
        return self.brand_name


class AttributeType(models.Model):
    att_type = models.CharField(max_length=100, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_attribute_type'

    def __str__(self):
        return self.att_type


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100, null=True, unique=True)
    att_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE, null=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_attribute'

    def __str__(self):
        return self.attribute_name


class Variation(models.Model):
    variation_name = models.CharField(max_length=100, null=True)
    attribute_name = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_variation'

    def __str__(self):
        return self.variation_name


class HeadCategory(models.Model):
    hc_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_head_category'

    def __str__(self):
        return self.hc_name


class ParentCategory(models.Model):
    hc_name = models.ForeignKey(HeadCategory, on_delete=models.CASCADE, null=True)
    pc_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_parent_category'

    def __str__(self):
        return self.pc_name


class Category(models.Model):
    pc_name = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, null=True)
    attribute_group = models.ManyToManyField(Attribute, through='CategoryAttribute')
    category_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    subcategory_option = models.TextField(max_length=500, null=True)  # True, False
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_category'

    def __str__(self):
        return self.category_name


class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_category_attribute'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    attribute_group = models.ManyToManyField(Attribute, through='SubCategoryAttribute')
    sub_category_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')  # Active,Inactive, Pending
    # attribute_name = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_sub_category'

    def __str__(self):
        return self.sub_category_name


class SubCategoryAttribute(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_subcategory_attribute'


class TemporaryProduct(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    season = models.CharField(max_length=10,null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='TemProduct', default='', null=True, blank=True)
    cost_price = models.CharField(max_length=100, null=True, blank=True)
    selling_price = models.CharField(max_length=100, null=True, blank=True)
    discount_price = models.CharField(max_length=100, null=True, blank=True)
    wholesale_price = models.CharField(max_length=100, null=True, blank=True)
    retail_price = models.CharField(max_length=100, null=True, blank=True)
    token_price = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_product_temp'

    def __str__(self):
        return self.product_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=100, null=True, unique=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    # season = models.CharField(max_length=10, choices=SEASONS_CHOICES, default='Spring')
    season = models.CharField(max_length=10,null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='Product', default='', null=True, blank=True)
    cost_price = models.CharField(max_length=100, null=True, blank=True)
    selling_price = models.CharField(max_length=100, null=True, blank=True)
    discount_price = models.CharField(max_length=100, null=True, blank=True)
    wholesale_price = models.CharField(max_length=100, null=True, blank=True)
    retail_price = models.CharField(max_length=100, null=True, blank=True)
    token_price = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_product'

    def __str__(self):
        return self.sku


# class ImageModel(models.Model):
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'image_model'
#
#     def __str__(self):
#         return self.title
