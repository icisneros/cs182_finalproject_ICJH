from PIL import Image
import numpy as np


if __name__ == '__main__':

	col = Image.open("SourceMaps/MD_0.png")
	gray = col.convert('L')

	# converting pixels to pure black or white
	bw = np.asarray(gray).copy()

	# Pixel range is 0...255, 256/2 = 128
	bw[bw < 128] = 0    # Black
	bw[bw >= 128] = 255 # White

	# Now we put it back in Pillow/PIL land
	imfile = Image.fromarray(bw)
	imfile.save("BinaryMaps/MD_1_bw.png")