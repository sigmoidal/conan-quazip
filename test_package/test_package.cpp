#include <iostream>
#include <quazip/quazip.h>

int main() {
    QuaZip zip;
    std::cout << "Hello world, QuaZIP is opened: " << zip.isOpen();
    return 0;
}