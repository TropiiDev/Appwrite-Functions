# Imports
import os

from appwrite.client import Client
from appwrite.services.tables_db import TablesDB
from appwrite.services.storage import Storage
from appwrite.query import Query
from appwrite.exception import AppwriteException
from dotenv import load_dotenv

load_dotenv()

# This Appwrite function will be executed every time your function is triggered
def main(context):
  # You can use the Appwrite SDK to interact with other services
  # For this example, we're using the Users service
  client = (
    Client()
    .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
    .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    .set_key(context.req.headers["x-appwrite-key"])
  )

  tablesDB = TablesDB(client)
  storage = Storage(client)

  db_id = os.getenv('APPWRITE_DATABASE_ID')
  bucket_id = os.getenv("APPWRITE_BUCKET_ID")

  files = None

  try:
    tracked_files = tablesDB.list_rows(
      database_id=db_id,
      table_id="trackedFiles"
    )

    for i in range(len(tracked_files.rows)):
      row_id = tracked_files.rows[i].id
      file_id = tracked_files.rows[i].data['fileId']

      storage.delete_file(
        bucket_id=bucket_id,
        file_id=file_id
      )

      tablesDB.delete_row(
        database_id=db_id,
        table_id="trackedFiles",
        row_id=row_id
      )

      context.log(f"Deleted {len(tracked_files.rows)} images")

  except AppwriteException as err:
    context.error("Could not list users: " + repr(err))

  # The req object contains the request data
  if context.req.path == "/ping":
    # Use res object to respond with text(), json(), or binary()
    # Don't forget to return a response!
    return context.res.text("Pong")

  return context.res.json(
    {
      "message": "Finished"
    }
  )
