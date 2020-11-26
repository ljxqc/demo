from django import forms
from .models import *
from django.core.exceptions import ValidationError

def weight_validate(value):
    if not str(value).isdigit():
        raise ValidationError('请输入正确的重量')


# class ProductForm(forms.Form):
    # name = forms.CharField(max_length=20, label='名字')
    # weight = forms.CharField(max_length=50, label='重量')
    # size = forms.CharField(max_length=50, label='尺寸')
    # choices_list = [(i+1, v['type_name']) for i, v in enumerate(Type.objects.values('type_name'))]
    # type = forms.ChoiceField(choices=choices_list, label='产品类型')

class ProductForm(forms.Form):
    name = forms.CharField(max_length=20, label='名字', widget=forms.widgets.TextInput(attrs={'class':'cl'}),
                           error_messages={'aaa': '名字不能为空'},)
    weight = forms.CharField(max_length=50, label='重量', validators=[weight_validate])
    size = forms.CharField(max_length=50, label='尺寸')
    choices_list = [(i+1, v['type_name']) for i, v in enumerate(Type.objects.values('type_name'))]
    type = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class':'type','size':'4'}),choices=choices_list, label='产品类型')


class ProductModelForm(forms.ModelForm):
    productId = forms.CharField(max_length=20, label='产品序号')
    class Meta:
        model = Product  # 绑定模型
        # fields = '__all__'   # fields 用于设置转换字段，'__all__'是将全部模型字段转换为表单字段
        fields = ['name', 'weight', 'size', 'type']
        exclude = []  # 用于禁止模型转换字段
        labels = {  # 设置 HTML 元素控件的 label 标签
            'name': '产品名称',
            'weight': '重量',
            'size': '尺寸',
            'type': '产品类型',
        }
        widgets = {  # 定义 widgets, 设置表单字段的css 样式
            'name': forms.widgets.TextInput(attrs={'class': 'cl'}), }
        field_classes = {  # 定义字段的类型，一般情况下模型的字段会自动转换为表单字段
            'name': forms.CharField
        }

        help_texts = {  # 帮助提示信息
            # 'name': '名称'
        }
        error_messages = {  # 自定义错误信息
            '__all__': {'required': '请输入内容', 'invalid': '请检查输入内容'},  # __all__ 设置全部错误信息
            'weight': {'required': '请输入重量数值', 'invalid': '请检查数值是否正确'}  # 设置某个字段的错误信息
        }
        #自定义表单字段 weight 的数据清洗
        def clean_weight(self):
            data = self.clean_data['weight']
            return data + 'g'
