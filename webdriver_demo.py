#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author dbxiao
'''

from selenium import webdriver

d = webdriver.Firefox()
d.get("http://www.baidu.com")
print d.page_source
d.execute_script("document.getElementById(arguments[0]).value=arguments[1];",
"su","button")
d.execute_script("console.log(arguments[1]);console.log(arguments[0])","a","b")
"""Traceback (most recent call last):
  File "C:/Users/v_dbxiao/PycharmProjects/untitled1/testweb.py", line 9, in
  <module>
    d.execute_script("alert(arguments[1]);alert(arguments[0])","a","b")
  File "C:\Python27\lib\site-packages\selenium\webdriver\remote\webdriver.py",
  line 465, in execute_script
    'args': converted_args})['value']
  File "C:\Python27\lib\site-packages\selenium\webdriver\remote\webdriver.py",
  line 236, in execute
    self.error_handler.check_response(response)
  File "C:\Python27\lib\site-packages\selenium\webdriver\remote\errorhandler.py
  ", line 192, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: Failed to find value 
field"""
d.execute_script("alert(arguments[1]);alert(arguments[0])","a","b")