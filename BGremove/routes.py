import os
from flask import render_template, request, redirect, send_file, session, url_for
from BGremove.Different_Modules import remove_files, bg_remover, bg_removerURL, process_image_from_url, save_images, saved_images_folder, sessions, sessions_folder
from BGremove.forms import ImageUploadForm, ImageURLForm
from BGremove import app



@app.route('/', methods=['GET','POST'])
def bgremove():
    idt = sessions()
    sessions_folder()
    form_upload = ImageUploadForm()
    if idt: 
        if form_upload.validate_on_submit():
            if form_upload.image.data:
                remove_files()
                uploaded_image_path = saved_images_folder(form_upload.image.data)
                bg_removed_image_path = bg_remover(form_upload.image.data)

                uploaded_images = [url_for('static',
                                           filename=f'uploads/{session["user_id"]}/{os.path.basename(uploaded_image_path)}')]
                bg_removed_images = [url_for('static',
                                             filename=f'uploads/{session["user_id"]}/{os.path.basename(bg_removed_image_path)}')]
                
                bg_removed_filename = os.path.basename(bg_removed_image_path)

                return render_template('bgremove.html', form=form_upload,
                                       uploaded_images=uploaded_images,
                                       bg_removed_images=bg_removed_images,
                                       bg_removed_filename=bg_removed_filename)

    return render_template('bgremove.html', form=form_upload)




@app.route('/URL', methods=['GET','POST'])
def bgremoveURL():
    idt = sessions()
    sessions_folder()
    form_url = ImageURLForm()
    if idt:
        if form_url.validate_on_submit():
            image_url = form_url.image_url.data
            upload_image = process_image_from_url(image_url)
            bg_removed_file = bg_removerURL(upload_image)

            uploaded_images = [url_for('static',
                                            filename=f'uploads/{session["user_id"]}/{os.path.basename(upload_image)}')]
            bg_removed_images = [url_for('static',
                                            filename=f'uploads/{session["user_id"]}/{os.path.basename(bg_removed_file)}')]
            
            bg_removed_filename = os.path.basename(bg_removed_file)


            return render_template('bgremoveURL.html', form=form_url, 
                                   uploaded_images=uploaded_images, 
                                   bg_removed_images=bg_removed_images,
                                   bg_removed_filename=bg_removed_filename)
    return render_template('bgremoveURL.html', form=form_url)





@app.route('/download_bg_removed/<filename>')
def download_bg_removed(filename):
    user_id = session.get('user_id')
    if user_id:
        user_upload_folder = os.path.join(app.root_path, 'static/uploads', user_id)
        bg_removed_file_path = os.path.join(user_upload_folder, filename)
        
        if os.path.exists(bg_removed_file_path):
            return send_file(bg_removed_file_path, as_attachment=True)
    
    return 'File not found', 404

