import subprocess
from datetime import datetime
import time

COLORS = {
    'red': "\033[91m",
    'green': "\033[92m",
    'yellow': "\033[93m",
    'blue': "\033[94m",
    'reset': "\033[0m",
}


def colorize(text, color):
    return COLORS[color] + text + COLORS['reset']
#print(colorize("This is red text", 'red'))


def ping():
    print(f"\nStarting packet loss test at: {datetime.now()}")
    try:
        raw_results = subprocess.run(["ping -c2 10.10.100.70"], shell=True, capture_output=True, text=True)
        lines = raw_results.stdout.split('\n')
        percent = lines[-3].split()[5]
        packet_loss = int(percent.rstrip('%'))
        rtt_line = lines[-2].split()[3]
        rtt = float(rtt_line.split('/')[1])
        if packet_loss < 15:
                print(colorize('Packet loss is: ' + str(packet_loss)+'%', 'green'))
        elif packet_loss < 30:
                print(colorize('Packet loss is: ' + str(packet_loss)+'%', 'yellow'))
        else:
                print(colorize('Packet loss is: ' + str(packet_loss)+'%', 'red'))
        
        if rtt < 250:
               print(colorize('Round Trip Time latency is: ' + str(rtt)+' ms', 'green'))
        elif rtt < 500:
                print(colorize('Round Trip Time latency is: ' + str(rtt)+' ms', 'yellow'))
        else:
                print(colorize('Round Trip Time latency is: ' + str(rtt)+' ms', 'red'))
        return packet_loss
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        # close files
        #exit()

def bwtest():
    print(f"\nStarting Bandidth test at: {datetime.now()}")
# ssh -S /tmp/rd1 dummy@ "dd if=/dev/urandom bs=1048576 count=100" | dd of=/dev/null    
# BWtest does not account for ssh overhead or disk IO speeds
    try:
        raw_output = subprocess.run(['ssh -S /tmp/test.ssh dummy@ "dd if=/dev/urandom bs=1048576 count=100" | dd of=/dev/null'], shell=True, capture_output=True, text=True)
        lines = raw_output.stderr.split('\n')
        bw_line = lines[-2].split(',')[3]
        bw = float(bw_line.split()[0])
        unit = bw_line.split()[1]
        if unit == "MB/s":
            if bw > 3:
                print(colorize('Bandwidth is: ' + str(bw)+' MB/s', 'green'))
            else:
                print(colorize('Bandwidth is: ' + str(bw)+' MB/s', 'yellow'))
        else:
            print(colorize('Bandwidth is: ' + str(bw)+' KB/s', 'red'))
        return bw
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        # close files
        #exit()

#input ip
#input path
#input ssh control socket
try:
    print("Press Ctrl+C to exit")
    packet_loss_total=[]
    bw_total=[]
    while True:
        packet_loss_total.append(ping())
        time.sleep(1 * 60)
        bw_total.append(bwtest())
        time.sleep(1 * 60)
except KeyboardInterrupt:
    packet_loss_avg = sum(packet_loss_total)/len(packet_loss_total)
    bw_avg = sum(bw_total)/len(bw_total)
    print(f"\nPacket loss average is {packet_loss_avg}")
    print(f"\nBW average is {bw_avg}")
    # BW ave does not account for KB vs MB
    exit()




