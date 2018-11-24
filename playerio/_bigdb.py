from datetime import datetime

class BigDBObject:

	def __init__(self):
		raise NotImplementedError('BigDBObject is currently a static class!')

	@staticmethod
	def parse(obj_items):
		items = {}

		for item in obj_items:
			item_fields = item.value.ListFields()

			# Extract the value
			value = None
			if item.value.type == 0 or len(item_fields) == 2: 
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
				value = BigDBObject.parse(value)
			
			# Some fields don't have a name(?)
			if hasattr(item, 'name'):
				items[item.name] = value
	
		return items
