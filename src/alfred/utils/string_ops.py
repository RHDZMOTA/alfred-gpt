
def camel_to_snake(value: str) -> str:
    return "".join(
        char if not char.isupper() else
        ("" if i and (substr := value[i-1] + (next_char or "")) == substr.upper() else "_") + char.lower()
        for i, (char, next_char) in enumerate(zip(value, [*value[1:], None]))
    ).lstrip("_")
