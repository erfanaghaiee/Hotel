#proje hotel

# کتابخانه های مورد نیاز
import csv
from datetime import datetime
import pandas as pd


# فایل هایی که با انها کار میکنیم
file_sign=r'C:\Users\Arapardaz\Desktop\proje_hotel\sign.csv'
file_room=r'C:\Users\Arapardaz\Desktop\proje_hotel\rooms.csv'
file_date_reserve=r'C:\Users\Arapardaz\Desktop\proje_hotel\reservation.csv'



# کلاسی برای اتاق های هتل و تبدیل ویژگی های اتاق ها به رشته
class Rooms:
    def __init__(self,room_number,room_type,price,facilities,capacity):
        self.roomnumber=room_number
        self.roomtype=room_type
        price=price.strip()
        self.price=float(price)
        self.facilities=facilities
        self.capacity=capacity
        
        
        
    def total_cost(self,stay_duration):
        return self.price * stay_duration
    
        
            
    def __str__(self):
        return f'Room {self.roomnumber} , type:{self.roomtype} , price:{self.price} , facilities:{self.facilities} , capacity:{self.capacity} '
    
# کلاسی برای اطلاعات رزرو و تبدیل انها به یک رشته
class Reserve:
    def __init__(self,roomnumber,check_in,check_out,username,total_price,status):
        self.roomnumber=roomnumber
        self.check_in=check_in
        self.check_out=check_out
        self.username=username
        self.status=status
        self.totalprice=total_price
    
    def __str__(self):
        return f'user name:{self.username} ,romm number:{self.roomnumber}, check in  date:{self.check_in} , check out date:{self.check_out} ,total cost:{self.totalprice} ,status:{self.status}'

# بررسی اینکه ایا تاریخ از تاریخ خروج مهمان گذشته است یا نه

def parse_date(str_date):
    format=['%Y-%m-%d',
            '%m/%d/%Y' ]
    for fmt in format:
        try:
            return datetime.strptime(str_date , fmt)
        except ValueError:
            continue
    print('error')
    return None

rows=[]
with open(file_date_reserve , 'r' ) as f:
    reader=csv.DictReader(f)
    
    for row in reader:
        rows.append(row)

today=datetime.now()

for row in rows:
    check_out=parse_date(row['check out date'])
    if check_out < today:
        row['status']='completed'

with open(file_date_reserve , 'w' , newline='') as f:
    fieldnames=rows[0].keys() if rows else []
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


        
                

# انجام ثبت نام کاربر و ورود کاربر به سیستم

while True:
    status=input('do you already have an account(yes or no) or type ( exit ) to quit:').lower()
    if status=='exit':
        print(':)')
        break    

    if status=='no':
        firstname=input('enter your name:')
        lastname=input('enter your last name:')
        username=input('enter user name:')
        #بررسی اینکه ایا قبلا این نام کاربری استفاده شده یا نه
        try:
            with open (file_sign , 'r' , newline='') as f:
                user=csv.reader(f)
                for row in user:
                    while row[2]==username:
                        print('this username has already been used.')
                        username=input('enter a another username:')
        except FileNotFoundError:
            print('pleas create sign.csv file')
        
        # بررسی اینکه رمز بیشتر از 8 کاراکتر باشد    
        password=input('enter your password:')
        while len(password)<8:
            print('your password is weak pleas change it (the number of characters is small).')
            password=input('enter a good password:')
        money=float(input('enter your account money:'))
        
        print()
        print('thank you for sign up')
    
        with open(file_sign , 'a' , newline='') as f:
            signup=csv.writer(f)
            signup.writerow([firstname , lastname , username , password, money])

    elif status=='yes':
        username=input('enter your user name:')
        password=input('enter your password:')
        found=False
        
        # بررسی اینکه ایا نام کاربر و رمز ان درست است یا نه.
        try:
            with open(file_sign , 'r') as f:
                login=csv.reader(f)
                for row in login:
                    if len(row)>=5:
                        if row[2]==username and row[3]==password:
                            found = True
                            break
        except FileNotFoundError:
            print('pleas creat file')
            
        if found:
            print('-----------------------------------------------')
            print(f'welcome {username}')
            
            # یاد اوری در صورت داشتن رزرو
            today=datetime.now()
            date_format='%m/%d/%Y'
            with open(file_date_reserve , 'r' ) as f:
                reader=csv.reader(f)
                next(reader)
                for row in reader:
                    if row[3]==username and row[5]=='active':
                        v_in=datetime.strptime(row[1] , date_format)   #تاریخ ورود کاربر
                        if (v_in - today).days <= 1 and (v_in - today).days > 0: # یک روز یا کمتر مانده با تاریخ ورود
                            print('**you have a reservation in less than 24 hours**')
                        else:
                            pass
            print('-----------------------------------------------')
            request=input('what do you want?(reservation , my_history , cencel):').lower()
            print()
            if request=='reservation':
                room_list=[]
                # چاپ اتاق های هتل برای کاربر
                try:
                    with open(file_room , 'r') as  f:
                        rooms=csv.reader(f) 
                        next(rooms) #عبور از سطر اول
                        for row in rooms:
                            if len(row) >= 5:
                                new_room=Rooms(row[0],row[1],row[2],row[3],row[4])
                                room_list.append(new_room)
                        print('available rooms:')
                        for i in room_list:
                                print(i)
                        print()
                                                            
                        while True:
                            # انجام فیلتر اتاق ها بر اساس خواسته کاربر
                            filter=input('do you want to filter (yes or no):').lower()
                            if filter=='no':
                                break
                            
                            elif filter=='yes':
                                filter_type=input('on what basis do you want to filter(room_type,price,facilities):').lower()
                                # فیلتر بر اساس نوع اتاق
                                if filter_type=='room_type':
                                        room_type=input('what do you want(single , double , suite):').lower()
                                        if room_type=='single':
                                                for t in room_list:
                                                    if t.roomtype=='single':
                                                        print(f'match found: {t}')
                                                    
                                                    
                                        elif room_type=='double':
                                                for t in room_list:
                                                    if t.roomtype=='double':
                                                        print(f'match found: {t}')
                                                    
                                                
                                        elif room_type=='suite':
                                                for t in room_list:
                                                    if t.roomtype=='suite':
                                                        print(f'match found: {t}')
                                                    
                                        else:                            
                                            print('invalid input')
                                    # فیلتر بر اساس قیمت
                                elif filter_type=='price':
                                    try:
                                        max_price=float(input('tell the max amount that you want(0 , 1000000):'))
                                        for p in room_list:
                                            if p.price<=max_price:
                                                print(f'match found: {p}')
                                    except ValueError:
                                        print('please enter a valid number for price')
                                        
                                    #  فیلتر بر اساس ویژگی های اتاق       
                                elif filter_type=='facilities':
                                    tv=input('do you want tv? (yes or no):')
                                    wifi=input('do you want wifi (yes or no):')
                                    if tv=='yes' and wifi=='yes':
                                        for t in room_list:
                                            if 'TV' and 'wifi' in t.facilities:
                                                print(f'match found:{t}')
                                    elif tv=='yes' and wifi=='no':
                                        for t in room_list:
                                            if 'TV' in t.facilities:
                                                print(f'match found:{t}')
                                    elif tv=='no' and wifi=='yes':
                                        for t in room_list:
                                            if 'wifi' in t.facilities:
                                                print(f'match found:{t}')
                                    elif tv=='no' and wifi=='no':
                                        print('there is no room without tv or wifi')
                                    else:
                                        print('invalid input')                        
                                else:
                                    print('invalid input')
                                
                            else:
                                print('invalid input')
                                
                        while True:
                            # رزرو اتاق 
                            question=input('do you want a room(yes or no):')
                            print()
                            if question=='no':
                                print(f'goodbye {username}')
                                print()
                                break
                            elif question=='yes':
                                # دریافت تاریخ ورود و خروج از کاربر به شکل میلادی
                                    room_choice=(input('which of the rooms do you want(101-204):'))
                                    print('if you stay 7 days or more,you will receive 10 percent discount')
                                    check_in_date=input('enter check in date:mm/dd/yyyy :')
                                    check_out_date=input('enter check out date:mm/dd/yyyy  :')
                                    date_format='%m/%d/%Y'
                                    try:
                                        check_in=datetime.strptime(check_in_date,date_format)
                                        check_out=datetime.strptime(check_out_date,date_format)
                                    except:
                                        print()
                                        print('**date is not true**')
                                        print()
                                        break
                                    stay_duration=(check_out - check_in).days    # تعداد روز های رزرو  
                                    if stay_duration<=0:
                                        print('error: check out must be after check in.')
                                    
                                    else:
                                        is_avalible=True
                                    try:
                                        # بررسی وجود اتاق مدنظر در تاریخ مدنظر
                                        with open(file_date_reserve , 'r') as  f:
                                            reader=csv.reader(f)
                                            next(reader)
                                            for row in reader:
                                                    if row[0] == room_choice and row[5] == 'active':
                                                        c_in=datetime.strptime(row[1],date_format)
                                                        c_out=datetime.strptime(row[2],date_format)
                                                        #فرمول تداخل
                                                        if not(check_out<= c_in or check_in>=c_out):
                                                            is_avalible= False
                                                            print('room is not avalible in this date')
                                                            print()
                                                            break
                                                        
                                            

                                        if is_avalible:
                                            for r in room_list:
                                                if r.roomnumber==room_choice:
                                                    total_price=r.total_cost(stay_duration) # قیمت کل بر اساس تعداد روزهایی که اتاق را رزرو 
                                                    if stay_duration>=7:
                                                        total_price=(r.total_cost(stay_duration)) * 0.9  # تخفیف 10 درصدی
                                                        print('your reservation include 10 percent discount')
                                                    print(f'room is available total cost for {stay_duration} nights:{total_price}')
                                                    # نهایی کردن رزرو
                                            confirm=input('confirm booking?(yes or no):')
                                            if confirm.lower()=='yes':
                                                print()
                                                with open(file_sign , 'r' , newline='' ) as f:
                                                    reader=csv.reader(f)
                                                    next(reader)
                                                    for row in reader:
                                                        if row[2]==username:
                                                            for r in room_list:
                                                                if r.roomnumber==room_choice:
                                                                    if float(row[4])>=(total_price * 0.5): # row[4] همان پول اکانت شخص است
                                                                        print('your reservation is seccessful. ')
                                                                        print()
                                                                        room_status='active'
                                                                        new_money=float(row[4]) - (total_price * 0.5)  # پولی که باید پرداخت شود
                                                                        
                                                                        print('your factor:')
                                                                        print(f"name:{username} , roomnumber:{room_choice} , check in date:{check_in_date} , check out date:{check_out_date} , total price:{total_price} , status:{room_status}")
                                                                        print()
                                                                        print(f'now your account money is {new_money}')
                                                                        print()
                                                                        # ذخیره اطلاعات رزرو در فایل مربوطه
                                                                        with open (file_date_reserve , 'a') as f:
                                                                            writer=csv.writer(f)
                                                                            writer.writerow([room_choice,check_in_date,check_out_date,username,total_price,room_status])
                                                                        
                                                                        # تغییر پول حساب کاربر بعد از رزرو و ذخیره ان در فایل مربوطه
                                                                        df=pd.read_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv')
                                                                        
                                                                        df.loc[(df['username'] == username) , 'money']=new_money
                                                                        
                                                                        df.to_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv' , index=False)
                                                                        
                                                                        
                                                        
                                                                        break
                                                                    else:
                                                                        with open(file_sign , 'r' , newline='' ) as f:
                                                                            reader=csv.reader(f)
                                                                            next(reader)
                                                                            for row in reader:
                                                                                if row[2]==username:
                                                                                    shortage=(total_price * 0.5) - float(row[4]) # برای بخشی که پول کمه
                                                                        print('your money in not enough you must have half of total cost')
                                                                        print(f'you are {shortage} tomans short.' )
                                                                        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                                                                        # انجام عملیات شارژ حساب کاربر
                                                                        charge=input('do you want charge your account?(yes or no):')
                                                                        if charge=="no":
                                                                            print('ok')
                                                                            break
                                                                        elif charge=='yes':
                                                                            how_much=float(input('how much (toman):'))

                                                                            df=pd.read_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv')
                                                                            
                                                                            df.loc[df['username'] == username , 'money']+=how_much
                                                                            
                                                                            df.to_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv' , index=False)
                                                                            
                                                                            print('Thank you')
                                                                            print()
                                                                            
                                                                            with open(file_sign , 'r') as f:
                                                                                reader=csv.reader(f)
                                                                                for row in reader:
                                                                                    if row[2]==username:
                                                                                        new_money=row[4]
                                                                                        print(f'new account money is {new_money}')
                                                                                        print()
                                                                            break
                                                                            
                                                                                          
                                                                                        
                                                                        else:
                                                                            print('invalid input')
                                                        
                                                                        
                                                                    
                                                                        
                                                
                                            elif confirm.lower()=='no':
                                                print('ok')
                                                print()
                                                
                                                
                                            else:
                                                print('invalid input')
                                                print()
                            
                                    
                                    except FileNotFoundError:
                                        pass
                                
                            else:
                                print('invalid input')
                                print()
                        
                        
                        
                                                            
                except FileNotFoundError:
                    print('please create file rooms.csv')
                    
                    
                    
                    
            elif request=='my_history' or request=='history':
                # بررسی رزرو های گذشته کاربر که در فایل ذخیره شده است
                my_list=[]
                with open(file_date_reserve , 'r') as f:
                    reader=csv.reader(f)
                    next(reader)
                    for row in reader:
                        if row[3]==username:
                            my_reserve=Reserve(row[0],row[1],row[2],row[3],row[4],row[5])
                            my_list.append(my_reserve)
                    if len(my_list)==0:
                        print('you did not have any reservation')
                    else:
                        for r in my_list:
                            print(r) # چاپ انها
                            print('--------------------------------------------------------------------------------------------------')

            elif request=='cancel':
                my_list=[]
                # تغییر وضعیت رزور به حالت کنسل با درخواست کاربر
                with open(file_date_reserve , 'r') as f:
                    reader=csv.reader(f)
                    next(reader)
                    for row in reader:
                        if row[3]==username and row[5]=='active':
                            my_reserve=Reserve(row[0],row[1],row[2],row[3],row[4],row[5])
                            my_list.append(my_reserve)
                    if len(my_list)==0:
                        print('you did not have any active reserve')
                    else:    
                        print('your active reserve:')
                        print()
                        for r in my_list:
                            print(r)
                            print('--------------------------------------------------------------------------------------------------')
                    while True:        
                        r_number=input('which room do you want to cencel(room_number) or type return:').lower()
                        if r_number=='return':
                            print()
                            break
                        print('-------------------------------------------')
                        with open(file_date_reserve , 'r') as f:
                            reader=csv.reader(f)
                            next(reader)
                            find=False
                            for row in reader:    
                                if row[3]==username and row[5]=='active':
                                    if row[0]==r_number:
                                        find=True
                                        sure=input('are you sure?(yes or no):').lower()
                                        print()
                                        if sure=='no':
                                            print('ok')
                                            print()
                                            break
                                        elif sure=='yes':
                                            print('canceling is seccessful.')
                                            print()
                                            # بررسی اینکه در چه تاریخی رزرو کنسل شده
                                            date_format='%m/%d/%Y'
                                            check_in=datetime.strptime(row[1] , date_format)
                                            today=datetime.now()
                                            if (check_in - today).days >= 2: # بیشتر از 48 ساعت فاصله
                                                back_money=(float(row[4]) * 0.5)      #پولی که پرداخت کرده بود  
                                                print(f'your money has been refunded in full {back_money} toman.')
                                                print()
                                            else: # کمتر از 48 ساعت فاصله
                                                back_money=(float(row[4]) * 0.5)/2    # نصف پولی که پرداخت کرده بود
                                                print(f'half of your money was returned {back_money} toman.')
                                                print()
                                        
                                        
    
                                            # تغییر به حالت کنسل
                                        
                                            df=pd.read_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\reservation.csv')
                                        
                                            df.loc[(df['roomnumber'] == int(r_number)) & (df['username']== username ),'status'] = 'cancelled'
                                        
                                            df.to_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\reservation.csv' , index=False)
                                        
                                            ########################################################################################
                                        
                                            #تغییر پول حساب کاربر بعد از لغو رزرو و ذخیره ان در فایل مربوطه
                                        
                                            df=pd.read_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv')
                                                                        
                                            df.loc[(df['username'] == username) , 'money']+=back_money
                                                                        
                                            df.to_csv(r'C:\Users\Arapardaz\Desktop\proje hotel\sign.csv' , index=False)
                                        
                                            with open (file_sign , 'r') as f:
                                                # چاپ پول حساب کاربر
                                                reader=csv.reader(f)
                                                next(reader)
                                                for row in reader:
                                                    if row[2]==username:
                                                        new_money=row[4]
                                                        print(f'now your account money is {new_money} toman.')
                                                        print()
                                                        break
                                        
                                            break
                                        
                                        
                                       
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        else:
                                            print('invalid input')
                                            print()
                            if find==False:
                                print('**room not found**')
                                print()         
                    
                    
                    
                        
            else:
                print('invalid input') 
                print()                
        
        else:
            print('username or password is incorrect')
            print()
    else:
        print('invalid input please type yes or no or exit .')
        print()
        
#finish



  




        
    
    

    
    



