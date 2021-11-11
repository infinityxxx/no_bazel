import isodate


def duration_formatted(duration: isodate.Duration) -> 'Iso8601DurationStr':
    """Return ISO-8601 duration string as Iso8601DurationStr."""
    return Iso8601DurationStr(isodate.duration_isoformat(duration))


class Iso8601DurationStr(str):
    """ISO-8601 duration string."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(example="P7D", type="string", format=cls.__name__)

    @classmethod
    def validate(cls, value: str) -> 'Iso8601DurationStr':
        try:
            isodate.parse_duration(value)
        except isodate.ISO8601Error as exc:
            raise ValueError("Invalid duration") from exc
        return cls(value)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"
