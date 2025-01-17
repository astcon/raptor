CC = /usr/bin/h5cc -I$(RAPTOR)/src -I$(PWD)
#CC = h5cc -I$(RAPTOR)/src -I$(PWD)

CFLAGS = -fopenmp  -std=c99  -lm -lgsl -Wall -Wno-unused-but-set-variable
#CFLAGS = -fopenmp  -std=gnu99  -O3 -march=native -mtune=native -flto -funroll-loops -lgsl
#CFLAGS =  -std=c99  -Wall -Wno-unused-but-set-variable -I/opt/homebrew/include -lm -lgsl

LDFLAGS = -fopenmp -lm -lgsl -lgslcblas
#LDFLAGS = -L/opt/homebrew/lib  -lm -lgsl -lgslcblas

VPATH=$(RAPTOR)/src:
CPATH=$(RAPTOR)/src:

OBJDIR=build

TARGET=RAPTOR

SOURCES=main.c core.c io.c GRmath.c gr_integrator.c rte_integrator.c pol_rte_integrator.c metric.c pol_emission.c tetrad.c model.c constants.c camera.c
OBJECTS := $(patsubst %.c,$(OBJDIR)/%.o,$(SOURCES))

all: create_directories $(SOURCES) $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

create_directories:
	@test -d $(OBJDIR) || mkdir -v $(OBJDIR)


$(OBJECTS): $(OBJDIR)/%.o: %.c
	$(CC) $(CFLAGS)  -c $^ -o $@


clean:
	rm -rf $(OBJECTS) $(TARGET)
