// Thanks to Sean Cross / chumby industries
// for the dank functions

#include<stdio.h>
#include<stdlib.h>
#include<linux/i2c.h>
#include<linux/i2c-dev.h>
#include<fcntl.h>
#include<string.h>
#include<sys/ioctl.h>
#include<unistd.h>
#include<time.h>

int set_i2c_register(int,unsigned char,unsigned char,unsigned char);
int get_i2c_register(int,unsigned char,unsigned char,unsigned char*);

void delay(int millis)
{
	long pause;
	clock_t now, then;

	pause = millis*(CLOCKS_PER_SEC/1000);
	now = then = clock();
	while ((now - then) < pause)
	{
		now = clock();
	}
}

int main(int argc, char **argv)
{
	int fd;
	char *filename = "/dev/i2c-1";
	unsigned char mxl,mxh,done;	

	fd = open(filename,O_RDWR);

	set_i2c_register(fd,0x68,0x37,0x22);
	delay(10);
	set_i2c_register(fd,0x0C,0x0A,0x00);
	delay(10);
	set_i2c_register(fd,0x0C,0x0A,0x06);
	delay(10);

	while (1) {
		get_i2c_register(fd,0x0C,0x04,&mxh);
		get_i2c_register(fd,0x0C,0x09,&done);
		get_i2c_register(fd,0x0C,0x03,&mxl);
		get_i2c_register(fd,0x0C,0x09,&done);
		printf("mx = %x%x\n",mxh,mxl);
		delay(100);
	}

	return 0;
}

int set_i2c_register(int file,
		unsigned char addr,
		unsigned char reg,
		unsigned char value) {

	unsigned char outbuf[2];
	struct i2c_rdwr_ioctl_data packets;
	struct i2c_msg messages[1];

	messages[0].addr  = addr;
	messages[0].flags = 0;
	messages[0].len   = sizeof(outbuf);
	messages[0].buf   = outbuf;

	/* The first byte indicates which register we'll write */
	outbuf[0] = reg;

	/* 
	 * The second byte indicates the value to write.  Note that for many
	 * devices, we can write multiple, sequential registers at once by
	 * simply making outbuf bigger.
	 */
	outbuf[1] = value;

	/* Transfer the i2c packets to the kernel and verify it worked */
	packets.msgs  = messages;
	packets.nmsgs = 1;
	if(ioctl(file, I2C_RDWR, &packets) < 0) {
		perror("Unable to send data");
		return 1;
	}

	return 0;
}

int get_i2c_register(int file,
		unsigned char addr,
		unsigned char reg,
		unsigned char *val) {
	unsigned char inbuf, outbuf;
	struct i2c_rdwr_ioctl_data packets;
	struct i2c_msg messages[2];

	/*
	 * In order to read a register, we first do a "dummy write" by writing
	 * 0 bytes to the register we want to read from.  This is similar to
	 * the packet in set_i2c_register, except it's 1 byte rather than 2.
	 */
	outbuf = reg;
	messages[0].addr  = addr;
	messages[0].flags = 0;
	messages[0].len   = sizeof(outbuf);
	messages[0].buf   = &outbuf;

	/* The data will get returned in this structure */
	messages[1].addr  = addr;
	messages[1].flags = I2C_M_RD/* | I2C_M_NOSTART*/;
	messages[1].len   = sizeof(inbuf);
	messages[1].buf   = &inbuf;

	/* Send the request to the kernel and get the result back */
	packets.msgs      = messages;
	packets.nmsgs     = 2;
	if(ioctl(file, I2C_RDWR, &packets) < 0) {
		perror("Unable to send data");
		return 1;
	}
	*val = inbuf;

	return 0;
}
