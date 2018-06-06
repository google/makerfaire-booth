from google.protobuf import text_format
from object_detection.protos import string_int_label_map_pb2

LABEL_MAP = "data/label_map.pb.txt"
f = open(LABEL_MAP).read()
m = text_format.Parse(f, string_int_label_map_pb2.StringIntLabelMap())
layers = [item.name for item in m.item]
layer_dict = dict([(item.id, item.name) for item in m.item])
