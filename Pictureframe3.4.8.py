# --coding: utf-8 --
import os
import shutil
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import PySimpleGUI as sg
from pillow_heif import register_heif_opener
#import piexif


def frameMode(img, width, color):  # 模式1
    # 读取原始图片长宽
    w, h = img.size
    # 添加四周边框
    w += 2 * width
    h += 2 * width
    # 生成的白框图片
    img_new = Image.new('RGB', (w, h), color)
    img_new.paste(img, (width, width))
    return img_new


def logoMode(img, logopic, width, color):  # 模式2
    # 读取原始图片长宽
    w, h = img.size
    # 添加四周边框
    w += 2 * width
    h += 2 * width
    # 生成的白框图片
    img_new = Image.new('RGB', (w, h), color)
    img_new.paste(img, (width, width))
    # 底部加宽w2 h2是白框图片wh，img_new2是底部加宽的图片
    w2, h2 = img_new.size
    img_new2 = Image.new('RGB', (w2, h2 + 2*width), color)
    img_new2.paste(img_new, (0, 0, w2, h2))
    w4, h4 = img_new2.size
    # 重新定义logo背景和大小
    w_logo, h_logo = logopic.size
    logopic2 = Image.new('RGBA', (w_logo, h_logo), color)
    logopic2 = Image.alpha_composite(logopic2, logopic)
    w3 = int(2.5 * width)
    h3 = int(3.47 * w3)
    if w_logo != h_logo:
        logopic2 = logopic2.resize((h3, w3))
    else:
        logopic2 = logopic2.resize((w3, w3))
    w_logo2 = logopic2.size[0]
    img_new2.paste(logopic2, (int(
        (w4 - w_logo2) / 2), int(h4 - (2.75 * width))))
    return img_new2


def bottomMode(img, logopic, pic_exif, width, color):  # 模式3
    camera_model, shoot_time, aperture, focus, iso, shutter_speed, lens_model = pic_exif
    # 读取原始图片长宽
    w, h = img.size
    # 底部加宽
    h1 = int(h+width/3 + 3 * width)
    # 生成的白框图片
    img_new = Image.new('RGB', (w, h1), color)
    img_new.paste(img, (0, 0))
    w4, h4 = img_new.size
    # 大黑色字
    upfont = ImageFont.truetype("src/SourceHanSansCN-Bold.otf", int(width/1.7))
    # 小灰色字
    dwfont = ImageFont.truetype(
        "src/SourceHanSansCN-Normal.otf", int(width/2.2))
    draw = ImageDraw.Draw(img_new)
    # 左边文字
    draw.text((width, h+width), camera_model, fill=(0, 0, 0), font=upfont)
    draw.text((width, int(h4-width-width/2.2)), lens_model,
              fill=(100, 100, 100), font=dwfont)
    # 右边文字黑色
    wtext, htext = draw.textsize(
        focus+"  "+aperture+"  "+shutter_speed+"  "+iso, font=upfont)
    draw.text((w4-width-wtext, h+width), focus+"  "+aperture+"  " +
              shutter_speed+"  "+iso, fill=(0, 0, 0), font=upfont)
    draw.text((w4-width-wtext, int(h4-width-width/2.2)),
              shoot_time, fill=(100, 100, 100), font=dwfont)
    # 右边灰线
    draw.line([int(w4-width-wtext-width/2), int(h+width+htext/3.2), int(w4-width -
              wtext-width/2), int(h4-width-htext/8)], width=int(width/30), fill=(140, 140, 140))
    hline = int(h4-width-htext/8)-int(h+width+htext/3.2)
    # logo
    w_logo, h_logo = logopic.size
    logopic2 = Image.new('RGBA', (w_logo, h_logo), color)
    logopic2 = Image.alpha_composite(logopic2, logopic)
    logopic2 = logopic2.resize((int(w_logo/(h_logo/hline)), int(hline)))
    w_logo2 = logopic2.size[0]
    img_new.paste(
        logopic2, (int(w4-2*width-wtext-w_logo2), int(h+width+htext/3.2)))
    return img_new


def picOut(img_new, name_l, savepic, picMode, folder, filter2, quality2):  # 导出
    # 生成朋友圈格式
    w, h = img_new.size
    # 判断照片横竖
    if w < h:
        rew = int((1080 / w) * h)
        img_new2 = img_new.resize((1080, rew))
    else:
        reh = int((1080 / h) * w)
        img_new2 = img_new.resize((reh, 1080))
    # 照片锐化处理
    if filter2 == '锐化':
        filter3 = ImageFilter.SHARPEN
    elif filter2 == "细节":
        filter3 = ImageFilter.DETAIL
    elif filter2 == "平滑":
        filter3 = ImageFilter.SMOOTH
    elif filter2 == "边沿增强":
        filter3 = ImageFilter.EDGE_ENHANCE
    img_new2 = img_new2.filter(filter3)
    if savepic == 1:
        try:
            os.makedirs(folder + '\Pictrue_output\Bottom_out')
            os.makedirs(folder + '\Pictrue_output\Frame_out')
            os.makedirs(folder + '\Pictrue_output\LOGO_out')
            os.makedirs(folder + '\Pictrue_output\PYQ_out')
        except:
            pass

        if picMode == 1:
            file_path = os.path.join('', '%s_f.jpg' % name_l)
            file_path2 = os.path.join('', '%s_fp.jpg' % name_l)
            img_new.save(folder + '/Pictrue_output/Frame_out/' + file_path,
                         quality=100,
                         dpi=(300.0, 300.0))  # 无损输出
            img_new2.save(folder + './Pictrue_output/PYQ_out/' + file_path2,
                          quality=quality2,
                          dpi=(96, 96))  # 朋友圈输出
        elif picMode == 2:
            file_path = os.path.join('', '%s_l.jpg' % name_l)
            file_path2 = os.path.join('', '%s_lp.jpg' % name_l)
            img_new.save(folder + '/Pictrue_output/LOGO_out/' + file_path,
                         quality=100,
                         dpi=(300.0, 300.0))  # 无损输出
            img_new.save(folder + './Pictrue_output/PYQ_out/' + file_path2,
                         quality=quality2,
                         dpi=(96, 96))  # 朋友圈输出
        elif picMode == 3:
            file_path = os.path.join('', '%s_b.jpg' % name_l)
            file_path2 = os.path.join('', '%s_bp.jpg' % name_l)
            img_new.save(folder + '/Pictrue_output/Bottom_out/' + file_path,
                         quality=100,
                         dpi=(300.0, 300.0))  # 无损输出
            img_new2.save(folder + './Pictrue_output/PYQ_out/' + file_path2,
                          quality=quality2,
                          dpi=(96, 96))  # 朋友圈输出
    else:
        if w < h:
            img_new2 = img_new.resize((int(w*0.7),int(h*0.7) ))
        else:
            img_new2 = img_new.resize((int(w),int(h) ))
        img_new2.save('src/cache/cache.jpg', quality=quality2, dpi=(30, 30))
        img_new4 = Image.open('src/cache/cache.jpg')
        img_new4.save('src/cache/cache.png')
        return img_new4


def pic_cache(img,name):  # 加载照片缓存
    if img.size[0] < img.size[1]:
        w2 = int(img.size[0]/(img.size[1]/200))
        h2 = 200
        w3 = int(img.size[0]/(img.size[1]/400))
        h3 = 400
    else:
        w2 = 200
        h2 = int(img.size[1]/(img.size[0]/200))
        w3 = 550
        h3 = int(img.size[1]/(img.size[0]/550))
    img2 = img.resize((w2, h2))
    img2.save('src/cache/'+name+".jpg", quality=80, dpi=(30, 30))#保存为缩略图
    img3 = img.resize((w3, h3))
    img3.save('src/cache/y'+name+".jpg", quality=100, dpi=(30, 30))#保存为预览处理图
    img4 = Image.open('src/cache/'+name+".jpg")
    img4.save('src/cache/'+name+'.png')


def picExif(img):  # 照片信息获取
    # 271 相机品牌 /272 相机型号 /42036 镜头型号 /33437 光圈值 /41989 35mm焦距 /37386 显示焦距 /37380 曝光补偿 /36867 拍摄时间 /33434 快门速度 /34855 iso
    try:
        exif_data = img._getexif()
        picDict = {}
    except:
        pic_exif = [" ", " ", " ", " ", " ", " ", " ", " "]
        return pic_exif
    try:
        for k, v in exif_data.items():
            picDict[str(k)] = str(v)
        # pic_exif里的顺序
        # camera_brand ,camera_model,shoot_time ,aperture ,focus ,iso ,shutter_speed,lens_model
    except:
        pic_exif = [" ", " ", " ", " ", " ", " ", " ", " "]
        return pic_exif
    try:
        camera_brand = picDict["271"]
    except:
        camera_brand = " "
    try:
        camera_model = picDict["272"]
    except:
        camera_model = " "
    try:
        shoot_time = picDict["36867"]
    except:
        shoot_time = " "
    try:
        aperture = "f"+str(picDict["33437"])
    except:
        aperture = " "
    try:
        focus = str(picDict["41989"]) + "mm"
    except:
        focus = " "
    try:
        iso = "ISO"+str(picDict["34855"])
    except:
        iso = " "
    try:
        shutter_speed = picDict["33434"]
        if float(shutter_speed) < 1:
            shutter_speed = str(int(1/float(shutter_speed)))
            shutter_speed = "1/" + shutter_speed
        else:
            pass
    except:
        shutter_speed = " "
    try:
        lens_model = picDict["42036"]
    except:
        lens_model = " "

    pic_exif = [camera_brand, camera_model, shoot_time,
                aperture, focus, iso, shutter_speed, lens_model]
    return pic_exif

'''
def picExif(img):  # 照片信息获取
    # 271 相机品牌 /272 相机型号 /42036 镜头型号 /33437 光圈值 /41989 35mm焦距 /37386 显示焦距 /37380 曝光补偿 /36867 拍摄时间 /33434 快门速度 /34855 iso
    try:
        exif_data = piexif.load(img.info['exif'])
        picDict = {}
    except:
        pic_exif = [" ", " ", " ", " ", " ", " ", " ", " "]
        return pic_exif
    try:
        for k, v in exif_data.items():
            picDict[str(k)] = str(v)
        # pic_exif里的顺序
        # camera_brand ,camera_model,shoot_time ,aperture ,focus ,iso ,shutter_speed,lens_model
    except:
        pic_exif = [" ", " ", " ", " ", " ", " ", " ", " "]
        return pic_exif
    try:
        camera_brand = picDict["271"]
    except:
        camera_brand = " "
    try:
        camera_model = picDict["272"]
    except:
        camera_model = " "
    try:
        shoot_time = picDict["36867"]
    except:
        shoot_time = " "
    try:
        aperture = "f"+str(picDict["33437"])
    except:
        aperture = " "
    try:
        focus = str(picDict["41989"]) + "mm"
    except:
        focus = " "
    try:
        iso = "ISO"+str(picDict["34855"])
    except:
        iso = " "
    try:
        shutter_speed = picDict["33434"]
        if float(shutter_speed) < 1:
            shutter_speed = str(int(1/float(shutter_speed)))
            shutter_speed = "1/" + shutter_speed
        else:
            pass
    except:
        shutter_speed = " "
    try:
        lens_model = picDict["42036"]
    except:
        lens_model = " "

    pic_exif = [camera_brand, camera_model, shoot_time,
                aperture, focus, iso, shutter_speed, lens_model]
    return pic_exif
'''
def mainGUI(light_mode):
    # sg.theme_previewer()
    if light_mode:
        sg.theme('LightGreen3')
    else:
        sg.theme('DarkTeal')
    LIGHT_GRAY_BUTTON_COLOR = f'#212021 on #e0e0e0'
    DARK_GRAY_BUTTON_COLOR = '#e0e0e0 on #212021'
    logo_brand = []
    for file_name in os.listdir('src\logo'):
        logo_name, ext = os.path.splitext(file_name)
        logo_brand.append(logo_name)
    layout_1 = [[sg.Slider(range=(0, 600), default_value=110, size=(13, 10), resolution=10,
                           orientation='v', key='-width1-', enable_events=True), sg.Image(r'src/mode1.png', k="-mode_1-")]]
    layout_2 = [[sg.Slider(range=(50, 400), default_value=110, size=(13, 10), resolution=10, orientation='v', key='-width2-', enable_events=True), sg.Image(r'src/mode2.png', k="-mode_2-"),],
                [sg.Text(' '*14), sg.Combo(logo_brand, default_value="2035", size=(8, 1), key="-logo2-", enable_events=True), ]]
    layout_31 = [
        [sg.Text('  '), sg.Input("型号", size=(6, 1), key="-camera_model-", enable_events=True), sg.Text('   '),  sg.Text(' '*22),
         sg.Combo(logo_brand, default_value="2035", size=(
             8, 1), key="-logo-", enable_events=True), sg.Text(' '),
         sg.Input("mm", size=(4, 1), key="-focus-", enable_events=True),
         sg.Input("f", size=(3, 1), key="-aperture-", enable_events=True),
         sg.Input("s", size=(5, 1), key="-shutter_speed-", enable_events=True),
         sg.Input("iso", size=(5, 1), key="-iso-", enable_events=True)
         ],
        [sg.Text('  '), sg.Input("镜头型号", size=(10, 1), key="-lens_model-", enable_events=True), sg.Text(' '*21), sg.Input("2022", size=(10, 1), key="-shoot_time-", enable_events=True), sg.Text(' ')
         ]]
    layout_3 = [[sg.Slider(range=(50, 400), default_value=140, size=(13, 10), resolution=10, orientation='v', key='-width3-', enable_events=True), sg.Image(r'src/mode3.png', k="-mode_3-")],
                [sg.Frame("", layout_31, border_width=1)]]
    layout_0 = [[sg.Text(' '*6), sg.Image(r'src/mode3.png', k="-mode_0-")]]
    layout_mode = [[sg.Button("边框", border_width=0, k="-f_mode-", button_color='grey'), sg.Button("居中LOGO", border_width=0, k="-l_mode-", button_color='grey'), sg.Button("底栏", border_width=0, k="-b_mode-", button_color='grey')],
                   [
                       sg.Frame("", layout_1, visible=False,
                                k="-layout_1-", border_width=0),
        sg.Frame("", layout_2, visible=False,
                           k="-layout_2-", border_width=0),
        sg.Frame("", layout_3, visible=False, k="-layout_3-", border_width=0)]
    ]
    layout_theme = [[sg.B('Light', size=(5, 1), border_width=0, button_color=LIGHT_GRAY_BUTTON_COLOR), sg.B(
        'Dark', size=(5, 1), border_width=0, button_color=DARK_GRAY_BUTTON_COLOR)]]
    layout = [[sg.Button("导入照片", border_width=0), sg.Text(' '), sg.ProgressBar(8, orientation='h', size=(21, 20), visible=False,	bar_color=("green", 'grey'), border_width=0, key='progressbar')],
              [sg.Listbox(values=[], size=(25, 9), enable_events=True,visible=False, key="-img_list-"),sg.Frame("", layout_0, visible=False, k="-layout_0-", border_width=0),],
              [sg.Text('_'*60)],
              [sg.Frame("", layout_mode, border_width=0)],
              [sg.Text('朋友圈选项：'), sg.Text('图片质量'),
               sg.Input('90', size=(4, 1), border_width=0, key='-quality-', enable_events=True), sg.Text('效果处理'), sg.Combo(
                  ['锐化', '细节', '平滑', '边沿增强'], default_value="细节", size=(8, 1), key="-filter-", enable_events=True), sg.Text(' '*11), sg.Button("预览", border_width=0)],
              [sg.Text('_'*60)],
              [sg.Text('导出位置:'), sg.Text(size=(25, 1), key='-save_folder-'), sg.Button('选择', border_width=0),
               sg.Button("导出", border_width=0), sg.Button("批处理(不推荐)", border_width=0)],
              [sg.Frame("", layout_theme, border_width=1), sg.Text(
                  ' '*30), sg.Button("导入logo", border_width=0), sg.Button("清除缓存", button_color="grey", border_width=0)]

              ]
    window = sg.Window('Pictureframe3', layout, icon='src/icon.ico', font=("src/SourceHanSansCN-Bold.otf", 15),
                       resizable=True, finalize=True,  element_padding=(0, 1), auto_close_duration="2", border_depth=0, alpha_channel=0.95)
    return window


def main():
    light_mode = True
    window = mainGUI(light_mode)
    while True:  # Event Loop
        event, values = window.read()
        if event in (None, '退出'):
            break
        elif event == '清除缓存':
            try:
                shutil.rmtree("src/cache")
                sg.popup("清除成功！将重新打开程序。")
                window.close()
                window = mainGUI(light_mode)
            except:
                sg.popup("清除前不能预览任何图片！")
        elif event == '导入照片':
            img_get = sg.popup_get_file("",
                                          multiple_files=True, file_types=(('jpg/png/heic', '*.jpg;*.png;*.heic'),),
                                          no_window=True)
            name_list=[]
            try:
                os.makedirs('src\cache')
            except:
                pass
            window['progressbar'].Update(0, len(img_get), visible=True)
            for a in range(len(img_get)):
                pic_path,pic_file=os.path.split(img_get[a])#分离图片路径和图片
                name, ext = os.path.splitext(pic_file)#分离图片名和图片格式
                name_list.append(pic_file)
                cache_pic = os.path.join('', '%s.jpg' % name)
                pac = os.path.exists("src/cache/"+cache_pic)#定义要检查的缓存文件
                if pac is True:#检查该缓存文件是否存在
                    pass
                else:
                    img_cache = Image.open(img_get[a])
                    pic_cache(img_cache, name)
                window['progressbar'].UpdateBar(a+1)
            window['-img_list-'].update(name_list, visible=True)
        elif event == '选择':
            save_folder = sg.popup_get_folder("选择保存的文件夹", no_window=True)
            window['-save_folder-'].update(save_folder)
        elif event == '导出':
            try:
                window['progressbar'].Update(0, 1, visible=True)
                logopic = Image.open("src/logo/"+values['-logo-']+".png")
                logopic2 = Image.open("src/logo/"+values['-logo2-']+".png")
                if mode == 1:
                    img_new = frameMode(
                        img, int(values['-width1-']), color=(250, 250, 250))
                elif mode == 2:
                    img_new = logoMode(img, logopic2, int(
                        values['-width2-']), color=(250, 250, 250))
                elif mode == 3:
                    pic_exif2 = [values['-camera_model-'], values['-shoot_time-'], values['-aperture-'],
                                 values['-focus-'], values['-iso-'], values['-shutter_speed-'], values['-lens_model-']]
                    img_new = bottomMode(img, logopic, pic_exif2, int(
                        values['-width3-']), color=(250, 250, 250))
                picOut(img_new, name_l, 1, mode,  save_folder,
                       values["-filter-"], int(values['-quality-']))
                window['progressbar'].UpdateBar(1)
            except:
                sg.popup('请先选择照片和处理模式以及路径！')
        elif event == "批处理(不推荐)":
            color = (250, 250, 250)
            try:
                window['progressbar'].Update(0, len(img_get), visible=True)
                for i in range(len(img_get)):
                    image = Image.open(img_get[i])
                    pic_exif3 = picExif(image)
                    try:
                        logopic2 = Image.open("src/logo/"+pic_exif3[0]+".png")
                    except:
                        logopic2 = Image.open("src/logo/2035.png")
                    del pic_exif3[0]
                    name_x, ext1 = os.path.splitext(name_list[i])
                    if mode == 1:
                        img_new = frameMode(image, int(
                            values['-width1-']), color)
                    elif mode == 2:
                        img_new = logoMode(image, logopic2, int(
                            values['-width2-']), color)
                    elif mode == 3:
                        img_new = bottomMode(
                            image, logopic2, pic_exif3, int(values['-width3-']), color)
                    picOut(img_new,name_x, 1, mode,  save_folder,
                           values["-filter-"], int(values['-quality-']))
                    window['progressbar'].UpdateBar(i+1)
                sg.popup('批量导出成功！')
            except:
                sg.popup('请先选择照片和处理模式以及路径！')
        elif event in ('预览', "-width1-", "-width2-", "-width3-", "-logo-", "-logo2-", '-quality-', "-filter-", '-camera_model-', '-shoot_time-', '-aperture-', '-focus-', '-iso-', '-shutter_speed-', '-lens_model-'):
            folder = 'Applet'
            try:
                img_chche3 = Image.open('src/cache/y'+name_l+".jpg")
                wh = img_chche3.size[0] / img.size[0]  # 计算原图和预览图缩小了多少倍
                if mode == 1:
                    img_new = frameMode(
                        img_chche3, int((values['-width1-']+10)*wh), color=(250, 250, 250))
                elif mode == 2:
                    logopic2 = Image.open("src/logo/"+values['-logo2-']+".png")
                    img_new = logoMode(img_chche3, logopic2, int(
                        (values['-width2-']+10)*wh), color=(250, 250, 250))
                elif mode == 3:
                    logopic = Image.open("src/logo/"+values['-logo-']+".png")
                    pic_exif2 = [values['-camera_model-'], values['-shoot_time-'], values['-aperture-'],
                                 values['-focus-'], values['-iso-'], values['-shutter_speed-'], values['-lens_model-']]
                    img_new = bottomMode(img_chche3, logopic, pic_exif2, int(
                        (values['-width3-']+10)*wh), color=(250, 250, 250))
                img_new4 =  picOut(img_new,name_l, 3, mode, folder,
                       values["-filter-"], int(values['-quality-']))
                w4,h4 = img_new4.size
                if mode == 1:
                    window["-mode_1-"].update(
                        source='src/cache/cache.png',size=(w4,h4), visible=True)
                if mode == 2:
                    window["-mode_2-"].update(
                        source='src/cache/cache.png', size=(w4,h4), visible=True)
                if mode == 3:
                    window["-mode_3-"].update(
                        source='src/cache/cache.png',size=(w4,h4),  visible=True)
            except:
                pass
        elif event == '-img_list-':
            img_list = values["-img_list-"][0]
            img = Image.open(pic_path+'/'+img_list)
            name_l, ext1 = os.path.splitext(img_list)#分离列表里图片名和图片格式
            window["-mode_0-"].update('src/cache/'+name_l+".png", visible=True)
            window["-layout_0-"].update(visible=True)
            window["-mode_1-"].update('src/mode1.png')
            window["-mode_2-"].update('src/mode2.png')
            window["-mode_3-"].update('src/mode3.png')
            pic_exif = picExif(img)
            if pic_exif[0] != " ":
                window['-logo-'].update(pic_exif[0])
                window['-logo2-'].update(pic_exif[0])
            else:
                pass
            window['-camera_model-'].update(pic_exif[1])
            window['-shoot_time-'].update(pic_exif[2])
            window['-aperture-'].update(pic_exif[3])
            window['-focus-'].update(pic_exif[4])
            window['-iso-'].update(pic_exif[5])
            window['-shutter_speed-'].update(pic_exif[6])
            window['-lens_model-'].update(pic_exif[7])
        elif event == '-f_mode-':
            mode = 1
            window['-layout_1-'].update(visible=True)
            window['-layout_2-'].update(visible=False)
            window['-layout_3-'].update(visible=False)
            window['-f_mode-'].update(button_color="green")
            window['-l_mode-'].update(button_color='grey')
            window['-b_mode-'].update(button_color='grey')
        elif event == '-l_mode-':
            mode = 2
            window['-layout_1-'].update(visible=False)
            window['-layout_2-'].update(visible=True)
            window['-layout_3-'].update(visible=False)
            window['-f_mode-'].update(button_color='grey')
            window['-l_mode-'].update(button_color="green")
            window['-b_mode-'].update(button_color='grey')
        elif event == '-b_mode-':
            mode = 3
            window['-layout_1-'].update(visible=False)
            window['-layout_2-'].update(visible=False)
            window['-layout_3-'].update(visible=True)
            window['-f_mode-'].update(button_color='grey')
            window['-l_mode-'].update(button_color='grey')
            window['-b_mode-'].update(button_color="green")
        elif event == 'Light' and not light_mode or event == 'Dark' and light_mode:
            light_mode = not light_mode
            window.close()
            window = mainGUI(light_mode)
        elif event == '导入logo':
            sg.popup("logo比例尽量为3.5：1或者1：1，\n且为透明背景的png格式图片。")
            logo_list1 = sg.popup_get_file(
                "", multiple_files=True, file_types=(('png', '*.png'),), no_window=True)
            for l in range(len(logo_list1)):
                try:
                    shutil.rmtree('src/logo'+logo_list1[l])
                except:
                    pass
                fpath, fname = os.path.split(logo_list1[l])
                shutil.copy(logo_list1[l], 'src/logo/'+fname)
            sg.popup("导入成功！")
    window.close()


if __name__ == "__main__":
    register_heif_opener()
    main()
