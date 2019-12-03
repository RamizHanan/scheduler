# Task Scheduler

__Description:__
OS task scheduler that can schedule as Rate Monotonic and Earliest Deadline First, both using energy efficient and non energy efficient modes.

__How to use:__

python3 main.py [text file] [schedule method] [optional: ee]

Example:
```
python3 main.py input1.txt rm

python3 main.py input1.txt rm ee

python3 main.py input1.txt edf

python3 main.py input1.txt edf ee
```

__STATUS:__
- [X] RM
- [x] RM EE
- [x] EDF
- [x] EDF EE

__Contributers:__
- Rigoberto Macedo  
- Ramiz Hanan
