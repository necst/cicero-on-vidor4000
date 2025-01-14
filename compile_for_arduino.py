# #####################
# Parameters to modify
# #####################

# The regex to compile
regex = "a+(b|c)+"
	

# If True, requires that the regular expression matches with the start of the string (equivalent to ^<your_regex>)
no_prefix = False
# If True, requires that regular expression matches with the end of the string (equivalent to <your_regex>$)
no_postfix = False
# NB: no_postfix=True does not seem to work, as the compiled code does not recognize any string even if it is valid

output_file = "code.h"


# ##################
# Compilation logic
# ##################

def compile_regex(regex):
    import sys

    # Add Cicero compiler folder to path
    sys.path.append('cicero_compiler')

    import re2compiler
    
    code = re2compiler.compile(data=regex, O1=True, no_postfix=no_postfix, no_prefix=no_prefix)
    return code.split('\n')


def code_to_bytes(code):
    res = bytearray()
    
    for line in code:
        if line.lstrip() == '':
            break
        tmp = int(line, 16)
        res += tmp.to_bytes(2, 'big')
    return res


def get_byte_repr(byte):
    return str(int.from_bytes(byte, 'big'))


def write_bytes_to_file(code_bytes):
    res = ""
    numbytes = len(code_bytes)
    
    # Encode the number of bytes of code in the two first bytes of the file
    numbytes_bytes = numbytes.to_bytes(2, 'big')
    for i in range(0, 2):
        res += get_byte_repr(numbytes_bytes[i:i+1]) + ','
        
    for i in range(0, numbytes):
        if i == numbytes - 1:
            res += get_byte_repr(code_bytes[i:i+1])
        else:
            res += get_byte_repr(code_bytes[i:i+1]) + ','
    
    with open(output_file, "w") as f:
        f.write(res);
        print("Done")


if __name__ == "__main__":
    code = compile_regex(regex)
    code_bytes = code_to_bytes(code)
    write_bytes_to_file(code_bytes)


