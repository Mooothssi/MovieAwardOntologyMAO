from decouple import config
import os

OWL_FILEPATH = config('OWL_FILE_PATH', default="proto-movie.owl")
OUT_PATH = config('OUT_PATH', default="out/")
OUT_FILENAME = config('OUT_FILENAME', default="out.owl")

DB_NAME = config('DB_NAME', default="mao")
DB_HOST = config('DB_HOST', default="localhost:3306")
DB_PASSWORD = config('DB_PASSWORD')
DB_USERNAME = config('DB_USERNAME', default="root")
DB_DRIVER = config('DB_DRIVER', default="pymssql")
DB_DIALECT = config('DB_DIALECT', default="mssql")

if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)
