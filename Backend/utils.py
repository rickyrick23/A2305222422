import shortuuid

def generate_shortcode():
    return shortuuid.ShortUUID().random(length=6)
