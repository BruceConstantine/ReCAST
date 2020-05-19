from django.test import TestCase

# Create your tests here.
from ReCAST.DO.Excel_In import Excel_In

e = Excel_In([1,222],[[1,2],[111,2]]);
print(e.get_plantATP());
print(e.toJSON());