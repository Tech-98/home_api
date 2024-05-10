from flask import Flask, jsonify
from ewelink import Client, DeviceOffline
import aladhan

def get_time(prayer):
    client = aladhan.Client()
    prayer_times = client.get_timings_by_address("London")
    for k, v in prayer_times.prayers_only.items():
        # print(f"{k} at {v.time}, {v.remaining} left")
        if str(prayer) == str(k):
            return v.time.strftime('%H:%M')

def get_next_time():
    client = aladhan.Client()
    prayer_times = client.get_timings_by_address("London")
    for k, v in prayer_times.prayers_only.items():
        if v.remaining.days == 0:
            return v.time.strftime('%H:%M')
        
def get_next_prayer():
    client = aladhan.Client()
    prayer_times = client.get_timings_by_address("London")
    for k, v in prayer_times.prayers_only.items():
        if v.remaining.days == 0:
            return k
        
app = Flask(__name__)

# Initialize eWeLink Client
client = Client(email="saif.ally1998@gmail.com", password="Agent@98")


@app.route("/login")
async def login():
    try:
        await client.login()
        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/device_info")
async def device_info():
    try:
        await client.login()
        device = client.get_device('100145d4cc')
        device_info = {
            "device_name": device.name,
            "online": device.online,
            "state": device.state,
            "created_at": device.created_at,
            "brand_name": device.brand.name,
            "logo_url": device.brand.logo.url
        }
        return jsonify(device_info), 200
    except DeviceOffline:
        return jsonify({"error": "Device is offline"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/turn_on")
async def turn_on():
    try:
        await client.login()
        print(client.user)
        device = client.get_device('100145d4cc')
        await device.on()
        return jsonify({"message": "Device turned on"}), 200
    except DeviceOffline:
        return jsonify({"error": "Device is offline"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/turn_off")
async def turn_off():
    try:
        await client.login()
        device = client.get_device('100145d4cc')
        await device.off()
        return jsonify({"message": "Device turned off"}), 200
    except DeviceOffline:
        return jsonify({"error": "Device is offline"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/switch")
async def switch():
    await client.login()
    device = client.get_device('100145d4cc')
    print(device.state)
    if str(device.state) == "Power.on":
        await device.off()
        return "turned off"
    else:
        await device.on()
        return "turned on"

@app.route('/next_time')
async def next_time():
    return get_next_time()

@app.route('/next_prayer')
async def next_prayer():
    return get_next_prayer()

@app.route('/fajr')
async def fajr():
    return get_time("Fajr")
@app.route('/dhuhr')
async def dhuhr():
    return get_time("Dhuhr")
@app.route('/asr')
async def asr():
    return get_time("Asr")
@app.route('/maghrib')
async def maghrib():
    return get_time("Maghrib")
@app.route('/isha')
async def isha():
    return get_time("Isha")

if __name__ == "__main__":
    app.run(host='192.168.1.145', port='9128',debug=True)