from utils.qiniu_storage import storage


class MyStorage(object):
    """自定义文件存储系统类"""

    def save(self, name, content):
        path=storage(content.read())
        return path

    def get_available_name(self,name):
        return name

    def url(self,name):
        return "http://pnu1eclcx.bkt.clouddn.com/"+ name
