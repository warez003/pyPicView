class PathList:
    def __init__(self, paths=None, cur_path=None):
        if bool(paths) and bool(cur_path):
            self.__list = paths
            self.__cur_index = self.__list.index(cur_path)
        else:
            self.__list = []
    
    @property
    def exists(self):
        return bool(self.__list)
    
    @property
    def count(self):
        return len(self.__list)
    
    @property
    def cur_index(self):
        return self.__cur_index
    
    @property
    def first(self):
        return self.__list[0]
    
    @property
    def last(self):
        return self.__list[self.count - 1]
    
    @property
    def cur_elem(self):
        return self.item_by_index(self.cur_index)
    
    def clear(self):
        self.__list.clear()
    
    def prev(self):
        if self.__cur_index - 1 > 0:
            self.__cur_index = self.__cur_index - 1
            return self.__list[self.cur_index]
        elif self.__cur_index - 1 == 0:
            self.__cur_index = 0
            return self.first
        elif self.__cur_index - 1 < 0:
            self.__cur_index = self.__list.index(self.last)
            return self.last
    
    def next(self):
        if self.__cur_index + 1 < self.count:
            self.__cur_index = self.__cur_index + 1
            return self.__list[self.cur_index]
        elif self.__cur_index + 1 == self.count:
            self.__cur_index = 0
            return self.first
    
    def add(self, item):
        self.__list.append(item)
        self.__cur_index = self.__list.index(item)
        