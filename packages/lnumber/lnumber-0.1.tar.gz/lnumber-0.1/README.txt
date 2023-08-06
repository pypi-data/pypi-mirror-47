This is a python wheel for the lnumber module. Although this can be installed using

pip install lnumber

for best performance, it is still advisable, to install this package manually via:

compiling the .so file:

gcc -c ../src/laman_number.cpp -I../inc -I../ -std=c++11 -O3 -s -DNDEBUG -flto -fopenmp -fpic -m64 -Wall -Wextra -Wno-unknown-pragmas -Wno-sign-compare -fpic -o ../laman_number.o
gcc -c ../src/lib.cpp -I../inc -I../ -std=c++11 -O3 -s -DNDEBUG -flto -fopenmp -fpic -m64 -Wall -Wextra -Wno-unknown-pragmas -Wno-sign-compare -fpic -o ../lib.o
gcc -shared -lstdc++ -lm -lgmp -lgmpxx -lgomp -o ./lnumber.so ../laman_number.o ../lib.o 

and renaming the __init__.py as lnumber.py and placing this and the generated .so files into a searchable python path (e.g. site-packages or a path in PYTHONPATH) 

I originally programmed this in windows, however I have not yet distributed a windows python package (please email me if you need this). I will soon distribute a precompiled windows pip install for this package.

More information and documentation about the C++ program and compilation (including compiling in msvc rather than gcc) can be found in the original websvn tarball link of the code:
http://svn.risc.uni-linz.ac.at/websvn/dl.php?repname=jcapco&path=%2Flnumber%2F&rev=0&isdir=1

For further question please email me (Jose Capco) at jcapco-at-risc-dot-jku-dot-at
