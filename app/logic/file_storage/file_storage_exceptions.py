class FileSizeLimitError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'File size to large!'
    
    def __str__(self):
        return 'FileSizeLimitError exception: {}'.format(self.message)

class FileExtensionError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'Unsupported file extension!'
    
    def __str__(self):
        return 'FileExtensionError exception: {}'.format(self.message)

class FileMimeTypeError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'Unsupported mime type!'
    
    def __str__(self):
        return 'FileMimeTypeError exception: {}'.format(self.message)

class FileNotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'Cannot perform operation, file not found!'
    
    def __str__(self):
        return 'FileNotFoundError exception: {}'.format(self.message)
