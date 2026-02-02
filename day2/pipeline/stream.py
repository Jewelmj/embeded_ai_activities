from pipeline.loader import read_image
from pipeline.preprocess import preprocess_image

def image_stream(image_paths, batch_size=4):
    """Rule 4 & Step 5: Yield batches of images instead of one-by-one."""
    batch = []
    for path in image_paths:
        img = read_image(path)
        if img is not None:
            # Rule 2: Resize early inside the stream
            processed = preprocess_image(img)
            batch.append(processed)
        
        if len(batch) == batch_size:
            yield batch
            batch = []
    
    # Yield remaining images
    if batch:
        yield batch