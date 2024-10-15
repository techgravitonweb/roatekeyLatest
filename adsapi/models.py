from unicodedata import category
from django.db import models
from embed_video.fields import EmbedVideoField
from account.models import User
from jsonfield import JSONField
from picklefield.fields import PickledObjectField
from paymentapi.models import Order
# Create your models here.
STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharastra','Maharastra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telengana','Telengana'),
    ('Tripura','Tripura'),
    ('Uttarkhand','Uttarkhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)

class Product(models.Model):
    CONDITION = (
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    )
    image = models.CharField(max_length=1502222222222222,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=150,null=False,blank=False)
    price = models.DecimalField(max_digits=11,decimal_places=2,null=True,blank=False)
    tags = models.CharField(max_length=150,null=True,blank=False)
    description = models.TextField()
    category = models.CharField(max_length=50,null=True,blank=True)
    brand = models.CharField(max_length=200)
    condition = models.CharField(max_length=100, choices=CONDITION)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    City = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=6)
    lati = models.CharField(max_length=100,default=0)
    long = models.CharField(max_length=100,default=0)
    date_created = models.CharField(max_length=150,null=False,blank=False ,default="null")
    video = EmbedVideoField(null=True, blank=True) 
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    subCategoryType=models.CharField(default="null",max_length=3232)
    subCategoryValue=models.CharField(default="null",max_length=3232)
    viewsproduct = models.IntegerField(default=0)
    phoneNumber =models.CharField(default="null",null=True,blank=True,max_length=112)
    BuildUpArea =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Flor =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    ApartMentType =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Availability =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    FurnishedType =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Property =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Parking =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    PowerBackup =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Gym =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Garden =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Pool =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Lift =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    PlanCategory = models.CharField(max_length=2322,null=True)
    featured_ads = models.CharField(max_length=2322,null=True)
    ads_limit = models.CharField(max_length=2322,null=True)
    ads_timing = models.CharField(max_length=2322,null=True)
    top_listing = models.CharField(max_length=2322,null=True)
    support = models.CharField(max_length=2322,null=True)
    colorCheck= models.CharField(max_length=2322,null=True)
    sizeCheck= models.CharField(max_length=2322,null=True)
    oldPetsCheck= models.CharField(max_length=2322,null=True)
    start= models.CharField(max_length=2322,null=True)
    end= models.CharField(max_length=2322,null=True)
    school=models.CharField(max_length=2322,null=True)
    college=models.CharField(max_length=2322,null=True)
    brand=models.CharField(max_length=2322,null=True)
    engine=models.CharField(max_length=2322,null=True)
    year=models.CharField(max_length=2322,null=True)
    kmdriven=models.CharField(max_length=2322,null=True)
    setkmDriven=models.CharField(max_length=2322,null=True)
    registrationYear=models.CharField(max_length=2322,null=True)
    setregistrationYear=models.CharField(max_length=2322,null=True)
    extraField=models.CharField(max_length=232333332,null=True)
    adsType=models.CharField(max_length=232333332,null=True)
    plan=models.CharField(max_length=232333332,null=True)
    DaysLimit=models.IntegerField(default=0)
    expiry=models.BooleanField()
    deleted=models.BooleanField(default=False)



#Wishlist Models
class WishListItems(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    #wishlist = models.ForeignKey(WishList,on_delete=models.CASCADE, related_name='wishlistitems')
    item = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)  


# class AdsMessage(models.Model):
#     userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
#     adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
#     message=models.JSONField()
# class AdsMessagename(models.Model):
#     userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
#     adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
#     message=models.TextField()
import datetime
class adsmangeme(models.Model):
    userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
    message=models.TextField()
    connectMember=models.CharField(max_length=223232,default="srishtisrija@gmail.com")
    date_created =models.CharField(max_length=20,default=datetime.datetime.now().strftime('%Y-%m-%d'))



class AdsAdressLatLon(models.Model):
    ads=models.ForeignKey(Product, on_delete=models.CASCADE)
    lat=models.IntegerField()
    lon=models.IntegerField()

class ImageAdsModels(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True) 
    image=models.CharField(max_length=1502222222222222,null=True,blank=True)

class RealEstateEnquery(models.Model):
    firstName=models.CharField(max_length=232)
    lastName=models.CharField(max_length=232)
    email=models.CharField(max_length=343)
    zip_code=models.CharField(max_length=232)
    date_created = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
class ReportAds(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    report=models.CharField(max_length=23222)
    dates = models.CharField(max_length=30,default=datetime.datetime.now().strftime('%Y-%m-%d'))
class AdsComment(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    email=models.CharField(max_length=23222)
    datetimeValue=models.CharField(max_length=232)
    message=models.CharField(max_length=23222)

class LastLogin(models.Model):
    userlogin= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    lastloginValue =models.CharField(max_length=2322)


class QrCode(models.Model):
    image= models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    product= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)

class Pricing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2322,null=True)
    days = models.CharField(max_length=2322,null=True)
    regulars = models.CharField(max_length=2322,null=True)
    topAds = models.CharField(max_length=2322,null=True)
    featured = models.CharField(max_length=2322,null=True)
    response=models.CharField(max_length=1211,null=True)
    teleSupport = models.BooleanField(default=False)
    chatSupport=models.BooleanField(default=False)
    dedicatedRm=models.BooleanField(default=False)
    hol9Website=models.BooleanField(default=False)
    OrderID=models.CharField(max_length=1211,null=True)
    ads_timing = models.CharField(max_length=30,default=datetime.datetime.now().strftime('%Y-%m-%d'))


#admin auth 
class AdminAuth(models.Model):
    username=models.CharField(max_length=2322,null=False)
    password =models.CharField(max_length=2322,null=False)
    name=models.CharField(max_length=2322,null=True)



class PaymentDetailsValues(models.Model):
    UserValue=models.ForeignKey(User, on_delete=models.CASCADE)
    PlanValue=models.ForeignKey(Pricing, on_delete=models.CASCADE)
    OrderValue=models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.CharField(max_length=10,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
class WishlistData(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    wishlistData=models.CharField(max_length=2322,null=False)

class CurrentDate(models.Model):
    dateFiled=models.CharField(max_length=1211)