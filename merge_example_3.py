from PIL import Image

def h(im1, im2):
	dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (im1.width, 0))
	return dst

def v(im1, im2):
	dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (0, im1.height))
	return dst

def o(key):
	fname = f'examples/example_3{key}.png'
	return Image.open(fname)

a = o('a')
b = o('b')
c = o('c')
d = o('d')
e = o('e')
f = o('f')

ab = v(a, b)
abc = v(ab, c)
de = h(d, e)
abcdef = v(abc, h(de, f))
abcdef.save('examples/example_3.png')