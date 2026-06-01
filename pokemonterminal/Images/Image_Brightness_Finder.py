import cv2

# Load an image (change the path to your image)
image = cv2.imread('/home/adam/Pokemon_Images/test.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Calculate the mean pixel value
mean_brightness = gray_image.mean()

print(f'Mean Brightness: {mean_brightness}')






# def brightness('/home/adam/Pokemon_Images/test.png'):
#    im = image.open('/home/adam/Pokemon_Images/test.png')
#    stat = ImageStat.Stat(im)
#    gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) 
#          for r,g,b in im.getdata())
