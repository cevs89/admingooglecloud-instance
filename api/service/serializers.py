import serpy


class RegisterServiceSerializer(serpy.Serializer):
    id = serpy.Field()
    service = serpy.Field()
    machine = serpy.Field()
    project = serpy.Field()
    zone = serpy.Field()
    instance = serpy.Field()
    status = serpy.Field()
    description = serpy.Field()
