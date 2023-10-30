![Logo](https://imagizer.imageshack.com/img922/7023/lhgfe7.png)

# PDF to Excel

The aim of this project is to automate the conversion of a PDF file, which lists articles and appendices, into an xlsx file. This program works specifically for files constructed in the same way as the "Régulations.pdf" file.


## Deployment

To use this script, clone the repository on your desktop. 
## How to use

There are two ways to launch the program.

1 - Directly from the terminal
  - Launch the python file, with the Article or annex as argument.
  ```bash
    python3 split-in-excel.py Article 5
  ```

2 - With the sh executable
  - Modify the txt file "things-to-keep.txt", and write all the Articles and/or Annexes you need.
  - Double-click on the "launch-split.sh" file, or run it with the command 
  ```bash
    ./launch-split.sh
  ```

## Authors

- [@wwLeji](https://github.com/wwLeji)