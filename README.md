# Pyqt-Chart
A file binary sequence visualization program using pyqt5 and pyqtgraph

## Sample Figure
![](demo.png)

## Requirement
- Python 3.6+
- PyQt5
- Pyqtgraph
- NumPy

## Usage
Open engine.py to run or run the shell command as:
```shell
   python engine.py 
```

And then choose an arbitrary file to analyze. The file should be less than 200KB 
and then size limit can be modified in "MaxFileSize" item in config.json (by KB). 

## Function
This program is a demo that uses PyQt5 and Pyqtgraph. It will read file in binary 
byte stream and plot the byte value in three forms: Value, integrate(sum) and 
differential(successive difference value).