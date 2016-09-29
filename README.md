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

+++++++++++++++++++++++++++

2016/9/29

经过筛选处理后的数据正样本16862个，负样本55655个
负样本是用imagenet上的部分数据,由于文件夹结构错综复杂，先写个脚本压压惊，`deal_imagenet.ipynb`将指定目录(imagenetphoto1/ImageNet_Utils/)下的所有以JPEG结尾的图片都存到imagenetphoto2文件夹下。

接着继续使用`logo_converttoimg.ipynb`文件，修改下路径参数:
```
os.path.walk(r'/root/dl-data/imagenetphoto2', processDirectory, None )
```
将文件夹imagenetphoto2中的图片转化成jpeg格式，并且将转化成功的图片路径写入(/root/dl-data/imagenet_path.txt)文件中

此时我们有了储存正例路径的文件`logo_pathforsxw1080.txt`和负例路径文件`imagenet_path.txt`开始准备读入torch中save t7大功告成，然而并没有那么顺利因为总数据量有73000左右，我直接申请了(73000,3,256,256),结果电脑很不给面子地表示我申请了106G的内存，让我一边凉快去顺便买一个新的RAM。没办法，只能看看有没有办法节约一下空间，调研了一晚上还是决定，分开做t7文件，做成(4096,3,256,256)的。

因为训练的数据需要打散，`SetLabel.ipynb`文件从正负样本文件夹中读取文件复制到同一文件夹下，并制作了存放`“path label”`数据的文件`/root/dl-data/dataset/dataset.txt`

现在，应该属于万事俱备的状态了，可是在真正将数据存入初始化好的tensor中时，报错了，错误信息是`Empty input file`。

打印出错图片的路径看一下然后就郁闷了，报错的不是固定一张图片，说明不是图片本身的问题，应该是系统读取文件到内存时候出的错，然后我拿了`imagenet_path.txt`测试了一下，4096张图片完美输入没有出错！仔细对比了一下两个txt后我估计是`imagenet_path.txt`文件内的路径都访问的是同一文件夹，但是`dataset.txt`因为里面有正样本的数据在(正样本不同类别是放在同一文件夹下的不同文件夹中，路径复杂)路径变得非常复杂，思前想后觉得应该是这个原因。

那就写呗。

接着写一个脚本`combinefile.ipynb`，继续根据`logo_pathforsxw1080.txt`和`imagenet_path.txt`将正负样本图片复制到同一个文件夹下，并且注上label。但是用了这个方法问题并没有解决！！见到这样的我，只能默默拿起了trycatch机制。。。

trycatch果然让人省心，运行一下`generate_t7.ipynb`成功生成t7文件
