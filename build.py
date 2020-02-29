from os import environ
from cpt.packager import ConanMultiPackager


print('---CONAN_ env vars')
for v in environ:
    if v.startswith('CONAN_') and v != 'CONAN_PASSWORD':
      print(v)
print('---CONAN_ env vars')

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=False)
    builder.run()
