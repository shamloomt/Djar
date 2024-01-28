from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from adminpanel.models import Product, Categories, Cart, Order_details, Orders, Base_Info, Pr_Fav,Discounts, Discounts_used
from adminpanel.serializers import Product_Model_Serializer, Cart_Serializer, getcat_Serializer, Orders_Serializer, Order_Details_Serializer, Base_Info_Serializer, Pr_Fav_Serializer
from rest_framework.decorators import api_view
from django.utils.encoding import uri_to_iri
from users import models as user_model
# from openpyxl import load_workbook
from datetime import date, datetime
import jdatetime
# import requests

class GetAll_Product(APIView):
    def get(self, request):
        query = Product.objects.all()
        serializer = Product_Model_Serializer(query, many = True, context = {'request' : request})

        return Response(serializer.data, status = status.HTTP_200_OK)

class GetAll_Categories(APIView):
    def get(self, request):
        query = Categories.objects.all()
        serializer = getcat_Serializer(query, many = True, context = {'request' : request})
        cat_res = []
        c = 0
        for i in query:
            cat_res.append(
                {
                    'id' : (query.values('id')[c])['id'],
                    'name' : (query.values('name')[c])['name'],
                    'parent' : (query.values('parent')[c])['parent'],
                    "pic_cat": "http://37.152.189.137:10543/" + (query.values('pic_cat')[c])['pic_cat']
                }
            )
            c += 1

        # return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(cat_res)

class get_product_with_cat(APIView):
    def get(self, request, catID):
        query = Product.objects.filter(cat_1 = catID) | Product.objects.filter(cat_2 = catID) | Product.objects.filter(cat_3 = catID) | Product.objects.filter(cat_4 = catID) | Product.objects.filter(cat_5 = catID)
        serializer = Product_Model_Serializer(query, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_productSingle(request, pk):
    pr = Product.objects.filter(id = pk)
    serializer = Product_Model_Serializer(pr, many=True)

    return Response(serializer.data)

@api_view(['PUT'])
def update_product(request, pk):
    pr_up = Product.objects.get(id = pk)
    serializer = Product_Model_Serializer(instance = pr_up, data = request.data)

    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

################ CART ################
@api_view(['GET'])
def Cart_View(request, pk):
    get_prid = Cart.objects.filter(User_ID = pk).values()

    # carts = Cart.objects.select_related('pr_ID').get(User_ID = pk).pr_ID.image_1
    carts = Cart.objects.filter(User_ID = pk).prefetch_related('pr_ID')
    img = []
    c = 0
    for i in carts:
        img.append({
            'pr_ID' : (get_prid.values('pr_ID')[c])['pr_ID'],
            'name' : str(i.pr_ID.name),
            'img' : str(i.pr_ID.image_1),
            'single_pack' : str(i.pr_ID.single_pack_WS),
            'packet_pack' : str(i.pr_ID.packet_pack_WS),
            'box_pack' : str(i.pr_ID.box_pack_WS),
        })
        c += 1

    serializer = Cart_Serializer(carts, many=True)
    return Response(serializer.data + img)

@api_view(['POST'])
def Cart_Add(request):
    serializer = Cart_Serializer(data=request.data)
    res = []
    if serializer.is_valid():
        prod = Product.objects.get(name = serializer.validated_data['pr_ID'])
        
        m = serializer.validated_data['Qty_all_Select']
       
        if prod.stock == None or prod.stock >= m:
            box = prod.box_Qty_WS
            pack = prod.packet_Qty_WS
            b = 0
            p = 0
            s = 0
            pric = 0

            if prod.box_pack_WS == True:
                if m >= box:
                    b = m // box
                    serializer.validated_data['box_pack'] = True
                    serializer.validated_data['Qty_select_box'] = b
                    pric += (serializer.validated_data['Qty_select_box'] * serializer.validated_data['Qty_in_box']) * serializer.validated_data['box_price_one']
                    m = m - (b * box)

                else:
                    serializer.validated_data['box_pack'] = False
                    serializer.validated_data['Qty_select_box'] = 0

            if prod.packet_pack_WS == True:
                if m >= pack:
                    p = m // pack
                    serializer.validated_data['packet_pack'] = True
                    serializer.validated_data['Qty_select_packet'] = p
                    pric += (serializer.validated_data['Qty_select_packet'] * serializer.validated_data['Qty_in_packet']) * serializer.validated_data['packet_price_one']
                    m = m - (p * pack)

                else:
                    serializer.validated_data['packet_pack'] = False
                    serializer.validated_data['Qty_select_packet'] = 0

            if prod.single_pack_WS == True:
                if m > 0:
                    s = m
                    serializer.validated_data['single_pack'] = True
                    serializer.validated_data['Qty_select_single'] = s
                    pric += serializer.validated_data['single_price'] * s

                else:
                    serializer.validated_data['single_pack'] = False
                    serializer.validated_data['Qty_select_single'] = 0

            serializer.validated_data['Qty_all_Select'] = (b * box) + (p * pack) + s
            serializer.validated_data['total_price'] = pric
            
            serializer.save()

            # به روزرسانی موجودی کالا
            if prod.stock != None:
                prod.stock -= serializer.validated_data['Qty_all_Select']
                prod.save()

            return Response(serializer.data)
        
        else:
            res = [{'error':'عدم موجودی کافی در انبار. تعداد موجود ' + str(prod.stock) + ' عدد'}]
            return Response(res)
    

@api_view(['PUT'])
def Cart_Update(request, pk):
    cart = Cart.objects.get(id = pk)
    serializer = Cart_Serializer(instance=cart, data = request.data)
    res = []
    if serializer.is_valid():
        prod = Product.objects.get(name = serializer.validated_data['pr_ID'])
        m = serializer.validated_data['Qty_all_Select']
        c = cart.Qty_all_Select
        st = prod.stock
        new_st = 0

        if prod.stock != None:
            new_st = st + c

        if prod.stock == None or new_st >= m:
            if prod.stock != None:
                prod.stock += c
                prod.save()

            box = prod.box_Qty_WS
            pack = prod.packet_Qty_WS
            b = 0
            p = 0
            s = 0
            pric = 0

            if prod.box_pack_WS == True:
                if m >= box:
                    b = m // box
                    serializer.validated_data['box_pack'] = True
                    serializer.validated_data['Qty_select_box'] = b
                    pric += (serializer.validated_data['Qty_select_box'] * serializer.validated_data['Qty_in_box']) * serializer.validated_data['box_price_one']
                    m = m - (b * box)
                else:
                    serializer.validated_data['box_pack'] = False
                    serializer.validated_data['Qty_select_box'] = 0

            if prod.packet_pack_WS == True:
                if m >= pack:
                    p = m // pack
                    serializer.validated_data['packet_pack'] = True
                    serializer.validated_data['Qty_select_packet'] = p
                    pric += (serializer.validated_data['Qty_select_packet'] * serializer.validated_data['Qty_in_packet']) * serializer.validated_data['packet_price_one']
                    m = m - (p * pack)
                else:
                    serializer.validated_data['packet_pack'] = False
                    serializer.validated_data['Qty_select_packet'] = 0
                    
            if prod.single_pack_WS == True:
                if m > 0:
                    s = m
                    serializer.validated_data['single_pack'] = True
                    serializer.validated_data['Qty_select_single'] = s
                    pric += serializer.validated_data['single_price'] * s
                else:
                    serializer.validated_data['single_pack'] = False
                    serializer.validated_data['Qty_select_single'] = 0

            serializer.validated_data['Qty_all_Select'] = (b * box) + (p * pack) + s
            serializer.validated_data['total_price'] = pric
            
            serializer.save()

            # به روزرسانی موجودی کالا
            if prod.stock != None:
                prod.stock -= serializer.validated_data['Qty_all_Select']
                prod.save()

            return Response(serializer.data)
        
        else:
            res = [{'error':'عدم موجودی کافی در انبار. تعداد موجود ' + str(prod.stock) + ' عدد'}]
            return Response(res)

#Cart and Order Merge: uid= user id , oid= order id
@api_view(['GET'])
def Cart_Merge_Order(request, uid, oid):
    order_id = Order_details.objects.filter(order_id = oid).values()
    cart_current = Cart.objects.filter(User_ID = uid).values()
    res_status = []

    for i in range(0, len(order_id)):
        for j in range(0, len(cart_current)):
            Prod = Product.objects.get(id = order_id.values('pr_ID_id')[i]['pr_ID_id'])
            total_price_card = 0
            all_Select = 0

            if order_id.values('pr_ID_id')[i] == cart_current.values('pr_ID_id')[j]:
                st = Cart.objects.get(id = cart_current.values('id')[j]['id'])
                
                if order_id.values('single_pack')[i]['single_pack'] == True:
                    
                    st.single_pack = True
                    st.Qty_select_single += order_id.values('Qty_select_single')[i]['Qty_select_single']
                    st.single_price = Prod.single_price_WS
                    
                    all_Select += st.Qty_select_single
                    total_price_card += st.Qty_select_single * Prod.single_price_WS
                    
                elif cart_current.values('single_pack')[i]['single_pack'] == True:
                    all_Select += st.Qty_select_single
                    total_price_card += st.Qty_select_single * Prod.single_price_WS

                if order_id.values('packet_pack')[i]['packet_pack'] == True:
                    st.packet_pack = True
                    st.Qty_in_packet = Prod.packet_Qty_WS
                    st.Qty_select_packet += order_id.values('Qty_select_packet')[i]['Qty_select_packet']
                    st.packet_price_one = Prod.packet_price_WS_one
                    
                    all_Select += Prod.packet_Qty_WS * st.Qty_select_packet
                    total_price_card += (Prod.packet_Qty_WS * st.Qty_select_packet) * Prod.packet_price_WS_one
                
                elif cart_current.values('packet_pack')[i]['packet_pack'] == True:
                    all_Select += Prod.packet_Qty_WS * st.Qty_select_packet
                    total_price_card += (Prod.packet_Qty_WS * st.Qty_select_packet) * Prod.packet_price_WS_one

                if order_id.values('box_pack')[i]['box_pack'] == True:
                    st.box_pack = True
                    st.Qty_in_box = Prod.box_Qty_WS
                    st.Qty_select_box += order_id.values('Qty_select_box')[i]['Qty_select_box']
                    st.box_price_one = Prod.box_price_WS_one

                    all_Select += Prod.box_Qty_WS * st.Qty_select_box
                    total_price_card += (Prod.box_Qty_WS * st.Qty_select_box) * Prod.box_price_WS_one
                
                elif cart_current.values('box_pack')[i]['box_pack'] == True:
                    all_Select += Prod.box_Qty_WS * st.Qty_select_box
                    total_price_card += (Prod.box_Qty_WS * st.Qty_select_box) * Prod.box_price_WS_one

                st.Qty_all_Select = all_Select
                st.total_price = total_price_card
                st.save()

                res_status.append({'pr_id' : str(order_id.values('pr_ID_id')[i]['pr_ID_id']),
                                   'status' : 'updated'})
            else:

                if order_id.values('single_pack')[i]['single_pack'] == True:
                    all_Select += order_id.values('Qty_select_single')[i]['Qty_select_single']
                    total_price_card += (order_id.values('Qty_select_single')[i]['Qty_select_single'] * Prod.single_price_WS)

                if order_id.values('packet_pack')[i]['packet_pack'] == True:
                    all_Select +=  order_id.values('Qty_select_packet')[i]['Qty_select_packet']
                    total_price_card += ((order_id.values('Qty_select_packet')[i]['Qty_select_packet'] * Prod.packet_Qty_WS) * Prod.packet_price_WS_one)

                if order_id.values('box_pack')[i]['box_pack'] == True:
                    all_Select += order_id.values('Qty_select_box')[i]['Qty_select_box']
                    total_price_card += ((order_id.values('Qty_select_box')[i]['Qty_select_box'] * Prod.box_Qty_WS) * Prod.box_price_WS_one)

                add_to_cart = Cart(

                    User_ID = uid,

                    sale_type = order_id.values('single_pack')[i]['single_pack'],
                    single_pack = order_id.values('single_pack')[i]['single_pack'],
                    single_price = Prod.single_price_WS,
                    Qty_select_single = order_id.values('Qty_select_single')[i]['Qty_select_single'],

                    packet_pack = order_id.values('packet_pack')[i]['packet_pack'],
                    Qty_in_packet = Prod.packet_Qty_WS,
                    packet_price_one = Prod.packet_price_WS_one,
                    Qty_select_packet = order_id.values('Qty_select_packet')[i]['Qty_select_packet'],

                    box_pack = order_id.values('box_pack')[i]['box_pack'],
                    Qty_in_box = Prod.box_Qty_WS,
                    box_price_one = Prod.box_price_WS_one,
                    Qty_select_box = order_id.values('Qty_select_box')[i]['Qty_select_box'],

                    Qty_all_Select = all_Select,
                    total_price =  total_price_card,

                    pr_ID_id = Prod.id #order_id.values('pr_ID_id')[i]['pr_ID_id']
                    
                )
                add_to_cart.save()

                res_status.append({'pr_id' : str(order_id.values('pr_ID_id')[i]['pr_ID_id']),
                                   'status' : 'added'})
                
    return Response(res_status)

@api_view(['DELETE'])
def Cart_Delete(request, pk):

    cart = Cart.objects.filter(id = pk)
    # print(cart.id)
    c = (cart.values('Qty_all_Select')[0])['Qty_all_Select']
    # c = cart.Qty_all_Select
    prod = Product.objects.get(id = (cart.values('pr_ID')[0])['pr_ID'])
    
    if prod.stock != None:
        prod.stock += c
        prod.save()
    
    cart.delete()
    
    return Response('Deleted')

################ ORDERS ################
@api_view(['GET'])
def User_Orders_View(request, pk):
    orders = Orders.objects.filter(User_ID = pk)
    serializer = Orders_Serializer(orders, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def Order_View(request, pk):
    orders = Orders.objects.filter(order_id = pk)
    serializer = Orders_Serializer(orders, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def Order_Add(request):
    serializer = Orders_Serializer(data=request.data)

    order_id = Base_Info.objects.get(caption = 'order_No').value# خواندن آخرین شماره سفارش
    new_orderID = str(int(order_id) + 1) # ایجاد شماره سفارش جدید
    #Base_Info.objects.update(caption = 'order_No', value = new_orderID) # ذخیره شماره سفارش جدید
    Base_Info.objects.filter(caption='order_No').update(value = new_orderID)
    userID = 0
    name_and_family = ''
    user_mobile = ''

    if serializer.is_valid():
        
        mydata = Cart.objects.filter(User_ID = serializer.validated_data['User_ID']).values()
        price_sum = 0

        userID = (mydata.values('User_ID')[0])['User_ID']
        name_and_family = serializer.validated_data['frist_name'] + ' ' + serializer.validated_data['last_name']
        user_mobile = serializer.validated_data['mobile']
        # p_status = serializer.validated_data['Payment_status']

        Ord = Orders( #اضافه کردن سفارش جدید در مدل order
            
            order_id = new_orderID,
            User_ID = userID,
            frist_name = serializer.validated_data['frist_name'],
            last_name = serializer.validated_data['last_name'],
            province = serializer.validated_data['province'],
            city = serializer.validated_data['city'],
            address = serializer.validated_data['address'],
            mobile = serializer.validated_data['mobile'],
            phone = serializer.validated_data['phone'],
            postcode = serializer.validated_data['postcode'],
            mail = serializer.validated_data['mail'],
            Description = serializer.validated_data['Description'],
            total_price = price_sum,
            discount_code = serializer.validated_data['discount_code'],
            payable = serializer.validated_data['payable'],
            order_status = 1,
            Payment_status = 1

        )

        Ord.save()

        for i in range(0, len(mydata)): #اضافه کردن جزئیات سفارش

            p = Order_details(

                    order_id_id = new_orderID,
                    pr_ID_id = (mydata.values('pr_ID')[i])['pr_ID'],
                    sale_type = (mydata.values('sale_type')[i])['sale_type'],
                    
                    single_pack = (mydata.values('single_pack')[i])['single_pack'],
                    single_price = (mydata.values('single_price')[i])['single_price'],
                    Qty_select_single = (mydata.values('Qty_select_single')[i])['Qty_select_single'],

                    packet_pack = (mydata.values('packet_pack')[i])['packet_pack'],
                    Qty_in_packet = (mydata.values('Qty_in_packet')[i])['Qty_in_packet'],
                    packet_price_one = (mydata.values('packet_price_one')[i])['packet_price_one'],
                    Qty_select_packet = (mydata.values('Qty_select_packet')[i])['Qty_select_packet'],

                    box_pack = (mydata.values('box_pack')[i])['box_pack'],
                    Qty_in_box = (mydata.values('Qty_in_box')[i])['Qty_in_box'],
                    box_price_one = (mydata.values('box_price_one')[i])['box_price_one'],
                    Qty_select_box = (mydata.values('Qty_select_box')[i])['Qty_select_box'],

                    Qty_all_Select = (mydata.values('Qty_all_Select')[i])['Qty_all_Select'],

                    total_price = (mydata.values('total_price')[i])['total_price']
            )

            p.save()

            # st = Product.objects.get(id = (mydata.values('pr_ID')[i])['pr_ID']) # به روزرسانی موجودی کالا
            # if st != 'null':
            #     st.stock = st.stock - (mydata.values('Qty_all_Select')[i])['Qty_all_Select']
            #     st.save()

            price_sum += (mydata.values('total_price')[i])['total_price']

        payble_price = price_sum
        price_of_discount = 0

        if serializer.validated_data['discount_code'] != 'nodiscount':
            disCode = serializer.validated_data['discount_code']

            if disCode:
                dic_code_res = Discounts.objects.filter(code = disCode).values()
                
                if (dic_code_res.values('discount_type')[0])['discount_type'] == 1:
                    discount_value = int((dic_code_res.values('discount')[0])['discount']) / 100
                    discount_precent = float(price_sum) * discount_value

                    price_of_discount = int(price_sum) - int(discount_precent)
                    payble_price = price_of_discount

                if (dic_code_res.values('discount_type')[0])['discount_type'] == 2:
                    price_of_discount = price_sum - int((dic_code_res.values('discount')[0])['discount'])
                    payble_price = price_of_discount

                dicUsed_res = Discounts_used.objects.filter(discount_id = disCode, user_id = userID).values() #ثبت کد تخفیف استفاده شده برای کاربر

                if dicUsed_res:
                    used_user = (dicUsed_res.values('used')[0])['used']
                    used_user += 1
                    Discounts_used.objects.filter(discount_id = disCode, user_id = userID).update(used = used_user)
                   
                else:
                    
                    D = Discounts_used(discount_id_id = disCode,
                                        user_id = userID,
                                        used = 1)
                    D.save()
                

        pr_all = Orders.objects.get(order_id=new_orderID) # اضافه کردن قیمت کل سفارش
        pr_all.total_price = price_sum
        pr_all.payable = payble_price
        pr_all.save()
      
        instance = Cart.objects.filter(User_ID = userID) #حذف موارد سفارش از سبد خرید
        instance.delete()

        # carts = Cart.objects.filter(User_ID = pk).prefetch_related('pr_ID')

        order_res = [
            { #Response
                'order_id' : new_orderID,
                'User_ID' : userID,
                'total_price' : int(price_sum),
                'Payable' : int(payble_price)
            }
        ]

    s_save = False
    um = user_model.UserAccount.objects.get(id = userID)

    if um.frist_name == None:
        um.frist_name = serializer.validated_data['frist_name']
        s_save = True

    if um.last_name == None:
        um.last_name = serializer.validated_data['last_name']
        s_save = True
    
    if um.province == None:
        um.province = serializer.validated_data['province']
        s_save = True

    if um.city == None:
        um.city = serializer.validated_data['city']
        s_save = True

    if um.address == None:
        um.address = serializer.validated_data['address']
        s_save = True

    if um.phone == 0 or um.phone == None:
        um.phone = serializer.validated_data['phone']
        s_save = True

    if um.postcode == 0 or um.postcode == None:
        um.postcode = serializer.validated_data['postcode']
        s_save = True

    if um.mail == None:
        um.mail = serializer.validated_data['mail']
        s_save = True

    if um.Description == None:
        um.Description = serializer.validated_data['Description']
        s_save = True  

    if s_save == True: um.save()
    
    
    ############ SMS SEND FOR ADMIN:
    # if p_status == 2: #online_pay
    #     sms_send('forCustomer_OnlinePay', user_mobile, name_and_family, new_orderID, payble_price)

    # if p_status == 5: #check_pay
    #     sms_send('forCustomer_checkPay', user_mobile, name_and_family, new_orderID, payble_price)
    # sms_send()
    # sms_send('forAdmin', '', '', new_orderID, payble_price)

    return Response(order_res)
    

@api_view(['PUT'])
def Order_Update(request, pk):
    order = Orders.objects.get(order_id = pk)
    
    serializer = Orders_Serializer(instance=order, data = request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

################ ORDER_DETAILS ################

@api_view(['GET'])
def Order_dtails_View(request, pk):
    orders_f = Order_details.objects.filter(order_id = pk).values()
    # serializer = Order_Details_Serializer(orders_f, many=True)
        
    AddToRes = []

    for i in range(0, len(orders_f)):
        mydata = Product.objects.filter(id = (orders_f.values('pr_ID')[i])['pr_ID']).values()

        AddToRes.append({
            'order_id' : pk,
            'pr_id': (orders_f.values('pr_ID')[i])['pr_ID'],
            'pr_name' :(mydata.values('name')[0])['name'],
            'pr_image' :(mydata.values('image_1')[0])['image_1'],
            'sale_type' : (orders_f.values('sale_type')[i])['sale_type'],
            'single_pack' : (orders_f.values('single_pack')[i])['single_pack'],
            'single_price' : int((orders_f.values('single_price')[i])['single_price']),
            'Qty_select_single' : (orders_f.values('Qty_select_single')[i])['Qty_select_single'],
            'packet_pack' : (orders_f.values('packet_pack')[i])['packet_pack'],
            'Qty_in_packet' : (orders_f.values('Qty_in_packet')[i])['Qty_in_packet'],
            'packet_price_one' : int((orders_f.values('packet_price_one')[i])['packet_price_one']),
            'Qty_select_packet' : (orders_f.values('Qty_select_packet')[i])['Qty_select_packet'],
            'box_pack' : (orders_f.values('box_pack')[i])['box_pack'],
            'Qty_in_box' : (orders_f.values('Qty_in_box')[i])['Qty_in_box'],
            'box_price_one' : int((orders_f.values('box_price_one')[i])['box_price_one']),
            'Qty_select_box' : (orders_f.values('Qty_select_box')[i])['Qty_select_box'],
            'Qty_all_Select' : (orders_f.values('Qty_all_Select')[i])['Qty_all_Select'],
            'total_price' : int((orders_f.values('total_price')[i])['total_price']),
        })
        
    return Response(AddToRes)

################ BASE_INFO ################

@api_view(['GET'])
def Base_info(request, pk):
    carts = Base_Info.objects.filter(caption = pk)
    serializer = Base_Info_Serializer(carts, many=True)

    return Response(serializer.data)

################ Search ################
@api_view(['GET'])
def Search(request, pk):
    pk = uri_to_iri(pk)
    
    if '%20' in pk:
        pk = pk.replace("%20", " ")

    pr_res = Product.objects.filter(name__contains = pk)
    serializer1 = Product_Model_Serializer(pr_res, many=True)

    pr_res = Categories.objects.filter(name__contains = pk)
    serializer2 = getcat_Serializer(pr_res, many=True)

    return Response(serializer2.data + serializer1.data)

################ Product Favorite ################
@api_view(['GET'])
def PrFav_Get(request, pk):
    pr_res = Pr_Fav.objects.filter(User_ID = pk).values()
    # serializer = Pr_Fav_Serializer(pr_res, many=True)
    
    res = []
    for i in range(0, len(pr_res)):
        mydata = Product.objects.filter(id = (pr_res.values('pr_ID')[i])['pr_ID']).values()

        res.append({
            'User_ID' : pk,
            'pr_id' : (mydata.values('id')[0])['id'],
            'pr_name' : (mydata.values('name')[0])['name'],
            'pr_image' : (mydata.values('image_1')[0])['image_1'],
        })
        
    return Response(res)

@api_view(['POST'])
def PrFav_Add(request):
    serializer = Pr_Fav_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def PrFav_Delete(request, pk_u, pk_p):
    prfav = Pr_Fav.objects.filter(User_ID = pk_u, pr_ID = pk_p)
    prfav.delete()
    
    return Response('Deleted!')

################ DISCOUNTS ################
@api_view(['GET'])
def Discount_Get(request, dis_code, pk):
    dic_code_res = Discounts.objects.filter(code = dis_code).values()
    res = []
    if dic_code_res:
        if (dic_code_res.values('code_type')[0])['code_type'] == 1:
            dicUsed_res = Discounts_used.objects.filter(discount_id = dis_code, user_id = pk).values()

            if dicUsed_res:
                exp_date = str((dic_code_res.values('expire_date')[0])['expire_date']).split('-')
                td = date.today()
                d1 = td.strftime("%Y-%m-%d")
                today = str(d1).split('-')
                expire_date_jalali = str(jdatetime.date.fromgregorian(day = int(exp_date[2]), month = int(exp_date[1]), year = int(exp_date[0])))

                if datetime(int(exp_date[0]), int(exp_date[1]), int(exp_date[2])) > datetime(int(today[0]), int(today[1]), int(today[2])):

                    if (dic_code_res.values('usable')[0])['usable'] > (dicUsed_res.values('used')[0])['used']:
                        res.append(
                                {
                                    'discount' : (dic_code_res.values('discount')[0])['discount'],
                                    'discount_type' : (dic_code_res.values('discount_type')[0])['discount_type'],
                                    'expire_date' : expire_date_jalali,
                                }
                            )
                    else:

                        res.append({
                            'error' : 'شما قبلاً از این کد تخفیف استفاده کرده اید'
                        })

                else:
                     res.append({
                            'error':'مهلت استفاده از این کد تخفیف به پایان رسیده است'
                        })
                     
            else:
                exp_date = str((dic_code_res.values('expire_date')[0])['expire_date']).split('-')
                td = date.today()
                d1 = td.strftime("%Y-%m-%d")
                today = str(d1).split('-')
                expire_date_jalali = str(jdatetime.date.fromgregorian(day = int(exp_date[2]), month = int(exp_date[1]), year = int(exp_date[0])))

                if datetime(int(exp_date[0]), int(exp_date[1]), int(exp_date[2])) > datetime(int(today[0]), int(today[1]), int(today[2])):
                    res.append(
                                {
                                    'discount' : (dic_code_res.values('discount')[0])['discount'],
                                    'discount_type' : (dic_code_res.values('discount_type')[0])['discount_type'],
                                    'expire_date' : expire_date_jalali,
                                }
                            ) 
                else:
                     res.append({
                            'error':'مهلت استفاده از این کد تخفیف به پایان رسیده است'
                        })   
                


        if (dic_code_res.values('code_type')[0])['code_type'] == 2:
            dicUsed_res = Discounts_used.objects.filter(discount_id = dis_code, user_id = pk).values()

            if dicUsed_res:
                exp_date = str((dic_code_res.values('expire_date')[0])['expire_date']).split('-')
                td = date.today()
                d1 = td.strftime("%Y-%m-%d")
                today = str(d1).split('-')
                expire_date_jalali = str(jdatetime.date.fromgregorian(day = int(exp_date[2]), month = int(exp_date[1]), year = int(exp_date[0])))
                
                if datetime(int(exp_date[0]), int(exp_date[1]), int(exp_date[2])) > datetime(int(today[0]), int(today[1]), int(today[2])):
                    

                    if (dic_code_res.values('usable')[0])['usable'] > (dicUsed_res.values('used')[0])['used']:
                        res.append(
                            {
                                'discount' : (dic_code_res.values('discount')[0])['discount'],
                                'discount_type' : (dic_code_res.values('discount_type')[0])['discount_type'],
                                'expire_date' : expire_date_jalali,
                            }
                        )
                    else:
                        res.append({
                        'error' : 'شما قبلاً از این کد تخفیف استفاده کرده اید'
                    })
                        
                else:
                     res.append({
                            'error':'مهلت استفاده از این کد تخفیف به پایان رسیده است'
                        })
    else:
        res.append({
                        'error':'کد تخفیف وارد شده اشتباه است'
                    })
    
    return Response(res)


# def sms_send(sub, phone_number, name, orderNo, price):
# def sms_send():
#     # import requests
#     from sms_ir import SmsIr

#     sms_ir = SmsIr(
#         'TZdzv5LZAmRxemxYrU6leRet7fZgiDl7ZdezvXR6P6ywMyHrTKKApFtMvhl3gWt9',
#         '30007732010630',
#     )

#     sms_ir.send_verify_code(
#         number="09353816277",
#         template_id=513547,
#         parameters=[
#             {
#                 "name" : "ORDNUM",
#                 "value": "12345",
#             },
#             {
#                 "name" : "PRICE",
#                 "value": "1520000",
#             },
#         ],
#     )
#     #sms send for customer:
#     if sub == 'forCustomer_OnlinePay':

#         url = 'https://api.sms.ir/v1/send/verify'
#         headers = {'User-Agent':'Thunder Client (https://www.thunderclient.com)',
#                 'Content-Type':'application/json',
#                 'Accept':'text/plain',
#                 'x-api-key':'TZdzv5LZAmRxemxYrU6leRet7fZgiDl7ZdezvXR6P6ywMyHrTKKApFtMvhl3gWt9'}

#         myobj = {
#                     "mobile": str(phone_number),
#                     "templateId": '344123',
#                     "parameters": [
#                         {
#                             "name": "NAME",
#                             "value": str(name)
#                         },
#                         {
#                             "name":"ORDERNO",
#                             "value": str(orderNo)
#                         },
#                         {
#                             "name":"PRICE",
#                             "value": str(price)
#                         }
#                     ]
#                 }

#         x = requests.post(url, json = myobj, headers=headers)

#     if sub == 'forCustomer_checkPay':

#         url = 'https://api.sms.ir/v1/send/verify'
#         headers = {'User-Agent':'Thunder Client (https://www.thunderclient.com)',
#                 'Content-Type':'application/json',
#                 'Accept':'text/plain',
#                 'x-api-key':'TZdzv5LZAmRxemxYrU6leRet7fZgiDl7ZdezvXR6P6ywMyHrTKKApFtMvhl3gWt9'}

#         myobj = {
#                     "mobile": str(phone_number),
#                     "templateId": '146276',
#                     "parameters": [
#                         {
#                             "name": "NAME",
#                             "value": str(name)
#                         },
#                         {
#                             "name":"ORDERNO",
#                             "value": str(orderNo)
#                         },
#                         {
#                             "name":"PRICE",
#                             "value": str(price)
#                         }
#                     ]
#                 }

#         x = requests.post(url, json = myobj, headers=headers)

#     #sms send for admin:
#     if sub == 'forAdmin':

    # phone_admin = Base_Info.objects.get(caption = 'phone_admin').value
    # p = phone_admin.split(',')
    
    # for i in p:
    #     url = 'https://api.sms.ir/v1/send/verify'
    #     headers = {'User-Agent':'Thunder Client (https://www.thunderclient.com)',
    #             'Content-Type':'application/json',
    #             'Accept':'text/plain',
    #             'x-api-key':'TZdzv5LZAmRxemxYrU6leRet7fZgiDl7ZdezvXR6P6ywMyHrTKKApFtMvhl3gWt9'}
    
    #     myobj = {
    #                 "mobile": i,
    #                 "templateId": '513547',
    #                 "parameters": [
    #                     {
    #                         "name": "ORDNUM",
    #                         "value": 123
    #                     },
    #                     {
    #                         "name":"PRICE",
    #                         "value": 15000000
    #                     }
    #                 ]
    #             }

    #     x = requests.post(url, json = myobj, headers=headers)


# def send(request):

#     order_id = Order_details.objects.filter(order_id = 8).values()
#     cart_current = Cart.objects.filter(User_ID = 1).values()

#     for i in range(0, len(order_id)):
#         for j in range(0, len(cart_current)):
#             if order_id.values('pr_ID_id')[i] == cart_current.values('pr_ID_id')[j]:
#                 Prod = Product.objects.get(id = order_id.values('pr_ID_id')[i]['pr_ID_id'])
#                 st = Cart.objects.get(id = cart_current.values('id')[j]['id'])
#                 total_price_card = 0
#                 all_Select = 0

#                 if order_id.values('single_pack')[i]['single_pack'] == True:
                    
#                     st.single_pack = True
#                     st.Qty_select_single += order_id.values('Qty_select_single')[i]['Qty_select_single']
#                     st.single_price = Prod.single_price_WS
                    
#                     all_Select += st.Qty_select_single
#                     total_price_card += st.Qty_select_single * Prod.single_price_WS
                    
#                 if order_id.values('packet_pack')[i]['packet_pack'] == True:
#                     st.packet_pack = True
#                     st.Qty_in_packet = Prod.packet_Qty_WS
#                     st.Qty_select_packet += order_id.values('Qty_select_packet')[i]['Qty_select_packet']
#                     st.packet_price_one = Prod.packet_price_WS_one
                    
#                     all_Select += Prod.packet_Qty_WS * st.Qty_select_packet
#                     total_price_card += (Prod.packet_Qty_WS * st.Qty_select_packet) * Prod.packet_price_WS_one

#                 if order_id.values('box_pack')[i]['box_pack'] == True:
#                     st.box_pack = True
#                     st.Qty_in_box = Prod.box_Qty_WS
#                     st.Qty_select_box += order_id.values('Qty_select_box')[i]['Qty_select_box']
#                     st.box_price_one = Prod.box_price_WS_one

#                     all_Select += Prod.box_Qty_WS * st.Qty_select_box
#                     total_price_card += (Prod.box_Qty_WS * st.Qty_select_box) * Prod.box_price_WS_one
                
#                 st.Qty_all_Select = all_Select
#                 st.total_price = total_price_card
#                 st.save()
        
#         Cart_View(1)
        # return(st)
        
    # finalCart = Cart.objects.filter(User_ID = 1).values()

    # return(finalCart.values())

    # if order_id.pr_ID == st.pr_ID:
    # st = Cart.objects.get(id = 6)
    # st.single_price = 5000 #st.stock - (mydata.values('Qty_all_Select')[i])['Qty_all_Select']
    # st.save()



    # p = Cart.objects.get(id = 6)
    # p = Cart(single_price = 6000)#, parent = str(i.split(',')[1]))
    # p.save()

    # pass
########################################################################
# def send(request):
#     # قبل از ساخت دسته بندی ها اول دسته بندی بدون دسته بندی رو به صورت دستی توی دیتابیس وارد کن
#     R = open('cat.txt', "r", encoding="utf8")
#     cats = R.readlines()
#     R.close()

#     for i in cats:
#         p = Categories(name = str(i.split(',')[0]), parent = str(i.split(',')[1]))
#         p.save()

#     R = open('baseinfos.txt', "r", encoding="utf8")
#     info = R.readlines()
#     R.close()

#     for i in info:

#         p = Base_Info(caption = str(i.split(',')[0]), value = str(i.split(',')[1]).split('\n')[0])
#         p.save()
########################################################################################
    # for i in range(1,64):
    #     mydata = Categories.objects.get(id = i)
    #     print(mydata)
    #     if (mydata.values('pic_cat')[0])['pic_cat'] == 'null':

    #         p = Categories(pic_cat = 'store_image/cats/djar.png')
    #         p.save()

        # return Response(status.HTTP_200_OK)

# def send_Cart(request):
    # proid = Product.objects.get(id=6)
    # p = Cart(id = 6, single_price = 6000)
    # p.save()

# def send_Order(request):
#     # proid = Order.objects.get(id=1)
#     p = Order(order_id = 11, pr_ID = 1)
#     p.save()


# def send(request):
    
    
#     prod = Product.objects.all()
#     for i in prod:
        
#         if 'ك' in i.name:
#             a = i.name
#             b = a.replace('ك','ک')

#             if 'ي' in b:
#                 b = b.replace('ي','ی')

#             i.name = b

        # if i.box_price_WS_one == None or i.box_price_WS_one == "0":
        #     i.box_price_WS_one = 1
        # if i.box_price_WS_box == None or i.box_price_WS_box == "0":
        #     i.box_price_WS_box = 1

        # if i.packet_Qty_WS == None or i.packet_Qty_WS == "0":
        #     i.packet_Qty_WS = 1
        # if i.packet_price_WS_one == None or i.packet_price_WS_one == "0":
        #     i.packet_price_WS_one = 1
        # if i.packet_price_WS_box == None or i.packet_price_WS_box == "0":
        #     i.packet_price_WS_box = 1
        # if i.packet_priceOff_WS == None or i.packet_priceOff_WS == "0":
        #     i.packet_priceOff_WS = 1

        # if i.single_price_WS == None or i.single_price_WS == "0":
        #     i.single_price_WS = 1
        
            # i.save()

    

# send()



#     wb = load_workbook(filename="Talakoob Rangi.xlsx")
   
#     for j in range(0, len(wb.sheetnames)):
#         sheet_name = wb.sheetnames[j]
#         sheet = wb[sheet_name]
#         print(sheet)
#         print(sheet.max_row)
#         for i in range(3, sheet.max_row + 1):
#             print(sheet['B' + str(i)].value)
#             if sheet['B' + str(i)].value == None: break

#             ci = sheet['N' + str(i)].value
#             print(i)
#             print(ci)
#             catid = Categories.objects.get(id = int(ci))
            
#             pack_WS = False
#             box_WS = False

#             if sheet['V'+str(i)].value == 1: pack_WS = True
#             if sheet['AA'+str(i)].value == 1: box_WS = True

#             p = Product(
#                         name = sheet['B'+str(i)].value,
#                         # barcode = sheet['C' + str(i)].value,
#                         des_short = sheet['F'+str(i)].value,
#                         des_long = sheet['G'+str(i)].value,
#                         cat_1 = catid,

#                         single_pack_WS = True,
#                         # single_price_WS = 8000,

#                         packet_pack_WS = pack_WS,
#                         packet_Qty_WS = sheet['W'+str(i)].value,
#                         packet_price_WS_one = sheet['X'+str(i)].value,
#                         packet_price_WS_box = sheet['W'+str(i)].value * sheet['X'+str(i)].value,
                        
#                         box_pack_WS = box_WS,
#                         box_Qty_WS = sheet['AB'+str(i)].value,
#                         box_price_WS_one = sheet['AC'+str(i)].value,
#                         box_price_WS_box = sheet['AB'+str(i)].value * sheet['AC'+str(i)].value
                        
#                         )
#             p.save()
