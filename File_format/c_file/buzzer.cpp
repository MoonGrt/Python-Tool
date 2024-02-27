#include "mbed.h"

PwmOut buzzer(D10); // buzzer = PTA1

float frequency1[] = {NOTE_E6, NOTE_E6, 0, NOTE_E6, 0, NOTE_C6, NOTE_E6, 0, NOTE_G6, 0, 0,
                      0, NOTE_G5, 0, 0, 0, NOTE_C6, 0, 0, NOTE_G5, 0, 0, NOTE_E5, 0, 0,
                      NOTE_A5, 0, NOTE_B5, 0, NOTE_AS5, NOTE_A5, 0, NOTE_G5, NOTE_E6, NOTE_G6,
                      NOTE_A6, 0, NOTE_F6, NOTE_G6, 0, NOTE_E6, 0, NOTE_C6, NOTE_D6, NOTE_B5,
                      0, 0, NOTE_C6, 0, 0, NOTE_G5, 0, 0, NOTE_E5, 0, 0, NOTE_A5, 0, NOTE_B5,
                      0, NOTE_AS5, NOTE_A5, 0, NOTE_G5, NOTE_E6, NOTE_G6, NOTE_A6, 0, NOTE_F6,
                      NOTE_G6, 0, NOTE_E6, 0, NOTE_C6, NOTE_D6, NOTE_B5, 0, 0};

float beat1[] = {12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 9, 9, 9, 12,
                 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                 12, 12, 12, 12, 12, 12, 12, 12, 12, 9, 9, 9, 12, 12, 12, 12, 12, 12, 12,
                 12, 12, 12, 12, 12};

int length2 = 56;
float frequency2[] = {NOTE_E6, NOTE_DS6, NOTE_E6, NOTE_DS6, NOTE_E6, NOTE_B5, NOTE_D6, NOTE_C6, NOTE_A5,
                      NOTE_C5, NOTE_E5, NOTE_A5, NOTE_B5, NOTE_E5, NOTE_GS5, NOTE_B5, NOTE_C6,
                      NOTE_E6, NOTE_DS6, NOTE_E6, NOTE_DS6, NOTE_E6, NOTE_B5, NOTE_D6, NOTE_C6, NOTE_A5,
                      NOTE_C5, NOTE_E5, NOTE_A5, NOTE_B5, NOTE_E5, NOTE_GS5, NOTE_B5, NOTE_C6,
                      NOTE_B5, NOTE_C6, NOTE_D6, NOTE_E6, NOTE_G5, NOTE_F6, NOTE_E6, NOTE_D6,
                      NOTE_F5, NOTE_E6, NOTE_D6, NOTE_C6, NOTE_E5, NOTE_D6, NOTE_C6, NOTE_B5,
                      NOTE_E5, NOTE_E6};
float beat2[] = {12, 12, 12, 12, 12, 12, 12, 12, 9, 12, 12, 12, 9,
                 12, 12, 12, 9, 12, 12, 12, 12, 12, 12, 12, 12, 9,
                 12, 12, 12, 9, 12, 12, 12, 9, 12, 12, 12, 9, 12, 12, 12, 9,
                 12, 12, 12, 9, 12, 12, 12, 9, 12, 9};

float frequency3[] = {659, 554, 659, 554, 550, 494, 554, 587, 494, 659, 554, 440}; // frequency array
float beat3[] = {1, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 2};                          // beat arrays

int main()
{
  display.clearDisplay();
  display.setTextCursor(0, 0);
  display.printf("Music1\n");
  display.display();
  while (1)
  {
    for (int i = 0; i <= length1; i++)
    {
      if (frequency1[i] == 0)
        buzzer = 0.0;
      else
      {
        buzzer.period(1.0 / frequency1[i]); // period = (1.0 / frequency)
        buzzer = 0.5;                       // duty cycle = 50%
      }
      thread_sleep_for(2500.0 / beat1[i]); // duration = (C / beat) ms
      if (!sw)
        return 0;
    }
  }
}

int Music2()
{
  display.clearDisplay();
  display.setTextCursor(0, 0);
  display.printf("Music2\n");
  display.display();
  while (1)
  {
    for (int i = 0; i <= length2; i++)
    {
      if (frequency2[i] == 0)
        buzzer = 0.0;
      else
      {
        buzzer.period(1.0 / frequency2[i]); // period = (1.0 / frequency)
        buzzer = 0.5;                       // duty cycle = 50%
      }
      thread_sleep_for(3500.0 / beat2[i]); // duration = (C / beat)ms
      if (!sw)
        return 0;
    }
  }
}

int Music3()
{
  display.clearDisplay();
  display.setTextCursor(0, 0);
  display.printf("Muisc3\n");
  display.display();
  while (1)
  {
    for (int i = 0; i < 12; i++)
    {
      buzzer.period(1 / (frequency3[i])); // set PWM period
      buzzer = 0.5;                       // set duty cycle
      wait(0.5 * beat3[i]);               // hold for beat period
      if (!sw)
        return 0;
    }
  }
}