import time

def encoder(encoder_list):
    print("fake encoder started")
    x = 0
    while True:
        encoder_list[0] = x
        x = x+1
        time.sleep(0.03)

if __name__ == "__main__":
    print ("started")
    list = [0]
    encoder(list)

