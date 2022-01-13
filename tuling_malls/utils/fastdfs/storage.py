from django.core.files.storage import Storage
class MYstorage(Storage):
    def open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        pass
    def save(self, name, content, max_length=None):
        pass
    def url(self,name):
        return 'http://192.168.88.2:8888/'+name