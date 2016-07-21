import json, socket

class JsonConn(object):
	''' a socket with some check on msg leng (prefixed length). Full for
	client side, incomplete for server side. '''

	def __init__(self,conn=None):
		if conn == None:  # NOT RECOMMENDED
			self.socket = socket.socket()
		else:
			self.socket = conn
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	def close(self):
		self.socket.close()
	def connect(self, (host, port)):
		self.socket.connect((host, port))
		return self


	# filno
	def fileno(self): return self.socket.fileno()

	# sending / receiving starts here

	def jsend(self, msg):
		msglen = str(len(msg))
		paddedlen = msglen.rjust(4,'0')
		self.socket.sendall(paddedlen+msg)
	 	# is this ok?
		# what to retunr?

	def jrecv(self, max=2048):
		length_str = self.read_n(4)
		if length_str == 'nil': return 'nil'
		length = int(length_str)
		if length > max: return Exception('Data recvd bigga than max')
		return self.read_n(length)

	def read_n(self, length):
		buf = ''
		n=length
		while n > 0:
			data = self.socket.recv(n)
			if data == '':
				return 'nil'   # is this approach ok?
			#	raise RuntimeError('unexpected connection close')
			buf += data
			n -= len(data)
		return buf


''' 	"""
	A JSON socket connection. All the
	data is serialized in JSON with jsend()  before being sent, and
	deserialized to its original format within jrecv.
	"""

	def __init__(self, conn):
		self.socket = conn

	def close(self):
		self.socket.close()

	def jsend(self, data):
		try:
			serialized = json.dumps(data)
		except (TypeError, ValueError), e:
			raise Exception('You can only send JSON-serializable data')
		# send the length of the serialized data first
		self._send('%d\n' % len(serialized))
		# send the serialized data
		self.socket.sendall(serialized)
		return self

	def jrecv(self, max=4096):
		# read the length of the data, letter by letter until we reach EOL
		length_str = ''
		char = self.socket.recv(1)
		while char != '\n':
			length_str += char
			char = self.socket.recv(1)
		total = int(length_str)
		if total > max:
			return Exception('Data received was too big')
		# use a memoryview to receive the data chunk by chunk efficiently
		view = memoryview(bytearray(total))
		next_offset = 0
		while total - next_offset > 0:
			recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
			next_offset += recv_size
		try:
			deserialized = json.loads(view.tobytes())
		except (TypeError, ValueError), e:
			raise Exception('Data received was not in JSON format')
		return deserialized

'''
