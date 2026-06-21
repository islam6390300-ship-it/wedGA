from PIL import Image, ImageDraw, ImageFilter
import random, math, os

BASE='/mnt/data/galymzhan_aida_invite/assets'
os.makedirs(BASE, exist_ok=True)
random.seed(11)
W,H=1080,1920

def gradient_bg(c1, c2, name, vignette=True):
    img=Image.new('RGB',(W,H),c1)
    px=img.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            # diagonal + vertical gradient
            u=(x/W*0.25 + t*0.75)
            r=int(c1[0]*(1-u)+c2[0]*u)
            g=int(c1[1]*(1-u)+c2[1]*u)
            b=int(c1[2]*(1-u)+c2[2]*u)
            px[x,y]=(r,g,b)
    if vignette:
        mask=Image.new('L',(W,H),0)
        d=ImageDraw.Draw(mask)
        for i in range(900,0,-8):
            val=int(255*(1-i/900)**1.7)
            d.ellipse((W/2-i*0.8,H/2-i,W/2+i*0.8,H/2+i),fill=val)
        overlay=Image.new('RGB',(W,H),(0,0,0))
        img=Image.composite(img, overlay, mask.filter(ImageFilter.GaussianBlur(80)))
    img.save(os.path.join(BASE,name), quality=92)

def draw_noise(img, alpha=18):
    noise=Image.new('RGBA',img.size,(0,0,0,0))
    nd=ImageDraw.Draw(noise)
    for _ in range(25000):
        x=random.randrange(W); y=random.randrange(H)
        a=random.randrange(0,alpha)
        nd.point((x,y),fill=(255,255,255,a))
    return Image.alpha_composite(img.convert('RGBA'), noise)

def hero():
    img=Image.new('RGBA',(W,H),(10,12,32,255))
    # base gradient
    base=Image.open(os.path.join(BASE,'tmp_base.jpg')).convert('RGBA') if os.path.exists(os.path.join(BASE,'tmp_base.jpg')) else Image.new('RGBA',(W,H),(12,13,33,255))
    img=base
    d=ImageDraw.Draw(img,'RGBA')
    # suit and dress zones
    d.polygon([(0,0),(520,0),(470,H),(0,H)], fill=(6,8,25,230))
    d.polygon([(470,0),(1080,0),(1080,H),(620,H)], fill=(210,211,222,120))
    # joined hands simplified
    d.rounded_rectangle((330,690,610,900), radius=65, fill=(207,160,146,150))
    d.rounded_rectangle((510,730,760,925), radius=65, fill=(235,218,207,130))
    d.ellipse((420,828,496,904), fill=(225,224,238,120), outline=(255,255,255,110), width=8)
    d.ellipse((438,846,478,886), fill=(11,13,31,90))
    # bouquet hint
    for cx,cy,r,col in [(870,760,120,(245,245,247,100)),(950,880,90,(242,241,244,85)),(810,885,80,(237,237,242,65))]:
        for _ in range(70):
            ang=random.random()*math.tau
            rr=random.random()*r
            x=cx+math.cos(ang)*rr
            y=cy+math.sin(ang)*rr
            pr=random.randint(13,25)
            d.ellipse((x-pr,y-pr,x+pr,y+pr),fill=col)
    img=draw_noise(img,12)
    img.filter(ImageFilter.GaussianBlur(1)).convert('RGB').save(os.path.join(BASE,'hero-photo.jpg'),quality=92)

def couple_stairs():
    img=Image.new('RGBA',(W,H),(12,14,34,255))
    d=ImageDraw.Draw(img,'RGBA')
    # building columns
    for x in [120,300,500,720,920]:
        d.rounded_rectangle((x,100,x+90,1780), radius=36, fill=(78,80,108,85))
        d.rectangle((x-28,120,x+118,220), fill=(56,57,83,75))
        d.rectangle((x-40,1600,x+130,1740), fill=(45,46,68,95))
    # stairs
    for i,y in enumerate(range(1150,1730,80)):
        d.rectangle((0,y,W,y+28), fill=(40,42,62,140))
    # bride/groom silhouette
    d.ellipse((435,865,495,935), fill=(16,18,30,210))
    d.rectangle((430,930,505,1170), fill=(14,17,29,210))
    d.ellipse((512,880,572,948), fill=(16,18,30,210))
    d.polygon([(505,940),(590,980),(610,1170),(495,1165)], fill=(12,15,27,220))
    # dress veil
    d.polygon([(418,940),(285,1520),(555,1540),(520,1020)], fill=(235,236,244,115))
    d.polygon([(458,950),(110,1600),(520,1550)], fill=(230,231,242,70))
    img=draw_noise(img,15)
    img.filter(ImageFilter.GaussianBlur(1.5)).convert('RGB').save(os.path.join(BASE,'couple-stairs.jpg'),quality=92)

def hall():
    img=Image.new('RGBA',(W,H),(15,16,36,255))
    d=ImageDraw.Draw(img,'RGBA')
    # hall curtains and stage
    for x in range(0,W,135):
        d.polygon([(x,260),(x+70,260),(x+20,1500)], fill=(75,72,92,95))
        d.polygon([(x+60,250),(x+140,250),(x+115,1500)], fill=(235,232,242,60))
    d.rectangle((80,1210,1000,1520), fill=(28,30,50,180))
    d.rectangle((180,1080,900,1220), fill=(230,229,235,35))
    # lights
    for x,y in [(150,340),(930,360),(520,500)]:
        d.ellipse((x-35,y-35,x+35,y+35), fill=(244,244,255,85))
        d.polygon([(x,y),(x-520,1600),(x+90,1600)], fill=(255,255,255,28))
    # tables/flowers hint
    for cx in [250,520,800]:
        d.ellipse((cx-120,1180,cx+120,1275), fill=(235,235,242,45))
        d.rectangle((cx-110,1250,cx+110,1500), fill=(215,213,225,28))
    img=draw_noise(img,14)
    img.filter(ImageFilter.GaussianBlur(1.2)).convert('RGB').save(os.path.join(BASE,'hall.jpg'),quality=92)

def hands():
    img=Image.new('RGBA',(W,H),(18,17,36,255))
    d=ImageDraw.Draw(img,'RGBA')
    d.rectangle((0,0,W,H), fill=(20,20,44,255))
    # blurred background bokeh
    for _ in range(80):
        x=random.randrange(W); y=random.randrange(H)
        r=random.randrange(10,65)
        d.ellipse((x-r,y-r,x+r,y+r), fill=(150,145,170,random.randrange(8,30)))
    # hands
    d.rounded_rectangle((165,760,655,935), radius=88, fill=(215,158,140,135))
    d.rounded_rectangle((520,700,975,910), radius=95, fill=(230,207,195,120))
    d.line((260,880,690,850), fill=(255,255,255,120), width=12)
    d.ellipse((300,818,365,885), outline=(255,255,255,110), width=9)
    img=draw_noise(img,15)
    img.filter(ImageFilter.GaussianBlur(1.3)).convert('RGB').save(os.path.join(BASE,'hands.jpg'),quality=92)

def rings():
    img=Image.new('RGBA',(W,H),(112,107,125,255))
    d=ImageDraw.Draw(img,'RGBA')
    # blurred table
    for y in range(H):
        t=y/H
        col=(int(75+45*t), int(72+45*t), int(88+50*t),255)
        d.line((0,y,W,y),fill=col)
    # rings
    d.ellipse((260,980,515,1235), outline=(235,235,242,105), width=28)
    d.ellipse((615,1000,910,1248), outline=(225,225,232,100), width=38)
    d.ellipse((305,1025,470,1190), outline=(255,255,255,65), width=8)
    d.ellipse((675,1060,850,1200), outline=(255,255,255,55), width=10)
    # diamond sparkle
    d.polygon([(380,920),(440,995),(382,1075),(322,995)], fill=(238,238,255,90), outline=(255,255,255,100))
    for ang in range(0,360,45):
        x1=382+math.cos(math.radians(ang))*85; y1=995+math.sin(math.radians(ang))*85
        x2=382+math.cos(math.radians(ang))*135; y2=995+math.sin(math.radians(ang))*135
        d.line((x1,y1,x2,y2),fill=(255,255,255,55),width=3)
    img=draw_noise(img,14)
    img.filter(ImageFilter.GaussianBlur(1.1)).convert('RGB').save(os.path.join(BASE,'rings.jpg'),quality=92)

def flower(filename, palette='blue', size=520):
    img=Image.new('RGBA',(size,size),(0,0,0,0))
    d=ImageDraw.Draw(img,'RGBA')
    if palette=='blue':
        colors=[(139,169,218,230),(107,137,196,240),(179,199,232,225),(76,98,160,230),(205,218,245,220)]
        center=(43,50,105,245)
    else:
        colors=[(239,240,230,235),(222,228,205,235),(248,249,240,230),(215,220,194,230),(255,255,250,225)]
        center=(170,175,145,220)
    cx=cy=size/2
    # cluster petals
    for i in range(230):
        # gaussian disc
        r=random.random()**0.5*(size*0.42)
        theta=random.random()*math.tau
        x=cx+math.cos(theta)*r*1.05
        y=cy+math.sin(theta)*r*0.95
        pr=random.randint(size//42, size//24)
        col=random.choice(colors)
        # 4/5 petal small flower
        petal_count=5
        rot=random.random()*math.tau
        for k in range(petal_count):
            a=rot+k*math.tau/petal_count
            px=x+math.cos(a)*pr*0.62
            py=y+math.sin(a)*pr*0.62
            d.ellipse((px-pr*0.75,py-pr*0.52,px+pr*0.75,py+pr*0.52), fill=col)
        d.ellipse((x-pr*0.25,y-pr*0.25,x+pr*0.25,y+pr*0.25), fill=center)
    # shadow/depth
    shadow=Image.new('RGBA',(size,size),(0,0,0,0))
    sd=ImageDraw.Draw(shadow,'RGBA')
    sd.ellipse((size*.08,size*.10,size*.92,size*.92), fill=(0,0,0,50))
    shadow=shadow.filter(ImageFilter.GaussianBlur(18))
    img=Image.alpha_composite(shadow,img)
    img.save(os.path.join(BASE,filename))

# create bases
# temp gradient for hero
base=Image.new('RGB',(W,H),(12,13,32))
px=base.load()
for y in range(H):
    for x in range(W):
        t=(0.55*y/H+0.45*x/W)
        px[x,y]=(int(10+80*t), int(10+75*t), int(31+95*t))
base.save(os.path.join(BASE,'tmp_base.jpg'),quality=92)
hero(); couple_stairs(); hall(); hands(); rings()
flower('flower-blue.png','blue',620)
flower('flower-blue-small.png','blue',360)
flower('flower-white.png','white',620)
flower('flower-white-small.png','white',380)
# remove tmp
try: os.remove(os.path.join(BASE,'tmp_base.jpg'))
except FileNotFoundError: pass
