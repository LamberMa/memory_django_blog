from django.forms import fields, Form, widgets
from django.core.exceptions import ValidationError


# 用户注册相关Form组件定义
class RegisterForm(Form):
    """
    RegisterForm的实例中的fields是一个有序的字典，简单来说也就是我们写的这字段都是有顺序的
    一个一个往下的来匹配的。
    """

    # 用户名form组件
    username = fields.CharField(
        label='用户名',
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '最大长度请不要超过32',
            'min_length': '请输入至少6个字符',
        },
        widget=widgets.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入您的用户名', })
        )
    # 用户昵称form组件
    nickname = fields.CharField(
        label='昵称',
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '最大长度请不要超过32个字符',
            'min_length': '请输入至少6个字符',
        },
        widget=widgets.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入您的昵称'}
        )
    )
    # 用户邮箱字段
    email = fields.EmailField(
        label='邮箱',
        required=True,
        widget=widgets.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入您的密码'}
        )
    )

    # 用户密码form组件
    password = fields.CharField(
        label='密码',
        max_length=32,
        min_length=10,
        required=True,
        error_messages={
            'required': '密码为必填字段，请不要留空',
            'max_length': '最大长度请不要超过32个字符',
            'min_length': '密码长度不要小于10个字符',
        },
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入您的密码'}
        )
    )
    # 确认密码form组件
    re_password = fields.CharField(
        label='确认密码',
        max_length=32,
        min_length=10,
        required=True,
        error_messages={
            'required': '密码为必填字段，请不要留空',
            'max_length': '最大长度请不要超过32个字符',
            'min_length': '密码长度不要小于10个字符',
        },
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入您的密码'},
        ),
    )
    avatar = fields.FileField(
        required=False,
        widget=widgets.FileInput(
            attrs={'id': 'imgSelect', },
        )
    )
    auth_code = fields.CharField(
        label='验证码',
        error_messages={
            'required': '验证码不能为空'
        },
        widget=widgets.TextInput(
            attrs={'class': 'form-control', 'placeholder': '验证码', },
        ),
    )

    # 我想要验证码在Form组件里直接验证，但是要获取验证码要从session中去取
    # 要想从session中取的话就要找request，但是实际上是没有的
    # 因此我们可以调用父类的构造函数，定义一下request
    # 在实例化的时候多传递一个request就可以了，重新封装
    def __init__(self, request, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_auth_code(self):
        input_code = self.cleaned_data['auth_code']
        session_code = self.request.session.get('auth_code')
        if input_code.upper() == session_code.upper():
            # 要return值，因为clean_%这方法要拿到返回值然后赋值给cleaned_data的。
            return input_code
        # 如果上面有问题会被捕获到，如下为源码
        # except ValidationError as e
        #     self.add_error(name, e)，name就是循环的字段名称
        raise ValidationError('验证码错误')

    def clean(self):
        # 不排除会报错，因此使用保险的方式就是使用get去调用而不是直接读取key
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('re_password')
        if password1 == password2:
            # 这里其实不return值也是可以的，看clean方法内部。
            return self.cleaned_data
        # 这个异常会默认放到一个特殊的key：__all__这个key中
        # 前端要想去这个__all__中的数据的话不能用obj.errors.__all__
        # 当然后端可以这样取，obj.errors['__all__']或者obj.errors[NON_FIELD_ERRORS]
        # 但是在前段上面两种方式都不能显示出来，需要用如下的形式去显示
        # obj.non_field_errors，这样就说明了，取整体的错误和取单个字段的错误信息的方式是不一致的。
        raise ValidationError('两次密码不一致')
        # 或者可以直接手动绑定错误信息，前者是字段名，后者是报错。
        # 这样在前端就可以直接进行调用了。
        # self.add_error('re_password', ValidationError('密码不一致'))


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空不能为空',
            'min_length': '请不要输入少于6个字符',
            'max_length': '请不要输入超过18个字符',
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入您的用户名'
        }),
    )
    password = fields.CharField(
        max_length=16,
        required=True,
        min_length=6,
        error_messages={
            'required': "密码不能为空"
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入您的密码'
        })
    )
    t2 = fields.IntegerField()