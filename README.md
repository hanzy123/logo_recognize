#logo_recognize
##数据采集及预处理文件
```
--get_logo.py 从百度图片中爬取logo图片
```
目前打算训练用的正样本20000张，负样本80000张

爬图片用的是百度图片搜索引擎，由于百度图片直接搜索打开的是高端的动态下拉自动加载(这种情况下直接抓取链接的源代码只能抓取第一页的图片链接)，目前的解决方法是回到以前的手动翻页版本(页面右上角有切换按钮)，该版本的搜索关键字和页码可以通过设置链接中的word和pn字段来实现。
```
--logo_converttoimg.py 将图片格式转化成jpeg格式
```
由于最后我们使用的torch.tensor需要的是jpeg格式的图片，而我们抓下来的数据图片并不全是jpeg的，有的图片虽然后缀名是.jpg实际上图片的编码格式并非如此，python查看图片格式的方式:
```
imghdr.what(file_path)
```
ImageMagick提供在bush中直接使用命令来进行图片covert，resize等操作，非常方便

os x ImageMagick安装
```
http://www.cactuslab.com/imagemagick/
```
python里执行bush命令
```
import os
os.system(order)
```
```
--resize_img.py 修改图片大小
```   
当初怀疑lua的image.scale命令有问题(实际上后来发现是图片资源本身有问题)写了这个用python resize图片的类，也一起放上来吧。
```
--generate_t7.ipynb 将图片读取并另存为torch需要的.t7文件
```	
写这个真是搞死我了，刚学lua各种不懂，用的是itorch jupyter notebook

另外至今没有搞清楚为什么有的图片就是不能image.load成功，lua又没有自带的trycatch机制，只能通过获取错误信息并判断。
```
fun=function()  
    Imgs.data[count] = image.scale(img1, 128, 128):float()  
end  
  
tryCatch=function(fun)  
    ret,errMessage=pcall(fun);
    return ret,errMessage
end  

a,b = tryCatch(fun);
if a == true then 
      print("count = ")
      print(count)
      count = count + 1
else
      print('no')
end
```
个人理解是要先定义一个名为fun的函数来包含有可能报错的语句，然后定义trycatch函数中pcall方法，pcall(fun)后会返回两个值，这里命名为ret和errMessage，如果函数没报错，ret的返回值为boolean类型的true(不是str类型!)

先写那么多啦，如果有问题，实时更新。
