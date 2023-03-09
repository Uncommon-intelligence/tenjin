import os
import sys
from dotenv import load_dotenv

sys.path.append("../tenjin")

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

slack_token = os.environ.get("SLACK_TOKEN")
