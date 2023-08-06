# Install

```sh
# the latest
pip install colabo.flow.go

# upgrade AFTER installing
pip install --upgrade colabo.flow.go

# a speciffic one
pip install colabo.flow.go==0.0.4
```

# Use

```py
# import
from colabo.flow.go import go_pb2
from colabo.flow.go import ColaboFlowGo

# create an ColaboFlowGo object
colaboFlowGo = ColaboFlowGo()

create an execute request object
request = go_pb2.ActionExecuteRequest(
    flowId='search-sounds', name='mediator', flowInstanceId='fa23', dataIn='hello from client', params='quick')

# send the go object to the go service
response = colaboFlowGo.executeActionSync(request)

# print the respons from the go service
print("response = %s" % (response))
```

# More Details

+ [Github Colabo repository](https://github.com/Cha-OS/colabo)
+ [This package inside the Colabo repo](https://github.com/Cha-OS/colabo/tree/master/src/services/puzzles/flow/go/python)
+ [DEVELOPMENT.md](https://github.com/Cha-OS/colabo/blob/master/src/services/puzzles/flow/go/python/DEVELOPMENT.md)
+ Relevant Colabo Puzzles
    + [Python](https://github.com/Cha-OS/colabo/tree/master/src/services/puzzles/flow/go/python)
    + [ColaboFlow Go Services](https://github.com/Cha-OS/colabo/tree/master/src/services/puzzles/flow/go)
    + [Backend](https://github.com/Cha-OS/colabo/tree/master/src/backend/dev_puzzles/flow/go)
    + [Frontend](https://github.com/Cha-OS/colabo/tree/master/src/frontend/dev_puzzles/flow/go)
    + [Isomorphic](https://github.com/Cha-OS/colabo/tree/master/src/isomorphic/dev_puzzles/flow/go)