class Edit:
    def __init__(self, path=None):
        if bool(path):
            from PIL import Image
            self.__obj = Image.open(path)
            self.__path = path
        else:
            self.__obj = None
            self.__path = None
    
    @property
    def exists(self):
        return bool(self.__obj)
    
    @property
    def qtimage(self):
        from PIL import ImageQt
        return ImageQt.ImageQt(self.__obj)
    
    @property
    def path(self):
        return self.__path
    
    @property
    def obj(self):
        return self.__obj
    
    def clear(self):
        self.__obj = None
        self.__path = None
    
    def open(self, path):
        from PIL import Image
        self.__obj = Image.open(path)
        self.__path = path
    
    def rotate(self, angle):
        self.__obj = self.__obj.rotate(angle, expand=True)
    
    def resize(self,target_size):
        self.__obj = self.__obj.resize(target_size)
    
    def filter(self, filter_name):
        if filter_name:
            from PIL import ImageFilter
            if filter_name == 'BLUR':
                self.__obj = self.__obj.filter(ImageFilter.BLUR)
            elif filter_name == 'CONTOUR':
                self.__obj = self.__obj.filter(ImageFilter.CONTOUR)
            elif filter_name == 'DETAIL':
                self.__obj = self.__obj.filter(ImageFilter.DETAIL)
            elif filter_name == 'EDGE_ENHANCE':
                self.__obj = self.__obj.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_name == 'EMBOSS':
                self.__obj = self.__obj.filter(ImageFilter.EMBOSS)
            elif filter_name == 'FIND_EDGES':
                self.__obj = self.__obj.filter(ImageFilter.FIND_EDGES)
            elif filter_name == 'SHARPEN':
                self.__obj = self.__obj.filter(ImageFilter.SHARPEN)
            elif filter_name == 'SMOOTH':
                self.__obj = self.__obj.filter(ImageFilter.SMOOTH)
            elif filter_name == 'SMOOTH_MORE':
                self.__obj = self.__obj.filter(ImageFilter.SMOOTH_MORE)