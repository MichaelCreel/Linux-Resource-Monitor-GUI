CC = gcc
CFLAGS = -Wall -O2
TARGET = resource-monitor
SRC = resource-monitor.c

all: $(TARGET)
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)