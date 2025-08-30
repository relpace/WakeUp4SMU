import json
import re
import logging
import random
import requests
import datetime
from typing import Tuple, Dict, List, Set, Iterable, Optional

from smulogin import login
from fetcher import fetch_week_event
from aggregate import aggregate


def main():
    account = input('Enter your account: ')
    password = input('Enter your password: ')
    session = requests.Session()
    login(account, password, session)
    se = fetch_week_event(session,1,22)
    aggregated = aggregate(se)
    print(aggregated)
if __name__ == "__main__":
    main()


