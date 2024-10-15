import json
from django.conf import UserSettingsHolder
from django.http import HttpResponse
from django.shortcuts import render
from httplib2 import Response
import requests
from account.models import User
import datetime
from .models import *
from blogsapi.models import *
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from account.models import *
from blogsapi.models import *
# from commentbox.models import *
from otp_reg.models import *
from pagesapi.models import *
from paymentapi.models import *
from profileapi.models import * 


# from rest_framework import serializers
# Create your views here.
import ast

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#WishList Views
from .models import WishListItems
from rest_framework.generics import CreateAPIView,DestroyAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .serializers import WishListItemsTestSerializer
from django.shortcuts import get_object_or_404
class AddtoWishListItemsView(CreateAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WishListItems.objects.all()
    serializer_class = WishListItemsTestSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_seller:
            item = get_object_or_404(Product, pk=self.kwargs['pk'])
            serializer.save(owner=user, item=item)
        else:                
            raise serializers.ValidationError("This is not a customer account.Please login as customer.")


    def perform_destroy(self, instance):
        instance.delete()
from django.core import serializers
import ast
class AdsMessageName(APIView):
  def post(self, request, format=None):
    if not request.data.get("adsid"):
        userid=request.data.get("userid")
        UserIdMail=User.objects.get(pk=userid)
        data=adsmangeme.objects.filter(userid=UserIdMail)
        for x in data:
            x.connectMember=x.adsUserId.email
            print("xxxxxxx",x.adsUserId.email)
        qs_json = serializers.serialize('json', data)
        for x in data:
            print(x.message)
            print("dataval;uie",data)
            return HttpResponse(qs_json, content_type='application/json')
    userid=request.data.get("userid")
    UserIdMail=User.objects.get(pk=userid)
    adsid=request.data.get("adsid")
    print("!!!user",UserIdMail.email)
    message=request.data.get("message")
    datetime=request.data.get("datetime")
    adsuserid=Product.objects.get(pk=adsid)
    print("@@@userid",adsuserid.user.id)
    print(request.data.get)
    s=adsmangeme.objects.create(userid=UserIdMail,adsUserId=adsuserid.user,message=message)
    print(s.message)
    s.save()
    # if adsmangeme.objects.filter(userid=userid).filter(adsUserId=adsuserid.user.id):
    #     # updatemessage=adsmangeme.objects.get(userid=userid).get(adsUserId=adsuserid.user.id)
    #     # updatemessage.message[datetime]=message
    #     # updatemessage.save()
    #     updatemessage=adsmangeme.objects.filter(userid=userid).filter(adsUserId=adsuserid.user.id)
    #     for x in updatemessage:
    #         # message={}
    #         # s[datetime]=message
    #         print(x.message)
    #         print(type(x.message))
    #         s=ast.literal_eval(x.message)
    #         print(s)
    #         print(message)
    #         s[datetime]=message
    #         print(s)
    #         x.message=s
    #         x.save()
    #         # print("x",x.message["232/23/2/3"])
    #     print("updatemessage",updatemessage)
    #     # data=json.loads(updatemessage)
    #     print(type(updatemessage))
    #     print("already their ",adsmangeme.objects.filter(userid=userid).get(adsUserId=adsuserid.user.id))
        
    # else:
    #     message={}
    #     message[datetime]=message
    #     s=adsmangeme.objects.create(userid=UserIdMail,adsUserId=adsuserid.user,message=message)
    #     print(s.message)
    #     s.save()
    #     return HttpResponse("stored in database", content_type='application/json')
    #     print("not their ")
    return HttpResponse("qs_json", content_type='application/json')
  def get(self,request):
    userid=request.data.get("userid")
    UserIdMail=User.objects.get(pk=userid)
    
    data=adsmangeme.objects.filter(userid=UserIdMail)
    for x in data:
        x.connectMember=x.adsUserId.email
        print("xxxxxxx",x.adsUserId.email)
    qs_json = serializers.serialize('json', data)
    for x in data:
        print(x.message)
    print("dataval;uie",data)
    return HttpResponse(qs_json, content_type='application/json')


class AdsAdressLatLonView(APIView):
  def get(self, request):
    allads=Product.objects.all()
    for x in allads:
        print("not their ",x.id)
        lat=12.12222
        lon=77.2322
        if(not AdsAdressLatLon.objects.filter(ads=x.id)):
            print("not their ",x.id)
            address=x.locality+x.city+x.state+","+x.zip_code
            print("address value",address)
            # url = "https://address-from-to-latitude-longitude.p.rapidapi.com/geolocationapi"
            # querystring = {"address":address}
            # headers = {
	        #     "X-RapidAPI-Key": "331734c762msh87686d3f66d810fp1c85ebjsn31d2ac2b6d68",
	        #     "X-RapidAPI-Host": "address-from-to-latitude-longitude.p.rapidapi.com"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print("ads latitude longtitude",response.text)
            # print(response.text)
            s=AdsAdressLatLon.objects.create(ads_id=x.id,lat=lat+2,lon=lon+2)
            s.save()
        else:
            print("else block ")
    jsonLatLonData=AdsAdressLatLon.objects.all()
    qs_json = serializers.serialize('json', jsonLatLonData)
    return HttpResponse(qs_json, content_type='application/json')


class chatMessages(APIView):
  def post(self, request, format=None):
    # s=adsmangeme.objects.all().delete()
    userid=request.data.get("userid")
    adsUserEmail=request.data.get("adsUserEmail")
    print("values printing userid adsuseremail",userid,adsUserEmail)
    s=User.objects.get(email=adsUserEmail)
    print("user id ads ",s.pk)
    messageData=adsmangeme.objects.filter(userid=userid,adsUserId=s.pk)
    # for x in messageData:
    #     print(x.message)
    #     print(type(x.message))
        # print( ast.literal_eval(x.message))
        # print(type( ast.literal_eval(x.message)))
        # print(json.dumps(ast.literal_eval(x.message)))
        # data=json.dumps(ast.literal_eval(x.message))
    qs_json = serializers.serialize('json', messageData)
    return HttpResponse(qs_json, content_type='application/json')
# @api_view(['GET', 'POST'])
# def AdsMessage(request):
#     print("@@fjdiojfdoi")
#     if request.method=="POST":
#         print("callking")
#         return render ("stored")

class chatting(APIView):
  def post(self, request, format=None):
    sender=request.data.get("sender")
    reciever=request.data.get("reciever")
    # senderEmailId=User.objects.get(pk=sender)
    # print("senderEmailid",senderEmailId)
    message=request.data.get("message")
    print("fdfjdsl")
    # datetime=str(datetime.datetime.now())
    s=adsmangeme.objects.create(userid=User.objects.get(email=sender),adsUserId=User.objects.get(email=reciever),message=message,connectMember=sender)
    s.save()
    # qs_json = serializers.serialize('json', messageData)
    return HttpResponse("qs_json", content_type='application/json')


class uploadImages(APIView):
    def post(self, request, format=None):
        imagelist=request.data.get("imageList")
        adsid=request.data.get("adsid")
        s=Product.objects.get(pk=adsid)
        print(imagelist)
        # for x in imagelist:
        return HttpResponse("qs_json", content_type='application/json')

class RealEstateEnquery1(APIView):
    def post(self, request, format=None):
        firstName=request.data.get("firstName")
        lastName=request.data.get("lastName")
        email=request.data.get("email")
        zip_code=request.data.get("zip_code")
        s=RealEstateEnquery.objects.create(firstName=firstName,lastName=lastName,email=email,zip_code=zip_code)
        s.save()
        return HttpResponse("sucess", content_type='application/json')


class ReportAds1(APIView):
    def post(self, request, format=None):
        ads=request.data.get("ads")
        adsModel=Product.objects.get(pk=ads)
        reportMessage=request.data.get("report")
        s=ReportAds.objects.create(ads=adsModel,report=reportMessage)
        s.save()
        return HttpResponse("sucess", content_type='application/json')


class AdsUpload(APIView):
    def post(self, request, format=None):
        imageList=request.data.get("imageList")
        adsiD= request.data.get("adsId")
        print(imageList)
        print(adsiD)
        if imageList is None:
            s1= ImageAdsModels.objects.filter(ads_id=adsiD)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        else:
            s=ImageAdsModels.objects.create(image=imageList,ads_id=adsiD)
            s.save()
            print(s)
            # imageList1=request.data.get("imageList1")
            print("@@@@imagelist data ,ads id",imageList,adsiD)
            print("image view",list(imageList))
        
            return HttpResponse("sucess", content_type='application/json')

class adsCommentBoxView(APIView):
    def post(self, request, format=None):
        # imageList=request.data.file("imageList")
        ads= request.data.get("ads")
        if "message" not in request.POST:
            print("for data calling ")
            s1=AdsComment.objects.filter(ads_id=ads)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        email= request.data.get("email")
        message= request.data.get("message")
        datevalue= datetime.datetime.now().strftime('%Y-%m-%d')
        print("value")
        s=AdsComment.objects.create(ads_id=ads,email=email,message=message,datetimeValue=datevalue)
        s.save()
        # s1=AdsComment.objects.filter(ads=ads)
        # qs_json = serializers.serialize('json', s1)
        return HttpResponse("Success", content_type='application/json')

class blogCommentBoxView(APIView):
    def post(self, request, format=None):
        # imageList=request.data.file("imageList")
        blogs= request.data.get("blogs")
        if "message" not in request.POST:
            print("for data calling ")
            s1=BlogComment.objects.filter(ads_id=blogs)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        email= request.data.get("email")
        message= request.data.get("message")
        datevalue= datetime.datetime.now().strftime('%Y-%m-%d')
        s=BlogComment.objects.create(ads_id=blogs,email=email,message=message,datetimeValue=datevalue)
        s.save()
        # s1=AdsComment.objects.filter(ads=ads)
        # qs_json = serializers.serialize('json', s1)
        return HttpResponse("Success", content_type='application/json')
import qrcode
from PIL import Image

class qrCodeAds(APIView):
    def post(self, request, format=None):
        product= request.data.get("product")
        Logo_link = 'hola9.png'

        logo = Image.open(Logo_link)

        # taking base width
        basewidth = 100

        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
	        error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        # taking url or text
        url = 'https://www.geeksforgeeks.org/'

        # adding URL or text to QRcode
        QRcode.add_data(url)

        # generating QR code
        QRcode.make()

        # taking color name from user
        QRcolor = 'black'

        # adding color to QR code
        QRimg = QRcode.make_image(
	    fill_color=QRcolor, back_color="white").convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
	        (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        # save the QR code generated
        QRimg.save('gfg_QR.png')
        return HttpResponse("Success", content_type='application/json')
class PricingViews(APIView):
    def post(self, request, format=None):
        user=request.data.get("user")
        category =request.data.get("category")
        featured_ads =request.data.get("featured_ads")
        ads_limit =request.data.get("ads_limit")
        ads_timing =request.data.get("ads_timing")
        top_listing=request.data.get("top_listing")
        support=request.data.get("support")
        adsLeft=request.data.get("adsLeft")
        if Pricing.objects.filter(user_id=user):
            s=Pricing.objects.get(user_id=user)
            s.category=category
            s.featured_ads=featured_ads
            s.ads_limit=ads_limit
            s.ads_timing=ads_timing
            s.top_listing=top_listing
            s.support=support
            s.adsLeft=adsLeft
            s.save()
        else:
            s=Pricing.objects.create(user_id=user,category=category,featured_ads=featured_ads,ads_limit=ads_limit,ads_timing=ads_timing,top_listing=top_listing,support=support,adsLeft=adsLeft)
            s.save()
        print("s.id is printing ........................................",s.id)
        return HttpResponse("Success",content_type='application/json') 

class getPricingViews(APIView):
    def post( self,request, format=None):
        user =request.data.get("user")
        s=Pricing.objects.filter(user_id=user)
        print(s)
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json')       
class updatePlanLimit(APIView):
    def post( self,request, format=None):
        user =request.data.get("user")
        s=Pricing.objects.filter(user_id=user)
        print(s)
        for x in s:
            x.adsLeft=int(x.adsLeft)-1
            x.adsLeft=str(x.adsLeft)
            x.save()
        return HttpResponse("success", content_type='application/json') 


#under developement userDataCount api
class UserDataCount(APIView):
    def post( self,request, format=None):
        return HttpResponse("success", content_type='application/json')  

class allAdsByInerval(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        condition=request.data.get("condition")
        isActive=request.data.get("isActive")
        user=request.data.get("user")
        print(type(start),type(end))
        if isActive:
            s=Product.objects.filter(is_active=isActive).order_by('-viewsproduct')[int(start):int(end)]
        else:
            if condition=="min":
                s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('price')[int(start):int(end)]
            elif  condition =="max":
                s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-price')[int(start):int(end)]
            elif condition == "featured":
                s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).filter(~Q(PlanCategory="Free"))[int(start):int(end)]
            else:
                s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-id')[int(start):int(end)]
        if user:
            s=Product.objects.filter(user=user).filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-id')[int(start):int(end)]
        print(s)
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json') 
from django.db.models import F, Q, TextField, Value
class categoryAdsByInterval(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        category=request.data.get("category")
        subcateory=request.data.get("subCategory")
        locality=request.data.get("locality")
        location=request.data.get('location')
        searchQuery=request.data.get('searchQuery')
        minPrice=request.data.get('minPrice')
        maxPrice=request.data.get('maxPrice') 
        print("changing")
        print(start,end ,category,subcateory,locality,location)
        if location and subcateory and minPrice and maxPrice and searchQuery:
            print("all search filed is passed")
            s=Product.objects.filter(category=category).filter(subCategoryValue=subcateory).filter(city=location).filter(price__gte=int(minPrice)).filter(price__lte=maxPrice).filter(title__icontains=searchQuery)
        elif subcateory:
            print("subcategory")
            s=Product.objects.filter(category=category).filter(subCategoryValue=subcateory)
        elif location:
            print("location dpendtecny")
            s=Product.objects.filter(city=location)
            print(s.count())
        elif locality and category:
            print("localty calling only ")
            #.filter(locality="hello")
            s=Product.objects.filter(category=category).filter(locality=locality)
            for x in s:
                print(x.locality)
            print(s,s.count())
        else:
            print("category")
            s=Product.objects.filter(category=category)
        print(s)
        s=s.filter(is_active=True).filter(expiry=False).filter(deleted=False)[int(start):int(end)]
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json')  
class subCategoryAdsByInterva(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        subCategory=request.data.get("subCategory")
        s=Product.objects.filter(subCategoryValue=subCategory)[int(start):int(end)]
        print(s)
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json')  
class adminAuth(APIView):
    def post( self,request, format=None):
        username =request.data.get("username")
        password=request.data.get("password")
        s=AdminAuth.objects.filter(username=username).filter(password=password)
        if s:
            return HttpResponse("true", content_type='application/json')
        else:
            return HttpResponse("false", content_type='application/json')  


class webCountData(APIView):
    def post( self,request, format=None):
        dateads = request.data.get("dateads")
        if dateads=="all":
                data={"user":{
                "Register":[User.objects.all().count()],
                "temetrydaa":[TelemetryDaa.objects.all().count()],
                "ReviewSection":[ReviewSection.objects.all().count()],
                "jobs":[JobApply.objects.all().count()],
                "jobsrequired":[JobsRequired.objects.all().count()]
            },
            "ads":{
                "ads":[Product.objects.all().count()],
                "premium":[Pricing.objects.all().count()],
                "payment_detail":[PaymentDetailsValues.objects.all().count()],
                "RealEstateEnquery":[RealEstateEnquery.objects.all().count()],
                "AdminAuth":[AdminAuth.objects.all().count()],
                "adsmangeme":[adsmangeme.objects.all().count()],
                "LastLogin":[LastLogin.objects.all().count()],
                "ReportAds":[ReportAds.objects.all().count()]
            },
            "Payment":{
                "Order":[Order.objects.all().count()],
                "TransationIdone":[TransationIdone.objects.all().count()]
            },
            "OTP_registration":{
                "OTPVerifiaction":[OTPVerifiaction.objects.all().count()]
            },
            "Blogs":{
                "Blogs":[Blogs.objects.all().count()],
                "BlogComment":[BlogComment.objects.all().count()]
            },
            "Comentbox":{
                "AdsComment":[AdsComment.objects.all().count()]
            },
            "Contact":{
                "contacts":[Contact.objects.all().count()]
            },
            "Profile":{
                "Profile":[Profile.objects.all().count()]
            }
            }
        else:
            data={"user":{
            # "Register":User.objects.filter(created_at=dateads).count(),
            "RegisterData":User.objects.filter(created_at=dateads).count(),
            "telemetrydaa":TelemetryDaa.objects.filter(date=dateads).count(),
            "ReviewSection":ReviewSection.objects.filter(created_at=dateads).count(),
            "jobs":JobApply.objects.filter(created_at=dateads).count(),
            "jobsrequired":JobsRequired.objects.filter(created_at=dateads).count(),


        },
        "ads":{
            "ads":Product.objects.filter(date_created=dateads).count(),
            "premium_ads":Product.objects.filter(~Q(PlanCategory="Free")).filter(date_created=dateads).count(),
            "premium_plan":Pricing.objects.filter(ads_timing=dateads).count(),
            "payment_detail":PaymentDetailsValues.objects.filter(date=dateads).count(),
            # "AdsComment":AdsComment.objects.filter(datetimeValue=dateads).count(),
            "RealEstateEnquery":RealEstateEnquery.objects.filter(date_created=dateads).count(),
        },
        "Payment":{
            "Order":Order.objects.filter(order_dateTele=dateads).count(),
            "TransationIdone":TransationIdone.objects.filter(date_created=dateads).count(),
        },
        # "OTP_registration":{
        #     "OTPVerifiaction":OTPVerifiaction.objects.filter(date=dateads).count(),
        # },
        "Blogs":{
            "Blogs":Blogs.objects.filter(published_time=dateads).count(),
            "BlogComment":BlogComment.objects.filter(datetimeValue=dateads).count(),
        },
        "Comentbox":{
            # "AdsComment":AdsComment.objects.filter(date=dateads).count(),
        },
        "Contact":{
            "contacts":Contact.objects.filter(created_at=dateads).count(),
        },
        "Profile":{
            "Profile":Profile.objects.filter(date=dateads).count(),
        }
        }

        return HttpResponse(json.dumps(data) , content_type='application/json')  

    

class featuredAdsData(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        category=request.data.get("category")
        if category :
            ads=Product.objects.filter(category=category)
        else:
            ads=Product.objects.all()
        recommended=ads.filter(plan="Gold").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        Premium=ads.filter(plan="Platinum").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        Featured=ads.filter(plan="Silver").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        s=recommended.union(Premium,Featured).reverse()
        s1 = serializers.serialize('json', s[int(start):int(end)])
        return HttpResponse(s1 , content_type='application/json') 
class webCountAsperDate (APIView):
    def post( self,request , format=None):
        dateads = request.data.get("dateads")
        ads=Product.objects.filter(date_created=dateads).count()
        premium=Pricing.objects.filter(ads_timing=dateads).count()
        user=User.objects.filter(created_at=dateads).count()
        blog=Blogs.objects.filter(published_time=dateads).count()
        premium=Pricing.objects.filter(ads_timing=dateads).count()
        data={"ads":ads,"user":user,"blog":blog,"premium":premium}
        return HttpResponse(json.dumps(data), content_type='application/json')    
        

class webCountasPerDateData(APIView) :
    def post( self,request , format=None): 
        dateads = request.data.get("dateads")
        if dateads=="all":
            s=Product.objects.all()
        else:
            s=Product.objects.filter(date_created=dateads)
        data = serializers.serialize('json', s) 
        return HttpResponse(data, content_type='application/json') 



class webCountUSERPerDateData(APIView) :
    def post( self,request, format=None): 
        dateads = request.data.get("dateads")
        print(type(dateads))
        finalData={}
        # print(dateads)
        if dateads=="all":
            finalData["RegisterData"]= serializers.serialize('json', User.objects.all()),
            finalData["TelemetryDaa"]= serializers.serialize('json',TelemetryDaa.objects.all()),
            finalData["ReviewSection"]= serializers.serialize('json',ReviewSection.objects.all()),
            finalData["Jobs"]= serializers.serialize('json',JobApply.objects.all()),
            finalData["jobsrequired"]= serializers.serialize('json',JobsRequired.objects.all())
            finalData["ads"]= serializers.serialize('json',Product.objects.all()),
            finalData["premium"]= serializers.serialize('json',Pricing.objects.all()),
            finalData["payment_details"]= serializers.serialize('json',PaymentDetailsValues.objects.all()),
            finalData["RealEstateEnquery"]= serializers.serialize('json',RealEstateEnquery.objects.all()),
            finalData["Blogs"]=serializers.serialize('json',Blogs.objects.all()),
            finalData["Blogscomment"]=serializers.serialize('json',BlogComment.objects.all()),
            finalData["AdsComment"]=serializers.serialize('json',AdsComment.objects.all()),
            finalData["Contact"]=serializers.serialize('json',Contact.objects.all()),
            finalData["Profile"]=serializers.serialize('json',Profile.objects.all()),
            finalData["Order"]=serializers.serialize('json',Order.objects.all()),
            finalData["TransationIdone"]=serializers.serialize('json',TransationIdone.objects.all()),
            finalData["OTPVerifiaction"]=serializers.serialize('json',OTPVerifiaction.objects.all()),
            finalData["AdminAuth"]=serializers.serialize('json',AdminAuth.objects.all()),
            finalData["adsmangeme"]=serializers.serialize('json',adsmangeme.objects.all()),
            finalData["LastLogin"]=serializers.serialize('json',LastLogin.objects.all()),
            finalData["ReportAds"]=serializers.serialize('json',ReportAds.objects.all())

        else: 

            finalData["RegisterData"]=serializers.serialize('json',User.objects.filter(created_at=dateads))
            finalData["telemetrydaa"]=serializers.serialize('json',TelemetryDaa.objects.filter(date=dateads))
            finalData["ReviewSection"]=serializers.serialize('json',ReviewSection.objects.filter(created_at=dateads))
            finalData["jobs"]=serializers.serialize('json',JobApply.objects.filter(created_at=dateads))
            finalData["jobsrequired"]=serializers.serialize('json',JobsRequired.objects.filter(created_at=dateads))
            finalData["ads"]=serializers.serialize('json',Product.objects.filter(date_created=dateads))
            finalData["premium"]=serializers.serialize('json',Pricing.objects.filter(ads_timing=dateads))
            finalData["payment_detail"]=serializers.serialize('json',PaymentDetailsValues.objects.filter(date=dateads))
            finalData["RealEstateEnquery"]=serializers.serialize('json',RealEstateEnquery.objects.filter(date_created=dateads))
            finalData["Blogs"]=serializers.serialize('json',Blogs.objects.filter(published_time=dateads))
            finalData["BlogComment"]=serializers.serialize('json',BlogComment.objects.filter(datetimeValue=dateads))
            finalData["AdsComment"]=serializers.serialize('json',AdsComment.objects.filter(date=dateads))
            finalData["contacts"]=serializers.serialize('json',Contact.objects.filter(created_at=dateads))
            finalData["Profile"]=serializers.serialize('json',Profile.objects.filter(date=dateads))
            finalData["Order"]=serializers.serialize('json',Order.objects.filter(order_dateTele=dateads))
            finalData["OTPVerifiaction"]=serializers.serialize('json',OTPVerifiaction.objects.filter(date=dateads))
            finalData["TransationIdone"]=serializers.serialize('json',TransationIdone.objects.filter(date_created=dateads))
            # finalData["AdminAuth"]=serializers.serialize('json',AdminAuth.objects.filter(date=dateads))
            finalData["adsmangeme"]=serializers.serialize('json',adsmangeme.objects.filter(date_created=dateads))
            # finalData["LastLogin"]=serializers.serialize('json',LastLogin.objects.filter(date=dateads))
            finalData["ReportAds"]=serializers.serialize('json',ReportAds.objects.filter(dates=dateads))          
        return HttpResponse(json.dumps(finalData),content_type='application/json')

class webCountBLOGSPerDateData(APIView) :
    def post( self,request , format=None): 
        dateads = request.data.get("dateads") 
        if dateads=="all":
            s=Blogs.objects.all()
        else: 
            s=Blogs.objects.filter(published_time=dateads)
        data = serializers.serialize('json', s) 
        return HttpResponse(data, content_type='application/json') 

import pandas
from datetime import timedelta
from datetime import datetime
class dataCuntMultipleValues(APIView) :
    def post( self,request , format=None): 
        data={"index":[],"value":[]}
        requestData=request.data.get("requestData")
        start = request.data.get("start") 
        start = datetime.strptime(start[2:], '%y-%m-%d')
        end = request.data.get("end") 
        end = datetime.strptime(end[2:], '%y-%m-%d')
        print(start>end,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'))
        alldates=[]
        print(end,start)
        delta = end-start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            print("daym",type(day.strftime('%Y-%m-%d')))
            if(requestData=="user"):
                s=User.objects.filter(created_at=day.strftime('%Y-%m-%d')).count()
            elif(requestData=="ads"):
                s=User.objects.filter(date_created=day.strftime('%Y-%m-%d')).count()
            elif(requestData=="blog"):
                s=User.objects.filter(published_time=day.strftime('%Y-%m-%d')).count()
            data["index"].append(day.strftime('%Y-%m-%d'))
            data["value"].append(s)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')
import ast
import difflib
class AdsDataFilter(APIView) :
    def post( self,request , format=None):
        start =request.data.get("start")
        end= request.data.get("end")
        print("hi")
        requestData=ast.literal_eval(request.data.get("requestData"))
        print("hello")
        extraField=requestData["extrafiled"] if type(requestData["extrafiled"]) is dict   else ast.literal_eval(requestData["extrafiled"])
        del requestData['extrafiled']
        print(requestData,extraField)
        s=Product.objects.all()
        print(s.count()) 
        filters = {}
        for key1 in requestData:
            if not (key1=="minPrice" or key1=="maxPrice" or key1=="searchValue"):
                key1=key1
                filters[key1] = requestData[key1]
        s1=Product.objects.filter(**filters)
        print(Product.objects.filter(subCategoryValue="Refrigerators/Fridge").filter(category="Furniture"))
        print(s1)
        if 'minPrice' in requestData or 'maxPrice' in requestData:
            s1=s1.filter(price__gte=int(requestData['minPrice']),price__lte=int(requestData['maxPrice']))
        finalProduct=Product.objects.filter(category="e3322222")
        print("latest",finalProduct)
        if len(extraField) != 0:
            for x1 in s1:
                count=len(extraField)
                countTemp=0
                if x1.extraField:
                    if (not x1.extraField =="null"):
                        x1.extraField=ast.literal_eval(x1.extraField)
                        newTempObjProdctExtraFiled={}
                        for x in x1.extraField:
                            z1=x.encode("ascii", "ignore")
                            z2=x1.extraField[x].encode("ascii", "ignore")
                            z11=z1.decode()
                            z44=z2.decode()
                            newTempObjProdctExtraFiled[z11]=z44
                        for singlekeyValue in extraField:
                            if singlekeyValue in newTempObjProdctExtraFiled.keys():
                                m=difflib.SequenceMatcher(None,extraField[singlekeyValue],newTempObjProdctExtraFiled[singlekeyValue]).ratio()
                                if(m*100>80):
                                    countTemp=countTemp+1
                            # if extraField[singlekeyValue] is newTempObjProdctExtraFiled[singlekeyValue]:
                            #     countTemp=countTemp+1
                            #     print("checking")
                print(count,countTemp)
                print(type(count),type(countTemp))
                if(count==countTemp):
                    t1=Product.objects.filter(pk=x1.pk).filter(is_active=True).filter(expiry=False).filter(deleted=False)
                    if t1 :
                        finalProduct=finalProduct.union(t1)
        if "tital" in requestData:
            print("tital is also calling",requestData["title"])
            s1=s1.filter(title__icontains=requestData["title"])
            finalProduct=finalProduct.filter(title__icontains=requestData["title"])
        print("data in tital",s1.count())
        finalProduct = serializers.serialize('json', finalProduct[int(start):int(end)] if len(extraField) != 0 else s1.filter(is_active=True).filter(expiry=False).filter(deleted=False)[int(start):int(end)]) 
        return HttpResponse(finalProduct, content_type='application/json')  
        

# Creates a sorted dictionary (sorted by key)
from collections import OrderedDict
class allPlanData(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        # print(Product.objects.filter(user_id=46))
        # print(user)
        # obj={}
        # obj["Free"]=Product.objects.filter(user=user).filter(PlanCategory="Free").count()
        # print(obj)
        # obj1={}
        # obj1["Premium"]=Product.objects.filter(user=user).filter(PlanCategory="Premium").count()
        # print(obj1)
        # obj2={}
        # obj2["Recommended"]=Product.objects.filter(user=user).filter(PlanCategory="Recommended").count()
        # print(obj2)
        # obj3={}
        # obj3["Featured"]=Product.objects.filter(user=user).filter(PlanCategory="Featured").count()
        # print(obj3)
        # result = json.dumps(obj)
        # result1 = json.dumps(obj1)
        # result2=json.dumps(obj2)
        # result3=json.dumps(obj3)
        allPricingPlanData=Pricing.objects.filter(user=userId)
        planObj={"free":0,"premium":0,"featured":0,"recommended":0}
        allPricingPlanDataList=[]
        for x in allPricingPlanData:
            if(x.category=="Free"):
                planObj["free"]=(planObj["free"]+1)
            elif (x.category=="Featured"):
                planObj["featured"]=(planObj["featured"]+1)
            elif (x.category=="Premium"):
                planObj["premium"]=(planObj["premium"]+1)
            elif (x.category=="Recommended"):
                planObj["recommended"]=(planObj["recommended"]+1)
            allPricingPlanDataList.append(x.category)
        
        planObj["free"]=planObj["free"]*5
        planObj["premium"]=planObj["premium"]*60
        planObj["featured"]=planObj["featured"]*20
        planObj["recommended"]=planObj["recommended"]*100
        print(allPricingPlanDataList)
        print(planObj)
        currentUserPlan=Pricing.objects.filter(user=userId).order_by('-id')[:1]
        currentUserPlanCategory=None
        for x in currentUserPlan:
            currentUserPlanCategory=x.category
        print(currentUserPlan)
        totalUserAds=Product.objects.filter(user=userId)
        finalObj={"totalCount":{
                    "free":[Product.objects.filter(user=userId).filter(PlanCategory="Free").count(),planObj["free"]-Product.objects.filter(user=userId).filter(PlanCategory="Free").count()],
                    "featured":[Product.objects.filter(user=userId).filter(PlanCategory="Featured").count(),planObj["featured"]-Product.objects.filter(user=userId).filter(PlanCategory="Featured").count()],
                    "premium":[Product.objects.filter(user=userId).filter(PlanCategory="Premium").count(),planObj["premium"]-Product.objects.filter(user=userId).filter(PlanCategory="Premium").count()],
                    "recommended":[Product.objects.filter(user=userId).filter(PlanCategory="Recommended").count(),planObj["recommended"]-Product.objects.filter(user=userId).filter(PlanCategory="Recommended").count()]}
                    ,"currentPlan":currentUserPlanCategory,"TotalPlan":list(set(allPricingPlanDataList)),"leftPlan":[]}
        print(finalObj)
        if(not finalObj["totalCount"]["free"][1]==0):
            finalObj["leftPlan"].append("Free")
        if(not finalObj["totalCount"]["featured"][1]==0):
            finalObj["leftPlan"].append("Featured")
        if(not finalObj["totalCount"]["premium"][1]==0):
            finalObj["leftPlan"].append("Premium")
        if(not finalObj["totalCount"]["recommended"][1]==0):
            finalObj["leftPlan"].append("Recommended")
        print(finalObj)
        
        templist=[]
        for key in finalObj["totalCount"]:
            if(finalObj["totalCount"][key][0]==0 and finalObj["totalCount"][key][1]==0):
                templist.append(key)
        temoObj=finalObj["totalCount"]
        for i in templist:
            temoObj.pop(i)
            print(temoObj)
        finalObj["totalCount"]=temoObj
        # finalObj["totalCount"]= OrderedDict(sorted(finalObj["totalCount"].items()))
        result2=json.dumps(finalObj)
        # nalProduct = serializers.serialize('json',result) 
        return HttpResponse(result2, content_type='application/json')


class wishlistData(APIView):
    def post( self,request , format=None):
        condition=request.data.get("request")
        wishlist=request.data.get("wishlist")
        print("wihlist list data ",wishlist,type(wishlist))
        user=request.data.get('user')
        if condition =="GET":
            print("hello")
            finalWishlist=WishlistData.objects.filter(User_id=user)
            finalProduct = serializers.serialize('json', finalWishlist) 
            if not WishlistData.objects.filter(User_id=user):
                finalProduct = serializers.serialize('json', []) 
            return HttpResponse(finalProduct, content_type='application/json')
        if WishlistData.objects.filter(User_id=user):
            s=WishlistData.objects.get(User_id=user)
            s.wishlistData=wishlist
            s.save()
        else:
            s1=WishlistData.objects.create(wishlistData=wishlist,User_id=user)
            s1.save()
        finalWishlist=WishlistData.objects.filter(User_id=user)
        finalProduct = serializers.serialize('json', finalWishlist) 
        return HttpResponse(finalProduct, content_type='application/json')
    def get(self,request):
        user=request.data.get('user')
        finalWishlist=WishlistData.objects.filter(User_id=user)
        finalProduct = serializers.serialize('json', finalWishlist) 
        return HttpResponse(finalProduct, content_type='application/json')


class allPricingPlanData(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        allPricingPlanData=Pricing.objects.filter(user=userId)
        s=Product.objects.filter(user=userId)
        for x in s:
            print(x.plan)
        print("@@@@@@@sss value",s)
        totalPlans=[]
        planObj={"free":0,"Silver":0,"Gold":0,"Platinum":0}
        for x in allPricingPlanData:
            if(x.category=="Free"):
                planObj["free"]=planObj["free"]+1
            elif(x.category=="Silver"):
                planObj["Silver"]=planObj["Silver"]+1
            elif(x.category=="Gold"):
                planObj["Gold"]=planObj["Gold"]+1
            elif(x.category=="Platinum"):
                planObj["Platinum"]=planObj["Platinum"]+1
            totalPlans.append(x.category)
        finalObj={"planDataDetails":{},"postAdsForm":{},"leftPlan":[]}
        finalObj["totalPlan"]=[*set(totalPlans)]
        finalObj["numberOfTimePlan"]=planObj
        for plan in finalObj["totalPlan"]:
            if plan=="Free":
                finalObj["planDataDetails"]["Free"]={}
                finalObj["planDataDetails"]["Free"]["totalAds"]=3
                finalObj["planDataDetails"]["Free"]["reponse"]="Limited"
                finalObj["planDataDetails"]["Free"]["PostedregualAds"]=Product.objects.filter(user_id=userId).filter(plan="Free").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Free"]["leftRegularAds"]=3*planObj["free"]-Product.objects.filter(user_id=userId).filter(plan="Free").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Free"]["limitDays"]=7
                finalObj["postAdsForm"]["Free"]={}
                finalObj["postAdsForm"]["Free"]["category"]=[]
                tempVal=False
                if finalObj["planDataDetails"]["Free"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Free"]["category"].append("Regular")
                if tempVal:
                    finalObj["leftPlan"].append("Free")
                finalObj["postAdsForm"]["Free"]["days"]=7
            elif plan=="Silver":
                finalObj["planDataDetails"]["Silver"]={}
                finalObj["planDataDetails"]["Silver"]["totalAds"]=10
                finalObj["planDataDetails"]["Silver"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Silver"]["limitDays"]=15
                finalObj["planDataDetails"]["Silver"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Silver"]["leftRegularAds"]=5*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Silver"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Silver"]["leftTopAds"]=2*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Silver"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Silver"]["leftFeaturedAds"]=3*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Silver"]["TeleSupport"]=True
                

                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Silver"]={}
                finalObj["postAdsForm"]["Silver"]["category"]=[]
                if finalObj["planDataDetails"]["Silver"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Silver"]["category"].append("Regular")
                if finalObj["planDataDetails"]["Silver"]["leftTopAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Silver"]["category"].append("TopAds")
                if finalObj["planDataDetails"]["Silver"]["leftFeaturedAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Silver"]["category"].append("Featured")
                
                if tempVal:
                    finalObj["leftPlan"].append("Silver")
                finalObj["postAdsForm"]["Silver"]["days"]=15

            elif plan=="Gold":
                finalObj["planDataDetails"]["Gold"]={}
                finalObj["planDataDetails"]["Gold"]["totalAds"]=10
                finalObj["planDataDetails"]["Gold"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Gold"]["limitDays"]=30
                finalObj["planDataDetails"]["Gold"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Gold"]["leftRegularAds"]=10*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Gold"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Gold"]["leftTopAds"]=5*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Gold"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Gold"]["leftFeaturedAds"]=5*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Gold"]["TeleSupport"]=True
                finalObj["planDataDetails"]["Gold"]["chatSupport"]=True
                finalObj["planDataDetails"]["Gold"]["DeticatedRm"]=True

                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Gold"]={}
                finalObj["postAdsForm"]["Gold"]["category"]=[]
                if finalObj["planDataDetails"]["Gold"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Gold"]["category"].append("Regular")
                if finalObj["planDataDetails"]["Gold"]["leftTopAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Gold"]["category"].append("TopAds")
                if finalObj["planDataDetails"]["Gold"]["leftFeaturedAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Gold"]["category"].append("Featured")
                if tempVal:
                    finalObj["leftPlan"].append("Gold")
                finalObj["postAdsForm"]["Gold"]["days"]=30

            elif plan=="Platinum":
                finalObj["planDataDetails"]["Platinum"]={}
                finalObj["planDataDetails"]["Platinum"]["totalAds"]=3
                finalObj["planDataDetails"]["Platinum"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Platinum"]["limitDays"]=60
                finalObj["planDataDetails"]["Platinum"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Platinum"]["leftRegularAds"]=10*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Platinum"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Platinum"]["leftTopAds"]=5*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="TopAds").count()
                finalObj["planDataDetails"]["Platinum"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Platinum"]["leftFeaturedAds"]=5*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Platinum"]["TeleSupport"]=True
                finalObj["planDataDetails"]["Platinum"]["chatSupport"]=True
                finalObj["planDataDetails"]["Platinum"]["DeticatedRm"]=True
                finalObj["planDataDetails"]["Platinum"]["Hol9Web"]=True

                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Platinum"]={}
                finalObj["postAdsForm"]["Platinum"]["category"]=[]
                if finalObj["planDataDetails"]["Platinum"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Platinum"]["category"].append("Regular")
                if finalObj["planDataDetails"]["Platinum"]["leftTopAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Platinum"]["category"].append("TopAds")
                if finalObj["planDataDetails"]["Platinum"]["leftFeaturedAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Platinum"]["category"].append("Featured")
                if tempVal:
                    finalObj["leftPlan"].append("Platinum")
                finalObj["postAdsForm"]["Platinum"]["days"]=30
                finalObj["postAdsForm"]["Platinum"]["days"]=60
        print(finalObj)
        result2=json.dumps(finalObj)
        return HttpResponse(result2, content_type='application/json')

import json

class getExtraCat(APIView):
    def post( self,request , format=None):
        category=request.data.get("category")
        subcategory=request.data.get("subcategory")
        json1_file = open('/hola9Main/hola9DjangoLatest/adsapi/json/subcategory.json','r+', encoding="utf-8")
        obj=json.load(json1_file)
        print(list[obj.keys()])
        if category and subcategory:
            result2=json.dumps(obj[category][subcategory])
        elif category:
            result2=json.dumps(list(obj[category].keys()))
        print(result2)
        return HttpResponse(result2, content_type='application/json')

import time
import datetime
def jobEveryDAYRun(request):
    s=datetime.datetime.now().strftime('%y-%m-%d')
    print(s)
    p=True
    while(p):
        if not CurrentDate.objects.filter(dateFiled=str(s)):
            modelUpdate=CurrentDate.objects.create(dateFiled=s)
            productData=Product.objects.all()
            for x in productData:
                if x.DaysLimit==0:
                    x.expiry=True
                else:
                    x.DaysLimit=x.DaysLimit-1
                x.save()
        p=False
        print("hello wrold")
    return HttpResponse("success", content_type='application/json')
class webpopuplist(APIView):
    def post(self,request,format=None):
        dateads= request.data.get("dateads")
        idvalues=request.data.get("id")
        s={}
        if dateads=="User":
            s=User.objects.filter(pk=idvalues)   
        elif dateads=="Product":
            s=Product.objects.filter(pk=idvalues)
        elif dateads == "TelemetryDaa":
            s=TelemetryDaa.objects.filter(pk=idvalues)
        elif dateads == "ReviewSection":
            s=ReviewSection.objects.filter(pk=idvalues)
        elif dateads == "JobApply":
            s=JobApply.objects.filter(pk=idvalues)
        elif dateads == "JobsRequired":
            s=JobsRequired.objects.filter(pk=idvalues)
        elif dateads == "Pricing":
            s=Pricing.objects.filter(pk=idvalues)
        elif dateads == "PaymentDetailsValues":
            s=PaymentDetailsValues.objects.filter(pk=idvalues)
        elif dateads == "RealEstateEnquery":
            s=RealEstateEnquery.objects.filter(pk=idvalues)
        elif dateads == "Blogs":
            s=Blogs.objects.filter(pk=idvalues)
        elif dateads == "BlogComment":
            s=BlogComment.objects.filter(pk=idvalues)
        elif dateads == "AdsComment":
            s=AdsComment.objects.filter(pk=idvalues)
        elif dateads == "Contact":
            s=Contact.objects.filter(pk=idvalues)
        elif dateads == "Profile":
            s=Profile.objects.filter(pk=idvalues)
        elif dateads == "Order":
            s=Order.objects.filter(pk=idvalues)
        elif dateads == "TransationIdone":
            s=TransationIdone.objects.filter(pk=idvalues)
        elif dateads == "adsmangeme":
            s=adsmangeme.objects.filter(pk=idvalues)
        elif dateads == "OTPVerifiaction":
            s=OTPVerifiaction.objects.filter(pk=idvalues)
        elif dateads == "AdminAuth":
            s=AdminAuth.objects.filter(pk=idvalues)
        elif dateads == "LastLogin":
            s=LastLogin.objects.filter(pk=idvalues)
        elif dateads == "ReportAds":
            s=ReportAds.objects.filter(pk=idvalues)

        data=serializers.serialize('json',s)   
        return HttpResponse(data,content_type='application/json')

class DeletedAds(APIView):
    def post( self,request , format=None):
        adsid=request.data.get("adsId")
        ads=Product.objects.get(pk=adsid)
        ads.deleted=True
        ads.expiry=True
        ads.DaysLimit=0
        ads.save()
        return HttpResponse("success", content_type='application/json')

import json
class searchData(APIView):
    def post( self,request , format=None):
        s=Product.objects.all().values('title')
        list_result = [entry["title"] for entry in s] 
        listvalue=[]
        for  x in list_result:
            obj={}
            obj["value"]=x
            listvalue.append(obj)
        print(list_result)
        return HttpResponse(json.dumps(listvalue), content_type='application/json')


class approveAds(APIView):
    def post( self,request , format=None):
        idValue=request.data.get('idValue')
        if not idValue:
            s=Product.objects.filter(is_active=False)
            data=serializers.serialize('json',s)
        else:
            s=Product.objects.get(pk=idValue)
            s.is_active=true
            s.save()
            data="success"
        return HttpResponse(data, content_type='application/json')
  





