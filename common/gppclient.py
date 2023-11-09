from .gtcpclient import GTcpClient
from .buffer_reader import BufferReader
from .buffer_writer import BufferWriter

class GppClient:

	TCP_CLIENT_TIMEOUT = 5

	CMD_MAIN_S2S = 0xe0
	CMD_SUB_S2S_GET_GPP = 0x91
	CMD_SUB_S2S_GET_MULTI_GPP = 0x92
	CMD_SUB_S2S_CHANGE_ENERGY = 0X95
	CMD_SUB_S2S_CHANGE_GPP = 0x93

	def __init__(self, ip, port):
		self._client = GTcpClient(ip, port, self.TCP_CLIENT_TIMEOUT)

	def get_gpp(self, uid):
		writer = BufferWriter()
		writer.add_uint8(self.CMD_MAIN_S2S)
		writer.add_uint8(self.CMD_SUB_S2S_GET_GPP)
		writer.add_uint32(uid)
		reply = self._client.request(writer.buffer)
		if reply is None:
			return None
		reader = BufferReader(reply)
		data = {}
		reader.get_uint16()
		data['uid'] = reader.get_uint32()
		if data['uid'] != uid:
			return None
		data['gpp'] = reader.get_uint32()
		data['level'] = reader.get_uint8()
		data['gpp_today'] = reader.get_uint8()
		data['gpp_to_next'] = reader.get_uint32()
		data['online'] = reader.get_uint32()
		data['energy'] = reader.get_uint32()
		data['max_energy'] = reader.get_uint32()
		return data

	def get_multi_gpp(self, uids):
		writer = BufferWriter()
		writer.add_uint8(self.CMD_MAIN_S2S)
		writer.add_uint8(self.CMD_SUB_S2S_GET_MULTI_GPP)
		writer.add_uint32(len(uids))
		for uid in uids:
			writer.add_uint32(uid)
		reply = self._client.request(writer.buffer)
		if reply is None:
			return None
		reader = BufferReader(reply)
		reader.get_uint16()
		data_list = []
		size = reader.get_uint32()
		while size > 0:
			data = {}
			data['uid'] = reader.get_uint32()
			data['gpp'] = reader.get_uint32()
			data['level'] = reader.get_uint8()
			reader.skip(7)
			data_list.append(data)
			size = size - 1
		return data_list

	def change_energy(self, uid, amount):
		writer = BufferWriter()
		writer.add_uint8(self.CMD_MAIN_S2S)
		writer.add_uint8(self.CMD_SUB_S2S_CHANGE_ENERGY)
		writer.add_uint32(uid)
		writer.add_int32(amount)
		reply = self._client.request(writer.buffer)
		if reply is None:
			return None
		reader = BufferReader(reply)
		data = {}
		reader.get_uint16()
		data['uid'] = reader.get_uint32()
		if data['uid'] != uid:
			return None
		data['result'] = reader.get_uint8()
		if data['result'] != 1:
			return None
		data['energy'] = reader.get_uint32()
		data['max_energy'] = reader.get_uint32()
		data['energy_before_change'] = reader.get_uint32()
		return data

	def change_gpp(self, uid, amount):
		writer = BufferWriter()
		writer.add_uint8(self.CMD_MAIN_S2S)
		writer.add_uint8(self.CMD_SUB_S2S_CHANGE_GPP)
		writer.add_uint32(uid)
		writer.add_int32(amount)
		reply = self._client.request(writer.buffer)
		if reply is None:
			return None
		reader = BufferReader(reply)
		data = {}
		reader.get_uint16()
		data['uid'] = reader.get_uint32()
		if data['uid'] != uid:
			return None
		data['result'] = reader.get_uint8()
		if data['result'] != 1:
			return None
		data['gpp'] = reader.get_uint32()
		data['level'] = reader.get_uint8()
		data['gpp_before_change'] = reader.get_uint32()
		return data
