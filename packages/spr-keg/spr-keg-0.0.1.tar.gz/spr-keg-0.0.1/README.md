# Keg

This package contains set of utilities that will be used by boogie-service and dask workers. 

# How to upload to Anaconda cloud

- Follow directions here: http://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-packages/#uploading-conda-packages
- `conda config --set anaconda_upload no`
- `conda build .`
- `conda build . --output`
- `anaconda login` Ask scr for username and password
- `anaconda upload /path/to/spraoi-keg.tar.bz2`

