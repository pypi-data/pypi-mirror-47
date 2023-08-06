from thompcoutils.log_utils import get_logger
from thompcoutils.debug_utils import assert_test
import thompcoutils.file_utils as file_utils
import sys
from builtins import staticmethod
import ast
from configparser import ConfigParser, NoOptionError, NoSectionError, DuplicateSectionError
import os
import logging


class ConfigException(Exception):
    pass


class HiLow:
    """
    HiLow class provides a config file to store low and hi values.  If a low value for a tag/entry is lower than the
    existing value, it will be updated.  Similarly, if a hi value for is higher than the existing hi value, it will be
    updated.
    """

    def __init__(self, file_name, default_values):
        """
        :param file_name: name of the file to store values
        :param default_values: dictionary of reversed min/max values (i.e. {"rpms": {"hi": 0, "low": 99999},
                                                                            "prime numbers: {"hi": 0, "low": sys.maxint}
        """
        if not os.path.exists(file_name):
            file_utils.touch(file_name)
        self.cfg_mgr = ConfigManager(file_name)
        self.default_values = default_values

    def read_values(self, tag):
        """
        gets the current values for a tag/entry
        :param tag: tag/entry
        :return: a dictionary of values (i.e. {"hi": 10, "low": 2} )
        """
        hi = self.cfg_mgr.read_entry(section=tag, entry="hi", default_value=self.default_values[tag]["hi"])
        low = self.cfg_mgr.read_entry(section=tag, entry="low", default_value=self.default_values[tag]["low"])
        return {"hi": hi, "low": low}

    def write_values(self, tag, values):
        """
        writes values to the config file
        :param tag: tag/entry
        :param values: dictionary of values (i.e. {"hi": 10, "low": 2} )
        :return:
        """
        self.write_hi(tag=tag, hi=values["hi"])
        self.write_low(tag=tag, low=values["low"])

    def write_hi(self, tag, hi):
        # noinspection PyBroadException
        try:
            self.cfg_mgr.config.add_section(tag)
        except DuplicateSectionError:
            pass
        cfg_hi = self.read_hi(tag)
        if hi > cfg_hi:
            self.cfg_mgr.write_entry(section=tag, entry="hi", value=hi)

    def write_low(self, tag, low):
        cfg_low = self.read_low(tag)
        if low < cfg_low:
            self.cfg_mgr.write_entry(section=tag, entry="low", value=low)

    def read_hi(self, tag):
        try:
            defaults = self.default_values[tag]
        except KeyError:
            raise ConfigException("default values for {} should be set on construction of HiLo".format(tag))
        return self.cfg_mgr.read_entry(section=tag, entry="hi", default_value=defaults["hi"])

    def read_low(self, tag):
        return self.cfg_mgr.read_entry(section=tag, entry="low", default_value=self.default_values[tag]["low"])


class ConfigManager:
    def __init__(self, file_name, title=None, create=False):
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.create = create
        if not create:
            if os.path.exists(file_name):
                self.config.read(file_name)
            else:
                raise FileNotFoundError("File {} does not exist!".format(file_name))
        self.notes = []
        self.title = title
        self.values = {}

    @staticmethod
    def missing_entry(section, entry, file_name, default_value=None):
        logger = get_logger()
        logger.debug("starting")
        if default_value is None:
            log_fn = logger.critical
            message = "Required entry"
            default_value = ""
        else:
            log_fn = logger.debug
            message = "Entry"
            if default_value == "":
                default_value = "Ignoring."
            else:
                default_value = "Using default value of (" + str(default_value) + ")"
        log_fn(message + " \"" + entry + "\" in section [" + section + "] in file: " + file_name
               + " is malformed or missing.  " + str(default_value))
        if default_value == "":
            log_fn("Exiting now")
            sys.exit()

    @staticmethod
    def _insert_note(lines, line_number, note):
        if "\n" in note:
            message = note.split("\n")
        else:
            message = note
        if type(message) == str:
            lines.insert(line_number, "# " + message + ":\n")
        else:
            for l in message[:-1]:
                lines.insert(line_number, "# " + l + "\n")
                line_number += 1
            lines.insert(line_number, "# " + message[-1] + ":\n")

    def read_entry(self, section, entry, default_value, notes=None, value_type=None, use_default_if_missing=True):
        logger = get_logger()
        value = default_value
        if self.create:
            try:
                self.config.add_section(section)
            except DuplicateSectionError:
                pass
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": entry,
                                   "notes": notes})
            self.config.set(section, entry, str(default_value))
        else:
            if default_value is None:
                if value_type is None:
                    raise ConfigException("if default_value=None, value_type must be set")
                default_value = value_type
            try:
                if isinstance(default_value, str):
                    value = self.config.get(section, entry)
                elif isinstance(default_value, bool):
                    value = self.config.getboolean(section, entry)
                elif isinstance(default_value, int):
                    value = self.config.getint(section, entry)
                elif isinstance(default_value, float):
                    value = self.config.getfloat(section, entry)
                elif isinstance(default_value, dict):
                    value = ast.literal_eval(self.config.get(section, entry))
                elif isinstance(default_value, list):
                    value = ast.literal_eval(self.config.get(section, entry))
                else:
                    raise ConfigException("type {} not handled for ()".format(type(default_value), default_value))
            except NoOptionError:
                logger.debug("Entry {} in section [{}] is missing.  Using default value of {}".format(entry, section,
                                                                                                      default_value))
                if not use_default_if_missing:
                    value = None
            except NoSectionError:
                logger.debug("section [{}] is missing.  Using default value of {}".format(section, default_value))
                if not use_default_if_missing:
                    value = None
        return value

    def write_entry(self, section, entry, value, note=None):
        try:
            self.config.set(section, str(entry), str(value))
        except DuplicateSectionError:
            self.config.add_section(section)
            self.config.set(section, str(entry), str(value))

        if note is not None:
            self.notes.append({"section": section,
                               "entry": entry,
                               "notes": note})

    def read_section(self, section, default_entries, notes=None):
        key_values = default_entries
        if self.create:
            try:
                self.config.add_section(section)
            except DuplicateSectionError:
                pass
            for entry in default_entries:
                self.config.set(section, str(entry), str(default_entries[entry]))
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": None,
                                   "notes": notes})
        else:
            key_values = dict()
            for (key, val) in self.config.items(section):
                key_values[key] = val
        return key_values

    def write(self, out_file, stop=True):
        if os.path.isfile(out_file):
            raise ConfigException("File {} exists!  You must remove it before running this".format(out_file))
        f = open(out_file, "w")
        self.config.write(f)
        f.close()
        f = open(out_file)
        lines = f.readlines()
        f.close()
        if self.title is not None:
            ConfigManager._insert_note(lines, 0, self.title)
        for note in self.notes:
            in_section = False
            line_number = 0
            for line in lines:
                if "[" + note["section"] + "]" in line:
                    if note["entry"] is None:
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                    else:
                        in_section = True
                elif line.startswith("[") and line.endswith("]"):
                    in_section = False
                if in_section:
                    if line.startswith(note["entry"]):
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                line_number += 1
        f = open(out_file, "w")
        contents = "".join(lines)
        f.write(contents)
        f.close()
        print("Done writing {}".format(out_file))
        if stop:
            sys.exit()


def _test_replace(filename, old_string, new_string):
        # Safely read the input filename using 'with'
        try:
            with open(filename) as f:
                s = f.read()
                if old_string not in s:
                    print('"{old_string}" not found in {filename}.'.format(**locals()))
                    return

            # Safely write the changed content, if found in the file
            with open(filename, 'w') as f:
                print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
                s = s.replace(old_string, new_string)
                f.write(s)
        except Exception as e:
            raise e


def test_config_mgr():
    for write in [True, False]:
        file_name = "test.ini"
        if write:
            if os.path.isfile(file_name):
                os.remove(file_name)
        else:
            _test_replace(file_name, "Rover", "Baily")
        cfg_mgr = ConfigManager(file_name,
                                "This is the title of the ini file\n"
                                "You can have multiple lines if you use line breaks", write)
        first = cfg_mgr.read_entry("User 1", "first name", "Joe", "This is the first name")
        last = cfg_mgr.read_entry("User 1", "last name", "Brown", "This is the last name")
        age = cfg_mgr.read_entry("User 1", "age", 12)
        is_male = cfg_mgr.read_entry("User 1", "male", True)
        weight = cfg_mgr.read_entry("User 1", "weight", 23.5)
        values = cfg_mgr.read_entry("User 1", "values", {"height": 7.5, "weight": 10, "name": "Fred"})
        weights = cfg_mgr.read_entry("User 1", "weights", [23.5, 22])
        names = cfg_mgr.read_entry("User 1", "names", ["Joe", "Fred"])
        cfg_mgr.write_entry("User 1", "male", False)
        cfg_mgr.write_entry("User 1", "parent", "Fred")
        section = cfg_mgr.read_section("user 2", {"first name": "Sally",
                                                  "last name": "Jones",
                                                  "age": 15,
                                                  "is_male": False,
                                                  "weight": 41.3},
                                       "You only get to add notes at the top of the section using this method")
        if write:
            test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
            assert_test(test1 == "Rover", "value should be Rover")
        else:
            test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
            assert_test(test1 == "Baily", "value should be Rover")
            test2 = cfg_mgr.read_entry("User 1", "cat name", "Tinkerbell", use_default_if_missing=False)
            assert_test(test2 is None, "missing value should be none")

        print(first)
        print(last)
        print(age)
        print(is_male)
        print(weight)
        print(values)
        print(weights)
        print(names)
        print(section)
        if write:
            test_file = file_name
            cfg_mgr.write(test_file, stop=False)
            contents = open(test_file, "r")
            print("File contents are:")
            print("====================================================")
            print(contents.read())
            print("====================================================")
            contents.close()


def test_hi_low():
    file_name = "test.ini"
    if os.path.isfile(file_name):
        os.remove(file_name)
    tag = "first"
    tag2 = "second"
    max_value = 10
    min_value = 5
    hi_low = HiLow(file_name=file_name, default_values={tag: {"hi": 0, "low": 999},
                                                        tag2: {"hi": 0, "low": 999}})
    hi = hi_low.read_hi(tag=tag)
    assert_test(hi == 0, "HI should be {}".format(0))
    hi_low.write_hi(tag=tag, hi=max_value)
    hi = hi_low.read_hi(tag=tag)
    assert_test(hi == max_value, "Hi should be {}".format(max_value))
    hi_low.write_hi(tag=tag, hi=max_value - 1)
    hi = hi_low.read_hi(tag=tag)
    assert_test(hi == max_value, "Hi should be {}".format(max_value))
    max_value += 1
    hi_low.write_hi(tag=tag, hi=max_value)
    hi = hi_low.read_hi(tag=tag)
    assert_test(hi == max_value, "Value should be {}".format(max_value))

    low = hi_low.read_low(tag=tag)
    assert_test(low == 999, "Low should be {}".format(999))
    hi_low.write_low(tag=tag, low=min_value)
    low = hi_low.read_low(tag)
    assert_test(low == min_value, "Low should be {}".format(min_value))
    hi_low.write_low(tag=tag, low=min_value+1)
    low = hi_low.read_low(tag=tag)
    assert_test(low == min_value, "Value should be {}".format(min_value))
    min_value -= 1
    hi_low.write_low(tag=tag, low=min_value)
    low = hi_low.read_low(tag=tag)
    assert_test(low == min_value, "Value should be {}".format(min_value))

    hi_low.write_values(tag=tag2, values={"hi": 10, "low": 5})
    values = hi_low.read_values(tag=tag2)
    assert_test(values == {"hi": 10, "low": 5}, "values should match")


if __name__ == "__main__":
    log_configuration_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(log_configuration_file)
    test_config_mgr()
    test_hi_low()
    print("Done!")
