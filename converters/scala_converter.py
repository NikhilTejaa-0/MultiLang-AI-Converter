import re

def convert_scala_to_python(scala_code):

    code = scala_code

    # val → variable

    code = re.sub(
        r"\bval\b",
        "",
        code
    )

    # var → variable

    code = re.sub(
        r"\bvar\b",
        "",
        code
    )

    # println

    code = re.sub(
        r"println",
        "print",
        code
    )

    # Array

    code = re.sub(
        r"Array\((.*?)\)",
        r"[\1]",
        code
    )

    # List

    code = re.sub(
        r"List\((.*?)\)",
        r"[\1]",
        code
    )

    # true/false

    code = re.sub(
        r"\btrue\b",
        "True",
        code
    )

    code = re.sub(
        r"\bfalse\b",
        "False",
        code
    )

    final_code = f"""
# Converted Scala → Python

{code}
"""

    return final_code