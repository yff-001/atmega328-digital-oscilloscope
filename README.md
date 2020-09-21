# A Digital Oscilloscope Based On ATmega328

ATmega328 chip has a rather powerful analog to digital converter. It's a 10 bit resolution successive approximation ADC. Input voltage range is 0 - Vcc. 

For this project, I picked Arduino Nano as the main part of the system. The front end is designed around a LM324 op-amp. Power is supplied by a 9V adapter. It powers the Arduino Nano and LM324. 

In this project, I attempt to run this ADC at its maximum speed. In order to achieve that,

<p align="center">
  <img src="https://github.com/yff-001/atmega328-digital-oscilloscope/blob/master/images/pcb_top.png" width="1000" title="PCB Top">
</p>

<p align="center">
  <img src="https://github.com/yff-001/atmega328-digital-oscilloscope/blob/master/images/pcb_bottom.png" width="1000" title="PCB Bottom">
</p>