import re
import logging
import socket

try:
    raw_input
except NameError:
    def raw_input(prompt=''):
        return input(prompt)

try:
    import DNS
    ServerError = DNS.ServerError
    DNS.DiscoverNameServers()
except (ImportError, AttributeError):
    DNS = None

    class ServerError(Exception):
        pass

# All we are really doing is comparing the input string to one
# gigantic regular expression.  But building that regexp, and
# ensuring its correctness, is made much easier by assembling it
# from the "tokens" defined by the RFC.  Each of these tokens is
# tested in the accompanying unit test file.
#
# The section of RFC 2822 from which each pattern component is
# derived is given in an accompanying comment.
#
# (To make things simple, every string below is given as 'raw',
# even when it's not strictly necessary.  This way we don't forget
# when it is necessary.)
#
WSP = r'[ \t]'                                       # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'                       # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'                       # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

MX_DNS_CACHE = {}

def get_mx_record(email):
    if not DNS:
        raise Exception('For check the mx records or check if the email exists you must '
                        'have installed pyDNS python package')
    hostname = email[email.find('@') + 1:]
    if hostname not in MX_DNS_CACHE:
        try:
            MX_DNS_CACHE[hostname] = DNS.mxlookup(hostname)
        except ServerError as e:
            if e.rcode == 3:  # NXDOMAIN (Non-Existent Domain)
                MX_DNS_CACHE[hostname] = None
            else:
                raise

    return MX_DNS_CACHE[hostname]

def check_mx_record(email):
    mx_hosts = get_mx_record(email)
    if not mx_hosts:
        return False
    for mx in mx_hosts:
        if mx:
            return True
    return None # Unkown


def validate_email(email, check_mx=False, debug=False):
    """Given an email return if it passes regex check. Also check optionally for mx records via DNS lookup"""
    if debug:
        logger = logging.getLogger('validate_email')
        logger.setLevel(logging.DEBUG)
    else:
        logger = None

    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
        if check_mx:
            return check_mx_record(email)
    except AssertionError:
        return False
    return True

if __name__ == "__main__":
    import time
    while True:
        email = raw_input('Enter email for validation: ')

        mx = raw_input('Validate MX record? [yN] ')
        if mx.strip().lower() == 'y':
            mx = True
        else:
            mx = False

        logging.basicConfig()

        result = validate_email(email, mx, debug=True)
        if result:
            print("Valid!")
        elif result is None:
            print("I'm not sure.")
        else:
            print("Invalid!")

        time.sleep(1)
