import qiniu
access_key = "yBUD0ii3zHvlL2TJGmVRxZXxLBYhcx5S3ldd4H8Y"
secret_key = "-gQqej18kHP4hi8U7UsthaDGhGU4cE79VxShN2Kx"
bucket_name = "ihome"


def storage(data):
    '''
        access_key      秘钥管理 - AK
        secret_key      秘钥管理 - SK
        bucket_name     空间名

        data就是要上传的数据
        key是这个数据的键（就是七牛给这个图片起的名字，我们可以通过它拿到保存在七牛的这张图片）
    '''
    try:
        q = qiniu.Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = qiniu.put_data(token, None, data)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传图片失败")

        # 返回七牛中保存的图片名
    return ret["key"]


if __name__ == "__main__":
    with open('/home/python/Desktop/avarters/qiniu.png', "rb") as f:
        img_data = f.read()

    storage(img_data)
    # "http://pj9p8snfa.bkt.clouddn.com/ "+ storage(img_data)
    # FjrKtjcZZ3iMrrfo - LT8rGAZofC_