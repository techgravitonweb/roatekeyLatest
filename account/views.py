from contextlib import nullcontext
from genericpath import exists
import json
from site import addsitedir
from tkinter import EW
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from adsapi.models import Product,LastLogin,QrCode
from blogsapi.models import Blogs
from adsapi.serializers import ProductSerializer
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,jobdetailsSerializers,jobsRequiredSerialize
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
import http.client
from paymentapi.models import TransationIdone
import datetime
from pytz import timezone 

from profileapi.models import Profile
from .models import PhoneOTP , User ,ReviewSection,TelemetryDaa,JobApply,JobsRequired
import ast
from adsapi.models import Pricing,PaymentDetailsValues

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


from django.core import serializers

class userads(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    print(request.user.id)
    adsData=Product.objects.filter(user =request.user)
    print("adsData",adsData)
    serializer = serializers.serialize('json', adsData)
    print(serializer)
    qs_json = serializers.serialize('json', adsData)
    return HttpResponse(qs_json, content_type='application/json')

class userblogs(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    print(request.user.id)
    blogsData=Blogs.objects.filter(user =request.user)
    print("blogsData",blogsData)
    serializer = serializers.serialize('json', blogsData)
    print(serializer)
    qs_json = serializers.serialize('json', blogsData)
    return HttpResponse(qs_json, content_type='application/json')


class wishlist(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    wishlist=request.data.get('wishlist')
    print("wishlist ",wishlist,type("wishlist"),len(wishlist))

    
    if (len(wishlist) == 0):
      print("len is zerop")
      newlist=[]
    else:
      wishlist=wishlist+","
      newlist=[]
      y=""
      for x in wishlist:
        if x!=",":
          y=y+x
        else:
          newlist.append(int(y))
          print("value",newlist)
          y=""
          print(newlist)
    # print("@@WISHLIST",type(list(wishlist)))
    # wishlist=list(wishlist)
    # print("starting")
    # # wishlist=wishlist.remove(',')
    # print(wishlist)
    # wishlistone=[]
    # for x in wishlist:
    #   if x!=',':
    #     wishlistone.append(int(x))
    # print("current wishlist",wishlistone)
    # res = []
    # for i in wishlistone:
    #   if i not in res:
    #       res.append(i)
    # print("res",res)

    wishlist=Product.objects.filter(pk__in=newlist)
    print("@@findal dat in wishlist ",wishlist)
    wishlist = serializers.serialize('json', wishlist)
    return HttpResponse(wishlist, content_type='application/json')




class updateProfile1(APIView):
  def post(self, request, format=None):
    email=request.data.get("email")
    s=Profile.objects.filter(email=email)
    print(type(s))
    if(s):
      profile = serializers.serialize('json', s)
      return HttpResponse(profile, content_type='application/json')
    return HttpResponse("false", content_type='application/json')

class createFeatured(APIView):
  def post(self, request, format=None):
    image=request.data.get("image")
    user=request.data.get("user")
    title=request.data.get("title")
    price=request.data.get("price")
    tags=request.data.get("tags")
    description=request.data.get("description")
    category=request.data.get("category")
    brand=request.data.get("brand")
    condition=request.data.get("condition")
    state=request.data.get("state")
    city=request.data.get("city")
    locality=request.data.get("locality")
    zip_code=request.data.get("zip_code")
    # date_created=request.data.get("date_created")
    # video=request.data.get("video")
    is_featured=True
    is_active=False
    token=request.data.get("token")
    print(token)
    # print("success value",self.request.session["success"])
    s1=TransationIdone.objects.filter(id1=token)
    print("9999999999999999999999999999999999999999",s1)
    if s1:
      if("succ" in token):
        print("success")
        s=Product.objects.create(image=image,user_id=user,title=title,tags=tags,price=price,description=description,category=category,brand=brand,condition=condition,state=state,city=city,locality=locality,zip_code=zip_code,is_featured=is_featured,is_active=is_active)
        s.save()
        s1=TransationIdone.objects.get(id1=token)
        print(s.pk)
        print("fsedjklfjoisdpljufkl;dsfjkldsfjkl;esdjflksddfjdskl")
        s1.adsid_id=s.pk
        s1.userid_id=user
        s1.save()
      else:
        print("fail path")
        return HttpResponse("fail", content_type='application/json')
    else:
      return HttpResponse("fail", content_type='application/json')
    
    return HttpResponse("success", content_type='application/json')


class ordersPyament(APIView):
  def post(self,request,format=None):
    user=request.data.get("user")
    order=request.data.get("order")
    payment=request.data.get("payment")
    print(order)
    
    s1=Product.objects.filter(user_id=user)
    s=TransationIdone.objects.filter(userid_id=user)
    data = serializers.serialize('json', s1)
    print(data)
    # return HttpResponse(data,content_type='application/json')
    
      
    
    s=TransationIdone.objects.filter(userid_id=user)
    
    # return HttpResponse("unable to fetch",)
    for x in s:
      s1=Product.objects.filter(id=x.adsid_id)
      if s1:
        x.ProductData=serializers.serialize('json', s1)
      data = serializers.serialize('json', s)
      return HttpResponse(data,content_type='application/json')



class verifyEmail(APIView):
    def post(self,request,format=None):
      email=request.data.get("email")
      s=User.objects.filter(email=email)
      if s:
        return HttpResponse("already exist",content_type='application/json')
      else:
        return HttpResponse("not exist",content_type='application/json')



class verifyPhone(APIView):
    def post(self,request,format=None):
      phoneNumber=request.data.get("phoneNumber")
      print(phoneNumber)
      # s1=User.objects.filter(email=email)
      # s=User.objects.filter(phoneNumber=phoneNumber)
      try:
        user = User.objects.get(phoneNumber=phoneNumber)
      except:
        user=None
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['phone Number not exist']}}, status=status.HTTP_404_NOT_FOUND)
class verifyEmailLogin(APIView):
    def post(self,request,format=None):
      email=request.data.get("email")
      print(email)
      # s1=User.objects.filter(email=email)
      # s=User.objects.filter(phoneNumber=phoneNumber)
      try:
        user = User.objects.get(email=email)
      except:
        user=None
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email not exist']}}, status=status.HTTP_404_NOT_FOUND)
class viewsupdate(APIView):
    def post(self, request, format=None):
        adsID= request.data.get("adsID")
        s = Product.objects.get(pk=adsID)
        s.viewsproduct = s.viewsproduct+1
        s.save()
        return HttpResponse("success", content_type='application/json')          

class updateProfileApi(APIView):
    def post(self, request, format=None):
        user = request.data.get("user")
        print(user)
        if user is None:
          print('address')
          idvalues=request.data.get("idvalues")
          try:
            s=Profile.objects.filter(user_id=idvalues)
            data = serializers.serialize('json', s)
            return HttpResponse(data, content_type='application/json') 
          except:
            s=None
            return HttpResponse("Not exist", content_type='application/json') 
        else:
              image = request.data.get("image")
              user = request.data.get("user")
              name = request.data.get("name")
              email = request.data.get("email")
              PhoneNumber = request.data.get("PhoneNumber")
              print(PhoneNumber)
              address = request.data.get("address")
              state = request.data.get("state")
              city =request.data.get("city")
              zipcode = request.data.get("zipcode")
              print(Profile.objects.filter(user_id=user))
              if Profile.objects.filter(user_id=user) :
                s=Profile.objects.get(user_id=user)
                s.image=image
                s.name=name
                s.email=email
                s.PhoneNumber=PhoneNumber
                s.address=address
                s.state=state
                s.city=city
                s.zipcode=zipcode
                s.save()
              else:
                userID = User.objects.get(pk=user)
                s=Profile.objects.create(image=image,user=userID,city=city,name=name,email=email,PhoneNumber=PhoneNumber,address=address,state=state,zipcode=zipcode,)
                s.save()
              return HttpResponse("success", content_type='application/json') 

class userProfileDetailsApi(APIView):
    def post(self, request, format=None):
        user1 = request.data.get("user")
        s=User.objects.filter(pk=user1)   
        data = serializers.serialize('json', s)
        return HttpResponse(data,content_type='application/json')     

class lastLoginTime(APIView):
    def post(self, request, format=None):
        user1 = request.data.get("user")
        currentDateTime= datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print("start")
        checkUserExit=LastLogin.objects.filter(userlogin_id=user1)
        print("end")
        if checkUserExit:
          print("first")
          checkUserExit=LastLogin.objects.get(userlogin_id=user1)
          checkUserExit.lastloginValue=currentDateTime
          checkUserExit.save()
          print(checkUserExit)
          data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=checkUserExit.userlogin_id))
          return HttpResponse(data,content_type='application/json') 
        else:
          print("second")
          s=LastLogin.objects.create(userlogin_id=user1,lastloginValue=currentDateTime)
          s.save()
          print(s.pk)
          data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=s.userlogin_id))
          return HttpResponse(data,content_type='application/json')    


class lastLoginTimeGet(APIView):
  def post(self, request, format=None):
      user1 = request.data.get("user")
      data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=user1))
      return HttpResponse(data,content_type='application/json')    

import qrcode
from PIL import Image
import os
import base64
class QrCodeAds(APIView):
  def post(self, request, format=None):
        product= request.data.get("product")
        Logo_link = '/hola9Main/hola9DjangoLatest/adsapi/hola9.png'

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
        url = 'https://hola9.com/ads-listing/'+product

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
        QRimg.save('/hola9Main/hola9DjangoLatest/adsapi/gfg_QR.png')
        logo1 = Image.open("/hola9Main/hola9DjangoLatest/adsapi/gfg_QR.png")
        print(logo1)
        file_path = os.path.join("/hola9Main/hola9DjangoLatest/adsapi/", "gfg_QR.png")
        with open("/hola9Main/hola9DjangoLatest/adsapi/gfg_QR.png", "rb") as image_file:
          encoded_string = base64.b64encode(image_file.read())
        s=QrCode.objects.create(image=encoded_string,product_id=product)
        return HttpResponse("Success", content_type='application/json')

class getQrCodeAds(APIView):
  def post( self,request, format=None):
    product =request.data.get("product")
    s=QrCode.objects.filter(product_id=product)
    data = serializers.serialize('json', s)
    return HttpResponse(data, content_type='application/json')

class reviewSection(APIView):
    def get(self, request, format=None):
      review=ReviewSection.objects.all().order_by("-id")[0:5]
      data = serializers.serialize('json', review)
      return HttpResponse(data , content_type='application/json')
 
    
class TrackingTele(APIView):
  def post( self,request, format=None):
    teleData =request.data.get("data")
    data=ast.literal_eval(teleData)
    teleId=data["id"]
    print(teleId)
    if(TelemetryDaa.objects.filter(teleId=teleId)):
      details=TelemetryDaa.objects.get(teleId=teleId)
      objDetails=ast.literal_eval(details.data)
      print(details.data)
      print(data)
      # code for form handling in telemetry obj
      for x in data["form"]:
        if x in objDetails.keys():
            objDetails[x].append(data["form"][x])
        else:
          
          objDetails["form"][x]=data["form"][x]
          print(x)
          print(data)
          print(objDetails)
      # end of this obj form telemetry 
      for x in data["product"]:
        objDetails["product"].append(x)
      if(data==ast.literal_eval(details.data)):
        print("equal")
      else:
        print("not equal")
        for val in data["views"]:
          if val in objDetails["views"]:
            objDetails["views"][val]=objDetails["views"][val] + data["views"][val]
          else:
            objDetails["views"][val]=data["views"][val]
        #for views updating
        # if data["views"].keys() == objDetails["views"].keys():
        #   print("views equal keys")
        #   for key in objDetails["views"]:
        #     objDetails["views"][key]=objDetails["views"][key]+data["views"][key]    
        #   print("views equal keys",objDetails["views"])
        # else:
        #   print("views not equalt keys")
        print(objDetails)
        details.data=json.dumps(objDetails)
        details.save()

    else:
      objDetails=ast.literal_eval(teleData)
      print("data is their ",objDetails)
      s=TelemetryDaa.objects.create(data=teleData,teleId=teleId)
      s.save()
      print("create details",s)
      
    return HttpResponse("success", content_type='application/json')
  def get(self, request, format=None):
    s=TelemetryDaa.objects.all()
    data = serializers.serialize('json', s)
    return HttpResponse(data , content_type='application/json')
import ast
class PaymentDetails(APIView):
  def post( self,request, format=None):
    print(type(request.data.get("paymentDetails")))
    print(request.data.get("paymentDetails"))
    paymentDetails=ast.literal_eval(request.data.get("paymentDetails"))
    print(paymentDetails["UserID"])
    print(type(paymentDetails["UserID"]))
    pricingiD=None
    user=paymentDetails["UserID"]
    OrderID=paymentDetails["orderid"]
    category =paymentDetails["plan"]["category"]
    days =paymentDetails["plan"]["days"]
    regulars =paymentDetails["plan"]["regulars"]
    topAds =paymentDetails["plan"]["topAds"]
    featured=paymentDetails["plan"]["featured"]
    teleSupport=paymentDetails["plan"]["teleSupport"]
    response=paymentDetails["plan"]["response"]
    chatSupport=paymentDetails["plan"]["chatSupport"]
    dedicatedRm=paymentDetails["plan"]["dedicatedRm"]
    hol9Website=paymentDetails["plan"]["hola9Website"]
    print("sending--------------------------------")
    if False:
      s=Pricing.objects.get(user_id=user)
      s.category=category
      s.featured_ads=featured_ads
      s.ads_limit=ads_limit
      s.ads_timing=ads_timing
      s.top_listing=top_listing
      s.support=support
      s.adsLeft=adsLeft
      s.save()
      pricingiD=s.pk
    else:
      if paymentDetails["plan"]["category"]=="Free":
        s=Pricing.objects.create(user_id=user,category=category,days=days,regulars=regulars,topAds=topAds,featured=featured,teleSupport=teleSupport,response=response,chatSupport=chatSupport,dedicatedRm=dedicatedRm,hol9Website=hol9Website,OrderID=OrderID)
        s.save()
        pricingiD=s.pk
    # s1=PaymentDetailsValues.objects.create(UserValue_id=paymentDetails["UserID"],PlanValue_id=pricingiD,OrderValue_id=paymentDetails["orderid"])
    # s1.save()
    # print("s.id is printing ........................................",s1)
    return HttpResponse("Success",content_type='application/json') 




class jobDetails(APIView):
  def post(self, request, format=None):
    serializer = jobdetailsSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    applied = get_tokens_for_user(user)
    return Response("Sucess",content_type='application/json')
  


class jobsRequired(APIView):
  def post(self,request, formate=None):
      serializer = jobsRequiredSerialize(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      s=JobsRequired.objects.all()
      data = serializers.serialize('json', s)
      return HttpResponse(data, content_type='application/json')
  def get(self,request, formate=None):
      s=JobsRequired.objects.all()
      data = serializers.serialize('json', s)
      return HttpResponse(data, content_type='application/json')

class FullProfile(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        for x in Profile.objects.all():
          print(x.user_id)
        profileData=Profile.objects.filter(user=userId)
        print(profileData)
        data = serializers.serialize('json', profileData)
        return HttpResponse(data, content_type='application/json')



