# Copyright (c) 2007-2019 UShareSoft, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os.path

def find_relative_path_for(my_unit_test_data_file):
    # When Unit Tests are launched from pycharm, the path is the directory of the unit test file
    if os.path.isfile('../../../' + my_unit_test_data_file):
        return '../../../' + my_unit_test_data_file
    if os.path.isfile('../../../../' + my_unit_test_data_file):
        return '../../../../' + my_unit_test_data_file
    # When Unit Tests are launched from CI, the path is the project directory
    return my_unit_test_data_file