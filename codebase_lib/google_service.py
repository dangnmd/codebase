import googlemaps
from common.utils import log, get_timestamp_ms, to_str
import requests
from codebase_lib.constants import GooglePlaceSortType, Result
# from codebase_lib.managers import setting_manager
# import time
# import random
# import simplejson

DETAILS_FIELDS = [
	'place_id', 'name', 'formatted_address', 'geometry', 'formatted_phone_number', 'photo',
	'international_phone_number', 'opening_hours', 'address_component', 'website', 'type', 'rating'
]


class GoogleMapClient(object):

	def __init__(self, config):
		self.__config = config
		self.__place_api = None
		self.__route_api = None
		self.__error_handle_func = config.get('ERROR_HANDLE_FUNC')

	@property
	def place_api(self):
		if self.__place_api is None:
			self.__place_api = googlemaps.Client(
				key=to_str(self.__config['PLACE_API_KEY']),
				timeout=self.__config['TIMEOUT']
			)
		return self.__place_api

	@property
	def route_api(self):
		if self.__route_api is None:
			self.__route_api = googlemaps.Client(
				key=to_str(self.__config['ROUTE_API_KEY']),
				timeout=self.__config['TIMEOUT']
			)
		return self.__route_api

	def _handle_error(self, google_key, error):
		if self.__error_handle_func:
			self.__error_handle_func(google_key, error)

	def get_place_details(self, place_id, fields=None, language=None):
		if not fields:
			fields = DETAILS_FIELDS
		try:
			# log.info('google_map_request|start,place=%s', place_id)
			start_time = get_timestamp_ms()
			reply = self.place_api.place(place_id, fields=fields, language=language)
			elapsed = get_timestamp_ms() - start_time
			if reply['status'] != 'OK':
				log.warn('google_map_request|place_details|elapsed=%s,failed,place=%s,status=%s', elapsed, place_id, reply['status'])
				return None, reply['status']
			log.info('google_map_request|place_details|elapsed=%s, success,place=%s', elapsed, place_id)
			return reply['result'], None
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
			return None, Result.ERROR_GOOGLE_SEARCH_EXCEED_QUOTA
		except Exception as error:
			log.exception('google_map_request|place_details|place=%s,fields=%s,error=%s', place_id, fields, error)
			return None, error
		return reply, None

	def get_distance(self, src_location, dst_location):
		"""
			Get distance between 2 locations in met
			:param src_location: (lat, lng)
			:param dst_location: (lat, lng)
		"""
		response = {
			"transport_distance": 0,		# unit met
			"transport_time": 0				# unit minute
		}

		if not src_location or not dst_location:
			return response, 'invalid locations'
		try:
			google_response = self.route_api.distance_matrix([src_location], [dst_location], mode="driving", units="metric")
			rows = google_response.get('rows', [])
			if rows:
				elements = rows[0]['elements']
				if elements:
					element = elements[0]
					# -----------------------------
					# case failure
					# -----------------------------
					if element['status'] != 'OK':
						log.exception('google_map_request_distance_failed|src_location=%s|dst_location=%s', src_location, dst_location)
						return None, element['status']
					else:
						# google response: distance (m), duration (second)
						# => convert second to minute
						response["transport_distance"] = float(element['distance']['value'])
						transport_time = float(element['duration']['value']) / 60
						transport_time = int(round(transport_time))
						response["transport_time"] = transport_time
		except Exception as ex:
			log.exception('google_map_request_distance_failed|src_location=%s|dst_location=%s', src_location, dst_location)
			# self._handle_error(error)
			return None, ex
		return response, None

	def get_place_photo(self, photo_reference, max_width, max_height=None):
		try:
			if not (max_width or max_height):
				raise ValueError("a max_width or max_height arg is required")
			params = {
				"key": self.__config['PLACE_API_KEY'],
				"photoreference": photo_reference
			}
			if max_width:
				params["maxwidth"] = max_width
			if max_height:
				params["maxheight"] = max_height
			response = requests.request('GET', 'https://maps.googleapis.com/maps/api/place/photo', params=params, stream=True)
			if response.status_code == 403:
				raise Exception("quota_exceeded,url=%s" % response.url)
			image_data = response.iter_content(self.__config['CHUNK_SIZE'])
			# image_data = self.place_api.places_photo(photo_reference, max_width=max_width)
			return image_data, None
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
			return None, Result.ERROR_GOOGLE_SEARCH_EXCEED_QUOTA
		except Exception as error:
			log.exception('google_map_request_photo_failed|photo_reference=%s,max_width=%s,error=%s', photo_reference, max_width, error)
			# self._handle_error(error)
			return None, error

	def reverse_geocode(self, latlng, result_type=None):
		"""
		:param latlng: (lat, lng)
		:param result_type: None to get all, or list string ["country", "locality", "administrative_area_level_1", ...]
		"""
		try:
			log.info('google_reverse_geocode|start,latlng=%s,result_type=%s', latlng, result_type)
			reply = self.place_api.reverse_geocode(latlng, result_type=result_type)
			if not reply:
				log.warn('google_reverse_geocode|failed,latlng=%s,result_type=%s,status=%s', latlng, result_type, 'empty_reply')
				return None, 'empty_reply'
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
		except Exception as error:
			log.exception('google_reverse_geocode|failed,latlng=%s,result_type=%s,error=%s', latlng, result_type, error)
			# self._handle_error(error)
			return None, error
		log.info('google_reverse_geocode|success,latlng=%s', latlng)
		return reply, None

	def __get_gplaces(self, gg_place_data, field_address_name):
		gplaces = []
		for gg_place in gg_place_data:
			try:
				place_info = {
					"gplace_id": gg_place["place_id"],
					"gplace_name": gg_place["name"],
					"gplace_address": gg_place.get(field_address_name, ""),
					"gplace_position": {
						"lat": gg_place["geometry"]["location"]["lat"],
						"lng": gg_place["geometry"]["location"]["lng"]
					},
					"gplace_types": gg_place.get("types", [])
				}
				if "rating" in gg_place:
					place_info["rating"] = gg_place["rating"]
				gplaces.append(place_info)
			except Exception as error:
				log.exception("error_while_parse_google_place_info|error=%s,gg_place=%s", error, gg_place)
				# self._handle_error(error)
		return gplaces

	def search_nearby(self, language, position, radius, google_categories, sort_type, exclude_gplaces_id, next_page_token=None):
		try:
			# -------------------------------------------------
			# prepare data
			# -------------------------------------------------
			params = {
				"location": (position['lat'], position['lng']),
				"radius": radius,
				"language": language
			}
			if sort_type == GooglePlaceSortType.DISTANCE:
				params["rank_by"] = "distance"
				params.pop("radius", None)		# remove radius if sort by distance
			if google_categories:
				params["type"] = google_categories[0]		# get first by top priority
			else:
				params["type"] = "point_of_interest"
			if next_page_token:
				params["page_token"] = next_page_token
			# -------------------------------------------------
			# search
			# -------------------------------------------------
			start = get_timestamp_ms()
			gg_response = self.place_api.places_nearby(**params)
			end = get_timestamp_ms()
			elapsed = int((end - start) * 1000)
			log.info('google_search_nearby_elapse=%d', elapsed)
			# -------------------------------------------------
			# validate response
			# -------------------------------------------------
			if not gg_response:
				log.warn("google_place_search_failed|gg_response_is_none")
				return None, Result.ERROR_GOOGLE_SEARCH
			if gg_response['status'] != 'OK':
				result = gg_response['status']
				log.warn('google_place_search_failed|status=%s', result)
				if result == 'ZERO_RESULTS':
					return None, Result.ERROR_GOOGLE_SEARCH_NOT_FOUND
				return None, Result.ERROR_GOOGLE_SEARCH
			# -------------------------------------------------
			# response
			# -------------------------------------------------
			reply = {
				"gplaces": self.__get_gplaces(gg_response["results"], "vicinity")
			}
			if not reply['gplaces']:
				log.warn('google_search_place|exclude_places')
				return None, Result.ERROR_GOOGLE_SEARCH_NOT_FOUND
			result = []
			for gplace in reply['gplaces']:
				if gplace['gplace_id'] not in exclude_gplaces_id:
					result.append(gplace)
			reply['gplaces'] = result		# return all results from google (20 results)
			if "next_page_token" in gg_response:
				reply["next_page_token"] = gg_response["next_page_token"]
			return reply, None
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
			return None, Result.ERROR_GOOGLE_SEARCH_EXCEED_QUOTA
		except Exception as error:
			log.exception('google_place_search_failed|error=%s|language=%s,position=%s,radius=%s,google_categories=%s,sort_type=%s,exclude_gplaces_id=%s', error, language, position, radius, google_categories, sort_type, exclude_gplaces_id)
			# self._handle_error(error)
			return None, Result.ERROR_GOOGLE_SEARCH

	def search_place(self, keyword, language, position, radius, place_type, next_page_token):
		try:
			# --------------------------
			# prepare params
			# --------------------------
			params = {
				"query": keyword,
				"language": language
			}
			if position:
				params["location"] = (position['lat'], position['lng'])
			if radius:
				params["radius"] = radius
			if place_type:
				params["type"] = place_type
			if next_page_token:
				params["page_token"] = next_page_token
			# --------------------------
			# search
			# --------------------------
			start = get_timestamp_ms()
			gg_response = self.place_api.places(**params)		# `text_search` is better than `find_place`
			end = get_timestamp_ms()
			elapsed = int((end - start) * 1000)
			log.info('google_search_place_elapse=%d', elapsed)
			# --------------------------
			# response
			# --------------------------
			reply = {
				"gplaces": self.__get_gplaces(gg_response["results"], "formatted_address")
			}
			if gg_response.get("next_page_token"):
				reply["next_page_token"] = gg_response["next_page_token"]
			if not reply['gplaces']:
				return None, Result.ERROR_GOOGLE_SEARCH_NOT_FOUND
			return reply, None
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
			return None, Result.ERROR_GOOGLE_SEARCH_EXCEED_QUOTA
		except Exception as error:
			log.exception('google_place_search_error|error=%s|keyword=%s,language=%s,position=%s,radius=%s,place_type=%s', error, keyword, language, position, radius, place_type)
			return None, Result.ERROR_GOOGLE_SEARCH

	def search_auto_complete(self, keyword, language, position, radius, place_type):
		try:
			# --------------------------
			# prepare params
			# --------------------------
			params = {
				"input_text": keyword,
				"language": language,
				"session_token": ""
			}
			if position:
				params["location"] = (position['lat'], position['lng'])
			if radius:
				params["radius"] = radius
			if place_type:
				params["types"] = place_type
			# --------------------------
			# search
			# --------------------------
			start = get_timestamp_ms()
			gg_response = self.place_api.places_autocomplete(**params)		# `text_search` is better than `find_place`
			end = get_timestamp_ms()
			elapsed = int((end - start) * 1000)
			log.info('google_search_auto_complete_elapse=%d', elapsed)
			# --------------------------
			# response
			# --------------------------
			gplaces = []

			if gg_response:
				for gg_place in gg_response:
					place_info = {
						"gplace_id": gg_place["place_id"],
						"gplace_name": gg_place["structured_formatting"]["main_text"],
						"gplace_address": gg_place["description"],
						"gplace_position": {
							"lat": 0,
							"lng": 0
						},
						"gplace_types": gg_place.get("types", [])
					}
					gplaces.append(place_info)
			reply = {
				"gplaces": gplaces
			}
			if not reply['gplaces']:
				return None, Result.ERROR_GOOGLE_SEARCH_NOT_FOUND
			return reply, None
		except googlemaps.exceptions.Timeout as error:
			self._handle_error(self.__config['PLACE_API_KEY'], error)
			return None, Result.ERROR_GOOGLE_SEARCH_EXCEED_QUOTA
		except Exception as error:
			log.exception('google_place_search_error|error=%s|keyword=%s,language=%s,position=%s,radius=%s,place_type=%s', error, keyword, language, position, radius, place_type)
			# self._handle_error(error)
			return None, Result.ERROR_GOOGLE_SEARCH

# def get_google_api_client():
# 	google_config = setting_manager.get_setting(setting_manager.SettingKey.GOOGLE_API_KEYS)
# 	if google_config:
# 		google_config = simplejson.loads(google_config)
# 	# if not google_config:
# 	# from codebase_lib import config
# 	# google_config = config.GOOGLE_API_KEYS
# 	return GoogleMapClient(google_config)
