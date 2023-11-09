# pylint: disable=too-many-arguments
import json
from .pbdata import GxxProtocol_pb2
from .pbutils import pb_enum_to_class
from .gtcpclient import GTcpClient
from .buffer_writer import BufferWriter
from .utils import get_timestamp
from .logger import log
from .simplequeue import SimpleQueue

class GxxRouterClient:
	ServerType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'ServerType')
	CommandType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'CommandType')
	Command = pb_enum_to_class(GxxProtocol_pb2.Constant, 'Command')
	ClientPlatform = pb_enum_to_class(GxxProtocol_pb2.Constant, 'ClientPlatform')
	MessageType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'MessageType')
	MessageSessionType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'MessageSessionType')
	AppMessageDisplayType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'AppMessageDisplayType')
	NotificationType = pb_enum_to_class(GxxProtocol_pb2.Constant, 'NotificationType')
	NotificationFlag = pb_enum_to_class(GxxProtocol_pb2.Constant, 'NotificationFlag')

	MAX_LIST_LENGTH = 100
	MAX_TITLE_LENGTH = 100
	MAX_IMAGE_URL_LENGTH = 250
	MAX_DATA_LENGTH = 500

	SUSPEND_PERIOD_CHECK = 60 * 60

	def __init__(self, server_id, router_config_list):
		self._server_id = server_id
		self._packet_id = 0
		self._last_suspend_check = 0
		self._active_clients = SimpleQueue()
		self._suspend_clients = SimpleQueue()
		for router_config in router_config_list:
			self._active_clients.put(GTcpClient(**router_config))

	def _send_request(self, server_type, cmd, request_data):
		self._packet_id += 1
		current_timestamp = get_timestamp()

		router_header = GxxProtocol_pb2.ServerPacketHeader()
		router_header.id = self._server_id
		router_header.command_type = GxxRouterClient.CommandType.CMD_S2S_REQUEST
		router_header.command = GxxRouterClient.Command.CMD_ROUTE
		router_header.timestamp = current_timestamp
		router_header.router_extension.target_server_type = server_type
		router_header.router_extension.routing_key = cmd

		server_header = GxxProtocol_pb2.ServerPacketHeader()
		server_header.id = self._packet_id
		server_header.command_type = GxxRouterClient.CommandType.CMD_S2S_REQUEST
		server_header.command = cmd
		server_header.timestamp = current_timestamp

		router_header_data = router_header.SerializePartialToString()
		server_header_data = server_header.SerializePartialToString()
		writer = BufferWriter('!')
		writer.add_uint16(len(router_header_data))
		writer.add_buffer(router_header_data)
		writer.add_uint16(len(server_header_data))
		writer.add_buffer(server_header_data)
		writer.add_buffer(request_data.SerializePartialToString())

		# try to check suspend
		if self._active_clients.empty() or \
			(not self._suspend_clients.empty() and (current_timestamp - self._last_suspend_check > GxxRouterClient.SUSPEND_PERIOD_CHECK)):
			self._last_suspend_check = current_timestamp
			picked_client = self._suspend_clients.get()
			if picked_client.send(writer.buffer):
				self._active_clients.put(picked_client)
				log.data("gxx_router_send|server_id=%s,packet_id=%d,command=0x%02x,suspend_client=%s:%s",
					self._server_id, self._packet_id, cmd, picked_client.address, picked_client.port)
				return True
			else:
				self._suspend_clients.put(picked_client)

		while not self._active_clients.empty():
			picked_client = self._active_clients.get()
			if picked_client.send(writer.buffer):
				self._active_clients.put(picked_client)
				log.data("gxx_router_send|server_id=%s,packet_id=%d,command=0x%02x,client=%s:%s",
					self._server_id, self._packet_id, cmd, picked_client.address, picked_client.port)
				return True
			else:
				self._suspend_clients.put(picked_client)
				log.warn("gxx_router_send_fail|server_id=%s,packet_id=%d,command=0x%02x,client=%s:%s",
					self._server_id, self._packet_id, cmd, picked_client.address, picked_client.port)
		return False

	def buddy_import(self, uid, game_id, buddy_uids):
		if not buddy_uids:
			log.warn("gxx_router_import_empty_buddy_list|uid=%s,game_id=%s,buddy_uids=%s", uid, game_id, buddy_uids)
			return False

		request_data = GxxProtocol_pb2.LSBuddyImportRequest()
		request_data.uid = uid
		request_data.game_id = game_id
		request_data.buddy_uids.extend(buddy_uids)

		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_BUDDY_IMPORT, request_data)

	def app_request(self, app_id, from_uid, to_session_type, to_id_list, display_type, title, text,
		message=None, from_open_id=None, uri_list=None, image=None, data=None, media_tag=None, extra_data=None):
		'''
		:param to_session_type: MessageSessionType
		:param to_id_list: max 100
		:param title: max 100 chars
		:param image: max 250 chars
		:param display_type: AppMessageDisplayType
		:param data: max 500 chars
		'''
		if to_session_type != GxxRouterClient.MessageSessionType.MESSAGE_SESSION_USER and \
			to_session_type != GxxRouterClient.MessageSessionType.MESSAGE_SESSION_DISCUSSION:
			log.warn("app_request_to_invalid_message_session|app_id=%s,from_uid=%s,to_session_type=%s", app_id, from_uid, to_session_type)
			return False
		if len(to_id_list) > GxxRouterClient.MAX_LIST_LENGTH:
			log.warn("to_id_list_invalid_size|app_id=%s,from_uid=%s,to_session_type=%s,to_id_size=%s", app_id, from_uid, to_session_type, len(to_id_list))
			return False
		if len(title) > GxxRouterClient.MAX_TITLE_LENGTH or \
			(image and len(image) > GxxRouterClient.MAX_IMAGE_URL_LENGTH) or \
			(data and len(data) > GxxRouterClient.MAX_DATA_LENGTH):
			log.warn("some_fields_exceed_limit|app_id=%s,from_uid=%s,to_session_type=%s", app_id, from_uid, to_session_type)
			return False

		app_message = GxxProtocol_pb2.AppMessage()
		app_message.display_type = display_type
		app_message.app_id = app_id
		app_message.title = title
		app_message.text = text
		if message:
			app_message.message = message
		if from_open_id:
			app_message.open_id = from_open_id
		if image:
			app_message.image = image
		if uri_list:
			app_message.uris.extend(uri_list)
		if data:
			app_message.data = data
		if media_tag:
			app_message.media_tag = media_tag
		if extra_data:
			app_message.extra_data = extra_data

		request_data = GxxProtocol_pb2.LSMessageSendRequest()
		app_message_str = app_message.SerializePartialToString()
		for to_id in to_id_list:
			message_info = request_data.messages.add()
			message_info.from_uid = from_uid
			message_info.session_type = to_session_type
			message_info.session_id = to_id
			message_info.message_type = GxxRouterClient.MessageType.MESSAGE_TYPE_APP
			message_info.message = app_message_str

		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_MESSAGE_SEND, request_data)

	def system_notify(self, uid_list, notify_type, target_platform_list, notify_flag, title, content, link_name, link_list, icon, source, duration, expiry_time):
		'''
		:param notify_type: NotificationType
		:param notify_flag: NotificationFlag
		:return:
		'''
		if not uid_list:
			log.warn("uid_list_empty|notify_type=%s", notify_type)
			return False
		if len(uid_list) > GxxRouterClient.MAX_LIST_LENGTH:
			log.warn("uid_list_exceed_limit_size|notify_type=%s,uid_id_size=%s", notify_type, len(uid_list))
			return False
		if len(title) > GxxRouterClient.MAX_TITLE_LENGTH:
			log.warn("title_is_too_long|notify_type=%s,title=%s", notify_type, title)
			return False

		notify_message = GxxProtocol_pb2.NotificationMessage()
		notify_message.notification_type = notify_type
		notify_message.target_platforms.extend(target_platform_list)
		notify_message.flag = notify_flag
		notify_message.title = title
		notify_message.content = content
		notify_message.link_name = link_name
		if link_list:
			notify_message.links.extend(link_list)
		notify_message.icon = icon
		notify_message.source = source
		notify_message.duration = duration
		notify_message.expiry_time = expiry_time

		request_data = GxxProtocol_pb2.LSMessageSendRequest()
		notify_message_str = notify_message.SerializePartialToString()
		for uid in uid_list:
			message_info = request_data.messages.add()
			message_info.from_uid = uid
			message_info.session_type = GxxRouterClient.MessageSessionType.MESSAGE_SESSION_SYSTEM
			message_info.session_id = uid
			message_info.message_type = GxxRouterClient.MessageType.MESSAGE_TYPE_NOTIFICATION
			message_info.message = notify_message_str

		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_MESSAGE_SEND, request_data)

	def app_group_create(self, app_id, app_server_id, group_id, uids):
		return self._send_request(
			GxxRouterClient.ServerType.SERVER_LOGIC,
			GxxRouterClient.Command.CMD_LS_APP_GROUP_CREATE,
			GxxProtocol_pb2.LSAppGroupCreateRequest(
				app_id=app_id,
				app_server_id=app_server_id,
				group_id=group_id,
				uids=uids
			)
		)

	def discussion_remove(self, discussion_id):
		return self._send_request(
			GxxRouterClient.ServerType.SERVER_LOGIC,
			GxxRouterClient.Command.CMD_LS_DISCUSSION_REMOVE,
			GxxProtocol_pb2.LSDiscussionRemoveRequest(discussion_id=discussion_id)
		)

	def discussion_update(self, discussion_id, name, owner_uid, max_member_count=None, flag=None):
		request_data = GxxProtocol_pb2.LSDiscussionUpdateRequest(discussion_id=discussion_id)
		if name is not None:
			request_data.name = name
		if owner_uid is not None:
			request_data.owner_uid = owner_uid
		if max_member_count is not None:
			request_data.max_member_count = max_member_count
		if flag is not None:
			request_data.flag = flag
		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_DISCUSSION_UPDATE, request_data)

	def discussion_member_add(self, discussion_id, uids):
		request_data = GxxProtocol_pb2.LSDiscussionMemberAddRequest(discussion_id=discussion_id, uids=uids)
		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_DISCUSSION_MEMBER_ADD, request_data)

	def discussion_member_remove(self, discussion_id, uids):
		request_data = GxxProtocol_pb2.LSDiscussionMemberRemoveRequest(discussion_id=discussion_id, uids=uids)
		return self._send_request(GxxRouterClient.ServerType.SERVER_LOGIC, GxxRouterClient.Command.CMD_LS_DISCUSSION_MEMBER_REMOVE, request_data)

	def push_notification_send(self, uids, message_dict, data):
		if not isinstance(message_dict, dict):
			log.warn("message_invalid_type|type_message=%s,message_dict=%s", type(message_dict), message_dict)
			return False
		if "default" not in message_dict:
			log.warn("default_message_is_required|message_dict=%s", message_dict)
			return False
		message = json.dumps(message_dict)
		request_data = GxxProtocol_pb2.NSPushRequest(uids=uids, message=message, data=data)
		return self._send_request(GxxRouterClient.ServerType.SERVER_NOTIFY, GxxRouterClient.Command.CMD_NS_PUSH, request_data)
