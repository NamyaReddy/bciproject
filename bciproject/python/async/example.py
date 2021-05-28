import asyncio
from lib.cortex import Cortex
async def do_stuff(cortex):
    # await cortex.inspectApi()
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize()
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        await cortex.create_session(activate=True,
                                    headset_id=cortex.headsets[0])
        print("** CREATE RECORD **")
        await cortex.create_record(title="subject1_neutral1_s1")
        print("** SUBSCRIBE POW & EEG **")
        await cortex.subscribe(['eeg','pow'])
        while cortex.packet_count < 20:
            await cortex.get_data()
        #await cortex.inject_marker(label='halfway', value=1,time=cortex.to_epoch())
        #while cortex.packet_count < 20:
         #   await cortex.get_data()
        await cortex.close_session()


def test():
    cortex = Cortex('./cortex_creds.txt')
    asyncio.run(do_stuff(cortex))
    cortex.close()


if __name__ == '__main__':
    test()
    
'''from cortex2 import EmotivCortex2Client
import time

url = "wss://localhost:6868"

# Remember to start the Emotiv App before you start!
# Start client with authentication
client = EmotivCortex2Client(url,
                             client_id='AOALsENfduXaik2NsSIXvf7TOib2iMthOTTz4Pxl',
                             client_secret="EJ50qfacvuIenAfI0ikvL8aeFC9UeNZ47EGs4UL7kTPIuevBsvhvMwDtqOMnUHqoh9Em3oo5KSInipCXk4V8kfDTSZedWmWknwQsS63uBZYWSGMyKgh4x8QAQbWVitq3",
                             check_response=True,
                             authenticate=True,
                             debug=False)

# Test API connection by using the request access method
client.request_access()

# Explicit call to Authenticate (approve and get Cortex Token)
client.authenticate()

# Connect to headset, connect to the first one found, and start a session for it
client.query_headsets()
client.connect_headset(0)
client.create_session(0)
client.create_record(title='subject1_neutral1_s1')
# Subscribe to the motion and mental command streams
# Spins up a separate subscription thread
client.subscribe(streams=['pow'])
# Grab a single instance of data
#print(client.receive_data())
#print(client.data_streams.values())

# Continously grab data, while making requests periodically
counter = 0

while True:
    counter += 1
    time.sleep(0.1)

    if counter % 5000 == 0:
        print(client.request_access())

    # Try stopping the subscriber thread
    if counter == 20:
        client.stop_subscriber()
        break

    try:
        # Check the latest data point from the motion stream, from the first session
        #print(list(client.data_streams.values())[0]['eeg'][0])
        print(client.data_streams.values())
    except:
        pass
    
'''