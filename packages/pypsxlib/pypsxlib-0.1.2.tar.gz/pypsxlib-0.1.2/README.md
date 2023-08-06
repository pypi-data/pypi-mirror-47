
## About
Python library for reading, writing and managing Agisoft Photoscan/Metashape PSX projects. Unofficial.

Pretty rough at the moment. 

Questions? Contributions? Bug reports? Open an issue on the [gitlab page for the project](https://gitlab.com/dodgyville/pypsxlib).
I am very interested in hearing your use cases for `pypsxlib` to help drive the roadmap.


### Contributors
* Luke Miller

### Thanks

`pypsxlib` made for '39', supported by Creative Victoria 

### Roadmap
* Test suite to find where the psx specification is unsupported
* Make sure loading cameras and bounding boxes work
* Make sure saving cameras and bounding boxes work
* Create transformation objects for manipulation instead of strings
* Add point cloud support
* Add model support
* Add texture support


## Quickstart

### Installing
```
pip install pypsxlib
```

### How do I...

#### Load a .PSX project
```python3
from pypsxlib import Project 

project = Project().load_psx("myProject.psx")  # not all features supported
```

#### Save a .PSX project
```python3
project = Project("myProject")
project.path = "/path/for/project"
project.save()  # project.name and project.path must be set
```


#### Add a Chunk
```python3
p = Project("myProject")
p.defaults()  # create a new app and document
p.add_chunk()  # add an empty chunk
```


#### Access a chunk
```python3
chunk = p.apps[0].documents[0].chunks[0]
```

#### Access thumbnails
```python3
chunk.frames[0].thumbnails
```

### Source
```
git clone https://gitlab.com/dodgyville/pypsxlib.git
```

## Reference

### .psx project layout

```
myProject.psx
myProject.files/
myProject.files/project.zip
myProject.files/<chunkid>/
myProject.files/<chunkid>/chunk.zip
myProject.files/<chunkid>/<frameid>/
myProject.files/<chunkid>/<frameid>/frame.zip
myProject.files/<chunkid>/<frameid>/thumbnails/
myProject.files/<chunkid>/<frameid>/thumbnails/thumbnails.zip
```

## Changelog

### v0.1.2
* improve support for loading and saving thumbnails
* add loading and saving for camera transformations
* add loading and saving of bounding boxes
* add chunk transform, region and meta saving
* fix bugs

### v0.1.1
* improve support for loading project with multiple chunks and cameras
* improve support for loading models
* improve support for loading frames
* improve support for loading aligned photos

### v0.1.0
* initial release