#!/usr/bin/env python3.7
"""Uranus Bot helper funcs"""
from requests import get
from .mwt import MWT


@MWT(timeout=60*60)
def load_codenames():
    """
    load codenames data from XFU repo
    :return:
    """
    codenames = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/codenames/codenames.json").json()
    return codenames


def check_codename(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        codename = args[0].lower()
        status = False
        reply_markup = None
        codenames = load_codenames()
        if [i for i in codenames if codename == i.lower()]:
            status = True
        elif [i for i in codenames if codename == i.split('_')[0].lower()]:
            status = True
        if status:
            try:
                message, status, reply_markup = func(*args, **kwargs)
            except ValueError:
                message, status = func(*args, **kwargs)
        else:
            message = "Wrong codename!"
        return message, status, reply_markup
    return wrapper


@MWT(timeout=60*60)
def load_names():
    """
    load names data from XFU repo
    :return:
    """
    names = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/names/names.json").json()
    names = list(names.values())
    return names


def check_name(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        name = args[0].lower()
        status = False
        names = load_names()
        if [i for i in names if name in i.lower()]:
            message, status = func(*args, **kwargs)
        else:
            message = "Wrong name!"
        return message, status
    return wrapper


def set_branch(version):
    """
    checks MIUI branch based on MIUI version
    :param version: MIUI version, stable/weekly
    :return: branch
    """
    if 'V' in version:
        branch = 'Stable'
    else:
        branch = 'Weekly'
    return branch


def set_region(filename, version):
    """
    sets MIUI ROM region from ROM file
    :param filename: MIUI file, fastboot/recovery
    :param version: MIUI version
    :return: region
    """
    if 'eea_global' in filename or 'EU' in version:
        region = 'EEA'
    elif 'id_global' in filename or 'ID' in version:
        region = 'Indonesia'
    elif 'in_global' in filename or 'IN' in version:
        region = 'India'
    elif 'ru_global' in filename or 'RU' in version:
        region = 'Russia'
    elif 'global' in filename or 'MI' in version:
        region = 'Global'
    else:
        region = 'China'
    return region