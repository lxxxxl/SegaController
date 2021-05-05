// Retieves keys pressed on Sega Mega Drive controller and sends keycodes to PC via UART
// based on source code from https://eax.me/arduino-sega-controller/

#define PIN_UP_OR_Z 6
#define PIN_DOWN_OR_Y 7
#define PIN_LEFT_OR_X 8
#define PIN_RIGHT_OR_MODE 9
#define PIN_B_OR_A 10
#define PIN_SEL 11
#define PIN_C_OR_START 12

enum Key {
  KEY_UP,
  KEY_DOWN,
  KEY_LEFT,
  KEY_RIGHT,

  KEY_START,
  KEY_MODE,

  KEY_A,
  KEY_B,
  KEY_C,

  KEY_X,
  KEY_Y,
  KEY_Z,
  KEY_MAX
};

// stores pressed state
bool keysPressed[KEY_MAX] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,};
// stores status of key (state changed or not)
bool keysStatus[KEY_MAX] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,};

// get status of all keys
void segaRead() {
    digitalWrite(PIN_SEL, HIGH);
    delayMicroseconds(20);

    updateStatus(KEY_UP, (digitalRead(PIN_UP_OR_Z) == LOW));
    updateStatus(KEY_LEFT, (digitalRead(PIN_LEFT_OR_X) == LOW));
    updateStatus(KEY_RIGHT, (digitalRead(PIN_RIGHT_OR_MODE) == LOW));
    updateStatus(KEY_DOWN, (digitalRead(PIN_DOWN_OR_Y) == LOW));

    updateStatus(KEY_C, (digitalRead(PIN_C_OR_START) == LOW));
    updateStatus(KEY_B, (digitalRead(PIN_B_OR_A) == LOW));

    digitalWrite(PIN_SEL, LOW);
    delayMicroseconds(20);

    updateStatus(KEY_A, (digitalRead(PIN_B_OR_A) == LOW));
    updateStatus(KEY_START, (digitalRead(PIN_C_OR_START) == LOW));

    digitalWrite(PIN_SEL, HIGH);
    delayMicroseconds(20);
    digitalWrite(PIN_SEL, LOW);
    delayMicroseconds(20);
    digitalWrite(PIN_SEL, HIGH);
    delayMicroseconds(20);
    digitalWrite(PIN_SEL, LOW);
    delayMicroseconds(20);
    digitalWrite(PIN_SEL, HIGH);
    delayMicroseconds(20);

    updateStatus(KEY_X, (digitalRead(PIN_LEFT_OR_X) == LOW));
    updateStatus(KEY_Y, (digitalRead(PIN_DOWN_OR_Y) == LOW));
    updateStatus(KEY_Z, (digitalRead(PIN_UP_OR_Z) == LOW));
    updateStatus(KEY_MODE, (digitalRead(PIN_RIGHT_OR_MODE) == LOW));

    digitalWrite(PIN_SEL, LOW);
    delayMicroseconds(20);

    digitalWrite(PIN_SEL, HIGH);
    delayMicroseconds(20);
}

// save key state and key transition
void updateStatus(Key key, bool value) {
  if (keysPressed[key] != value){
    keysPressed[key] = value;
    keysStatus[key] = true;
  }
  else
    keysStatus[key] = false;
}

void setup() {
    pinMode(PIN_SEL, OUTPUT);
    digitalWrite(PIN_SEL, HIGH);

    pinMode(PIN_UP_OR_Z, INPUT);
    pinMode(PIN_DOWN_OR_Y, INPUT);
    pinMode(PIN_LEFT_OR_X, INPUT);
    pinMode(PIN_RIGHT_OR_MODE, INPUT);
    pinMode(PIN_B_OR_A, INPUT);
    pinMode(PIN_C_OR_START, INPUT);

    Serial.begin(9600);
}

void loop() {
    segaRead();
    for (int i = 0; i < KEY_MAX; i++){
      if (keysStatus[i] == true)
        // send keys with changed status
        // indicate in 7nth bit if it was pressed (1 - pressed, 0 - released)
        Serial.write(i | keysPressed[i] << 7);
    }
    delay(10);
}
