import subprocess
import re

def do_lspci():
    result = subprocess.run("lspci -v | grep -A 10 \"Pericom\"", shell=True, capture_output=True, text=True)
    io=""
    irq = ""
    output_lines = result.stdout.splitlines()
    # find the I/O ports and the IRQ
    for line in output_lines:
        match = re.search(r'I/O ports at \b([a-zA-Z0-9]+)\b(?=.*size=)', line)
        if match:
            io = match.group(1)
        match = re.search(r', IRQ (\d+),', line)
        if match:
            irq = match.group(1)
    #print(f"IRQ = %s, io = %s" % (irq, io))
    return (io, irq)

def do_dmesg(io, irq):
    result = subprocess.run("dmesg | grep \"tty\"", shell=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    ttys = []
    regex = r'tty\S+'
    for line in lines:
        if f"I/O 0x{io[:2]}" in line and f"irq = {irq}" in line:
            match = re.search(regex, line)
            if match:
                ttys.append(match.group())
    return ttys

if __name__== "__main__":
    (io, irq)= do_lspci()
    ports = do_dmesg(io, irq)
    print(ports)