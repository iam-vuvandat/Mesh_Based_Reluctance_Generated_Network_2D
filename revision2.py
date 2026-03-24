import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.utils.data_helper import save, load
from motor_geometry.models.SPM import SPM

spm = SPM()