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

### 计算图像的分割结果
Method：POST

URL: /

参数类型:json

参数:'image_name': 必须，待处理图片名（相对路径); 'model_name': 可为空，预留参数, 默认值‘deeplab’; ‘signature_name’: 可为空，预留参数; 默认值‘predict_image'.

返回值类型：json

返回值：{'status': int, 'path': int}; 
status: 请求服务的状态码，0 is SUCCESS, 1 is FileNotFound, 2 is TFServerError, 3 is MaskSaveError, 4 is OtherErrors; 
path: 分割结果的相对存储路径。