import io
from PIL import Image
from .logger import log

class ImageProcessor:

	ALLOW_IMAGE_FORMAT = ['JPEG', 'BMP', 'PNG', 'GIF']

	def __init__(self, f):
		self._f = f
		self._img = None
		self._extension = None
		self._format = None

	@property
	def extension_name(self):
		return self._extension

	@property
	def size(self):
		if not self._load_image():
			return None
		return self._img.size

	def zoom_max_width(self, max_width):
		if not self._load_image():
			return None, None
		try:
			convert = False
			size = self._img.size
			if self._img.format != self._format:
				convert = True
			if size[0] > max_width:
				size = (max_width, self._img.size[1] * max_width / self._img.size[0])
				self._img = self._img.resize(size, Image.ANTIALIAS)
				convert = True
			if convert:
				self._f = self._create_pil_bytes_io()
				if (self._img.format == 'JPEG' or self._img.format == 'BMP') and self._img.mode != "RGB":
					self._img = self._img.convert("RGB")
				self._img.save(self._f, self._format)
			self._f.seek(0)
			return self._f, size
		except Exception as ex:
			log.exception('zoom_image_error|mode=max_width,ex=%s', ex)
			return None, None

	def zoom_fit_size(self, size, fmt=None):
		if not self._load_image():
			return None, None
		try:
			img = self._img
			src = img.size[0] * size[1]
			dest = img.size[1] * size[0]
			if src < dest:
				crop_height = img.size[0] * size[1] / size[0]
				crop_top = (img.size[1] - crop_height) / 2
				img = img.crop((0, crop_top, img.size[0], crop_top + crop_height))
			elif src > dest:
				crop_width = img.size[1] * size[0] / size[1]
				crop_left = (img.size[0] - crop_width) / 2
				img = img.crop((crop_left, 0, crop_left + crop_width, img.size[1]))
			if img.size[0] > size[0] or img.size[1] > size[1]:
				img = img.resize(size, Image.ANTIALIAS)
			elif src == dest:
				self._f.seek(0)
				return self._f, size
			f = self._create_pil_bytes_io()
			if not fmt:
				img.save(f, self._format)
			else:
				if (fmt == 'JPEG' or fmt == 'BMP') and img.mode != "RGB":
					img = img.convert("RGB")
				img.save(f, fmt)
			f.seek(0)
			return f, img.size
		except Exception as ex:
			log.exception('zoom_image_error|mode=fit_size,ex=%s', ex)
			return None, None

	def zoom_max_side_and_ratio(self, max_side, max_ratio, fmt=None):
		if not self._load_image():
			return None, None
		try:
			if max_ratio[0] < max_ratio[1]:
				max_ratio = (max_ratio[1], max_ratio[0])
			img = self._img
			size = img.size
			if size[0] >= size[1]:
				if size[0] * max_ratio[1] > size[1] * max_ratio[0]:
					size = (size[1] * max_ratio[0] / max_ratio[1], size[1])
				if size[0] > max_side:
					size = (max_side, size[1] * max_side / size[0])
			else:
				if size[1] * max_ratio[1] > size[0] * max_ratio[0]:
					size = (size[0], size[0] * max_ratio[0] / max_ratio[1])
				if size[1] > max_side:
					size = (size[0] * max_side / size[1], max_side)
		except Exception as ex:
			log.exception('zoom_image_error|mode=max_side_ratio,ex=%s', ex)
			return None, None
		return self.zoom_fit_size(size, fmt)

	def _load_image(self):
		if self._img is not None:
			return True
		try:
			self._img = Image.open(self._f)
		except Exception:
			return False
		self._format = self._img.format
		if self._format not in ImageProcessor.ALLOW_IMAGE_FORMAT:
			log.error('zoom_image_format_error|format=%s', self._format)
			return False
		if self._format == 'BMP':
			self._format = 'JPEG'
		self._extension = self._format.lower()
		if self._extension == 'jpeg':
			self._extension = 'jpg'
		return True

	def _create_pil_bytes_io(self):
		f = io.BytesIO()
		def fileno():
			raise AttributeError
		f.fileno = fileno
		return f
