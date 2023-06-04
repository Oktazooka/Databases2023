from randimage import get_random_image
import matplotlib

img_size = (200, 200)

for i in range (100):
  fname = "img" + str(i)+".png"
  img = get_random_image(img_size)
  matplotlib.image.imsave(fname, img)
