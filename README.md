# Multiprocessing HTTP Download (Python) #

This is a python module that parses an input file which stores a **filename** to its corresponding download **url**, and downloads from a range of download urls parallely. This program is particularly useful for downloading from multiple urls, it is not effective in downloading from a single URL and you would benefit more from a sequential downloader. This downloader also re-downloads from the last breakpoint if your program halts or gets interrupted.   

This project was intended to download multiple (>1000) large files (>10GB) reliably.

## 1 How to use ##

1. Prepare your input file list - The first line (0 index) is ignored during parsing. Make sure that you have at least one line at the first index before your relevant filenames and urls. (Refer to example below)
![image](https://user-images.githubusercontent.com/44689249/231369039-d29fbf21-a166-4902-a89f-e8fe74120908.png)
> Note: Your output folder name will follow the input filename. You do not need to manually create an output folder.

2.  Open `main.py` and edit the `filepath` variable under `__main__` method to point to your input file that you have created in step 1.
![image](https://user-images.githubusercontent.com/44689249/231369533-f376b5d1-4b24-442f-b936-45a36839ee7a.png)

3. Save your `main.py` file and enter "`python main.py`" into your command line. 

4. Observe that the output folder has been created and will begin to fill that folder multiple files at a time.

> Note: Mock inputs of varying sizes (`/input/tmp` has 7 files of 10GB) is provided inside the `./input` folder 

## 2 How it works ##
The parser implementation is trivial and will not be covered in this section as you are free to change how you would like to parse multiple urls.

### Multiprocessing ###
The inbuilt python module `concurrent.futures` is used which automatically determines the number of worker threads to spawn to handle the workload. This is system dependent and it normally defaults to your system **number of cores** multiplied by **5**. Each `concurrent.futures` thread handles the simultaneously downloading and unpacking of one url into the target file.     
![image](https://user-images.githubusercontent.com/44689249/231370841-cb3131ca-c8cd-44cc-b19b-ed6a8b19c85d.png)
> Note: Refer to this [link](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) to learn how to use `ThreadPoolExecutor`

### Redownloader ###
You will notice this function which checks if the current file size in your respective `/output/<dir_name>` matches the content length of the http download request. It will begin from the range of the current size if the file has been partially downloaded. 
![image](https://user-images.githubusercontent.com/44689249/231371775-a5ecac14-6481-4a30-b925-7eb1c77fc39b.png)

### Downloading and writing to file ###
`raise_for_status()` was used to maintain a persistent HTTP connection which prevents excessive "3-way-handshake" for every chunk. 

`shutil.copyfileobj` had to be used instead of the conventional `f.write()` as it often resulted in incompleted file extraction/saving as the buffer was not cleared. This is specifically the case when the file size was large (1GB) and you have multiple concurrent downloads and extractions happening. This method ensures that the buffer is actively cleared which prevents the situation of the memory running out of space and eventually crashing the entire program when the buffer is unable to flush.
![image](https://user-images.githubusercontent.com/44689249/231373076-75d0131d-cdb6-414e-8bee-144456fd598a.png)
