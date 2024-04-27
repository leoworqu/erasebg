from flask import session
from BGremove import app
from rembg import remove
import requests, os, secrets
from wtforms.validators import ValidationError


def sessions():
    if 'user_id' not in session:
        # Generate a unique identifier for the user
        session['user_id'] = secrets.token_hex(16)

    
    idt = session['user_id']
    return idt

def sessions_folder():
    user_id = session.get('user_id')
    if user_id:
        user_upload_folder = os.path.join(app.root_path, 'static/uploads', user_id)
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        return user_upload_folder
    else:
        return []
    

def remove_files():
    folder_path = os.path.join(app.root_path, 'static/uploads')
    user_id = session.get('user_id')

    if user_id:
        user_folder_path = os.path.join(folder_path, user_id)
        if os.path.isdir(user_folder_path):
            for file in os.listdir(user_folder_path):
                file_path = os.path.join(user_folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    
def save_images(form_picture):
    user_image_files = sessions_folder()
    PIC_FN = form_picture.filename
    picture_path = os.path.join(app.root_path, user_image_files, PIC_FN)
    
    form_picture.save(picture_path)
    return picture_path

def saved_images_folder(form_picture):
    user_image_files = sessions_folder()
    PIC_FN = form_picture.filename
    picture_path = os.path.join(app.root_path, user_image_files, PIC_FN)
    
    return picture_path


def bg_remover(form_image):

    user_image_files = sessions_folder()
    input_image = user_image_files
    filename, _ = os.path.splitext(form_image.filename)

    imagepath = save_images(form_image)
    text = 'removed-bg-' + filename + '.png'
    picture_path = os.path.join(app.root_path, input_image, text)

    input_path = imagepath
    output_path = picture_path

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

    return picture_path



def process_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        user_folder = sessions_folder()
        try:
            if user_folder:
                image_filename = os.path.basename(image_url)
                image_path = os.path.join(user_folder, image_filename)
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                return image_path
            else:
                return None
        except OSError:
            raise ValidationError('Only PNG, JPG, and WEBP files are allowed.')
    else:
        return None


def bg_removerURL(form_image):

    user_image_files = sessions_folder()
    input_image = user_image_files
    filename, _ = os.path.splitext(os.path.basename(form_image))

    text = 'removed-bg-' + filename + '.png'
    picture_path = os.path.join(app.root_path, input_image, text)

    input_path = form_image
    output_path = picture_path

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

    return picture_path


