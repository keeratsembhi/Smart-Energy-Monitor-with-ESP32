const int CURRENT_PIN = 36;  // VP (ACS712 OUT)
const int VOLTAGE_PIN = 39;  // VN (ZMPT101B OUT)

const float V_REF = 3.3; // esp32 adc reference voltage
const int ADC_RES = 4095; // esp32 adc resolution
const float ACS712_SENSITIVITY = 0.185; // V/A for 5A version
const float ACS712_OFFSET = 2.5;        

void setup() {
  Serial.begin(115200); // starts serial monitor and speed
}

void loop() {
  const int samples = 200;
  float voltageSum = 0;
  float currentSum = 0;

  for (int i = 0; i < samples; i++) {
    float vRaw = analogRead(VOLTAGE_PIN); // reads raw adc values for voltage and current
    float cRaw = analogRead(CURRENT_PIN);

    float vADC = (vRaw / ADC_RES) * V_REF; // converts raw adc values to actual voltages
    float cADC = (cRaw / ADC_RES) * V_REF;

    float vAC = vADC - 1.65; // subtract sensor offset to centor waveform
    float cAC = cADC - ACS712_OFFSET; // subtract sensor offset to centor waveform

    voltageSum += vAC * vAC;
    currentSum += cAC * cAC;

    delay(1); // space samples slightly
  }

  float voltageRMS = sqrt(voltageSum / samples); // calculate raw RMS
  float currentRMS = sqrt(currentSum / samples);

  // Calibration factors — tweak these to match multimeter values
  const float voltageCalibration = 158.5;  // try values between 150–170 for ZMPT101B
  const float currentCalibration = 0.394;  // try values between 0.35–0.42 for ACS712 5A

  // Apply calibration
  voltageRMS *= voltageCalibration;
  currentRMS *= currentCalibration;

  // Calculate real power
  float power = voltageRMS * currentRMS;

  // serial output
  Serial.print("Voltage RMS (V): ");
  Serial.println(voltageRMS, 3);
  Serial.print("Current RMS (A): ");
  Serial.println(currentRMS, 3);
  Serial.print("Power (W): ");
  Serial.println(power, 3);
  Serial.println("-------------");

  delay(1000);
}

