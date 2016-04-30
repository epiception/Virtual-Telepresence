/*
 * Firebird_Rpi.c
 *
 * Created: 23-04-2015 12:21:18
 * Author: Saurav Shandilya (e-Yantra Team)
 * Application: Development of Raspberry Pi controlled Firebird-V Robot.
 * Hardware: Firebird-V Atmega2560 Robot
 * 
 */ 

//**********************Definition and includes**********************
#define F_CPU 14745600

#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>

//*******************************************************************

//************************************Variable Declaration Starts*****************************

unsigned char rec_data = 0;						// single byte received at UDR2 is stored in this variable 
unsigned char uart_data_buff[25] = {0};			// storing uart data in this buffer
unsigned char copy_packet_data[25] = {0};		// storing uart data into another packet data for operation
unsigned char state = ' ';						// for switch cases in UART ISR
unsigned char end_char_rec = 0; 
unsigned char i = 0 , j = 0;					//
unsigned char data_packet_received = 0;			// flag to check if all data_packet is received- goes high when '\!' is received
unsigned char data_copied = 0;					// flag to check if uart_data_buff is copied into packet_data

unsigned char device_id = 0;
unsigned char device_type = 0;
unsigned char function_type = 0;
unsigned char param_count = 0;
unsigned char param_count_upper_nibbel;
unsigned char param_count_lower_nibbel;
unsigned char temp_1;							//for data > 8 bit
unsigned char temp_2;							//for data > 8 bit
unsigned int param_1 = 0, param_2 = 0, param_3 = 0;

volatile unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
volatile unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
volatile unsigned int Degrees; //to accept angle in degrees for turning

unsigned char data;			//to store received data from UDR1
unsigned char ADC_flag;
unsigned char left_motor_velocity = 0x00;
unsigned char right_motor_velocity = 0x00;

//************************************Variable Declaration Ends*****************************


//*******************************Pin Configuration Starts****************************

//**********************Buzzer*******************************
void buzzer_pin_config (void)
{
	DDRC = DDRC | 0x08;		//Setting PORTC 3 as outpt
	PORTC = PORTC & 0xF7;		//Setting PORTC 3 logic low to turnoff buzzer
}

//**********************DC Motor*******************************
void motion_pin_config (void)
{
	DDRA = DDRA | 0x0F;
	PORTA = PORTA & 0xF0;
	DDRL = DDRL | 0x18;   //Setting PL3 and PL4 pins as output for PWM generation
	PORTL = PORTL | 0x18; //PL3 and PL4 pins are for velocity control using PWM.
}

//**********************Encoder Left and Right*******************************
//Function to configure INT4 (PORTE 4) pin as input for the left position encoder
void left_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xEF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x10; //Enable internal pull-up for PORTE 4 pin
}

//Function to configure INT5 (PORTE 5) pin as input for the right position encoder
void right_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xDF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x20; //Enable internal pull-up for PORTE 4 pin
}

//**********************ADC*******************************
void adc_pin_config (void)
{
	DDRF = 0x00;  //set PORTF direction as input
	PORTF = 0x00; //set PORTF pins floating
	DDRK = 0x00;  //set PORTK direction as input
	PORTK = 0x00; //set PORTK pins floating
}

//**********************Servo motors*******************************
void servo1_pin_config (void)
{
	DDRB  = DDRB | 0x20;  //making PORTB 5 pin output
	PORTB = PORTB | 0x20; //setting PORTB 5 pin to logic 1
}

//Configure PORTB 6 pin for servo motor 2 operation
void servo2_pin_config (void)
{
	DDRB  = DDRB | 0x40;  //making PORTB 6 pin output
	PORTB = PORTB | 0x40; //setting PORTB 6 pin to logic 1
}

//Configure PORTB 7 pin for servo motor 3 operation
void servo3_pin_config (void)
{
	DDRB  = DDRB | 0x80;  //making PORTB 7 pin output
	PORTB = PORTB | 0x80; //setting PORTB 7 pin to logic 1
}

//**********************BarLEDs*******************************
void LED_bargraph_config (void)
{
	DDRJ = 0xFF;  //PORT J is configured as output
	PORTJ = 0x00; //Output is set to 0
}

//**********************SPI(for sensors on ATmega8)*******************************
void spi_pin_config (void)
{
	DDRB = DDRB | 0x07;
	PORTB = PORTB | 0x07;
}

//**********************Port Initilizations*******************************
void port_init()
{
	motion_pin_config();
	buzzer_pin_config();
	left_encoder_pin_config();
	right_encoder_pin_config();
	adc_pin_config();
	servo1_pin_config();
	servo2_pin_config();
	servo3_pin_config();
	LED_bargraph_config();
	spi_pin_config();
}

//*******************************Pin Configuration Ends****************************

//*******************************UART Initialization Starts****************************

//Function To Initialize UART2 - Rub robot using USB cable
// desired baud rate:9600
// actual baud rate:9600 (error 0.0%)
// char size: 8 bit
// parity: Disabled
void uart2_init(void)
{
	UCSR2B = 0x00; //disable while setting baud rate
	UCSR2A = 0x00;
	UCSR2C = 0x06;
	UBRR2L = 0x5F; //set baud rate lo
	UBRR2H = 0x00; //set baud rate hi
	UCSR2B = 0x98;
}
//*******************************UART Initialization Ends****************************


//*******************************ADC Initialization Starts****************************
// Conversion time: 56uS
void adc_init(void)
{
	ADCSRA = 0x00;
	ADCSRB = 0x00;		//MUX5 = 0
	ADMUX = 0x20;		//Vref=5V external --- ADLAR=1 --- MUX4:0 = 0000
	ACSR = 0x80;
	ADCSRA = 0x86;		//ADEN=1 --- ADIE=1 --- ADPS2:0 = 1 1 0
}

//*******************************ADC Initialization Ends****************************

//*******************************PWM Initialization Starts****************************

// Timer 5 initialized in PWM mode for velocity control
// Prescale:256
// PWM 8bit fast, TOP=0x00FF
// Timer Frequency:225.000Hz
void timer5_init()
{
	TCCR5B = 0x00;	//Stop
	TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT5L = 0x01;	//Counter lower 8-bit value to which OCR5xH value is compared with
	OCR5AH = 0x00;	//Output compare register high value for Left Motor
	OCR5AL = 0xFF;	//Output compare register low value for Left Motor
	OCR5BH = 0x00;	//Output compare register high value for Right Motor
	OCR5BL = 0xFF;	//Output compare register low value for Right Motor
	OCR5CH = 0x00;	//Output compare register high value for Motor C1
	OCR5CL = 0xFF;	//Output compare register low value for Motor C1
	TCCR5A = 0xA9;	/*{COM5A1=1, COM5A0=0; COM5B1=1, COM5B0=0; COM5C1=1 COM5C0=0}
 					  For Overriding normal port functionality to OCRnA outputs.
				  	  {WGM51=0, WGM50=1} Along With WGM52 in TCCR5B for Selecting FAST PWM 8-bit Mode*/
	
	TCCR5B = 0x0B;	//WGM12=1; CS12=0, CS11=1, CS10=1 (Prescaler=64)
}

//*******************************PWM Initialization Starts****************************

//*******************************Timers for Servo Initialization Starts****************************

//TIMER1 initialization in 10 bit fast PWM mode  
//prescale:256
// WGM: 7) PWM 10bit fast, TOP=0x03FF
// actual value: 52.25Hz 
void timer1_init(void)
{
 TCCR1B = 0x00; //stop
 TCNT1H = 0xFC; //Counter high value to which OCR1xH value is to be compared with
 TCNT1L = 0x01;	//Counter low value to which OCR1xH value is to be compared with
 OCR1AH = 0x03;	//Output compare Register high value for servo 1
 OCR1AL = 0xFF;	//Output Compare Register low Value For servo 1
 OCR1BH = 0x03;	//Output compare Register high value for servo 2
 OCR1BL = 0xFF;	//Output Compare Register low Value For servo 2
 OCR1CH = 0x03;	//Output compare Register high value for servo 3
 OCR1CL = 0xFF;	//Output Compare Register low Value For servo 3
 ICR1H  = 0x03;	
 ICR1L  = 0xFF;
 TCCR1A = 0xAB; /*{COM1A1=1, COM1A0=0; COM1B1=1, COM1B0=0; COM1C1=1 COM1C0=0}
 					For Overriding normal port functionality to OCRnA outputs.
				  {WGM11=1, WGM10=1} Along With WGM12 in TCCR1B for Selecting FAST PWM Mode*/
 TCCR1C = 0x00;
 TCCR1B = 0x0C; //WGM12=1; CS12=1, CS11=0, CS10=0 (Prescaler=256)
}

//*******************************Timer for Servo Initialization Ends****************************

//*******************************Interrupt for position encoder Initialization Starts****************************

void left_position_encoder_interrupt_init (void) //Interrupt 4 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x02; // INT4 is set to trigger with falling edge
	EIMSK = EIMSK | 0x10; // Enable Interrupt INT4 for left position encoder
	sei();   // Enables the global interrupt
}

void right_position_encoder_interrupt_init (void) //Interrupt 5 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x08; // INT5 is set to trigger with falling edge
	EIMSK = EIMSK | 0x20; // Enable Interrupt INT5 for right position encoder
	sei();   // Enables the global interrupt
}

//*******************************Interrupt for position encoder Initialization ends****************************

//*******************************SPI Initialization Starts****************************
//SPI initialize
// clock rate: 921600hz
void spi_init(void)
{
	SPCR = 0x53; //setup SPI
	SPSR = 0x00; //setup SPI
	SPDR = 0x00;
}
//*******************************SPI Initialization Ends****************************

//ISR for right position encoder
ISR(INT5_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}


//ISR for left position encoder
ISR(INT4_vect)
{
	ShaftCountLeft++;  //increment left shaft position count
}

//Function To Initialize all The Devices
void init_devices()
{
	cli(); //Clears the global interrupts
	port_init();  //Initializes all the ports
	uart2_init(); //Initialize UART1 for serial communication
	adc_init(); 
	timer5_init();	// timer for PWM generation
	left_position_encoder_interrupt_init();
	right_position_encoder_interrupt_init();
	timer1_init();	// timer for servo motors
	spi_init();
	sei();   //Enables the global interrupts
} 

//-------------------------------------------------------------------------------
//-- ADC Conversion Function --------------
//-------------------------------------------------------------------------------
unsigned char ADC_Conversion(unsigned char ch)
{
	unsigned char a;
	if(ch>7)
	{
		ADCSRB = 0x08;
	}
	ch = ch & 0x07;			  //Store only 3 LSB bits
	ADMUX= 0x20 | ch;			  //Select the ADC channel with left adjust select
	ADC_flag = 0x00; 			  //Clear the user defined flag
	ADCSRA = ADCSRA | 0x40;	  //Set start conversion bit
	while((ADCSRA&0x10)==0);	  //Wait for ADC conversion to complete
	a=ADCH;
	ADCSRA = ADCSRA|0x10;        //clear ADIF (ADC Interrupt Flag) by writing 1 to it
	ADCSRB = 0x00;
	return a;
}

// Function for robot velocity control
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR5AL = (unsigned char)left_motor;
	OCR5BL = (unsigned char)right_motor;
}

void motor_enable (void)
{
	PORTL |= 18;		// Enable left and right motor. Used with function where velocity is not used
}
void buzzer_on (void)
{
	PORTC |= 0x08;
}

void buzzer_off (void)
{
	PORTC &= 0xF7;
}

void forward (void)
{
	//PORTA &= 0xF0;
	PORTA = 0x06;
}

void back (void)
{
	//PORTA &= 0xF0;
	PORTA = 0x09;
}

void left (void)
{
	//PORTA &= 0xF0;
	PORTA = 0x05;
}

void right (void)
{
	//PORTA &= 0xF0;
	PORTA = 0x0A;
}

void stop (void)
{
	PORTA = 0x00;
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = DistanceInMM / 5.338; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	while(1)
	{
		if(ShaftCountRight > ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}

void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}

void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

//Function to rotate Servo 1 by a specified angle in the multiples of 1.86 degrees
void servo_1(unsigned char degrees)
{
	float PositionPanServo = 0;
	PositionPanServo = ((float)degrees / 1.86) + 35.0;
	OCR1AH = 0x00;
	OCR1AL = (unsigned char) PositionPanServo;
}


//Function to rotate Servo 2 by a specified angle in the multiples of 1.86 degrees
void servo_2(unsigned char degrees)
{
	float PositionTiltServo = 0;
	PositionTiltServo = ((float)degrees / 1.86) + 35.0;
	OCR1BH = 0x00;
	OCR1BL = (unsigned char) PositionTiltServo;
}

//Function to rotate Servo 3 by a specified angle in the multiples of 1.86 degrees
void servo_3(unsigned char degrees)
{
	float PositionServo = 0;
	PositionServo = ((float)degrees / 1.86) + 35.0;
	OCR1CH = 0x00;
	OCR1CL = (unsigned char) PositionServo;
}

//servo_free functions unlocks the servo motors from the any angle
//and make them free by giving 100% duty cycle at the PWM. This function can be used to
//reduce the power consumption of the motor if it is holding load against the gravity.

void servo_1_free (void) //makes servo 1 free rotating
{
	OCR1AH = 0x03;
	OCR1AL = 0xFF; //Servo 1 off
}

void servo_2_free (void) //makes servo 2 free rotating
{
	OCR1BH = 0x03;
	OCR1BL = 0xFF; //Servo 2 off
}

void servo_3_free (void) //makes servo 3 free rotating
{
	OCR1CH = 0x03;
	OCR1CL = 0xFF; //Servo 3 off
}

void LED_bargraph_on (unsigned char data)
{
	PORTJ |= data;
}

void LED_bargraph_off (unsigned char data)
{
	PORTJ &= data;
}

//-------------------------------------------------------------------------------
//-- Function To Transmit/Receive through SPI interface ------
//-------------------------------------------------------------------------------
unsigned char spi_master_tx_and_rx (unsigned char data)
{
	unsigned char rx_data = 0;

	PORTB = PORTB & 0xFE;        // make SS pin low
	SPDR = data;
	while(!(SPSR & (1<<SPIF)));  //wait for data transmission to complete

	_delay_ms(1);                //time for ADC conversion in the slave microcontroller
	
	SPDR = 0x50;                 // send dummy byte to read back data from the slave microcontroller
	while(!(SPSR & (1<<SPIF)));  //wait for data reception to complete
	rx_data = SPDR;
	PORTB = PORTB | 0x01;        // make SS high
	return rx_data;
}



//SIGNAL(SIG_USART2_RECV) 		// ISR for receive complete interrupt
ISR(USART2_RX_vect)
{
	rec_data = UDR2; 				//making copy of data from UDR2 in 'data' variable

	while(!(UCSR2A && (1<<RXC2)));	// wait till data byte is received
	
	if (data_packet_received == 0) 
	{
		if (rec_data == '\n' )			// '\n' decimal value is 10
		{
			 //state = _second_last_byte 
			uart_data_buff[i] = rec_data;
			i++;
			end_char_rec = 1;
		//	UDR2 = rec_data;
		}

		else 
		{
			if((end_char_rec == 1) && (rec_data == '\r'))		//'\r' indicates end of transmission. It should come after '\n'
			{
				uart_data_buff[i] = rec_data;
				i++;
				end_char_rec = 2;
				data_packet_received = 1;
				
				for (j = 0;j<i;j++)				// i value is stored in ISR
				{
					copy_packet_data[j] = uart_data_buff[j];
					//UDR2 = copy_packet_data[j];
					uart_data_buff[j] = 0;
				}
			//	UDR2 = rec_data;
			}
	
			else if((end_char_rec == 1) && (rec_data != '\r'))		//'\r' is expected after '\n'. If not received, discard the data. 
			{
			//	UDR2 = 'x';
																	// discard the data and check 
			}
		
			else													// store other data bytes
			{
				uart_data_buff[i] = rec_data;
				i++;
			//	UDR2 = rec_data;
			}
		}
	}	
}	// end of ISR

void send_sensor_data(void)
{
	if (device_id == 0x00)
	{
		if (function_type == 0x00)
		{
			UDR2 = ADC_Conversion(0);		// Battery Voltage
		}
		
		else if (function_type == 0x01)
		{
			UDR2 = ADC_Conversion(1);		// right WL sensor
		}
		
		else if (function_type == 0x02)
		{
			UDR2 = ADC_Conversion(2);		// Center WL sensor
		}
		
		else if (function_type == 0x03)
		{
			UDR2 = ADC_Conversion(3);		// left WL sensor
		}
		
		else if (function_type == 0x04)
		{
			UDR2 = ADC_Conversion(4);		// IR Proximity sensor-1
		}
		
		else if (function_type == 0x05)
		{
			UDR2 = ADC_Conversion(5);		// IR Proximity sensor-2
		}
		
		else if (function_type == 0x06)
		{
			UDR2 = ADC_Conversion(6);		// IR Proximity sensor-3
		}
		
		else if (function_type == 0x07)
		{
			UDR2 = ADC_Conversion(7);		// IR Proximity sensor-4
		}
		
		else if (function_type == 0x08)
		{
			UDR2 = ADC_Conversion(8);		// IR Proximity sensor-5
		}
		
		else if (function_type == 0x09)
		{
			UDR2 = ADC_Conversion(9);		// Sharp Sensor-1
		}

		else if (function_type == 0x0A)
		{
			UDR2 = ADC_Conversion(10);		// Sharp Sensor-2
		}

		else if (function_type == 0x0B)
		{
			UDR2 = ADC_Conversion(11);		// Sharp Sensor-3
		}

		else if (function_type == 0x0C)
		{
			UDR2 = ADC_Conversion(12);		// Sharp Sensor-4
		}

		else if (function_type == 0x0D)
		{
			UDR2 = ADC_Conversion(13);		// Sharp Sensor-5
		}

		else if (function_type == 0x0E)
		{
			UDR2 = ADC_Conversion(14);		// Connected to servo pod
		}

		else if (function_type == 0x0E)
		{
			UDR2 = ADC_Conversion(15);		// Connected to servo pod
		}
	}
	
	if (device_id == 0x01)				// ATmega 8 ADC
	{
		if (function_type == 0x00)					// Whiteline sensor 4
		{
			UDR2 = spi_master_tx_and_rx(0);
		} 
		
		else if (function_type == 0x01)				// Whiteline sensor 5
		{
			UDR2 = spi_master_tx_and_rx(1);
		}
		
		else if (function_type == 0x02)				// Whiteline sensor 6
		{
			UDR2 = spi_master_tx_and_rx(2);
		}
		
		else if (function_type == 0x03)				// Whiteline sensor 7
		{
			UDR2 = spi_master_tx_and_rx(3);
		}
		
		else if (function_type == 0x04)				// Current Sensor
		{
			UDR2 = spi_master_tx_and_rx(4);
		}
		
		else if (function_type == 0x05)				// IR proximity sensor 6
		{
			UDR2 = spi_master_tx_and_rx(5);
		}
		
		else if (function_type == 0x06)				// IR proximity sensor 7
		{
			UDR2 = spi_master_tx_and_rx(6);
		}
		
		else if (function_type == 0x07)				// IR proximity sensor 8
		{
			UDR2 = spi_master_tx_and_rx(7);
		}
	}
				
}

void actuate_devices(void)
{
	if (device_id == 0x01)				// Buzzer has device id = 1
	{
		if (function_type == 0x00)
		{
			buzzer_on();
		}
		else if (function_type == 0x01)
		{
			buzzer_off();
		}
	}
	
	if (device_id == 0x02)				// Motor has device id = 2
	{
		if (function_type == 0x00)
		{
			motor_enable();
			forward();
		}
		else if (function_type == 0x01)
		{
			motor_enable();
			back();
		}
		else if (function_type == 0x02)
		{
			motor_enable();
			right();
		}
		else if (function_type == 0x03)
		{
			motor_enable();
			left();
		}
		else if (function_type == 0x04)
		{
			motor_enable();
			stop();
		}
		else if (function_type == 0x09)
		{
			//forward();
			//UDR2 = param_1;
			velocity(param_1,param_2);
			
		}	
	}

	if (device_id == 0x03)				// position encoder has device id = 3
	{
		if (function_type == 0x00)
		{
			forward_mm(param_1);
		}
		
		if (function_type == 0x01 )
		{
			back_mm(param_1);
		}
	}

	if (device_id == 0x04)				// servo has device id = 4
	{
		if (function_type == 0x00)
		{
			servo_1(param_1);
		}
		
		if (function_type == 0x01 )
		{
			servo_2(param_1);
		}
		
		if (function_type == 0x02 )
		{
			servo_3(param_1);
		}

		if (function_type == 0x03 )
		{
			servo_1_free();
		}

		if (function_type == 0x04 )
		{
			servo_2_free();
		}

		if (function_type == 0x05 )
		{
			servo_3_free();
		}
	}
	if (device_id == 0x05)
	{
		if (function_type == 0x00)
		{
			LED_bargraph_on(param_1);
		}

		if (function_type == 0x01)
		{
			LED_bargraph_off(param_1);
		}
	}
}

void decode_data(void)
{
	while (data_copied == 1)
	{
		device_id = copy_packet_data[0];
		device_type = copy_packet_data[1];
		function_type = copy_packet_data[2];
		param_count = copy_packet_data[3];
		param_count_upper_nibbel = param_count & 0x10;
		param_count_lower_nibbel = (unsigned char)(param_count & 0x0F);
		
		if ((param_count & 0x10) == 0x10)
		{
			temp_1 = copy_packet_data[4];
			temp_2 = copy_packet_data[5];
			
			param_1 = 256*temp_2 + temp_1;	
		}
		
		else
		{
			switch (param_count_lower_nibbel)
			{
				case 1:
				param_1 = copy_packet_data[4];
				break;
				case 2:
				param_1 = copy_packet_data[4];
				param_2 = copy_packet_data[5];
				break;
				default:
				break;
			}
		}
		data_copied = 0;
	//	UDR2 = 'D';
	}
	
	if ((data_copied == 0) && (device_type == 0x00))	// input devices such as sensors, which will send back data
	{
		send_sensor_data();
	}
	
	else if ((data_copied == 0) && (device_type == 0x01)) // output devices such as buzzer, motors
	{
	//	UDR2 = 'A';
		actuate_devices();
	}
}

void copy_data_packet()
{
	if (data_packet_received == 1)
	{
		
		//for (j = 0;j<i;j++)				// i value is stored in ISR
		//{
			//copy_packet_data[j] = uart_data_buff[j];
			////UDR2 = copy_packet_data[j];
			//uart_data_buff[j] = 0;
		//}
		i=0;
		j=0;
		data_packet_received = 0;
		end_char_rec = 0;
		data_copied = 1;
		
	//	UDR2 = data_copied;
		decode_data();
		//UDR2 = 'I';
		//_delay_ms(1000);
	}
	//UDR2 = 'O';
	
}

//Main Function
int main(void)
{
	init_devices();
	servo_2(0);
	servo_3(0);
	while(1)
	{
		copy_data_packet();
	}
}
