这里其实是用flask包装tensorflow serving client成了一个web服务。
部署tensorflow serving可参考博客 https://blog.csdn.net/qq_14975217/article/details/80985127
## 服务提供两个功能
### 获取待处理的图像文件列表
Method： POST

URL: /list

参数：无

返回值类型：json

返回值：{files: [root, dir_1, file01, file02, dir_2, file0a, ...]}; files列表为按顺序存储的目录和文件列表，用’--‘区分目录或文件的级别。
```
root/
--dir_1/
----file01
----file02
--dir_2/
----file0a
----file0b
--file*1
--file*2
...
...
```

### 下载图像
Method: GET
URL: /download
参数：filename
    
注意：filename的格式为"src/res_abcd.zxy",比如“src_1.jpg”
其中‘src’指示需要下载的是原图，‘res’指示需要下载的是tf model处理的结果；
abcd.zxy为图像名，

### 上传图像
Method: POST

URL: /upload

参数：指定要上传的文件

返回值类型：json

返回值：{'status': int}
0: success; 101: 文件格式错误； 102：文件已存在； 103：others

### 计算图像的分割结果
Method：POST

URL: /tf

参数类型:json

参数:'image_name': 必须，待处理图片名（相对路径); 'model_name': 可为空，预留参数, 默认值‘deeplab’; ‘signature_name’: 可为空，预留参数; 默认值‘predict_image'.

返回值类型：json

返回值：{'status': int, 'path': int}; 
status: 请求服务的状态码，0 is SUCCESS, 101 is FileNotFound, 102 is TFServerError, 103 is MaskSaveError, 104 is OtherErrors; 
path: 分割结果的相对存储路径。