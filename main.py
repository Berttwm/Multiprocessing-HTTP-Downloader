import concurrent.futures 
import datetime
import multiprocessing
import os
import requests
import shutil
import sys

from io import BytesIO


class MultiProcessDownloader():
	def __init__(self, filepath):
		# Step init: assertion checks
		assert os.path.exists(filepath), f"[*] Input file `{filepath}` cannot be found."
		self.filepath = filepath
		self.output_folder = f"./output/{filepath.split('input')[1].split('.')[0]}" # Specific output folder to save to
		self.filename_url_dict = {}

		# Step 1: get list of urls, store into global
		self.__get_url_ls()

		# Step 2: Begin multiprocess downloader
		self.__downloader()

	def __get_url_ls(self):
		with open(self.filepath, 'r') as file:
			file_line_ls = [line.rstrip() for line in file]

		for idx,line in enumerate(file_line_ls):
			if(idx == 0): # Skip header lines
				continue
			self.filename_url_dict[line.split("	")[0]] = line.split("	")[1] 

		print(f"[*] Parsed `{filepath}` successfully!")
		# for k, v in self.filename_url_dict.items():
		# 	print(f"k: {k}\nv: {v}\n")
	def __downloader(self):
		print(f"[*] Downloading from {len(self.filename_url_dict)} urls...")
		total_time_extract = 0 # in ms
		start = datetime.datetime.now()
		filename_ls = []
		url_ls = []
		for filename, url in self.filename_url_dict.items():
			filename_ls.append(filename)
			url_ls.append(url)
		# 	try:
		# 		total_time_extract += self.download_file(filename, url)
		# 	except Exception as e:
		# 		raise Exception(e)
			# break # Comment to test single
		# Multiprocessing handled by concurrent futures
		with concurrent.futures.ThreadPoolExecutor() as exector : 
			exector.map(self.download_file, filename_ls, url_ls)
		end = datetime.datetime.now()

		### Metrics calculation
		total_time = int((end-start).total_seconds() * 1000)
		print("*** Metrics ***")
		print("total elapsed time = {}/ms".format(total_time))
		# print("total download time = {}/ms".format(total_time - total_time_extract))
		# print("total extract time = {}/ms".format(total_time_extract))
		# print("percentage time spent on download = {}/%".format((total_time - total_time_extract)/total_time * 100))
		# print("percentage time spent on extract = {}/%".format(total_time_extract/total_time * 100))
		print("*** *** ***")
		print("avg download + save time for each of {} files = {}/ms".format(len(self.filename_url_dict), total_time/len(self.filename_url_dict)))

	def download_file(self, filename, url):
		# Step 1: Check if file has remaining size to be downloaded
		try:
			total_content_size = int(requests.get(url, stream=True).headers['Content-Length'])
			file_full_location = os.path.join(self.output_folder, filename)
			if os.path.exists(file_full_location):
				temp_size = os.path.getsize(file_full_location)
				if total_content_size == temp_size:
					return
				print(f"[*] Redownloading remaining data for `{filename}` starting at `{temp_size}`/Byte")
			else:
				temp_size = 0
			# Download from remaining size or from non remaining size
			headers = {'Range': 'bytes=%d-' % temp_size}
			copy_length = 16*1024*1024
			with requests.get(url, stream = True, headers=headers) as response:
				response.raise_for_status()
				with open(file_full_location, 'ab') as f:
					shutil.copyfileobj(response.raw, f, length=copy_length)
		except Exception as e:
			print(e)
			sys.exit(1)

if __name__ == '__main__':
	### Input: `filepath`
	filepath = f'./input/tmp.txt' 
	MultiProcessDownloader(filepath)
