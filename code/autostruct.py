import collections, struct

int_struct=struct.Struct("i")
bool_struct=struct.Struct("?")

class Struct(object):
	def __init__(self, instance):
		self.map=collections.OrderedDict()
		for var in sorted(dir(instance)):
			if not (var.startswith("_") or var.endswith("_")):
				val=getattr(instance, var)
				self.map[var]=type(val)

	def pack(self, instance):
		res=""
		for k, v in self.map.iteritems():
			res+=self.packval(getattr(instance, k), v)
		return res

	def unpack(self, instance, data):
		datapos=0
		structpos=0
		while structpos<len(self.map.values()):
			d, l = self.unpackval(data[datapos:], self.map.values()[structpos])
			setattr(instance, self.map.keys()[structpos], d)
			structpos+=1
			datapos+=l
		return datapos

	def packval(self, data, cls):
		if cls==int:
			return int_struct.pack(data)
		if cls==bool:
			return bool_struct.pack(data)
		if cls==str:
			return int_struct.pack(len(data))+data

	def unpackval(self, data, cls):
		if cls==int:
			return (int_struct.unpack(data[:4])[0], 4)
		if cls==bool:
			return (bool_struct.unpack(data[0])[0], 1)
		if cls==str:
			l=int_struct.unpack(data[:4])[0]
			s=data[4:4+l]
			return (s, l+4)