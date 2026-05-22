def brightness( im_file ):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) 
         for r,g,b in im.getdata())
