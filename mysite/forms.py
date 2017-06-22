# -*- coding: utf-8 -*-

from django import forms


class UserForm(forms.Form):
	username = forms.CharField(label = '用户名',max_length = 10, min_length = 3, 
		error_messages = {'required':'Dear,请输入用户名,最少3位,最多10位',
						'max_length':'Dear,请输入用户名,最少3位,最多10位',
						'min_length':'Dear,请输入用户名,最少3位,最多10位'},
		widget = forms.TextInput(attrs={'placeholder':'请输入用户名,最少3位'
			}))

	password = forms.CharField(label = '密 码',max_length = 10, min_length = 4,
		error_messages = {'required':'Dear,请输入密码,最少4位,最多10位',
						'max_length':'Dear,请输入密码,最少4位,最多10位',
						'min_length':'Dear,请输入密码,最少4位,最多10位'},
		widget = forms.PasswordInput(attrs={'placeholder':'请输入密码,最少4位数字或字母'
			}))

	password_yz = forms.CharField(label = '密 码',max_length = 10, min_length = 4, 
		# error_messages = {'required':'Dear,请输入密码,最少4位,最多10位',
		# 				'max_length':'Dear,请输入密码,最少4位,最多10位',
		# 				'min_length':'Dear,请输入密码,最少4位,最多10位'},
		widget = forms.PasswordInput(attrs={'placeholder':'请重复密码'
			}))

	email = forms.EmailField(label = '邮箱',max_length = 50,
		# error_messages = {'invalid':'Dear,邮箱格式不正确'},
		widget = forms.EmailInput(attrs={'placeholder':'请输入电子邮箱'
			}))


class CommentForm(forms.Form):
	comment_text = forms.CharField(max_length = 200,
		widget = forms.Textarea(attrs={
			'class':'comment-text',
			'placeholder':'请登录后评论,最多200字',
			}))