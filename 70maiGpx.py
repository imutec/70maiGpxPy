import sys
from pytz import timezone
import datetime

def main():
  argv = sys.argv
  if (len(argv) <= 0):
    return ()

  SPAN = 3600

  input = argv[1]

  if (len(argv) == 2):
    output = input.replace(".txt", ".gpx")
  else:
    output = argv[2]

  #local timezone
  localtz = datetime.datetime.now().astimezone().tzinfo
  #print(localtz)

  file = open(input, 'r')
  data = file.read().splitlines()
  file.close()

  gpx = open(output, "w")
  gpx.write("<gpx version = \"1.1\" creator = \"70maiDashcam\">\n")

  lasttimestamp = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)

  segment = False

  for record in data:
    fields = record.split(",")
    if len(fields) > 3:
      if fields[1] == "V":
        continue

      timeStamp = fields[0] #1時間遅れている?
      latitude  = fields[2] #緯度
      longitude = fields[3] #経度

      #Skip lat 0.000000, lon 0.000000
      if (latitude.strip() == "0.000000") or (longitude.strip() == "0.000000"):
        print("Skip lat 0.000000, lon 0.000000")
        continue

      #Chinese Timestamp
      chinaTimestamp = datetime.datetime.fromtimestamp(int(timeStamp), timezone("Asia/Shanghai"))

      #UTC datetimeを作成
      utcTimeStamp = datetime.datetime.fromisoformat(chinaTimestamp.strftime("%Y-%m-%dT%X+00:00"))

      #local timestamp
      localimeStamp = utcTimeStamp.astimezone(localtz)
      strLocalTimeStamp = localimeStamp.strftime("%Y-%m-%dT%XZ")
      
      delta = chinaTimestamp - lasttimestamp

      if (delta.seconds > SPAN):
        if segment:
          gpx.write("\t\t</trkseg>\n")
          gpx.write("\t</trk>\n")

        gpx.write("\t<trk><name>{}</name>\n".format(strLocalTimeStamp))
        gpx.write("\t\t<trkseg>\n")
        segment = True

      gpx.write("\t\t\t<trkpt lat=\"{}\" lon=\"{}\"><time>{}</time></trkpt>\n".format(latitude, longitude, chinaTimestamp.strftime("%Y-%m-%dT%XZ")))

      lasttimestamp = chinaTimestamp

  gpx.write("\t\t</trkseg>\n")
  gpx.write("\t</trk>\n")
  gpx.write("</gpx>")
  gpx.close()

if __name__ == "__main__":
  main()