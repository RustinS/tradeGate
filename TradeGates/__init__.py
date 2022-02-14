import os
import sys

PROJECT_PATH = os.getcwd()

print(PROJECT_PATH)

sys.path.append(PROJECT_PATH)
sys.path.append('../')
sys.path.append('../Exchanges')