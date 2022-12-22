from dataclasses import field
from PIL import Image
from django import forms
from django import forms
from django.forms import NumberInput,Textarea,TextInput
from Aldshop.models import Banners, Category, Products



class DateInput(forms.DateInput):
    input_type = 'date'
    
class add_product_form(forms.ModelForm):

    # x = forms.FloatField(widget=forms.HiddenInput())
    # y = forms.FloatField(widget=forms.HiddenInput())
    # width = forms.FloatField(widget=forms.HiddenInput())
    # height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = Products
        fields = (
                    'name', 
                    'description',
                    'specification',
                    'stock_available',
                    'is_trusted', 
                    'available_status', 
                    'manufacturing_date',
                    'price',
                    'category', 
                    # 'image_1', 
                    # 'image_2',
                    # 'image_3',
                    # 'image_4',
                    # 'x',
                    # 'y',
                    # 'width',
                    # 'height',
        )
        widgets = {
            'manufacturing_date':DateInput(),
            'name':TextInput(attrs={'style':'width:40%;border:1px solid grey;border-radius:10px;padding:1%;font-weight:bold;','onmouseover':'(this.placeholder = "Enter the Product Name")','onmouseout':'(this.placeholder = "")'}),
            'description':Textarea(attrs={'style':'width:40%;height:200px;border:2px solid grey;border-radius:10px;padding:10px;font-weight:bold;','onmouseover':'(this.placeholder = "write a short description about the product...")','onmouseout':'(this.placeholder = "")'}),
            'specification':Textarea(attrs={'style':'width:40%;border:2px solid grey;border-radius:10px;;padding:5%;font-weight:bold;','onmouseover':'(this.placeholder = "Please Provide the Specification of the current product...")','onmouseout':'(this.placeholder = "")'}),
            'stock_available':NumberInput(attrs={'style':'width:40%;border:2px solid grey;border-radius:10px;;padding:1%;font-weight:bold;','onmouseover':'(this.placeholder = "Enter the total stiock available")','onmouseout':'(this.placeholder = "")'}),
            'price':NumberInput(attrs={'style':'width:40%;border:2px solid grey;border-radius:10px;;padding:10px;font-weight:bold;','min':1,'max':10000,'onmouseover':'(this.placeholder = "Enter the price of the product")','onmouseout':'(this.placeholder = "")'}),
        }

        # def save(self):
        #     photo = super(add_product_form, self).save()

        #     x = self.cleaned_data.get('x')
        #     y = self.cleaned_data.get('y')
        #     w = self.cleaned_data.get('width')
        #     h = self.cleaned_data.get('height')

        #     image = Image.open(photo.file)
        #     cropped_image = image.crop((x, y, w+x, h+y))
        #     resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        #     resized_image.save(photo.file.path)

        #     return photo


class edit_banner(forms.ModelForm):
    class Meta:
        model = Banners
        fields = ['heading', 'description', 'image']




class add_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','image']


############################################################# 


class upload_product_image(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Products
        fields = ('image_1', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(upload_product_image, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo