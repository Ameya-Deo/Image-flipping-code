# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:37:42 2021

@author: ameya
"""

string1 = "https://my-demo-api.s3.us-east-2.amazonaws.com/R_1NyjoI0jhYGgF9L.jpg"
string1 = string1.split('/')[-1].split('.')[0]
print("new_string:",string1)