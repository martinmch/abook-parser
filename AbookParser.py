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

def parseAbook(abookfile):
    contacts = []
    with open(abookfile, 'r') as abook:
        contact = {}
        for line in abook:
            line = line.rstrip()
            if(line == ''):
                if(contact != {}):
                    contacts.append(contact)
                    contact = {}
                continue
            # If the line is header field, i.e. [a-z1-9+]
            if(line[0] == '[' and line[-1] == ']'):
                headerVal = line[1:len(line)-1]
                # If the header field contains an id (int)
                if isInt(headerVal):
                    contact['id'] = parseContactID(line)
                continue
            # If the line is a field, and we're building a contact.
            if('=' in line and 'id' in contact):
                name, value = parseField(line)
                contact[name] = value
                continue
    # Dump last contact.
    if(contact != {}): contacts.append(contact)
    return contacts

def main(abookfile):
    contacts = parseAbook(abookfile)
    print(dumps(contacts, indent=4))


if __name__ == "__main__":
    from sys import argv
    from json import dumps
    main(argv[1])
