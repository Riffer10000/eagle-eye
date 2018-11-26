#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>
#include "AVR_TTC_scheduler.c"

#define UBBRVAL 51

double reading;
bool status = true; // true = ingeklapt // false = uitgeklapt
int stand = 0;
int max = 5; // 20 degree angle
int min = 0;

void transmit(char c) {
	loop_until_bit_is_set(UCSR0A, UDRE0); // wait until data register empty
	UDR0 = c;
}

void adc_init(void) {
	ADMUX = (1<<REFS0);
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}

uint16_t adc_read(uint8_t pin) {
	ADMUX	&=	0xf0;
	ADMUX	|=	pin;
	ADCSRA |= _BV(ADSC);
	while((ADCSRA & _BV(ADSC)));
	return ADC;
}

void uart_init(void) {
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	UCSR0A = 0;
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
	TCCR1B |= _BV(CS12);
}


void getDistance(void) {
	PORTB &= ~_BV (1);
	_delay_us(2);
	PORTB |= _BV (1);
	_delay_us(10);
	PORTB &= ~_BV (1);
	loop_until_bit_is_set(PINB,2);
	TCNT1 = 0;
	loop_until_bit_is_clear(PINB,2);
	float count = ((float)TCNT1/16)/58*64*4;
	uint8_t distance = round(count);
	//UDR0 = 9 //distance;
	transmit(distance);
}

uint8_t getTemperature(void) {
	reading = adc_read(0);
	float voltage = reading * 5;
	voltage /= 1024;
	float tempC = (voltage - 0.5) * 100;
	uint8_t temp = round(tempC);
	//UDR0 = 8; //temp;
	return temp;
	//transmit(temp);
}

void getTemperatureInterval()
{
	int a;
	float totaal = 0.0;
	for(a = 0; a <10; a++)
	{
		totaal += getTemperature();
		_delay_ms(1000);
	}
	float avgtemp = totaal / 10.0;
	uint8_t tempInterval = round(avgtemp);
	transmit(tempInterval);
}

void getLight(void) {
	reading = adc_read(1);
	reading = 1023 - reading;
	reading = reading * 255 / 1023;
	uint8_t light = round(reading);
	//UDR0 = 7; //light;
	transmit(light);
}

uint8_t receive(void) {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}

void red_on(void) {
	PORTD |= _BV(PORTD5);

}
void red_off(void) {
	PORTD &= ~_BV(PORTD5);
}

void green_on(void) {
	PORTD |= _BV(PORTD7);
}

void green_off(void) {
	PORTD &= ~_BV(PORTD7);
}

void uitrol(void) {
	if (status == false) {
		transmit(77); // in- uitrol error
	}
	else {
		red_on();
		while(stand<max) {
			green_off();
			PORTD |= _BV(PORTD6);
			_delay_ms(400);
			PORTD &= ~_BV(PORTD6);
			_delay_ms(400);
			stand = stand + 1;
		}
		transmit(87);
		status = false;
	}
}

void inrol(void) {
	if (status == true) {
		transmit(77); //in- uitrol error
	}
	else {
		green_on();
		while(stand>min) {
			red_off();
			PORTD |= _BV(PORTD6);
			_delay_ms(400);
			PORTD &= ~_BV(PORTD6);
			_delay_ms(400);
			stand = stand - 1;
		}
		transmit(88);
		status = true;
	}
}

void protocol(void) {
	uint8_t task = receive();
	
	if(task == 53){
		inrol();
	}
	
	if(task == 54){
		uitrol();
	}
	
	if(task == 55) {
		getLight();
	}
	
	if(task == 56) {
		transmit(getTemperature());
	}
	
	if(task == 57) {
		getDistance();
	}
	
	if(task == 58) {
		getTemperatureInterval();
	}

	if(task != 53 && task != 54 && task != 55 && task != 56 && task != 57 && task != 58) {
		transmit(69);
	}
}

void port_init(void) {
	DDRB |= _BV(1); // Trigger port
	DDRB &= ~_BV (2); // Echo port
	DDRD |= _BV(DDD7); // Green led
	DDRD |= _BV(DDD6); // Orange led
	DDRD |= _BV(DDD5); // Red led
	
	red_off();
	green_on();
}

int main(void) {
	adc_init();
	uart_init();
	port_init();
	SCH_Init_T1();
	
	SCH_Add_Task(protocol, 0, 50);
	
	SCH_Start();
	
	while(1) {
		SCH_Dispatch_Tasks();
	}
}