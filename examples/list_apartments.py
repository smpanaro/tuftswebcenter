# Hack around so we can import webcenter.
import os, sys
lib_path = os.path.abspath('../webcenter/')
sys.path.append(lib_path)

from webcenter import *
from webcenter_credentials import *

wc = WebcenterSession(STUDENT_ID, SIS_PIN)
rankings = wc.get_housing_groups_report("Apartment")
number_of_members = 6
for group in rankings[number_of_members]:
    if group.name == "Christopher Walken":
        print "Our group {group} is currently {rank}/{total}".format(group = group.name, rank = group.rank, total = len(rankings[number_of_members]))
        break