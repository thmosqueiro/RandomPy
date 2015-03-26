CC = icc
LDFLAGS= -lm -lcvode -lcvodeserial

lorentz: $(OBJECTS)
	$(CC) -o Lorentz lorentz.c $(LDFLAGS)


all : lorentz

clean :
	rm -f *.o *~
