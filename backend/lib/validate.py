def is_PDF(file_name):
    extension = file_name.split('.')[-1]
    extension = extension.lower()

    if extension == 'pdf': return True
    else: return False