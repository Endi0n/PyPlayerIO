class BigDBObject:

	def __init__(self):
		raise NotImplementedError('BigDBObject is currently a static class!')

	@staticmethod
	def parse(obj_items):
		items = {}

		for item in obj_items:
			_, value_type = item.value.ListFields()[0]

			# Sometimes basic types the value type is omitted, reason unknown
			if type(value_type) is not int:
				value_type = -1

			_, value = item.value.ListFields()[-1]

			# Resolve recursively BigDBArray(type=9) and BigDBObject(type=10)
			if 9 <= value_type:
				value = BigDBObject.parse(value)
			
			items[item.name] = value
	
		return items
