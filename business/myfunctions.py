from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(uploaded_image, max_size=1*500*500):
    # Open the image from the uploaded file
    img = Image.open(uploaded_image)
    
    # Create a BytesIO object to hold the image data
    img_io = BytesIO()
    img.save(img_io, format=img.format)
    
    # Check the initial size
    if img_io.tell() <= max_size:
        return uploaded_image  # Image is already below the threshold
    
    # Compress the image
    quality = 85  # Starting quality for compression
    
    # Adjust the quality to compress the image
    while True:
        # Create a new BytesIO object for each iteration
        img_io = BytesIO()
        
        # Save the image to the BytesIO object with the current quality
        img.save(img_io, format=img.format, quality=quality)
        
        # Check the size of the compressed image
        if img_io.tell() <= max_size or quality <= 10:
            break
        
        # Reduce the quality for the next iteration
        quality -= 5

    # Save the compressed image to a new BytesIO object
    compressed_img_io = BytesIO()
    img.save(compressed_img_io, format=img.format, quality=quality)
    compressed_img_io.seek(0)
    
    # Retrieve necessary attributes from the original uploaded image
    if hasattr(uploaded_image, 'name'):
        name = uploaded_image.name
    else:
        name = 'compressed_image.' + img.format.lower()
        
    if hasattr(uploaded_image, 'content_type'):
        content_type = uploaded_image.content_type
    else:
        content_type = 'image/' + img.format.lower()

    if hasattr(uploaded_image, 'charset'):
        charset = uploaded_image.charset
    else:
        charset = None
    
    # Return the compressed image as an InMemoryUploadedFile object
    compressed_image = InMemoryUploadedFile(
        compressed_img_io,       # file
        None,                    # field_name
        name,                    # name
        content_type,            # content_type
        compressed_img_io.tell(), # size
        charset                  # charset
    )
    
    return compressed_image
