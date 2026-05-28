import re

def convert_sql_to_python(sql_code):

    code = sql_code

    # SELECT *

    code = re.sub(
        r"SELECT \* FROM (\w+)",
        r'df = spark.table("\1")',
        code,
        flags=re.IGNORECASE
    )

    # SELECT columns

    code = re.sub(
        r"SELECT (.+) FROM (\w+)",
        r'df = spark.table("\2").select("\1")',
        code,
        flags=re.IGNORECASE
    )

    # WHERE

    code = re.sub(
        r"WHERE (.+)",
        r'df = df.filter("\1")',
        code,
        flags=re.IGNORECASE
    )

    # GROUP BY

    code = re.sub(
        r"GROUP BY (.+)",
        r'df = df.groupBy("\1")',
        code,
        flags=re.IGNORECASE
    )

    # ORDER BY

    code = re.sub(
        r"ORDER BY (.+)",
        r'df = df.orderBy("\1")',
        code,
        flags=re.IGNORECASE
    )

    # COUNT

    code = re.sub(
        r"COUNT\(\*\)",
        r'count("*")',
        code,
        flags=re.IGNORECASE
    )

    final_code = f"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName(
    "ConvertedSQL"
).getOrCreate()

{code}

df.show()
"""

    return final_code