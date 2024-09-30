// Sensor pins pin D6 LED output, pin A0 analog Input
#include <Firebase_Arduino_WiFiNINA.h>
#include <DHT.h>

#define DATABASE_URL "test-765da-default-rtdb.firebaseio.com" //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app
#define DATABASE_SECRET "DB SECRET"
#define WIFI_SSID "WIFI"
#define WIFI_PASSWORD "PASSWORD"
FirebaseData firebaseData;
float hum, temp, rain;

#define sensorPin A0
String path = "/test";
#define DHTPIN 2  // digital pin number
#define DHTTYPE DHT22  // DHT type 11 or 22
DHT dht(DHTPIN, DHTTYPE);

String jsonStr;
void setup() {

  Serial.begin(9600);

  dht.begin();

  Serial.print("Connecting to WiFi...");
  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print(".");
    delay(300);
  }
  Serial.print(" IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  startFirebase();
  String path = "/test";
  String jsonStr;

}

void startFirebase(){
  Firebase.begin(DATABASE_URL, DATABASE_SECRET, WIFI_SSID, WIFI_PASSWORD);
  Firebase.reconnectWiFi(true);
}


void loop() {

  Serial.print("Analog output: ");

  rain = readSensor();
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  jsonStr = "{\"humidity\":" +  String(hum) + ",\"temperature\":" + String(temp) + ",\"rain\":" +  String(rain) + ",\"timestamp\":{\".sv\":\"timestamp\"}}";
  Serial.print(jsonStr);
  if (Firebase.pushJSON(firebaseData, path, jsonStr))
  {
    Serial.println("ok");
    Serial.println("path: " + firebaseData.dataPath());
    Serial.print("push name: ");
    Serial.println(firebaseData.pushName());
  }
  else
  {
    Serial.println("error, " + firebaseData.errorReason());
  }

  delay(300000);

}


//  This function returns the analog data to calling function

int readSensor() {

  int sensorValue = analogRead(sensorPin);  // Read the analog value from sensor

  int outputValue = map(sensorValue, 0, 1023, 255, 0); // map the 10-bit data to 8-bit data 

  return outputValue;             // Return analog rain value

}
