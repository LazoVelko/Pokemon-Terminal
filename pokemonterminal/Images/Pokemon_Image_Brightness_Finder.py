import cv2

# Load an image (change the path to your image)
image = cv2.imread('/home/adam/Pokemon_Images/Generation VI - Kalos/0655Delphox.png')

# Convert to grayscale
grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Calculate the mean pixel value
meanBrightness = grayscaleImage.mean()

meanBrightness = meanBrightness / 255

meanBrightness = round(meanBrightness, 3) 
print(meanBrightness)
