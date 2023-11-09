# -*- coding: utf-8 -*-
import math
import uuid
import urllib.request, urllib.parse, urllib.error
import requests
import imghdr
from common.logger import log
from codebase_lib import config
from codebase_lib.constants import GenderType, CountryCode, ClientType
from codebase_lib.utils import get_gender_type
from codebase_lib import media_api
from codebase_lib import config

DELI_DISH_NO_IMAGE_PNG = "deli-dish-no-image.png"

class DefaultAvatarUid:
	ADMIN = 0
	GUESS = -1

class DefaultAvatartUrl:
	ADMIN = "style/images/icons/foodylogo.jpg"
	GUESS = "style/images/icons/foodylogo-id.jpg"

PLACE_BACKGROUND_NO_IMAGE_DEFAULT = 'deli-res-bg-%s-image.png'

# image sizes
IMAGE_PLAN_ACTIVITY_PLACE_SIZES = [(120, 120), (180, 180), (400, 250), (750, 424)]
IMAGE_SEARCH_PLACE_SIZES = [(80, 80), (120, 120), (160, 160), (240, 240), (400, 250), (750, 424), (750, 520), (768, 260), (828, 520), (1125, 780), (1242, 780), (1536, 520)]
IMAGE_PLAN_LIST_ITEMS_PLACE_SIZES = [(375, 150), (414, 150), (750, 300), (400, 250), (750, 424),  (768, 150), (828, 300), (1242, 450), (1536, 300)]
IMAGE_PLAN_DETAIL_PLACE_SIZES = [(0, 0), (120, 120), (240, 240), (256, 256), (375, 150), (400, 250), (414, 150), (750, 300), (750, 424), (768, 150), (828, 300), (1080, 570), (1242, 450), (1536, 300), (1536, 864)]
IMAGE_USER_AVATAR_SIZES = [(100, 100), (200, 200)]
IMAGE_PLAN_COVER_SIZES = [(0, 0), (64, 64), (400, 250), (750, 300), (750, 424), (768, 150), (828, 300), (1080, 570), (1242, 450), (1536, 300), (1536, 864)]
IMAGE_ARTICLE_AVATAR_SIZES = [(200, 0), (340, 340), (510, 510), (800, 0)]
IMAGE_ARTICLE_FB_AVATAR_SIZES = [(940, 500)]
IMAGE_BANNER_SIZES = {
	ClientType.WEB: [(1600, 500), (650, 350), (380, 260)],
	ClientType.ANDROID: [(400, 150), (800, 300), (1200, 450), (780, 180), (1560, 360)],
	ClientType.IOS: [(750, 220), (768, 200), (828, 220), (1242, 330), (1536, 400)]
}
IMAGE_REWARD_AVATAR_SIZES = [(240, 240), (320, 240), (480, 360)]
IMAGE_PLACE_DETAIL_SIZES = {
	ClientType.WEB: [(400, 250), (750, 424), (750, 600), (768, 300), (828, 600), (1125, 900), (1242, 900), (1536, 900)],
	ClientType.IOS: [(400, 250), (750, 424), (750, 600), (768, 300), (828, 600), (1125, 900), (1242, 900), (1536, 900)],
	ClientType.ANDROID: [(400, 250), (750, 424), (780, 300), (800, 500), (1200, 750), (1560, 600)]
}
IMAGE_PROPERTIES_AVATAR_SIZES = [(16, 16), (24, 24), (50, 50), (70, 70)]
IMAGE_PLACE_MAP_SIZES = [(220, 280), (400, 400), (640, 400), (1024, 768), (1280, 720)]
IMAGE_NEWS_AVATAR_SIZES = [(60, 60), (120, 120)]
IMAGE_USER_PHOTO_SIZES = [(0, 0), (64, 64), (128, 128), (256, 256), (400, 250), (750, 424), (1080, 570), (1536, 864)]

NOTIFY_AVATAR_SIZES = [(60, 60), (120, 120)]

default_image_config = {
	"name": "default_image",
	"main_folder": "default",
	"resize_size": [414, 400, 100, 70, 50],
	"crop_size": [(48, 23), (80, 80), (96, 46), (120, 120), (128, 128), (144, 69), (160, 160), (200, 200), (240, 240)
		, (400, 216), (400, 400), (600, 324), (640, 400), (640, 1136), (750, 400), (750, 424), (750, 1334), (1242, 600)
		, (1242, 2208)]

}

media_config = {
	'default_male_avatar_image': "user-default-male.png",
	'default_female_avatar_image': "user-default-female.png",
	"min_crop_width": 20,
	"min_crop_height": 20,
	"media_root_url": config.MEDIA_CONFIG['download_url'],
	"default_image": "no-image.png",
	"default_config": default_image_config
}

restaurant_config = {
	"name": "Restaurant",
	"main_folder": "res",
	# "sub_folder": "bg",
	"max_resize_width": 800,
	"max_resize_height": 800,
	"max_width_without_watermark": 600,
	"max_height_without_watermark": 600,
	"resize_size": [1242, 800, 750, 640, 450, 320, 220, 210, 140, 120, 80, 70, 60],
	"crop_size": [(1242, 2208), (750, 1334), (640, 1136), (640, 960), (1242, 600), (750, 400), (750, 350), (600, 600), (585, 585), (640, 400), (612, 612),
		(460, 300), (414, 414), (400, 400), (375, 375), (320, 200), (320, 150), (300, 300), (300, 190), (250, 250), (210, 210), (180, 180), (160, 160),
		(150, 150), (140, 140), (145, 145), (125, 125), (120, 120), (112, 112), (80, 80), (70, 70), (60, 60), (56, 56), (60, 45), (214, 214), (285, 285),
		(340, 340), (570, 570), (270, 270), (360, 360), (640, 640), (750, 750), (1242, 1242), (230, 230)]
}

place_profile_config = {
	"name": "PlaceProfile",
	"main_folder": "res",
	"sub_folder": "prof",
	"max_resize_width": 1600,
	"max_resize_height": 1600,
	"max_width_without_watermark": 800,
	"max_height_without_watermark": 800,
	"resize_size": [640, 414, 300, 210, 200, 220, 160, 140, 120, 80, 70, 60, 50],
	"crop_size": [(1242, 600), (750, 400), (750, 424), (640, 400), (612, 612), (600, 290), (600, 324), (460, 300), (414, 414), (400, 250), (400, 216), (375, 375),
		(340, 255), (320, 150), (320, 200), (300, 145), (256, 160), (240, 240), (210, 210), (200, 125), (180, 180), (160, 160), (150, 95),
		(140, 140), (128, 80), (120, 120), (100, 100), (460, 300), (320, 150), (70, 70), (60, 60), (80, 80), (40, 40), (290, 220),
		(345, 220), (576, 330), (375, 150), (414, 150), (750, 300),  (768, 150), (828, 300), (1242, 450), (1536, 300)]
}

place_background_config = {
	"name": "RestaurantBackground",
	"main_folder": "res",
	"sub_folder": "bg",
	"max_resize_width": 800,
	"max_resize_height": 800,
	"resize_size": [1000, 800],
	"crop_size": [(1242, 600), (750, 400), (640, 400), (600, 600), (600, 324), (400, 216), (240, 240), (160, 160), (90, 90), (60, 60)]
}

default_avatar_config = {
	"name": "DefaultAvatar",
	"main_folder": "defaultavatar",
	"max_resize_width": 200,
	"max_resize_height": 200,
	"resize_size": [200, 140, 100, 80, 70, 65, 60, 50, 30, 40],
	"crop_size": [(200, 200), (140, 140), (100, 100), (80, 80), (70, 70), (65, 65), (60, 60), (50, 50), (30, 30), (40, 40)]
}
_avatar_config = {
	"name": "Avatar",
	"main_folder": "usr",
	"sub_folder": "avt",
	"max_resize_width": 200,
	"max_resize_height": 200,
	"resize_size": [200, 140, 100, 80, 70, 65, 60, 50, 30, 40],
	"crop_size": [(200, 200), (140, 140), (100, 100), (80, 80), (70, 70), (65, 65), (60, 60), (50, 50), (30, 30), (40, 40)]
}

user_cover_config = {
	"name": "UserCover",
	"main_folder": "usr",
	"sub_folder": "cover",
	"resize_size": [750, 768, 828, 1080, 1242, 1536],
	"crop_size": [(0, 0), (400, 250), (750, 300), (750, 424), (768, 150), (828, 300), (1080, 570), (1242, 450), (1536, 300)]
}

order_photo_config = {
	"name": "OrderPhoto",
	"main_folder": "Delivery",
	"sub_folder": "order",
	"size_folder_prefix": "s",
	"application": "beauty",
	"valid_image_type": ["jpeg", "png", "gif"],
	"auto_correct_orientation": True,
	"crop_size": [(214, 214), (70, 70), (414, 414), (600, 600)]
}
collection_config = {
	"name": "DeliveryCollection",
	"main_folder": "Delivery",
	"sub_folder": "Collection",
	"size_folder_prefix": "s",
	"resize_size": [300, 450],
	"crop_size": [(300, 200), (450, 300)]
}

images_config = {
	"name": "images",
	"main_folder": "images",
	"sub_folder": "",
}

old_blog_image_config = {
	"name": "images",
	"main_folder": "images",
	"sub_folder": "blogs",
}

plan_cover_config = {
	"name": "plan_cover",
	"main_folder": "plan",
	"sub_folder": "cover",
	# "max_resize_width": 200,
	# "max_resize_height": 200,
	# "resize_size": [200, 140, 100, 80, 70, 65, 60, 50, 30, 40],
	# "crop_size": [(200, 200), (140, 140), (100, 100), (80, 80), (70, 70), (65, 65), (60, 60), (50, 50), (30, 30), (40, 40)]
}

tour_image_config = {
	"name": "tour_images",
	"main_folder": "tour",
	"sub_folder": "content"
}

place_map_image_config = {
	"name": "place_map",
	"main_folder": "res",
	"sub_folder": "map"
}

place_property_config = {
	"name": "hotel_property_images",
	"main_folder": "hotel",
	"sub_folder": "property"
}

tour_image_config = {
	"name": "tour_images",
	"main_folder": "tour",
	"sub_folder": "content"
}

user_photo_config = {
	"name": "tour_picture",
	"main_folder": "upload_photos",
	"sub_folder": ""
}

class ImageLoader(object):
	MEDIA_AVATAR_DEFAULT_CROP_SIZE = 200
	MEDIA_SETTINGS_STATIC_PATH = '/'

	def __init__(self, media_config, image_config):
		self.media_config = media_config
		self.image_config = image_config

	def _get_size_folder(self, folder_prefix, path_char="\\", width=0, height=0):
		size_folder = ""
		if width > 0:
			if height > 0:
				size_folder = "%s%sx%s" % (folder_prefix, width, height)
			else:
				size_folder = "%s%s" % (folder_prefix, width)
		else:
			if folder_prefix == self.image_config.get("size_folder_config", "s"):
				if self.image_config.get("gen_normal_folder", True):
					size_folder = folder_prefix
			else:
				size_folder = folder_prefix
		return path_char.join([self.image_config.get('sub_folder', ""), size_folder]).strip(path_char)

	def _is_valid_crop_size(self, width, height):
		if self.image_config['name'] == self.media_config["default_config"]["name"]:
			if 10 <= width <= self.image_config.get('max_resize_width', 1024) and 10 <= height <= self.image_config.get("max_resize_height", 1024):
				return True
		for (w, h) in self.image_config.get("crop_size", []):
			if width == w and height == h:
				return True
		return False

	def _is_valid_resize_size(self, width):
		if self.image_config['name'] == self.media_config["default_config"]["name"]:
			if 10 <= width <= self.image_config.get('max_resize_width', 1024):
				return True
		for w in self.image_config.get("resize_size", []):
			if w == width:
				return True
		return False

	def _get_nearest_valid_crop_size(self, width):
		result = (self.media_config.get('min_crop_width', 20), self.media_config.get('min_crop_height', 20))
		min_delta = 9999
		for (w, h) in self.image_config.get("crop_size", []):
			delta = w - width
			abs_delta = delta if delta >= 0 else (abs(delta) * 2)
			if abs_delta < min_delta:
				min_delta = abs_delta
				result = (w, h)
		return result

	def _get_nearest_valid_resize(self, width):
		result = self.media_config.get("min_resize_width", 20)
		min_delta = 9999
		for w in self.image_config.get("resize_size", []):
			delta = w - width
			abs_delta = delta if delta >= 0 else (abs(delta) * 2)
			if abs_delta < min_delta:
				result = w
				min_delta = abs_delta
		return result

	@staticmethod
	def _remove_double_char(source, c):
		if not source:
			return ""
		return source.replace(c, "ᵔᵕ").replace("ᵕᵔ", "").replace("ᵔᵕ", c)

	def _combine_url(self, *paths):
		root_path = [path for path in paths if "://" in path]
		if not root_path:
			root_path = [path for path in paths if path.startswith('//')]
		root_path = root_path[0] if root_path else None

		result = "/".join([path for path in paths if path and path != root_path])
		result = result.replace("\\", "/")
		result = self._remove_double_char(result, "/")

		if root_path:
			root_path = root_path.strip("/")
			result = "/".join([root_path, result])
		return result

	def _id_to_folder_name(self, id, path_char="\\"):
		group_number = int(math.ceil(float(id) / self.media_config.get("max_folder_item", 10000)))
		return "g%s%s%s" % (group_number, path_char, id)

	def _get_default_image(self, width=0, height=0):
		image_loader = ImageLoader(self.media_config, self.media_config["default_config"])
		default_file_name = self.image_config.get("default_image", None)
		if not default_file_name:
			default_file_name = self.media_config.get("default_image", "")
		return image_loader.get_image_url(None, default_file_name, width, height)

	def get_image_url(self, id, file_name, width, height):
		if not file_name:
			return ""
		if file_name.lower().startswith('http://') or file_name.lower().startswith(
				'https://') or file_name.lower().startswith('//'):
			return file_name
		# file_name = file_name.encode('utf8') 	# fix unicode file name
		# file_name = urllib.quote(file_name)
		size_folder = ""

		if width == 0 and height == 0:
			size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/")
		elif width > 0:
			if height > 0:
				# if not self._is_valid_crop_size(width, height):
				# 	if self.image_config.get("rewrite_invalid_size_to_nearest_valid_size", True):
				# 		width, height = self._get_nearest_valid_crop_size(width)
				# 	else:
				# 		return ""
				size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/", width, height)
			else:
				# if not self._is_valid_resize_size(width):
				# 	if self.image_config.get("rewrite_invalid_size_to_nearest_valid_size", True):
				# 		width = self._get_nearest_valid_resize(width)
				# 	else:
				# 		return ""
				size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/", width)
		if size_folder:
			if id is not None:
				return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), self._id_to_folder_name(id, "/"), size_folder, file_name).lower()
			return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), size_folder, file_name).lower()
		else:
			if not self.image_config.get("gen_normal_folder", True):
				return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), self.image_config.get("sub_folder", ""), file_name).lower()
		return self._get_default_image(width, height)

	def _is_system_default_avatar(self, file_name):
		return file_name and file_name.lower().startswith("default-avatar")

	def _get_default_avatar_url(self, gender_type, width):
		default_file_name = self.media_config['default_male_avatar_image'] if gender_type == GenderType.MALE else self.media_config['default_female_avatar_image']
		self.image_config = default_image_config
		return self.get_image_url(None, default_file_name, width, 0)

	def _get_system_default_avatar_url(self, file_name, width=0, gender_type=GenderType.FEMALE):
		height = 0
		self.image_config = default_avatar_config
		result = self.get_image_url(None, file_name, width, height)
		if not result or result.strip() == '':
			result = self._get_default_avatar_url(gender_type, width)
		return result

	def _get_customize_avatar_url(self, uid, avatar, gender_type, width, height):
		# if self._is_system_default_avatar(avatar):
		# 	return self._get_system_default_avatar_url(avatar, width, gender_type)
		# if uid == DefaultAvatarUid.GUESS:  #guess
		# 	return '%s%s' % (self.MEDIA_SETTINGS_STATIC_PATH, DefaultAvatartUrl.GUESS)
		# elif uid == DefaultAvatarUid.ADMIN:  #admin
		# 	if config.COUNTRY == CountryCode.VIETNAM:
		# 		return '%s%s' % (self.MEDIA_SETTINGS_STATIC_PATH, DefaultAvatartUrl.ADMIN)
		# 	else:
		# 		return '%s%s' % (self.MEDIA_SETTINGS_STATIC_PATH, DefaultAvatartUrl.GUESS)
		# else:
		result = self.get_image_url(uid, avatar, width, height)
		if result == '':
			result = self._get_default_avatar_url(gender_type, width)
		return result

	def _get_cropped_avatar_url(self, uid, avatar, gender_type, target_size=0):
		if target_size <= 0:
			target_size = self.MEDIA_AVATAR_DEFAULT_CROP_SIZE
		return self._get_customize_avatar_url(uid, avatar, gender_type, target_size, target_size)

	def get_avatar_user(self, uid, avatar, gender, target_size):
		gender_type = get_gender_type(gender)
		return self._get_cropped_avatar_url(uid, avatar, gender_type, target_size)

	def get_place_image_url(self, place_id, file_name, width, height):
		if not file_name:
			return ""
		if file_name.lower().startswith('http://') or file_name.lower().startswith('https://') or file_name.lower().startswith('//'):
			return file_name

		file_name = file_name.encode('utf8') 	# fix unicode file name
		file_name = urllib.parse.quote(file_name)
		size_folder = ""

		if width == 0 and height == 0:
			size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/")
		elif width > 0:
			if height > 0:
				# accept any size (width, height)
				size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/", width, height)
			else:
				if not self._is_valid_resize_size(width):
					if self.image_config.get("rewrite_invalid_size_to_nearest_valid_size", True):
						width = self._get_nearest_valid_resize(width)
					else:
						return ""
				size_folder = self._get_size_folder(self.image_config.get("size_folder_prefix", "s"), "/", width)
		if size_folder:
			if place_id is not None:
				return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), self._id_to_folder_name(place_id, "/"), size_folder, file_name).lower()
			return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), size_folder, file_name).lower()
		else:
			if not self.image_config.get("gen_normal_folder", True):
				return self._combine_url(self.media_config.get("media_root_url", ""), self.image_config.get("main_folder", ""), self.image_config.get("sub_folder", ""), file_name).lower()
		return self._get_default_image(width, height)

_default_image_loader = ImageLoader(media_config, default_image_config)
_place_profile_image_loader = ImageLoader(media_config, place_profile_config)

def get_place_profile_image_url(place_id, file_name, width, height):
	if file_name:
		return _place_profile_image_loader.get_image_url(place_id, file_name, width, height)
	else:
		return _default_image_loader.get_image_url(None, PLACE_BACKGROUND_NO_IMAGE_DEFAULT, width, height)

def get_place_image(place_id, file_name, width, height):
	if file_name:
		return _place_profile_image_loader.get_place_image_url(place_id, file_name, width, height)
	else:
		# hien tai chua co anh default cho place
		return _default_image_loader.get_image_url(None, PLACE_BACKGROUND_NO_IMAGE_DEFAULT, width, height)

_place_background_image_loader = ImageLoader(media_config, place_background_config)

def get_place_background_image_url(file_name, width, height):
	if file_name:
		return _place_background_image_loader.get_image_url(None, file_name, width, height)
	else:
		return _default_image_loader.get_image_url(None, PLACE_BACKGROUND_NO_IMAGE_DEFAULT, width, height)

_avatar_image_loader = ImageLoader(media_config, _avatar_config)

def get_user_avatar_url(uid=None, avatar=None, gender=None, target_size=0):
	return _avatar_image_loader.get_avatar_user(uid, avatar, gender, target_size)

_place_image_loader = ImageLoader(media_config, restaurant_config)

def get_place_mobile_img(restaurant_id, file_name, width, height):
	if file_name:
		return _place_image_loader.get_image_url(restaurant_id, file_name, width, height)
	else:
		file_name = DELI_DISH_NO_IMAGE_PNG
		return _default_image_loader.get_image_url(None, file_name, width, height)

_order_photo_loader = ImageLoader(media_config, order_photo_config)
def get_order_images(order_id, file_name, current_width, current_height):
	images = []
	for size_width, size_height in order_photo_config["crop_size"]:
		value_photo = _order_photo_loader.get_image_url(order_id, file_name, size_width, size_height) if order_id \
			else _order_photo_loader.get_image_url(None, file_name, size_width, size_height)
		if size_width > 0:
			image = {
				"width": size_width,
				"height": size_height,
				"value": value_photo
			}
			if size_height == 0 and current_height > 0 and current_width > 0:
				image["height"] = int(math.trunc(current_height * size_width) / current_width)
			images.append(image)
		else:
			images.append({
				"width": size_width,
				"height": size_height,
				"value": value_photo
			})
	return images

_collection_loader = ImageLoader(media_config, collection_config)
def get_collection_image(file_name, width, height):
	if file_name:
		return _collection_loader.get_image_url(None, file_name, width, height)
	else:
		file_name = DELI_DISH_NO_IMAGE_PNG
		return _collection_loader.get_image_url(None, file_name, width, height)

def get_social_image_as_avatar(uid, image_url):
	# get image to memory (assume image has small size)
	try:
		res = requests.get(image_url, stream=False)
		res.raise_for_status()
		file_data = res.content
	except Exception as ex:
		log.exception("get_social_image_as_avatar|error=fail_to_get_image_from_source,image_url=%s", image_url)
		return None, ex

	# upload to media
	try:
		# check image type
		image_type = _get_image_type(file_data)

		if image_type not in config.VALID_IMAGE_TYPE:
			log.warn("avatar_image_type_invalid|uid=%s,image_type=%s", uid, image_type)
			return None, 'avatar_image_type_invalid'

		if image_type == "jpeg":
			image_type = "jpg"
		file_name = "usr-avt-%s.%s" % (uuid.uuid4(), image_type)

		# maybe resize to a reasonable size before uploading is better?

		file_name = media_api.upload_file(media_folder=_avatar_config["main_folder"], sub_folder=_avatar_config["sub_folder"],file_data=file_data,file_name=file_name, object_id=uid,
										user_id=uid, os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_avatar_to_media_fail|uid=%s, file_name=%s", uid, file_name)
			return None, 'upload_avatar_to_media_fail'

		return file_name, None

	except Exception as error:
		log.exception("upload_avatar_exception|uid=%s,error=%s", uid, error)
		return None, error

def upload_user_avatar(uid, image_type, file_data):
	try:
		file_name = "usr-avt-%s.%s" % (uuid.uuid1().hex, image_type)
		file_name = media_api.upload_file(media_folder=_avatar_config["main_folder"], sub_folder=_avatar_config["sub_folder"],file_data=file_data,file_name=file_name, object_id=uid,
										user_id=uid, os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_avatar_to_media_fail|uid=%s, file_name=%s", uid, file_name)
			return None
		return file_name
	except Exception as error:
		log.exception("upload_avatar_exception|uid=%s,error=%s", uid, error)
		return None

def _test_jpeg(file_data):
	if file_data[:2] == b'\xff\xd8':
		return "jpeg"
	return None

def _get_image_type(file_data):
	try:
		image_type = imghdr.what(None, file_data)
		if image_type is None:
			image_type = _test_jpeg(file_data)
		return image_type
	except:
		log.exception("get_image_type_fail")
	return ""

def delete_user_avatar_file(uid, file_name):
	return media_api.remove_file(
						media_folder=_avatar_config["main_folder"],
						sub_folder=_avatar_config["sub_folder"],
						file_name=file_name,
						object_id=uid,
						user_id=uid,
						os='py_server',
						app_id=1)

def get_image_type(filename):
	if '.' not in filename:
		return None
	image_type = filename.rsplit('.', 1)[1].lower()
	if image_type not in config.VALID_IMAGE_TYPE:
		return None
	return image_type

_plan_cover_loader = ImageLoader(media_config, plan_cover_config)


def upload_plan_cover(plan_id, uid, image_type, file_data):
	try:
		file_name = "plan-cover-%s.%s" % (uuid.uuid1().hex, image_type)
		file_name = media_api.upload_file(media_folder=plan_cover_config["main_folder"], sub_folder=plan_cover_config["sub_folder"], file_data=file_data, file_name=file_name, object_id=plan_id,
										user_id=uid, os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_plan_cover_to_media_fail|plan_id=%s,uid=%s,file_name=%s", plan_id, uid, file_name)
			return None
		return file_name
	except Exception as error:
		log.exception("upload_plan_cover_exception|plan_id=%s,uid=%s,error=%s", plan_id, uid, error)
		return None


def get_plan_cover(plan_id, file_name, width, height):
	if file_name:
		return _plan_cover_loader.get_image_url(plan_id, file_name, width, height)
	else:
		return _default_image_loader.get_image_url(None, PLACE_BACKGROUND_NO_IMAGE_DEFAULT, width, height)


def delete_plan_cover_file(plan_id, uid, file_name):
	return media_api.remove_file(
						media_folder=plan_cover_config["main_folder"],
						sub_folder=plan_cover_config["sub_folder"],
						file_name=file_name,
						object_id=plan_id,
						user_id=uid,
						os='py_server',
						app_id=1)

def upload_place_avatar(file_data, place_id, image_type):
	return _process_upload_place_photo(file_data, place_id, image_type)

def upload_place_photo(file_data, place_id):
	# upload to media
	try:
		# check image type
		image_type = _get_image_type(file_data)
		if image_type not in config.VALID_IMAGE_TYPE:
			log.warn("image_type_invalid|place_id=%s,image_type=%s", place_id, image_type)
			return None
		return _process_upload_place_photo(file_data, place_id, image_type)
	except Exception as error:
		log.exception("upload_place_photo_exception|place_id=%s,error=%s", place_id, error)
		return None

def _process_upload_place_photo(file_data, place_id, image_type):
	if image_type == "jpeg":
		image_type = "jpg"
	file_name = "place-img-%s.%s" % (uuid.uuid1().hex, image_type)

	# maybe resize to a reasonable size before uploading is better?

	file_name = media_api.upload_file(media_folder=place_profile_config["main_folder"], sub_folder=place_profile_config["sub_folder"],file_data=file_data,file_name=file_name, object_id=place_id,
									user_id=0, os='py_server', app_id=1)
	if not file_name:
		log.warn("upload_place_photo_to_media_fail|place_id=%s, file_name=%s", place_id, file_name)
		return None
	return file_name

def get_google_static_map_file_name(place_id, lat, lng):
	# get image to memory (assume image has small size)
	try:
		request_url = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&key={key}&size={w}x{h}&format=jpg&markers=color:red|label:C|{lat},{lng}&scale=2"
		request_url = request_url.format(lat=lat, lng=lng, key=config.GOOGLE_API_KEYS['PLACE_API_KEY'], w=1280, h=1280)
		res = requests.get(request_url, stream=False)
		res.raise_for_status()
		file_data = res.content
	except Exception as ex:
		log.exception("get_google_static_map|error=fail_to_get_image_from_source,image_url=%s|%s", request_url, ex)
		return None, ex
	# upload to media
	try:
		# check image type
		image_type = _get_image_type(file_data)
		if image_type not in config.VALID_IMAGE_TYPE:
			log.warn("avatar_image_type_invalid|place_id=%s,image_type=%s", place_id, image_type)
			return None, "avatar_image_type_invalid"
		if image_type == "jpeg":
			image_type = "jpg"
		file_name = "place-map-%s.%s" % (uuid.uuid4(), image_type)
		file_name = media_api.upload_file(media_folder=place_map_image_config["main_folder"], sub_folder=place_map_image_config["sub_folder"], file_data=file_data,file_name=file_name, object_id=place_id,os='py_server', app_id=1)
		if not file_name:
			log.warn("get_google_static_map_failed|place_id=%s, file_name=%s", place_id, file_name)
			return None, "get_google_static_map_failed"
		return file_name, None
	except Exception as error:
		log.exception("get_google_static_map_exception|place_id=%s,error=%s", place_id, error)
		return None, error

_image_loader = ImageLoader(media_config, images_config)
def get_image(file_name, width, height):
	return _image_loader.get_image_url(id=None, file_name=file_name, width=width, height=height)

_old_blog_image_config = ImageLoader(media_config, old_blog_image_config)
def get_old_blog_image(file_name):
	return _old_blog_image_config.get_image_url(id=None, file_name=file_name, width=0, height=0)

_tour_content_loader = ImageLoader(media_config, tour_image_config)
def get_tour_content_image(file_name, width, height):
	return _tour_content_loader.get_image_url(None, file_name, width, height)

_place_map_image_loader = ImageLoader(media_config, place_map_image_config)
def get_place_map_image(place_id, file_name, width, height):
	return _place_map_image_loader.get_image_url(place_id, file_name, width, height)

_place_property_image_loader = ImageLoader(media_config, place_property_config)
def get_place_property_image(file_name, width, height):
	return _place_property_image_loader.get_image_url(None, file_name, width, height)

def upload_user_cover(uid, image_type, file_data):
	try:
		file_name = "u-cover-%s.%s" % (uuid.uuid1().hex, image_type)
		file_name = media_api.upload_file(media_folder=user_cover_config["main_folder"], sub_folder=user_cover_config["sub_folder"], file_data=file_data, file_name=file_name, object_id=uid,
										user_id=uid, os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_user_cover_to_media_fail|uid=%s,file_name=%s", uid, file_name)
			return None
		return file_name
	except Exception as error:
		log.exception("upload_user_cover_exception|uid=%s,error=%s", uid, error)
		return None

def remove_user_cover(uid, file_name):
	try:
		rs = media_api.remove_file(media_folder=user_cover_config["main_folder"], sub_folder=user_cover_config["sub_folder"], file_name=file_name, object_id=uid, user_id=uid, os='py_server', app_id=1)
		if not rs:
			log.warn("cannot_remove_old_user_cover|uid=%s, file_name=%s", uid, file_name);
	except Exception as ex:
		log.exception("exception_while_remove_user_cover|uid=%s, file_name=%s", uid, file_name)

_user_cover_loader = ImageLoader(media_config, user_cover_config)
def get_user_cover_url(uid, file_name, width, height):
	if file_name:
		return _user_cover_loader.get_image_url(uid, file_name, width, height)
	else:
		return None

def remove_user_photo(uid, photo_id, file_name):
	"""
		remove photos that user upload for metrip
	"""
	try:
		rs = media_api.remove_file(
			media_folder=user_photo_config["main_folder"],
			sub_folder=user_photo_config["sub_folder"],
			file_name=file_name,
			object_id=photo_id,
			user_id=uid,
			os='py_server',
			app_id=1)
		if not rs:
			log.warn("cannot_remove_user_photo|uid=%s, file_name=%s", uid, file_name)
	except Exception as ex:
		log.exception("exception_while_remove_user_photo|uid=%s, file_name=%s", uid, file_name)

def user_upload_photo(file_name, photo_id, uid, image_type, file_data):
	"""
		user upload photos for trip
	"""
	try:
		file_name = media_api.upload_file(
			media_folder=user_photo_config["main_folder"],
			sub_folder=user_photo_config["sub_folder"],
			file_data=file_data, file_name=file_name,
			object_id=photo_id, user_id=uid,
			os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_user_photo_media_failed|plan_id=%s,uid=%s,file_name=%s", photo_id, uid, file_name)
			return None
		return file_name
	except Exception as error:
		log.exception("upload_user_photo_media_exception|plan_id=%s,uid=%s,error=%s", photo_id, uid, error)
		return None

_user_photo_loader = ImageLoader(media_config, user_photo_config)
def get_user_photo_url(photo_id, file_name, width, height):
	if file_name:
		return _user_photo_loader.get_image_url(photo_id, file_name, width, height)
	else:
		return None

def get_image_sizes(sizes):
	"""
	parse client photo sizes for api request
	"""
	result = []
	for size in sizes:
		result.append((size.get("width", 0), size.get("height", 0)))
	return result

def get_default_image(file_name, width, height, object_id=None):
	return _default_image_loader.get_image_url(object_id, file_name, width, height)

def upload_default_image(file_name, file_data):
	try:
		file_name = media_api.upload_file(
			media_folder=default_image_config["main_folder"],
			sub_folder="",
			file_data=file_data, file_name=file_name,
			object_id=None,
			os='py_server', app_id=1)
		if not file_name:
			log.warn("upload_default_image_media_failed|file_name=%s", file_name)
			return None
		return file_name
	except Exception as error:
		log.exception("upload_default_image_media_exception|error=%s", error)
		return None
