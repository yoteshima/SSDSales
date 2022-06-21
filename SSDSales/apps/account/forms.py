# -*- coding: utf-8 -*- 

import re

from django import forms
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _


class UserForm(forms.Form):
    """
    ユーザ登録用フォーム
    """
    last_name = forms.CharField(label=_('last name'), max_length=10)
    first_name = forms.CharField(label=_('first name'), max_length=10) 
    last_name_kana = forms.CharField(label=_('last name kana'), max_length=10)
    first_name_kana = forms.CharField(label=_('first name kana'), max_length=10) 
    tel_number0 = forms.CharField(label=_('tel number'), max_length=5) 
    tel_number1 = forms.CharField(label=_('tel number'), max_length=4) 
    tel_number2 = forms.CharField(label=_('tel number'), max_length=4) 
    email = forms.EmailField(label=_('email'), max_length=254)
    email_confirm = forms.EmailField(label=_('email confirm'), max_length=254)
    password = forms.CharField(label=_('password'),
                            max_length=30, widget=forms.PasswordInput())
    password_confirm = forms.CharField(label=_('password confirm'),
                            max_length=30, widget=forms.PasswordInput())
    detail = forms.CharField(label=_('detail'), widget=forms.Textarea())
    icon = forms.ImageField(label=_('icon'))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __valid_string(self, pattern, _str, error_message):
        for c in _str:
            # 一文字ずつ検証
            if not re.match(pattern, c):
                raise forms.ValidationError(error_message)
        return _str


    def __valid_tel_number(self, code):
        # 正規表現パターン
        pattern = r'^[0-9]+$'
        phone_number = self.cleaned_data[code]
        # 整数で入力されているか検証
        phone_number = self.__valid_string(pattern=pattern, _str=phone_number,
                        error_message=_('Please enter an integer.'))
        return phone_number


    def clean_last_name_kana(self):
        # 正規表現パターン
        pattern = r'^[ア-ン]+$'
        furigana = self.cleaned_data['last_name_kana']
        # 全角カタカナで入力されているか検証
        last_name_kana = self.__valid_string(pattern=pattern, _str=furigana,
                            error_message=_('Please enter in the full-width katakana.'))
        return last_name_kana


    def clean_first_name_kana(self):
        # 正規表現パターン
        pattern = r'^[ア-ン]+$'
        furigana = self.cleaned_data['first_name_kana']
        # 全角カタカナで入力されているか検証
        family_name_kana = self.__valid_string(pattern=pattern, _str=furigana,
                            error_message=_('Please enter in the full-width katakana.'))
        return family_name_kana


    def clean_tel_number0(self):
        return self.__valid_tel_number(code='phone_number0')


    def clean_tel_number1(self):
        return self.__valid_tel_number(code='phone_number1')


    def clean_tel_number2(self):
        return self.__valid_tel_number(code='phone_number2')


    def clean_email_confirm(self):
        email = self.cleaned_data['email']
        email_confirm = self.cleaned_data['email_confirm']
        # 確認用メールアドレスが合致するか検証
        if email != email_confirm:
            raise forms.ValidationError(_('Email addresses do not match.'))
        return email_confirm


    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        # 確認用パスワードが一致するか検証
        if password != password_confirm:
            raise forms.ValidationError(_('Passwords do not match.'))
        return password_confirm


    def save(self):
        upload_file = self.cleaned_data['icon']
        file_name = default_storage.save(upload_file.name, upload_file)
        return default_storage.url(file_name)
