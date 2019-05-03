from datetime import datetime

class BigDBObject(dict):

	def __init__(self, table, bigdb_obj):
		self.__table = table
		self.__key = bigdb_obj.key
		self.update(BigDBObject.__parse(bigdb_obj.items))

	@property
	def table(self):
		return self.__table
	
	@property
	def key(self):
		return self.__key

	@staticmethod
	def __parse(obj_items, parent_type=10):
		items = [] if parent_type == 9 else {}

		for item in obj_items or []:
			item_fields = item.value.ListFields()

			# Extract the value
			value = None
			if len(item_fields) > 0 and (item.value.type == 0 or len(item_fields) == 2):
				value = item_fields[-1][1]
			elif 1 <= item.value.type <= 3:
				value = 0
			elif item.value.type == 4:
				value = False
			elif 5 <= item.value.type <= 6:
				value = 0.0

			# Convert to python datetime
			if item.value.type == 8 and value:
				value = datetime.fromtimestamp(value / 1000)

			# Resolve recursively BigDBArray(type=9) and BigDBObject(type=10)
			if 9 <= item.value.type:
				value = BigDBObject.__parse(value, item.value.type)
			
			if hasattr(item, 'name'):
				items[item.name] = value
			else:
				items.append(value)

		return items
