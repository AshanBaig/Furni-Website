from flask import Flask, render_template,request
from flask_mail import Mail
from datetime import datetime
from abc import ABC,abstractmethod
import os

class Load_Product:
     '''This class loads the product to the main product list'''
     def loading_product_detail(self): 
          ''' This method loads the product details from text file into a list called prod_detail '''
          self.prod_detail=[]
          with open('product_detail.txt','r') as f:
               for i in f:
                    i=i.strip()   
                    i=i.split(',')
                    if i!=['']:  
                        self.prod_detail.append([i[0],i[1].strip(),int(i[2]),int(1)]) 
class MyApp:
    '''This is our main class.'''
    def __init__(self,prod_detail,email_here=0,email='') -> None:
        self.app=Flask(__name__)
        self.email_here=email_here
        self.subtotal=0
        self.app.config.update(MAIL_SERVER='smtp.gmail.com',
                                MAIL_PORT='465',
                                MAIL_USE_SSL=True,
                                MAIL_USERNAME='BAIG4630152@cloud.neduet.edu.pk',
                                MAIL_PASSWORD='**************')
        self.sendmail= Mail(self.app)
        self.cross_icon = 'download.png'
        self.button_index = []  # Cart item indices
        self.grand_total = 0
        self.product_detail=prod_detail
        self.len_productdetail = len(self.product_detail)
        self.user=User(self)
        self.products=Product(self)
        self.mail=Mail_service(self)
        self.route=Routes(self)
        self.entry=0
        self.email=email
    def run(self):
            self.app.run(debug=False)

class Update_Product:
    ''' This class is used in admin panel to add products and remove product.'''
    def remove_product(self,i):
        with open('product_detail.txt','a+') as f:
            f.seek( 0)
            f_lines=f.readlines()
            del f_lines[int(i)]
        with open('product_detail.txt','w') as f:
            for line in f_lines:
                f.write(line)
        product=Load_Product()
        product.loading_product_detail()
        MyApp.__init__(self.app_instance,product.prod_detail)
    def update_product(self,path,pname,pprice):
        '''This method takes the path of png file and other details of product.'''
        ALLOWED_EXTENSIONS = {'png'}

        if '.' in path.filename and path.filename.split('.')[1].lower() in ALLOWED_EXTENSIONS:
            with open('image_count.txt','r') as f:
                #For getting the total number of product and assign them the new name accrodingly.
                f.seek(0)
                f_lines=f.read()
                eval(f_lines)
                f_lines=int(f_lines)+1
                base, ext = os.path.splitext(path.filename)
                new_filename =f"banner_big\\banner{f_lines}{ext}"
                file_path = os.path.join('static', new_filename)
                path.save(file_path)
            with open('image_count.txt','w') as f:
                 f.write(str(f_lines))
                 
            with open('product_detail.txt','a+') as f:
                 new_filename=new_filename.split('\\')
                 f.write(f'\n{new_filename[0]}/{new_filename[1]},{pname},{int(pprice)},1')
                 
        else:
             return 

class Routes(Update_Product):
    '''This class defines the HTML routes.'''

    def __init__(self,app_instance) :
        self.app_instance=app_instance
        self.setup_routes()

    def setup_routes(self):
        app=self.app_instance.app
        user=self.app_instance.user
        mail=self.app_instance.mail
        product=self.app_instance.products
        
        @app.route('/')   #sets the route our home page
        def hello():  
                return render_template('index.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)
        
        @app.route('/index.html')  #redirects to the home page 
        def hello_again():
                return render_template('/index.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)
        
        @app.route('/signup.html',methods=['GET','POST'])   #sets the route to signup page
        def signup():
            return user.signup()
        
        @app.route('/UserID',methods=['GET','POST'])   #sets the route to login page
        def userID():
            return user.login()
        
        @app.route('/thankyou.html')    #sets the route to thankyou page
        def thankyou():
            return user.thankyou()
        
        @app.route('/profile.html')    #sets the route to user's profile
        def profile():
            return user.profile()
        
        @app.route('/checkout.html')   #sets the route to checkout page
        def check_out():
             return product.check_out()
        
        @app.route('/shop.html')    #sets the route to shop page
        def shop():
             return product.shop()
       
        @app.route('/cart.html',methods=['GET','POST'])    
        def cart():
            return product.cart()
        
        @app.route('/remove_index',methods=['POST'])
        def remove_index():
             return product.remove_index()
       
        @app.route('/handle_button', methods=['POST'])
        def handle_button():
             return product.handle_button()
        
        @app.route('/update_cart', methods=['POST'])
        def update_cart():
             return product.update_cart()
        
        @app.route('/contact.html',methods=['GET','POST'])
        def contact():
             return mail.contact()
        
        @app.route('/about.html')
        def about():
             return render_template('/about.html',email=self.app_instance.email_here    )
        
        @app.route('/home')  
        def logout():
            product=Load_Product()
            product.loading_product_detail()
            MyApp.__init__(self.app_instance,product.prod_detail)
            return render_template('index.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)
       
        @app.route('/admin.html',methods=['GET','POST'])
        def admin():     
             if request.method=='POST':
                if 'button' in request.form and request.form['button']!='add':
                     self.remove_product(request.form['button'])
                     return render_template('admin.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail))
            
                if self.app_instance.entry:
                    self.app_instance.entry=0
                    if 'path' in request.files:

                        self.update_product(request.files['path'],request.form['pname'],request.form['pprice'])
                        product=Load_Product()
                        product.loading_product_detail()
                        MyApp.__init__(self.app_instance,product.prod_detail)
                        #To update the length
                    return render_template('admin.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail))
            
                self.app_instance.entry=1
                return render_template('admin_entry.html') 
                    
             else:
                return render_template('admin.html',product_detail=self.app_instance.product_detail,len_productdetail=self.app_instance.len_productdetail)
            
class User_abstract(ABC):
    '''This is an abstract class for user profile.'''   
    
    @abstractmethod   
    def signup(self):
        pass 
    
    @abstractmethod
    def login(self):
        pass  
    
    @abstractmethod
    def profile(self):
        pass

class Mail_service:
     '''This class sends email to the user. 1) Confirmation of purchasing email  2) Feedback email'''

     def __init__(self,app_instance) :
            self.app_instance=app_instance

     def cart_mail(self):
    #For sending the message
        email_message = 'Your order has been confirmed\nOrder will be delivered in 5 to 7 working days.\nOrder Details:'
        
        # Add details of each product in the order
        for product in self.app_instance.button_index:
            product_name = self.app_instance.product_detail[product][1]
            price_per_unit = self.app_instance.product_detail[product][2]
            quantity = self.app_instance.product_detail[product][3]
            total_cost = quantity * price_per_unit
            email_message += f'\n{product_name}: ${price_per_unit} x {quantity} = ${total_cost}'

        # Add total cost and delivery information
        email_message += (
            f"\nTotal: ${self.app_instance.grand_total}\n"
        )

        # Send the email message
        recipients = [
            self.app_instance.email,
            'baig4630152@cloud.neduet.edu.pk',
            'ridaqasmi11@gmail.com',
            'asrasiddiqi01@gmail.com'
        ]
        try:
            self.app_instance.sendmail.send_message(
            subject='Thank you for Shopping with us!!',
            sender='BAIG4630152@cloud.neduet.edu.pk',
            recipients=recipients,
            body=email_message
        )
        except:
            pass
     def contact(self):
          if request.method=='POST':
                    fname=request.form['fname']
                    # lname=request.form['lname']
                    email=request.form['email']
                    message=request.form['message']
                    with open('Feedbackmsg.txt', 'a+') as file:
                        file.write(f'{fname},{email},{message}\n')
                    try:
                        self.app_instance.sendmail.send_message('Thank you for contacting us!! ',sender='BAIG4630152@cloud.neduet.edu.pk',recipients=[email,'baig4630152@cloud.neduet.edu.pk','ridaqasmi11@gmail.com','asrasiddiqi01@gmail.com'],body='Your feedback has been recieved \n"'+message+'"'+'\nWe will Contact you soon.')
                    except:
                        pass
          return render_template('contact.html',email=self.app_instance.email_here)
     
class User(User_abstract,Mail_service):
        def __init__(self,app_instance) :
            self.app_instance=app_instance
        
        def signup(self):
                if request.method=='POST':
                      self.app_instance.email=request.form['email']
                      if self.app_instance.email.count('@')>1 or self.app_instance.email.split('@')[1]!='gmail.com' or not  (self.app_instance.email.split('@')[0].isalnum()):
                        #a=2 is indicator to check if it is not follow our email pattern
                        return render_template('/signup.html',a=2,email=self.app_instance.email_here)

                      password=request.form['password']
                      name=request.form['name']
                      address=request.form['address']
                      contact_number=request.form['contact_number']
                      with open('idpass.txt','a+') as f:
                            f.seek(0)
                            for i in f:
                                list_email_pass=i.split(',')
                                if self.app_instance.email==list_email_pass[0].strip():
                                    #a=1 is indicator to check if it is used email
                                    return render_template('/signup.html.',a=1,email=self.app_instance.email_here)
                            else:
                                #signup-ed
                                self.app_instance.email_here=1
                                #if email is  not in use we just create the account and return the user in our main page
                                f.write(str(self.app_instance.email)+',')
                                f.write(str(password+'\n'))
    
                                filename=self.app_instance.email.split('@')[0]+'.txt'
                                with open(f'userfiles\\{filename}','a+') as uf:
                                    uf.write(f'{self.app_instance.email},{name},{address},{contact_number}')
                                     
                                return render_template('/index.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)  
                else:
                
                    return render_template('/signup.html',a=0,email=self.app_instance.email_here)

        def login(self):
        
            if request.method == 'POST':
                    self.app_instance.email=request.form['email']
                    password=request.form['password']
                    if self.app_instance.email=='admin@gmail.com' and password=='admin123':
                        return render_template('admin.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail))
            
                    with open('idpass.txt','a+') as f:
                        f.seek(0)
                        for i in f:
                            i=i.strip()
                            if i.split(',')[0]==self.app_instance.email:
                                if i.split(',')[1]==password:
                                      self.app_instance.email_here=1
                                    
                                      return render_template('/index.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here) 
                        #b=1  indicates that email or password is wrong     
                        return render_template('/login.html',email=self.app_instance.email_here,b=1)
            else:
                    return render_template('/login.html',email=self.app_instance.email_here,b=0) 
            
        def thankyou(self):
            filename=self.app_instance.email.split('@')[0]+'.txt'
            l=[]
            if len(self.app_instance.button_index)!=0:
                for i in self.app_instance.button_index:
                    l.append(self.app_instance.product_detail[i])
                date=datetime.now()
                d={str(date):l}
                #update current purchese in user account
                with open(f'userfiles\\{filename}','a+') as uf:
                    uf.write('\n'+str(d))
                self.cart_mail()
            product=Load_Product()
            product.loading_product_detail()
            MyApp.__init__(self.app_instance,product.prod_detail,email_here=1,email=self.app_instance.email)
            return render_template('/thankyou.html',email=self.app_instance.email_here)
        
        def profile(self):
            filename=self.app_instance.email.split('@')[0]+'.txt'
            with open(f'userfiles\\{filename}','a+') as uf:
                uf.seek(0)
                skip=1
                date_list=[]
                item_list=[]
                grandtotal=[]
                for i in uf:
                    if skip:
                        skip=0
                        info=i.strip().split(',')
                        continue
                    d=eval(i)
                    total=0
                    for key,value in d.items():
                        date_list.append(key)
                        item_list.append(value)
                        for item in value:
                        
                            total+=item[2]*item[3]
                        grandtotal.append(total)                    
            return render_template('/profile.html',email=self.app_instance.email_here,product_detail=self.app_instance.product_detail,info=info,date_list=date_list[::-1],item_list=item_list[::-1],len_list=len(item_list),grandtotal=grandtotal[::-1])
class Product:
        '''This class displays the product.'''

        def __init__(self,app_instance) :
            self.app_instance=app_instance
           
        def check_out(self):     
            if self.app_instance.email_here:
                if len(self.app_instance.button_index)>0:
                    return render_template('/checkout.html',product_detail=self.app_instance.product_detail,button_index=list(set(self.app_instance.button_index)),subtotal=self.app_instance.subtotal,email=self.app_instance.email_here)
                return render_template('/shop.html',cart_empty=1,product_detail=self.app_instance.product_detail,len_productdetail=self.app_instance.len_productdetail,email=self.app_instance.email_here)
            return render_template('/login.html',email=self.app_instance.email_here,b=2)  #b=2 plz login before prooceding to checkout
      
        def shop(self):
                return render_template('/shop.html',product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)
        
        def cart(self):
            self.app_instance.subtotal=0
            if self.app_instance.button_index:    
                for i in self.app_instance.button_index:  
                            self.app_instance.subtotal+=self.app_instance.product_detail[i][2]*self.app_instance.product_detail[i][3]   
            self.app_instance.grand_total=self.app_instance.subtotal  
            return render_template('cart.html', product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),button_index=list(set(self.app_instance.button_index)), subtotal=self.app_instance.subtotal, grand_total=self.app_instance.grand_total,email=self.app_instance.email_here)
        def remove_index(self):
                    
                    if int(request.form['button']) in self.app_instance.button_index:
                        self.app_instance.button_index.remove(int(request.form['button']))
                        self.app_instance.product_detail[int(request.form['button'])][3]=1
                    self.app_instance.subtotal=0
                    if self.app_instance.button_index:    
                        for i in self.app_instance.button_index:
                               self.app_instance.subtotal+=self.app_instance.product_detail[i][2]*self.app_instance.product_detail[i][3]   
                    self.app_instance.grand_total=self.app_instance.subtotal  
                    return render_template('cart.html', product_detail=self.app_instance.product_detail,button_index=list(set(self.app_instance.button_index)), subtotal=self.app_instance.subtotal, grand_total=self.app_instance.grand_total,email=self.app_instance.email_here)

                    
        def handle_button(self):
                if request.method == 'POST':
                    self.app_instance.button_index.append(request.form['button'])
                
                    self.app_instance.button_index=[int(x) for x in self.app_instance.button_index]               
                    return render_template('shop.html', button_index=self.app_instance.button_index,product_detail=self.app_instance.product_detail,len_productdetail=len(self.app_instance.product_detail),email=self.app_instance.email_here)          
        def update_cart(self):
                product_index = request.form['button']
                product_index=int(eval(product_index)[0])
                try:
                     quantity =int(request.form['quantity'])
                except:
                     quantity=1
                # Calculate the new total for the product
                unit_price = self.app_instance.product_detail[product_index][2]
                
                # Update product total
                self.app_instance.product_detail[product_index][3] = quantity
            
                # Recalculate the cart's subtotal and total
                self.app_instance.subtotal=0
                for i in self.app_instance.button_index:    
                    self.app_instance.subtotal += self.app_instance.product_detail[i][2]*self.app_instance.product_detail[i][3]
                self.app_instance.grand_total = self.app_instance.subtotal  # Add discounts or taxes if needed
                
                return render_template('cart.html', product_detail=self.app_instance.product_detail,button_index=list(set(self.app_instance.button_index)), subtotal=self.app_instance.subtotal, grand_total=self.app_instance.grand_total,email=self.app_instance.email_here)

if __name__ == "__main__":
        product=Load_Product()
        product.loading_product_detail()
        #association
        my_app = MyApp(product.prod_detail)     
        my_app.run()