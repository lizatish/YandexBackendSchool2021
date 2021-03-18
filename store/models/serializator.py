from uuid import UUID
from sqlalchemy_serializer import SerializerMixin


class JsonMixin(SerializerMixin):
    serialize_types = (
        (UUID, lambda x: str(x)),
    )
