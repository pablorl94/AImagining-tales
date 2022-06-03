import os
import numpy as np
import pandas as pd
import random 

def add_type_size(df):
    
    pages = ['cover']
    
    type_pages = ['middle', 'up', 'down']
    
    rest_pages = [random.choice(type_pages) for i in range(len(df)-1)]
    pages.extend(rest_pages)
    
    df['page_style'] = pages
    df['text_size'] = [40 if x=='cover' else 12 for x in pages]
    
    return df


def create_page_dict(page_type, text, summ, max_iter, text_size, font='Courier', style='graphic novel'):
    
    dict_page_style = {"type": page_type}
    dict_nn = {"seed": -1}
    dict_parameters = {"texts": [summ, style], "width": 300, "height": 300, "images_interval": 50, "init_image": None, "target_images" : None, "max_iterations": max_iter, "input_images": None}
    dict_pdf_style = {"font": font, "text_size": text_size, "text": text, "w_image":100, "h_image":80}
    
    dict_total = {"page_style": dict_page_style, "neural_network": dict_nn, "parameters": dict_parameters, "pdf_style": dict_pdf_style}
    
    return dict_total
  
  
  