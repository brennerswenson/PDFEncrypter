import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import math
import time
import random
import subprocess
from textwrap import TextWrapper
import sys

# # sets terminal window dimensions
#
# os.system('mode con: cols=100 lines=20')

# terminal colors


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# only will protect pdfs


def isPDFfile(fname):
    if not os.path.isfile(fname):
        return False
    (name, ext) = os.path.splitext(fname)
    return ext.lower() == '.pdf'

# create function to encrypt pdf


def encrypt(file):
    temp = open(file, 'rb')
    temp_reader = PdfFileReader(file)
    temp_writer = PdfFileWriter()
    for num in range(temp_reader.numPages):
        temp_writer.addPage(temp_reader.getPage(num))
    temp_writer.encrypt(password)
    temp_result = open(file, 'wb')
    temp_writer.write(temp_result)
    temp_result.close()

# make progress bar


def progress(count, total, suffix=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write(bcolors.YELLOW + '[%s] %s%s %s\r' %
                     (bar, percents, '%', suffix) + bcolors.ENDC)

    sys.stdout.flush()
    if count == total:
        print(bcolors.BOLD + '\n' + '\nDONE!\n' + bcolors.ENDC)


time.sleep(.5)

# text wrapper instance


wrapper = TextWrapper()

wrapper.width = 80

# make list of files to protect

all_files = os.listdir('.')

# empty list for pdfs

files_to_encrypt = []

# fill list with only pdfs

for file in all_files:
    if isPDFfile(file):
        files_to_encrypt.append(file)
    else:
        continue

# no. of files to protect

total = len(files_to_encrypt)

# get directory from user

print("\n")
directory = input(wrapper.fill(
    'Hi! Welcome to Strata PDF Encrypter, created by Brenner Swenson. \nPlease paste in the directory of where your pdf files are located: '))

# checks if input is a valid directory

if not os.path.exists(directory):

    directory = input(wrapper.fill(
        bcolors.RED + "Invalid directory, please enter a valid directory: " + bcolors.ENDC))

# second check if input is incorrect

if not os.path.exists(directory):

    directory = input(wrapper.fill(
        bcolors.RED + "Invalid directory, please enter a valid directory: " + bcolors.ENDC))


if not os.path.exists(directory):

    directory = input(wrapper.fill(
        bcolors.RED + "Invalid directory, please enter a valid directory. Last try: " + bcolors.ENDC))


if not os.path.exists(directory):

    print(bcolors.RED + "Invalid directory, press any key to close Encrypter and try again." + bcolors.ENDC)

    input('')

    quit()


os.chdir(directory)

# get password from user

password = str(input(wrapper.fill(
    'Enter password you want to encrypt all .pdf files in this directory with :  ')))

# phrases for fun, after encryption finishes

print('\n')

phrases = ['Now go take a long lunch. You deserve it.', 'Now go thank Brenner for making this, because of how much free time you have now.', 'Now go take a nap with all of the time you just saved.', 'Now go home at a decent time today, you just saved a bunch of time.', "Go test out the files and make sure Brenner didn't screw up. He probably made some mistake somewhere.",
           'Now go watch a YouTube video or something, you have some free time now. Watching cat videos is beneficial to your mental health.', 'Go test out your files! Make sure the password actually works.',  'Have an idea for a script that Brenner could make? Let him know!']

# Enables terminal coloring

subprocess.call('', shell=True)

start_time = time.time()

count = 0

print('Here we go...')
print('')

import concurrent.futures

# create 4 python instances for fast execution

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(encrypt, file)               : file for file in files_to_encrypt}

    for future in concurrent.futures.as_completed(futures):
        count += 1
        # progress bar
        progress(count, total, suffix='Encrypting pdf {z} of {y}...'.format(
            z=count, y=len(files_to_encrypt)))

# calculating performance time
end_time = time.time()
execution_time_secs = math.ceil(end_time - start_time)
execution_time_mins = ((end_time - start_time) / 60)
files_per_second = (count / execution_time_secs)

# message to display performance, formatting

msg = "{d} seconds, or {e:.{digits}f} minutes. That's about {g:.{digits}f} files per second." .format(
    d=execution_time_secs, e=execution_time_mins, digits=2, g=files_per_second)

# Finishing text

print(bcolors.OKGREEN + '{a} files encrypted in {c} {b}'.format(a=count,
                                                                b=wrapper.fill(random.choice(phrases)), c=wrapper.fill(msg)) + bcolors.ENDC)

print('')
time.sleep(1)

print('')

input(bcolors.BOLD + "Press any key to exit." + bcolors.ENDC)
