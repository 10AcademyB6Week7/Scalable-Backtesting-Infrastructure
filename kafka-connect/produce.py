from schema_registry.client import SchemaRegistryClient


sr = SchemaRegistryClient('localhost:8081')
my_schema = sr.get_by_id(schema_id=1)
print(my_schema)