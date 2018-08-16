#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'oW59DcqC9H89DxEKAJyEbvTx6R7EuA7K2-2rlcF-'
secret_key = 'zJk139xsjfqEtR-rdohtp5rVOa2wNWJ6IDQzqE6r'


# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'blog-storage'
# 上传到七牛后保存的文件名
key = 'my-python-logo2.png'

# 回调
policy={
 'callbackUrl': 'http://your.domain.com/callback.php',
 'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
}

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = './123.png'
ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)