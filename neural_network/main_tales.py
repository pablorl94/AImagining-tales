import os
import shutil
import pandas as pd 

import json
from pdf_pages import create_cover, create_middle_page, create_up_page, create_down_page
from image_model import model_selection, parameter_definition, fire_up_ai, get_image_by_index
from config_generator import add_type_size, create_page_dict


def create_json(csv_path):
    
    # Read csv file
    df = pd.read_csv(csv_path)
    
    # Add columns for type of page and text size
    df = add_type_size(df)
    
    input_json = []
    max_iter = 150
    
    for i, row in df.iterrows():
        if i > 7:
            break
        else:
            input_json.append(create_page_dict(row['page_style'], row['story'], row['summ'], max_iter, row['text_size']))

    
    return input_json
    

def generate_tale_pdf(config_file, pdf_name, generate_images=True):
    pdf = None
    images_paths = []
    new_path = 'results'

    if generate_images:
        # descargar el modelo
        print('Download model...')
        model_selection()
        i = 0

        if os.path.exists(new_path):
            shutil.rmtree(new_path)
        os.makedirs(new_path)

        for page in config_file:

            if os.path.exists('steps'):
                shutil.rmtree('steps')
            os.makedirs('steps')

            print("Getting parameters for NN...")
            args = parameter_definition(page)

            print("Generating image " + str(i))
            print("Launching AI...")
            fire_up_ai(args, page)

            print("Getting generated image...")
            image_path = get_image_by_index(index=page['parameters']['max_iterations'])
            new_image_path = new_path + '/' + 'image_' + str(i) + '.png'

            print("Saving generated image to results folder...")
            shutil.move(image_path, new_image_path)

            images_paths.append(new_image_path)
            i += 1

    if generate_images==False:
        images_paths = os.listdir('results')
        images_paths = ['results/'+x for x in images_paths]
        
    print('---------------------------------------------------------------------------')
    print("Building PDF....")
    for page_num, page in enumerate(config_file):
        print("Generating page " + str(page_num))
        if page['page_style']['type'] == 'cover':
            pdf = create_cover(page, images_paths[page_num])
        elif page['page_style']['type'] == 'middle':
            pdf = create_middle_page(pdf, page, images_paths[page_num])
        elif page['page_style']['type'] == 'up':
            pdf = create_up_page(pdf, page, images_paths[page_num])
        else:
            pdf = create_down_page(pdf, page, images_paths[page_num])

    pdf.output(pdf_name, 'F')
    print("DONE")
    return


if __name__ == '__main__':
    
    print("Reading CSV to generate json config file")
    
    csv_path = 'beautyandthebeast.csv'
    config_file = create_json(csv_path)
    
    with open("config.json", "w") as outfile:
        json.dump(config_file, outfile)
        
    
    # with open('config.json', "r") as f:
    #     config_file = json.load(f)

    pdf_name = 'tale.pdf'
    generate_tale_pdf(config_file, pdf_name, generate_images=False)
