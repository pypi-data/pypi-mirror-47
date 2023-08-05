# Hippo2client

## Installation

Simple install this module via pip (pip for Python 2 is also supported)

```
pip3 install --user hippo2client
```


## Usage

```
import hippo2client

# shorten git id is perfect, better then tags, because tags
# may not available everywhere to identify a version always
e = hippo2client.MajorEntity('72a56cd05b')

# there is a concept of an alias, this can make the git id
# more obvisious (this can be the output of git describe --always
# --dirty
e.set_alias('v1.5')

e.add_markdown('001', '# Heading - First Level')
e.add_markdown('002', '## Sub Heading - First Level')
e.add_markdown('003', '[link to second level (0001)](0001/)')
e.add_file("graph.png", path_to_image)
e.add_markdown('100', '![graph](graph.png)')

# second level
e.add_markdown('0001/001', '# Heading - Second Level')
e.add_markdown('0001/002', '## Sub Heading - Second Level')
e.add_markdown('0001/003', '[link to third level (0001)](0001/)') # note here, this is already relativ to 0001!
e.add_markdown('0001/004', '[level up link (0001)](..)')
e.add_file("0001/graph.png", path_to_image)
e.add_markdown('0001/100', '![graph](graph.png)')

# third level
e.add_markdown('0001/0001/001', '# Heading - Third Level')
e.add_markdown('0001/0001/002', '## Sub Heading - Third Level')
e.add_markdown('0001/0001/003', '[link to fourt level (0001)](0001/)') # note here, this is already relativ to 0001/0001!
e.add_markdown('0001/0001/004', '[level up link (0001)](..)') # note here, this is already relativ to 0001/0001!
e.add_file("0001/0001/graph.png", path_to_image)
e.add_markdown('0001/0001/100', '![graph](graph.png)')

# Fourth level
e.add_markdown('0001/0001/0001/001', '# Heading - Fourth Level')
e.add_markdown('0001/0001/0001/002', '## Sub Heading - Fourth Level')
e.add_markdown('0001/0001/0001/003', '[link to Fifth level (0001)](0001/)') # note here, this is already relativ to 0001/0001!
e.add_markdown('0001/0001/0001/004', '[level up link (0001)](..)') # note here, this is already relativ to 0001/0001!
e.add_file("0001/0001/0001/graph.png", path_to_image)
e.add_markdown('0001/0001/0001/100', '![graph](graph.png)')

# Fifth level
e.add_markdown('0001/0001/0001/0001/001', '# Heading - Fifth Level')
e.add_markdown('0001/0001/0001/0001/002', '## Sub Heading - Fifth Level')
e.add_markdown('0001/0001/0001/0001/003', 'Should be enough ...')
e.add_file("0001/0001/0001/0001/graph.png", path_to_image)
e.add_markdown('0001/0001/0001/0001/100', '![graph](graph.png)')
e.set_test_status('0001/0001/0001/0001', "passed")


URL = "http://localhost:8080/"
TIMEOUT = 10
a = hippo2client.Agent(url=URL, timeout=TIMEOUT)
a.add(e)
a.upload()
```

