import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from file.serializers import FileSerializer
from data_science.preprocess import Preprocess
import os
import string
import random

