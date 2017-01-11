#   Copyright © 2017 Joaquim Monteiro
#
#   This file is part of USBMaker.
#
#   PyRufus is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   USBMaker is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with USBMaker.  If not, see <https://www.gnu.org/licenses/>.

import os, re


def get_id_list():
    devices = os.listdir('/dev/disk/by-id/')

    not_usb_list = []
    is_part_list = []

    for device in devices:
        if not re.search('usb-', device):
            not_usb_list.append(device)

    for not_usb in not_usb_list:
        devices.remove(not_usb)

    for device in devices:
        if re.search('-part', device):
            is_part_list.append(device)

    for part in is_part_list:
        devices.remove(part)

    return devices


def get_block_device_name(device_id):
    return os.path.realpath('/dev/disk/by-id/' + os.readlink('/dev/disk/by-id/' + device_id))[5:]


def get_size(device_id):
    size_file = open('/sys/block/' + get_block_device_name(device_id) + '/size', mode='r')
    sectors = int(size_file.read().rstrip())
    size_file.close()

    block_size_file = open('/sys/block/' + get_block_device_name(device_id) + '/queue/logical_block_size', mode='r')
    block_size = int(block_size_file.read().rstrip())
    block_size_file.close()

    return sectors * block_size