# Copyright (C) GRyCAP - I3M - UPV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid

def get_stdin():
    return sys.stdin.read()

def join_paths(*paths):
    return os.path.join(*paths)

def get_tmp_dir():
    return tempfile.gettempdir()

def create_tmp_dir():
    return tempfile.TemporaryDirectory()

def get_random_tmp_folder():
    return join_paths(tempfile.gettempdir(), str(uuid.uuid4().hex))    

def lazy_property(func):
    ''' A decorator that makes a property lazy-evaluated.'''
    attr_name = '_lazy_' + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return _lazy_property

def find_expression(string_to_search, rgx_pattern):
    '''Returns the first group that matches the rgx_pattern in the string_to_search'''
    if string_to_search:    
        pattern = re.compile(rgx_pattern)
        match = pattern.search(string_to_search)
        if match :
            return match.group()

def base64_to_utf8_string(value):
    return base64.b64decode(value).decode('utf-8')

def utf8_to_base64_string(value):
    return base64.b64encode(value).decode('utf-8')

def encode_to_base64(value):
    return base64.b64encode(value)

def decode_from_base64(value):
    return base64.b64decode(value)

def dict_to_base64_string(value):
    return base64.b64encode(json.dumps(value)).decode("utf-8")

def divide_list_in_chunks(elements, chunk_size):
    """Yield successive n-sized chunks from th elements list."""
    if len(elements) == 0:
        yield []
    for i in range(0, len(elements), chunk_size):
        yield elements[i:i + chunk_size]
        
def get_random_uuid4_str():
    return str(uuid.uuid4())

def merge_dicts(d1, d2):
    '''
    Merge 'd1' and 'd2' dicts into 'd1'.
    'd2' has precedence over 'd1'
    '''
    for k,v in d2.items():
        if v:
            if k not in d1:
                d1[k] = v
            elif type(v) is dict:
                d1[k] = merge_dicts(d1[k], v)
            elif type(v) is list:
                d1[k] += v
    return d1

def is_value_in_dict(value, dictionary):
    return value in dictionary and dictionary[value]

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

def get_all_files_in_directory(dir_path):
    files = []
    for dirname, _, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files

def get_file_size(file_path):
    '''Return file size in bytes'''
    return os.stat(file_path).st_size

def create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name, exist_ok=True)
        
def create_file_with_content(path, content, mode='w'):
    with open(path, mode) as f:
        if isinstance(content, dict):
            content = json.dumps(content)
        f.write(content)        

def read_file(file_path, file_mode="r", file_encoding="utf-8"):
    if file_mode == 'rb':
        file_encoding = None
    with open(file_path, mode=file_mode, encoding=file_encoding) as content_file:
        return content_file.read()
    
def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)

def delete_folder(path):
    shutil.rmtree(path)
    
def create_tar_gz(files_to_archive, destination_tar_path):
    with tarfile.open(destination_tar_path, "w:gz") as tar:
        for file_path in files_to_archive:
            tar.add(file_path, arcname=os.path.basename(file_path))
    return destination_tar_path
      
def extract_tar_gz(tar_path, destination_path):
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=destination_path)

def is_variable_in_environment(variable):
    return is_value_in_dict(variable, os.environ)

def is_key_and_value_in_dictionary(key, dictionary):
    return (key in dictionary) and dictionary[key] and dictionary[key] != ""

def set_environment_variable(key, variable):
    if key and variable:
        os.environ[key] = variable

def get_environment_variables():
    return os.environ

def get_environment_variable(variable):
    if is_variable_in_environment(variable):
        return os.environ[variable]

def parse_arg_list(arg_keys, cmd_args):
    result = {}
    for key in arg_keys:
        if type(key) is tuple:
            if key[0] in cmd_args and cmd_args[key[0]]:
                result[key[1]] = cmd_args[key[0]]
        else:
            if key in cmd_args and cmd_args[key]:
                result[key] = cmd_args[key]
    return result

def _get_user_defined_variables():
    user_vars = {}
    for key in os.environ.keys():
        # Find global variables with the specified prefix
        if re.match("CONT_VAR_.*", key):
            user_vars[key.replace("CONT_VAR_", "")] = get_environment_variable(key)
    return user_vars

def set_file_execution_rights(file_path):
    execute_command(["chmod", "+x", file_path])
    
def execute_command(command):
    subprocess.call(command)
    
def execute_command_and_return_output(command):
    return subprocess.check_output(command).decode("utf-8")

def kill_process(self, process):
    # Using SIGKILL instead of SIGTERM to ensure the process finalization
    os.killpg(os.getpgid(process.pid), subprocess.signal.SIGKILL)
