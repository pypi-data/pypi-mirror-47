from distutils.core import setup
setup(
  name = 'datawiz',         
  packages = ['datawiz'],   
  version = '0.9',             
  description = 'DataWiz helps new data learners, hobbyist and industry practitioners write Machine Learning code faster by doing the heavy-lifting such as data cleaning, data transformation, preparation and more! ',   # Give a short description about your library
  author = 'Koye Sodipo',                   
  author_email = 'broskoye@hotmail.com',      
  keywords = ['Data Engineering', 'data preparation', 'data science', 'data cleaning','pandas','machine learning'],   
  install_requires=[            
          'numpy',
          'pandas',
          'sklearn',
          'scipy'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',  
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
