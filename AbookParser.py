#!/usr/bin/env python3

def isField(line): return '=' in line

def parseField(line):
    name, value, *_ = line.split('=')
    return (name, value)

def parseContactID(line):
    """Parses the contact ID line.

    Format: ^[1234]$
    :line: The contact ID line
    :returns: The contact id.
    """
    return int(line[1:len(line)-1])

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse(line, contact):
    """Parses a line of an abook file.
    The bool returned determines if the contact is done or not.

    :line: line of abookfile
    :contact: Contact being built
    :returns: (bool, contact)
    """
    done = False
    # Line is empty
    if(line == ''):
        done = True
        return (True, contact)
    # If the line is header field, i.e. [a-z1-9+]
    elif(line[0] == '[' and line[-1] == ']' and isInt(line[1:len(line)-1])):
        contact['id'] = parseContactID(line)
    # If the line is a field, and we're building a contact.
    elif('=' in line and 'id' in contact):
        name, value = parseField(line)
        contact[name] = value
    return (done, contact)

def parseAbook(abookfile):
    contacts = []
    with open(abookfile, 'r') as abook:
        contact = {}
        for line in abook:
            done, contact = parse(line.rstrip(),contact)
            if done and contact != {}:
                contacts.append(contact)
                contact = {}
    return contacts

def main(abookfile):
    contacts = parseAbook(abookfile)
    print(dumps(contacts, indent=4))


if __name__ == "__main__":
    from sys import argv
    from json import dumps
    main(argv[1])
