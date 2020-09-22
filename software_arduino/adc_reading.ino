/* seperate init_adc and start_adc works
 * program sends samples whenever buffer is full
 * set time division via switch case works
 * at prescaler value 8 and smaller, serial transimission slows down, it can be seen from tx blinking frequency
 */

// avr assembly language instructions
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))

const int record_length = 1000;

// declare a volatile and global variable
volatile byte x[record_length];
volatile int count = 0;
volatile uint16_t stop_index = 9999;
volatile bool freeze = false;

unsigned long st;
uint16_t wait_duration = record_length / 2;
bool _run = true;

void setup() {
  pinMode(13, OUTPUT);
  
  Serial.begin(115200);

  init_adc();
  initAnalogComparator();
  start_adc();
  startAnalogComparator();
}

void loop() {
  if (freeze) {
    Serial.write((byte *)x + stop_index, record_length - stop_index);
    Serial.write((uint8_t *)x, stop_index);

    freeze = false;
    start_adc();
    startAnalogComparator();
  }
  
  // user input sequence
  if (Serial.available() > 0) {
    byte c = Serial.read();
    setting(c);
  }
}

ISR(ADC_vect) {
  x[count] = ADCH;
  
  if (++count >= record_length) {
    count = 0;
  }

  if (stop_index == count) {
    stop_adc();
    freeze = true;
  }
}

ISR(ANALOG_COMP_vect) {
  cbi(ACSR, ACIE);
  
  stop_index = (count + wait_duration) % record_length;
}

void init_adc() {
  cli();
  ADCSRA = 0;                     // clear ADCSRA register
  ADCSRB = 0;                     // clear ADCSRB register, this sets ADTS2/1/0 to 0, thus turning on free running mode
  ADMUX |= (0 & 0x07);            // set A0 analog input pin
  ADMUX |= (1 << REFS0);          // set reference voltage
  ADMUX |= (1 << ADLAR);          // left align ADC value to 8 bits from ADCH register

  // set prescaler
  sbi(ADCSRA, ADPS2);
  cbi(ADCSRA, ADPS1);
  cbi(ADCSRA, ADPS0);

  // disable digital input buffer on all pins
  DIDR0 = 0xff;

  ADCSRA |= (1 << ADATE);         // enable auto trigger
  ADCSRA |= (1 << ADIE);          // enable interrupts when measurement complete
  sei();
}

void start_adc() {
  sbi(ADCSRA, ADEN);              // enable ADC
  sbi(ADCSRA, ADSC);              // start ADC
}

void stop_adc() {
  cbi(ADCSRA, ADEN);              // disable ADC
}

void initAnalogComparator(void) {
  cbi(ACSR,ACD);
 
  cbi(ACSR,ACBG);

  cbi(ACSR,ACIE);

  cbi(ACSR,ACIC);

  sbi(ACSR,ACIS1);
  sbi(ACSR,ACIS0);
  /*  ACIS1 ACIS0 Mode
      0     0     Toggle
      0     1     Reserved
      1     0     Falling Edge
      1     1     Rising Edge
  */

  sbi(DIDR1,AIN1D);
  sbi(DIDR1,AIN0D);
}

void startAnalogComparator(void) {
  // Enable Analog Comparator Interrupt
  sbi(ACSR,ACIE);
}

void stopAnalogComparator(void) {
  // Disable Analog Comparator interrupt
  cbi( ACSR,ACIE );
}

void setting(byte c) {
  switch (c) {
    // labels are hexadecimal representations of integers 2,4,8,16,32,64,128
    // because serial.read() returns a byte
    case 0x2:
    cbi(ADCSRA,ADPS2);
    cbi(ADCSRA,ADPS1);
    sbi(ADCSRA,ADPS0);
    break;
  case 0x4:
    cbi(ADCSRA,ADPS2);
    sbi(ADCSRA,ADPS1);
    cbi(ADCSRA,ADPS0);
    break;
  case 0x8:
    cbi(ADCSRA,ADPS2);
    sbi(ADCSRA,ADPS1);
    sbi(ADCSRA,ADPS0);
    break;
  case 0x10:
    sbi(ADCSRA,ADPS2);
    cbi(ADCSRA,ADPS1);
    cbi(ADCSRA,ADPS0);
    break;
  case 0x20:
    sbi(ADCSRA,ADPS2);
    cbi(ADCSRA,ADPS1);
    sbi(ADCSRA,ADPS0);
    break;
  case 0x40:
    sbi(ADCSRA,ADPS2);
    sbi(ADCSRA,ADPS1);
    cbi(ADCSRA,ADPS0);
    break;
  case 0x80:
    sbi(ADCSRA,ADPS2);
    sbi(ADCSRA,ADPS1);
    sbi(ADCSRA,ADPS0);
    break;
  case 0xAA:
    _run = !_run;
    break;
  }
}
