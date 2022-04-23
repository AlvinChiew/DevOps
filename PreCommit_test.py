# brew install pre-commit
# ln -s /bin/gcc /bin/gcc-5  # complaint from Lucas-C/pre-commit-hooks
# pre-commit install
# pre-commit migrate-config
#
# sample code that isn't compliant to black linter
# before: def main(name :str):
def main(name: str):
    print(f"hello, {name}")
