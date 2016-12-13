from PIL import Image
import numpy as np
import os


if __name__ == '__main__':

	source_im = input('Enter name of source image: ')

	col = Image.open("SourceMaps/" + source_im)
	gray = col.convert('L')

	# converting pixels to pure black or white
	bw = np.asarray(gray).copy()

	# Pixel range is 0...255, 256/2 = 128
	bw[bw < 128] = 0    # Black
	bw[bw >= 128] = 255 # White

	# Now we put it back in Pillow/PIL land
	imfile = Image.fromarray(bw)

	source_im_wo_ext = os.path.splitext(source_im)[0]
	out_im = source_im_wo_ext + "_binary.png"

	imfile.save("BinaryMaps/" + out_im)