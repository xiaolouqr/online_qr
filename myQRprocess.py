import qrcode
import os
from MyQR import myqr
from PIL import Image

'''image_model获取自定义二维码模式普通(N),中间LOGO(L),背景图片(B)
   image_version获取二维码版本(1-40)默认为1
   image_output获取二维码导出名字后缀为(.jpg,.bmp,.png,.gif)
   image_data获取需要生成二维码的数据
   error_level获取纠错码等级(L,M,Q,H)
   image_size获取需要生成二维码大小
   image_border获取二维码边框大小,即空白区
   image_pic需要设置为背景画面的图片
   image_icon需要添加在二维码中的LOGO
   image_rgbF二维码填充颜色
   image_rgbB二维码背景颜色
'''
# image_model
image_version=1
image_output=['test.jpg','test.bmp','test.png','test.gif']
image_data='http://www.baidu.com'
error_level='H'
# image_size
# image_border
image_pic='dog.jpg'
image_icon='dog.jpg'
image_rgbF='rgb(255,255,255)'
image_rgbB='rgb(0,0,0)'

#中间嵌入LOGO
def Make_image2(data,version,level,img_ico):
	#qrlevel为纠错码等级,默认为最高,类型为整型
	qrlevel=qrcode.constants.ERROR_CORRECT_H
	if level=='L':
		qrlevel=qrcode.constants.ERROR_CORRECT_L
	elif level=='M':
		qrlevel==qrcode.constants.ERROR_CORRECT_M
	elif level=='Q':
		qrlevel==qrcode.constants.ERROR_CORRECT_Q

	qr = qrcode.QRCode(
    version=version,
    error_correction=qrlevel,
    box_size=10,
    border=1
	)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill_color=image_rgbF,back_color=image_rgbB)
	img = img.convert('RGBA')
	icon = Image.open(img_ico)
	#以下代码均为调整icon的大小位置代码
	img_w,img_h = img.size
	#默认icon为二维码4分之一大小
	factor = 4
	size_w = int(img_w / factor)
	size_h = int(img_h / factor+10)
	icon_w,icon_h = icon.size
	if icon_w > size_w:
	    icon_w = size_w
	if icon_h > size_h:
	    icon_h = size_h
	# 调整icon图片大小 （ANTIALIAS是指平滑缩放）
	icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)
	w = int((img_w - icon_w) / 2)
	h = int((img_h - icon_h) / 2)
	# 重绘二维码
	img.paste(icon,(w,h))
	img.save(image_output[1])

#
def Make_image1(data,version,level,picture,save_name,color_b=False):
	if picture:
		pic=Image.open(picture)
		w,h=pic.size
		w=h=21+(version-1)*4
		pic.resize((w,h),Image.ANTIALIAS)

	try:
		version,level,file_add = myqr.run(
	        words=data,
	        version = version,
	        level=level,
	        picture=picture,
	        colorized=color_b,
	        contrast = 1.0,
	        brightness=1.0,
	        save_name=save_name,
	        save_dir=os.getcwd()
	        )
	except:
	    # 异常捕获
	    raise 
	    # 出现异常不抛出，不处理
	    pass
	    
def main():
	image_model=input('输入二维码模式(N/B/L)')
	if image_model=='N':
		Make_image1(image_data,image_version,error_level,None,image_output[1])
	elif image_model=='B':
		Make_image1(image_data,image_version,error_level,image_pic,image_output[1],color_b=True)
	elif image_model=='L':
		Make_image2(image_data,image_version,error_level,image_icon)

if __name__=='__main__':
	main()



