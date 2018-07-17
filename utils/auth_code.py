import random
# ImageFilter加滤镜，让色差更强一点
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def rd_check_code(width=120, height=30, char_length=5, font_file='static/fonts/kumo.ttf', font_size=28):
    """
    图片宽高，字符长度，字体路径，字体大小。注意这里static前面别加斜线。
    """
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndchar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndcolor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndchar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndcolor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndcolor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndcolor())
    # 设置色差
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
