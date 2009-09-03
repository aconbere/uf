from distutils.core import setup

setup(name="uf",
      version="1.0",
      author="Anders Conbere",
      author_email = "aconbere@conbere.org",
      license = "bsd",
      packages=["uf"],
      package_data={"uf": ["xsl/*.xsl", "examples/*.html"]}
     )
