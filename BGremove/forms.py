from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, URL

class ImageUploadForm(FlaskForm):
    image = FileField('Background removal Ai', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only! jpg, png, jpeg'),
                                                 FileRequired('File is required')])
    submit = SubmitField('Upload')

    def validate_image(self, image):
        if image.data:
            file_size = len(image.data.read())
            image.data.seek(0)
            max_size = 2 * 1024 * 1024  # 3MB in bytes
            if file_size > max_size:
                raise ValidationError('File size must be less than 2MB. But no limit on pixel size')
            
class ImageURLForm(FlaskForm):
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit_url = SubmitField('Process URL')



