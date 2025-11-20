//Heap (Montículo) en C++ usando vector
#include <iostream>
#include <vector>
using namespace std;

void heapify(vector<int>& arr, int n, int i) {
    int mayor = i;
    int izq = 2 * i + 1;
    int der = 2 * i + 2;

    if (izq < n && arr[izq] > arr[mayor])
        mayor = izq;

    if (der < n && arr[der] > arr[mayor])
        mayor = der;

    if (mayor != i) {
        swap(arr[i], arr[mayor]);
        heapify(arr, n, mayor);
    }
}

int main() {
    vector<int> heap = {20, 15, 10, 8, 7, 5};

    int n = heap.size();

    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(heap, n, i);

    cout << "Heap construido: ";
    for (int x : heap) cout << x << " ";
}
