from products import admin


def fetch_and_save_inmates():
  print('getting inmates')
  admin.get_inmates()
  
def classify_sex_offenders():
  admin.get_sex_offenders()